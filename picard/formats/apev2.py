# -*- coding: utf-8 -*-
#
# Picard, the next-generation MusicBrainz tagger
# Copyright (C) 2006 Lukáš Lalinský
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

from picard import config, log
from picard.coverart.image import TagCoverArtImage, CoverArtImageError
from picard.file import File
from picard.metadata import Metadata
from picard.util import encode_filename, sanitize_date, pack_performer, unpack_performer, isurl

import mutagen.apev2
import mutagen.monkeysaudio
import mutagen.musepack
import mutagen.wavpack
import mutagen.optimfrog
from .mutagenext import tak

from os import path
from time import strftime

# APEv2 metadata keys supported are based on those of mediamonkey / musicbee
# since these represent implementations of APEv2 support that have a pedigree.
#
# Picard extensions to mediamonkey / musicbee support will, where possible,
# conform to the official specifications in order to maximise compatibility
# with other players.
#
# See http://wiki.hydrogenaud.io/index.php?title=APE_key
# or http://age.hobba.nl/audio/mirroredpages/apekey.html
# which are (at the time of writing) identical.
#
# Note: This version can either store a single piece of cover art or store all
# cover art depending on a constant setting. Cover art is sorted by type in a
# defined priority sequence in order that a single piece is e.g. front cover
# rather than picture of CD, and to store in priority sequence if multiple
# cover art is saved.

