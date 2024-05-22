# -*- coding: utf-8 -*-
#
# Picard, the next-generation MusicBrainz tagger
#
# Copyright (C) 2006-2007 Lukáš Lalinský
# Copyright (C) 2010, 2018, 2020-2022 Philipp Wolfer
# Copyright (C) 2011-2012 Michael Wiencek
# Copyright (C) 2012 Chad Wilson
# Copyright (C) 2013, 2020-2021, 2023-2024 Laurent Monin
# Copyright (C) 2014 Sophist-UK
# Copyright (C) 2021 Gabriel Ferreira
# Copyright (C) 2021 Petit Minion
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.

from PyQt6 import QtCore

from picard import log
from picard.i18n import ngettext
from picard.metadata import Metadata


class Item(object):

    @property
    def can_save(self):
        """Return if this object can be saved."""
        return False

    @property
    def can_remove(self):
        """Return if this object can be removed."""
        return False

    @property
    def can_edit_tags(self):
        """Return if this object supports tag editing."""
        return False

    @property
    def can_analyze(self):
        """Return if this object can be fingerprinted."""
        return False

    @property
    def can_autotag(self):
        """Return if this object can be autotagged."""
        return False

    @property
    def can_refresh(self):
        """Return if this object can be refreshed."""
        return False

    @property
    def can_view_info(self):
        return False

    @property
    def can_submit(self):
        """Return True if this object can be submitted to MusicBrainz.org."""
        return False

    @property
    def can_show_coverart(self):
        """Return if this object supports cover art."""
        return self.can_edit_tags

    @property
    def can_browser_lookup(self):
        return True

    @property
    def is_album_like(self):
        return False

    @property
    def can_link_fingerprint(self):
        """Return True if this item can provide a recording ID for linking to AcoustID."""
        return False

    def load(self, priority=False, refresh=False):
        pass

    @property
    def tracknumber(self):
        """The track number as an int."""
        try:
            return int(self.metadata['tracknumber'])
        except BaseException:
            return 0

    @property
    def discnumber(self):
        """The disc number as an int."""
        try:
            return int(self.metadata['discnumber'])
        except BaseException:
            return 0

    @property
    def errors(self):
        if not hasattr(self, '_errors'):
            self._errors = []
        return self._errors

    def error_append(self, msg):
        log.error("%r: %s", self, msg)
        self.errors.append(msg)

    def clear_errors(self):
        self._errors = []

    @property
    def _images(self):
        return self.metadata.images

    def cover_art_description(self):
        """Return the number of cover art images for display in the UI

        Returns:
            A string with the cover art image count, or empty string if not applicable
        """
        if not self.can_show_coverart:
            return ''

        return str(len(self._images))

    def cover_art_description_detailed(self):
        """Return  a detailed text about the images and whether they are the same across
           all tracks for images in `images` for display in the UI

        Returns:
            A string explaining the cover art image count.
        """
        if not self.can_show_coverart:
            return ''

        number_of_images = len(self._images)
        if getattr(self, 'has_common_images', True):
            return ngettext("%i image", "%i images",
                            number_of_images) % number_of_images
        else:
            return ngettext("%i image not in all tracks", "%i different images among tracks",
                            number_of_images) % number_of_images


class MetadataItem(Item):
    metadata_images_changed = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()
        self.metadata = Metadata()
        self.orig_metadata = Metadata()
        self.update_metadata_images_enabled = True

    def enable_update_metadata_images(self, enabled):
        self.update_metadata_images_enabled = enabled

    def update_metadata_images(self):
        if self.update_metadata_images_enabled and self.can_show_coverart:
            if self.metadataitem_update_metadata_images():
                self.metadata_images_changed.emit()

    def keep_original_images(self):
        self.enable_update_metadata_images(False)
        for file in list(self.files):
            if file.can_show_coverart:
                file.keep_original_images()
        self.enable_update_metadata_images(True)
        self.update_metadata_images()

    # FIXME: find a better name
    def get_imagelist_state(self, state):
        """Meant to be defined in subclass if neeeded"""

    def _get_imagelist_state(self):
        from picard.util.imagelist import ImageListState

        state = ImageListState()
        self.get_imagelist_state(state)
        return state

    def remove_metadata_images(self, removed_sources):
        """Remove the images in the metadata of `removed_sources` from the metadata.

        Args:
            removed_sources: List of child objects (`Track` or `File`) which's metadata images should be removed from
        """
        state = self._get_imagelist_state()
        (removed_new_images, removed_orig_images) = state.get_metadata_images(removed_sources)

        if state.update_new_metadata:
            sources = [s.metadata for s in state.sources]
            self.metadata.remove_images(sources, removed_new_images)
        if state.update_orig_metadata:
            from picard.track import Track
            sources = [s.orig_metadata for s in state.sources if not isinstance(s, Track)]
            self.orig_metadata.remove_images(sources, removed_orig_images)

    def add_metadata_images(self, added_sources):
        """Add the images in the metadata of `added_sources` to the metadata.

        Args:
            added_sources: List of child objects (`Track` or `File`) which's metadata images should be added to current object
        """
        state = self._get_imagelist_state()
        (added_new_images, added_orig_images) = state.get_metadata_images(added_sources)
        changed = False

        if state.update_new_metadata:
            changed |= self.metadata.add_images(added_new_images)
        if state.update_orig_metadata:
            changed |= self.orig_metadata.add_images(added_orig_images)

        return changed

    def metadataitem_update_metadata_images(self):
        """Update the metadata images of the current object based on its children.

        Based on the type of the current object, this will update `self.metadata.images` to
        represent the metadata images of all children (`Track` or `File` objects).

        This method will iterate over all children and completely rebuild
        `self.metadata.images`. Whenever possible the more specific functions
        `add_metadata_images` or `remove_metadata_images` should be used.

        Returns:
            bool: True, if images where changed, False otherwise
        """
        from picard.track import Track
        from picard.util.imagelist import ImageList

        state = self._get_imagelist_state()

        changed = False
        for src_obj in state.sources:
            state.process_images(src_obj, Track)

        if state.update_new_metadata:
            updated_images = ImageList(state.new_images.values())
            changed |= updated_images.hash_dict().keys() != self.metadata.images.hash_dict().keys()
            self.metadata.images = updated_images
            self.metadata.has_common_images = state.has_common_new_images

        if state.update_orig_metadata:
            updated_images = ImageList(state.orig_images.values())
            changed |= updated_images.hash_dict().keys() != self.orig_metadata.images.hash_dict().keys()
            self.orig_metadata.images = updated_images
            self.orig_metadata.has_common_images = state.has_common_orig_images

        return changed


class FileListItem(MetadataItem):

    def __init__(self, files=None):
        super().__init__()
        self.files = files or []

    def iterfiles(self, save=False):
        yield from self.files

    def get_imagelist_state(self, state):
        state.sources = self.files
        state.update_new_metadata = True
        state.update_orig_metadata = True