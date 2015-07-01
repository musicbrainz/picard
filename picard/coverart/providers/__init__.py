# -*- coding: utf-8 -*-
#
# Picard, the next-generation MusicBrainz tagger
# Copyright (C) 2014 Laurent Monin
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

from picard import log, config
from picard.plugin import ExtensionPoint
from PyQt4.QtGui import QWidget


_cover_art_providers = ExtensionPoint()


class ProviderOptions(QWidget):

    """
        Abstract class for provider's options
    """

    options = []

    _options_ui = None

    def __init__(self, options_page, parent=None):
        super(ProviderOptions, self).__init__(parent)
        self.options_page = options_page
        if callable(self._options_ui):
            self.ui = self._options_ui()
            self.ui.setupUi(self)

    def load(self):
        pass

    def save(self):
        pass


def register_cover_art_provider(provider):
    _cover_art_providers.register(provider.__module__, provider)


def cover_art_providers():
    order = [p[0] for p in config.setting['ca_providers']]

    def _key_provider(p):
        try:
            return order.index(p.NAME)
        except ValueError:
            return 666 # move to the end
    providers = []
    for p in sorted(_cover_art_providers, key=_key_provider):
        providers.append(p)
    log.debug("CA Providers order: %s",
              ' > '.join([p.NAME for p in providers]))
    return providers


def is_provider_enabled(provider_name):
    enabled = False
    for name, checked in config.setting['ca_providers']:
        if name == provider_name:
            enabled = checked
            break
    return enabled


class CoverArtProvider:
    """Subclasses of this class need to reimplement at least `queue_images()`.
       `__init__()` does not have to do anything.
       `queue_images()` will be called if `enabled()` returns `True`.
       `queue_images()` must return `FINISHED` when it finished to queue
       potential cover art downloads (using `queue_put(<CoverArtImage object>).
       If `queue_images()` delegates the job of queuing downloads to another
       method (asynchronous) it should return `WAIT` and the other method has to
       explicitely call `next_in_queue()`.
       If `FINISHED` is returned, `next_in_queue()` will be automatically called
       by CoverArt object.
    """

    # default state, internal use
    _STARTED = 0
    # returned by queue_images():
    # next_in_queue() will be automatically called
    FINISHED = 1
    # returned by queue_images():
    # next_in_queue() has to be called explicitely by provider
    WAIT = 2

    def __init__(self, coverart):
        self.coverart = coverart
        self.release = coverart.release
        self.metadata = coverart.metadata
        self.album = coverart.album

    def enabled(self):
        enabled = is_provider_enabled(self.NAME)
        if not enabled:
            log.debug("%s disabled by user" % self.NAME)
        return enabled

    def queue_images(self):
        # this method has to return CoverArtProvider.FINISHED or
        # CoverArtProvider.WAIT
        old = getattr(self, 'queue_downloads') #compat with old plugins
        if callable(old):
            old()
            log.warning('CoverArtProvider: queue_downloads() was replaced by queue_images()')
        else:
            raise NotImplementedError

    def error(self, msg):
        self.coverart.album.error_append(msg)

    def queue_put(self, what):
        self.coverart.queue_put(what)

    def next_in_queue(self):
        # must be called by provider if queue_images() returns WAIT
        self.coverart.next_in_queue()

    def match_url_relations(self, relation_types, func):
        """Execute `func` for each relation url matching type in
           `relation_types`
        """
        try:
            if 'relation_list' in self.release.children:
                for relation_list in self.release.relation_list:
                    if relation_list.target_type == 'url':
                        for relation in relation_list.relation:
                            if relation.type in relation_types:
                                func(relation.target[0].text)
        except AttributeError:
            self.error(traceback.format_exc())


from picard.coverart.providers.caa import CoverArtProviderCaa
from picard.coverart.providers.amazon import CoverArtProviderAmazon
from picard.coverart.providers.whitelist import CoverArtProviderWhitelist
from picard.coverart.providers.caa_release_group import CoverArtProviderCaaReleaseGroup

__providers = [
    CoverArtProviderCaa,
    CoverArtProviderAmazon,
    CoverArtProviderWhitelist,
    CoverArtProviderCaaReleaseGroup,
]

for provider in __providers:
    register_cover_art_provider(provider)