class APEv2File(File):

    """Generic APEv2-based file."""
    _File = None

    # This table is derived from official specifications and
    # empirical test files created by MediaMonkey, MusicBee and mp3tag
    # plus Musicbrainz specific values

    INVOLVED_PEOPLE = "Involved People"

    __save_tags = {
        'acoustid_fingerprint': "Acoustid Fingerprint",
        'acoustid_id': "Acoustid ID",
        'album': "Album",
        'albumartist': "Album Artist",
        'albumartists': "Album Artist",
        'albumartistsort': "AlbumArtistSort",
        'albumgenre': "Album Genre",
        'albumrating': "Album Rating",
        'albumsort': "AlbumSort",
        'arranger': INVOLVED_PEOPLE,
        'artist': "Artist",
        'artists': "Artist",
        'artistsort': "ArtistSort",
        'asin': "ASIN",
        'barcode': "EAN/UPC",
        'bpm': "BPM",
        'catalognumber': "Catalog",
        'category': "Category",
        'comment': "Comment",
        'compilation': "Compilation",
        'composer': "Composer",
        'composersort': "ComposerSort",
        'conductor': "Conductor",
        'copyright': "Copyright",
        'country': "Country",
        'date': "Year",
        'discnumber': "Disc",
        'discsubtitle': "DiscSubtitle",
        'djmixer': INVOLVED_PEOPLE,
        'encodedby': "EncodedBy",
        'encodersettings': "EncoderSettings",
        'encodingtime': "EncodingTime",
        'engineer': INVOLVED_PEOPLE,
        'genre': "Genre",
        'grouping': "ContentGroup",
        'isrc': "ISRC",
        'key': "InitialKey",
        'keywords': "Keywords",
        'label': "Publisher",
        'language': "Language",
        'license': "License",
        'lyricist': "Lyricist",
        'lyrics': "Lyrics",
        'media': "MediaType",
        'mixer': INVOLVED_PEOPLE,
        'mood': "Mood",
        'musicbrainz_albumartistid': "MusicBrainz Album Artist ID",
        'musicbrainz_albumid': "MusicBrainz Album ID",
        'musicbrainz_artistid': "MusicBrainz Artist ID",
        'musicbrainz_discid': "MusicBrainz Disc ID",
        'musicbrainz_labelid': "MusicBrainz Label ID",
        'musicbrainz_original_albumid': "MusicBrainz Original Album ID",
        'musicbrainz_original_artistid': "MusicBrainz Original Artist ID",
        'musicbrainz_recordingid': "MusicBrainz Recording ID",
        'musicbrainz_releasegroupid': "MusicBrainz Release Group ID",
        'musicbrainz_trackid': "MusicBrainz Track ID",
        'musicbrainz_workid': "MusicBrainz Work ID",
        'musicip_fingerprint': "MusicMagic Fingerprint",
        'musicip_puid': "MusicMagic PUID",
        'occasion': "Occasion",
        'originalalbum': "Original Title",
        'originalartist': "Original Artist", # Also MP3TAG OrigArtist
        'originaldate': "Original Date",
        'originallyricist': "Original Lyricist",
        'originalyear': "Original Year",
        'performer': INVOLVED_PEOPLE,
        'playdelay': "Play Delay",
        'producer': INVOLVED_PEOPLE,
        'quality': "Quality",
        'recordingcopyright': "Publicationright",
        'recordingdate': "Record Date",
        'recordinglocation': "Record Location",
        'releasecountry': "Release Country",
        'releasestatus': "Release Status",
        'releasetype': "Release Type",
        'remixer': "MixArtist",
        'script': "Script",
        'subtitle': "Subtitle",
        'tempo': "Tempo",
        'title': "Title",
        'titlesort': "TitleSort",
        'totaldiscs': "Disc",
        'totaltracks': "Track",
        'tracknumber': "Track",
        'web_discogs_artist': "Discogs Artist URL",
        'web_discogs_label': "Discogs Label URL",
        'web_discogs_release': "Discogs Release URL",
        'web_discogs_releasegroup': "Discogs Release Master URL",
        'web_lyrics': "Lyrics URL",
        'web_official_artist': "Bibliography",
        'web_official_label': "Official Label URL",
        'web_official_release': "Official Release URL",
        'web_wikipedia_artist': "Wikipedia Artist URL",
        'web_wikipedia_label': "Wikipedia Label URL",
        'web_wikipedia_release': "Abstract",
        'web_wikipedia_work': "Wikipedia Work URL",
        'work': "Work",
        'writer': "Writer",
        # Unclear what should happen if config.setting['enable_ratings'] == False
        # ~rating current saved as-is - mediamonkey/musicbee use values 0-5
        '~rating': "Rating",
        '~tagdate': "TaggedDate",
        '~web_coverart': "Cover Art URL",
        '~web_musicbrainz_artist': "MusicBrainz Artist URL",
        '~web_musicbrainz_label': "MusicBrainz Label URL",
        '~web_musicbrainz_recording': "MusicBrainz Recording URL",
        '~web_musicbrainz_release': "MusicBrainz Release URL",
        '~web_musicbrainz_releasegroup': "MusicBrainz Release Group URL",
        '~web_musicbrainz_work': "MusicBrainz Work URL",
    }
        # None: "iTunesMediaType",
    __load_tags = {}
    for meta, tag in __save_tags.iteritems():
        __load_tags.setdefault(tag.lower(), []).append(meta)

    # Additional compatibility
    __load_tags["musicbrainz_trackid"] = ['musicbrainz_recordingid']
    __load_tags["musicbrainz_releasetrackid"] = ["musicbrainz_trackid"]

    __involvedpeople = [k for k, v in __save_tags.iteritems() if v == INVOLVED_PEOPLE]
    __web_tags = [k for k, v in __save_tags.iteritems() if v == "Related"]

    _supported_tags = __save_tags.keys()

    __compatibility = {
        "band": __save_tags['albumartist'], # MediaMonkey, MusicBee
        "involvedpeople": INVOLVED_PEOPLE, # Mp3Tag
        "musicbrainz_trmid": '', # Obsolete
        "origartist": __save_tags['originalartist'], # Mp3Tag
        "origlyricist": __save_tags['originallyricist'], # Mp3Tag
        "origalbum": __save_tags['originalalbum'], # Mp3Tag
        "origyear": __save_tags['originaldate'], # Mp3Tag
        "rating mm": __save_tags['~rating'], # Mp3Tag
        "rating winamp": __save_tags['~rating'], # Mp3Tag
        "rating wmp": __save_tags['~rating'], # Mp3Tag
        "musicbrainz_albumstatus": __save_tags['releasestatus'], # Picard < 1.4
        "musicbrainz_albumtype": __save_tags['releasetype'], # Picard < 1.4
        "display artist": __save_tags['artistsort'], # MusicBee
        "weblink": __save_tags['web_official_artist'], # Picard < 1.4
        "wwwartist": __save_tags['web_official_artist'], # Mp3Tag
        #"MusicMagic Fingerprint": '', # Obsolete
        #"musicip_fingerprint": '', # Obsolete
    }

    # Add Picard backward compatibility for tags saved with metadata names
    for tag, names in __load_tags.iteritems():
        if len(names) == 1 and names[0] not in __load_tags:
            name = names[0][1:] if names[0].startswith('~') else names[0]
            if name != tag:
                __compatibility[name] = tag

    # Add case variants for existing
    for tag in __compatibility.keys():
        __compatibility[tag.upper()] = __compatibility[tag]
        __compatibility[tag.title()] = __compatibility[tag]

    # Priority for image selection for single embedded image
    __IMAGE_TYPES = [
        "track",
        "front",
        "poster",
        "liner",
        "medium",
        "booklet",
        "back",
        "tray",
        "other",
    ]

    def _load(self, filename):
        log.debug("Loading file: %r", filename)
        file = self._File(encode_filename(filename))
        metadata = Metadata()
        self._info(metadata, file)
        if not file.tags:
            return metadata
        tags = file.tags

        # Fix old tag naming and make it compatible with Jaikoz
        t = {}
        for tag in tags.keys():
            if tag.lower() in [
                    'musicbrainz_recordingid',
                    'musicbrainz_trackid',
                    'musicbrainz_releasetrackid'
                ]:
                t[tag.lower()] = tag
        if ('musicbrainz_recordingid' not in t
                and 'musicbrainz_trackid' in t
                and 'musicbrainz_releasetrackid' in t):
            log.info('APEv2: File %r: Upgrading obsolete MBID tags',
                path.split(filename)[1])
            tags[t['musicbrainz_recordingid']] = tags[t['musicbrainz_trackid']]
            tags[t['musicbrainz_trackid']] = tags[t['musicbrainz_releasetrackid']]
        if 'musicbrainz_releasetrackid' in t:
            del tags[t['musicbrainz_releasetrackid']]

        for old, new in self.__compatibility.iteritems():
            if old not in tags:
                continue
            if new:
                if new in tags:
                    log.warning('APEv2: File %r: Cannot upgrade text tag - new tag already exists: %s=>%s',
                        path.split(filename)[1], old, new)
                    continue
                tags[new] = tags[old]
                log.info('APEv2: File %r: Upgrading tag: %s=>%s',
                    path.split(filename)[1], old, new)
            del tags[old]

        related_values = []
        for tag_name, values in tags.iteritems():
            name = tag_name.lower()
            if name == "related":
                continue
            elif name in ['artist', 'album artist']:
                name = self.__load_tags[name][0]
                name = name[:-1] if name.endswith('s') else name
                if type(values) != 'list':
                    value = [value]
                # [Album]Artist contains [album]artist followed by [album]artists
                metadata[name] = values[0]
                if len(values) > 1:
                    for value in values[1:]:
                        metadata.add('%ss' % name, value)
            elif name == "year":
                metadata["date"] = sanitize_date(values[0])
            elif name == "original date":
                date = sanitize_date(values[0])
                metadata["originaldate"] = date
                if 'originalyear' not in metadata:
                    metadata["originalyear"] = date[:4]
            elif name == "original year":
                date = sanitize_date(values[0])
                metadata["originalyear"] = date[:4]
                if 'originaldate' not in metadata:
                    metadata["originaldate"] = date
            elif name == "track":
                track = values[0].split('/', 2) if '/' in values[0] else [values[0]]
                metadata["tracknumber"] = track[0]
                if len(track) > 1:
                    metadata["totaltracks"] = track[1]
            elif name == "disc":
                disc = values[0].split('/', 2) if '/' in values[0] else [values[0]]
                metadata["discnumber"] = disc[0]
                if len(disc) > 1:
                    metadata["totaldiscs"] = disc[1]
            elif name == 'rating':
                # Unclear what should happen if config.setting['enable_ratings'] == False
                # Rating in WMA ranges from 0 to 99, normalize this to the range 0 to 5
                metadata["~rating"] = int(round(float(unicode(values[0])) / 5.0 * (config.setting['rating_steps'] - 1)))
            elif values.kind != mutagen.apev2.BINARY:
                for value in values:
                    value = value.replace("\r\n", "\n")
                    line = value.split("\n", 1)[0] if "\n" in value else value
                    if name == 'involved people':
                        # mediamonkey compatibility - stored as a single string
                        value = value.split('; ') if '; ' in value else [value]
                        for person in value:
                            role, person = unpack_performer(person)
                            if role and role in self.__involvedpeople:
                                metadata.add(role, person)
                            else:
                                if not role:
                                    log.info('APEv2: File %r: Loading performer without instrument: %s',
                                        path.split(filename)[1], person)
                                metadata.add('performer:%s' % role, person)
                    elif name == 'performer': # Backwards compatibility
                        # Name (Instrument) or Instrument=Name
                        role, person = unpack_performer(value)
                        if not role:
                            log.info('APEv2: File %r: Loading performer without instrument: %s',
                                path.split(filename)[1], person)
                        metadata.add('performer:%s' % role, person)
                    elif name in ['comment', 'lyrics']:
                        id, value = unpack_performer(value)
                        colon = ':' if id else ''
                        metadata.add('%s%s%s' % (name, colon, id), value)
                    elif name in self.__load_tags:
                        if len(self.__load_tags[name]) > 1:
                            log.error('APEv2: Key needing explicit decoding not handled: %s', name)
                        metadata.add(self.__load_tags[name][0], value)
                    elif name in self._supported_tags:
                        metadata.add('~apev2:%s' % tag_name, value)
                        log.info('APEv2: File %r: Loading APEv2 specific metadata which conflicts with known Picard tag: %s=%r',
                            path.split(filename)[1], tag_name, value)
                    else:
                        metadata.add(name, value)
                        log.info('APEv2: File %r: Loading user metadata: %s=%s',
                            path.split(filename)[1], name, value)
            elif name.startswith("cover art"):
                if '\0' in values.value:
                    descr, data = values.value.split('\0', 1)
                    try:
                        coverartimage = TagCoverArtImage(
                            file=filename,
                            tag=name,
                            data=data,
                        )
                    except CoverArtImageError as e:
                        log.error('APEv2: File %r: Cannot load image: %s', filename, e)
                    else:
                        metadata.append_image(coverartimage)
                else:
                    log.warning('APEv2: File %r: Invalid cover art skipped: %s',
                        path.split(filename)[1], tag_name)

        return metadata

    def _save(self, filename, metadata):
        """Save metadata to the file."""
        log.debug("Saving file: %r", filename)
        try:
            tags = mutagen.apev2.APEv2(encode_filename(filename))
        except mutagen.apev2.APENoHeaderError:
            tags = mutagen.apev2.APEv2()
        if config.setting["clear_existing_tags"]:
            tags.clear()
        elif metadata.images_to_be_saved_to_tags:
            for name, value in tags.items():
                if name.lower().startswith('cover art') and value.kind == mutagen.apev2.BINARY:
                    del tags[name]

        t = {}
        performers = []
        production = []
        for name, value in metadata.iteritems():
            value = value.encode('utf-8').replace("\r\n", "\n").replace("\n", "\r\n")
            name, desc = name.split(':', 1) if ':' in name else (name, '')

            if name in [
                        'totaltracks', 'totaldiscs',
                        'artists', 'albumartists',
                        'year',
                    ]:
                # These tags are handled manually below
                continue
            elif name == 'tracknumber':
                if 'totaltracks' in metadata:
                    t['Track'] = '%s/%s' % (value, metadata['totaltracks'])
                else:
                    t['Track'] = value
            elif name == 'discnumber':
                if 'totaldiscs' in metadata:
                    t['Disc'] = '%s/%s' % (value, metadata['totaldiscs'])
                else:
                    t['Disc'] = value
            elif name == "~rating":
                # Unclear what should happen if config.setting['enable_ratings'] == False
                t["Rating"] = str(float(value) * 5.0 / (config.setting['rating_steps'] - 1))
            elif name in ['artist', 'albumartist']:
                t[self.__save_tags[name]] = [value]
                for artist in metadata.getall('%ss' % name):
                    t[self.__save_tags[name]].append(artist.encode('utf-8'))
            elif name in ['comment', 'lyrics']:
                desc += '=' if desc else ''
                t.setdefault(self.__save_tags[name], []).append('%s%s' % (desc, value))
            elif name in self.__involvedpeople:
                # Performers and non-performers are separated here
                # so that performers appear first in the Involved People
                if name == 'performer':
                    if not desc:
                        log.info('APEv2: File %r: Saving performer without instrument: %s',
                            path.split(filename)[1], value)
                    # And vocalists appear before instrument performers
                    value = pack_performer(desc, value)
                    if 'vocal' in desc:
                        performers.insert(0, value)
                    else:
                        performers.append(value)
                else:
                    production.append(pack_performer(name, value))
            elif name in self.__save_tags:
                if isurl(value):
                    t.setdefault("Related", []).append(value)
                t.setdefault(self.__save_tags[name], []).append(value)
            elif name.startswith('~apev2:'):
                t.setdefault(name[7:], []).append(value)
            elif not name.startswith('~'):
                if name.lower() not in self.__load_tags:
                    log.info('APEv2: File %r: Saving user metadata: %s=%s',
                        path.split(filename)[1], name, value)
                    if isurl(value):
                        t.setdefault("Related", []).append(value)
                    t.setdefault(name.title(), []).append(value)
                else:
                    log.warning('APEv2: File %r: Unable to save user metadata - conflict with standard metadata: %s=%s',
                        path.split(filename)[1], name, value)

        if performers or production:
            t["Involved People"] = performers + production

        t["TaggedDate"] = strftime('%Y-%m-%dT%H:%M:%S')

        for name, values in t.iteritems():
            tags[name] = values if len(values) > 1 else values[0]

        # Although spec only allows one image, musicbee supports multiple images
        # and Mutagen allows us to create multiple images.
        # The previous version said that "the spec only supports a single image"
        # however the formal APEv2 specification does not support images at all.
        # The code below saves multiple images in priority sequence
        # with the intention that players that do not support multiple images
        # will see only the first, highest-priority image and ignore the others
        # however there is no guarantee that the sequence they are created
        # is the same sequence that they are written to the file or that
        # a player will show the first image.
        # To avoid saving > 1 image, set single_image = True.
        single_image = True
        image_types = {}
        for image in metadata.images_to_be_saved_to_tags:
            image_types.setdefault(image.maintype, []).append(image)

        for type in self.__IMAGE_TYPES:
            if type in image_types:
                images = image_types[type]
                i = '' if len(images) == 1 or single_image else 1
                for image in images:
                    num = ' #%d' % i if i else ''
                    cover_filename = key = 'Cover Art (%s)%s' % (image.maintype.title(), num)
                    cover_filename += image.extension
                    tags[key] = mutagen.apev2.APEValue(cover_filename.encode('utf-8') + '\0' + image.data, mutagen.apev2.BINARY)
                    if i:
                        i += 1
                    if single_image:
                        break
                if single_image:
                    break

        tags.save(encode_filename(filename))


class MusepackFile(APEv2File):

    """Musepack file."""
    EXTENSIONS = [".mpc", ".mp+"]
    NAME = "Musepack"
    _File = mutagen.musepack.Musepack

    def _info(self, metadata, file):
        super(MusepackFile, self)._info(metadata, file)
        metadata['~format'] = "Musepack, SV%d" % file.info.version


class WavPackFile(APEv2File):

    """WavPack file."""
    EXTENSIONS = [".wv"]
    NAME = "WavPack"
    _File = mutagen.wavpack.WavPack

    def _info(self, metadata, file):
        super(WavPackFile, self)._info(metadata, file)
        metadata['~format'] = "%s (%s)" % (self.NAME, file.info.version)

    def _save_and_rename(self, old_filename, metadata):
        """Includes an additional check for WavPack correction files"""
        wvc_filename = old_filename.replace(".wv", ".wvc")
        if path.isfile(wvc_filename):
            if config.setting["rename_files"] or config.setting["move_files"]:
                self._rename(wvc_filename, metadata)
        return File._save_and_rename(self, old_filename, metadata)


class OptimFROGFile(APEv2File):

    """OptimFROG file."""
    EXTENSIONS = [".ofr", ".ofs", ".off"]
    # .ofr=Standard, .ofs=DualStream, .off=IEEE float
    NAME = "OptimFROG"
    _File = mutagen.optimfrog.OptimFROG

    def _info(self, metadata, file):
        super(OptimFROGFile, self)._info(metadata, file)
        if file.filename.lower().endswith(".off"):
            metadata['~format'] = "OptimFROG IEEE Float Audio"
        elif file.filename.lower().endswith(".ofs"):
            metadata['~format'] = "OptimFROG DualStream Audio"
        else:
            metadata['~format'] = "OptimFROG Lossless Audio"


class MonkeysAudioFile(APEv2File):

    """Monkey's Audio file."""
    EXTENSIONS = [".ape"]
    NAME = "Monkey's Audio"
    _File = mutagen.monkeysaudio.MonkeysAudio

    def _info(self, metadata, file):
        super(MonkeysAudioFile, self)._info(metadata, file)
        metadata['~format'] = '%s - version %.2f' % (self.NAME, file.info.version)


class TAKFile(APEv2File):

    """TAK file."""
    EXTENSIONS = [".tak"]
    NAME = "Tom's lossless Audio Kompressor"
    _File = tak.TAK

    def _info(self, metadata, file):
        super(TAKFile, self)._info(metadata, file)
        metadata['~format'] = self.NAME
