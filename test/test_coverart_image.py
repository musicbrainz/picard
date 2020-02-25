# -*- coding: utf-8 -*-
#
# Picard, the next-generation MusicBrainz tagger
#
# Copyright (C) 2019 Philipp Wolfer
# Copyright (C) 2019-2020 Laurent Monin
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


from collections import defaultdict
import os.path
import unittest

from test.picardtestcase import (
    PicardTestCase,
    create_fake_png,
)

from picard import config
from picard.const.sys import IS_WIN
from picard.coverart.image import (
    CoverArtImage,
    CoverArtImageIOError,
    LocalFileCoverArtImage,
)
from picard.metadata import Metadata


def create_image(extra_data, types=None, support_types=False,
                 support_multi_types=False, comment=None):
    return CoverArtImage(
        data=create_fake_png(extra_data),
        types=types,
        comment=comment,
        support_types=support_types,
        support_multi_types=support_multi_types,
    )


class CoverArtImageTest(PicardTestCase):
    def setUp(self):
        super().setUp()
        settings = {
            'ascii_filenames': False,
            'caa_image_type_as_filename': False,
            'cover_image_filename': 'cover',
            'enabled_plugins': [],
            'save_images_overwrite': True,
            'windows_compatibility': False,
        }

        config.setting = settings.copy()

    def test_is_front_image_no_types(self):
        image = create_image(b'a')
        self.assertTrue(image.is_front_image())
        image.can_be_saved_to_metadata = False
        self.assertFalse(image.is_front_image())

    def test_is_front_image_types_supported(self):
        image = create_image(b'a', types=["booklet", "front"], support_types=True)
        self.assertTrue(image.is_front_image())
        image.is_front = False
        self.assertFalse(image.is_front_image())
        image = create_image(b'a', support_types=True)
        self.assertFalse(image.is_front_image())

    def test_is_front_image_no_types_supported(self):
        image = create_image(b'a', types=["back"], support_types=False)
        self.assertTrue(image.is_front_image())

    def test_maintype(self):
        self.assertEqual("front", create_image(b'a').maintype)
        self.assertEqual("front", create_image(b'a', support_types=True).maintype)
        self.assertEqual("front", create_image(b'a', types=["back", "front"], support_types=True).maintype)
        self.assertEqual("back", create_image(b'a', types=["back", "medium"], support_types=True).maintype)
        self.assertEqual("front", create_image(b'a', types=["back", "medium"], support_types=False).maintype)

    def test_compare_without_type(self):
        image1 = create_image(b'a', types=["front"])
        image2 = create_image(b'a', types=["back"])
        image3 = create_image(b'a', types=["back"], support_types=True)
        image4 = create_image(b'b', types=["front"])

        self.assertEqual(image1, image2)
        self.assertEqual(image1, image3)
        self.assertNotEqual(image1, image4)

    def test_compare_with_primary_type(self):
        image1 = create_image(b'a', types=["front"], support_types=True)
        image2 = create_image(b'a', types=["front", "booklet"], support_types=True, support_multi_types=True)
        image3 = create_image(b'a', types=["back"], support_types=True)
        image4 = create_image(b'b', types=["front"], support_types=True)
        image5 = create_image(b'a', types=[], support_types=True)
        image6 = create_image(b'a', types=[], support_types=True)

        self.assertEqual(image1, image2)
        self.assertNotEqual(image1, image3)
        self.assertNotEqual(image1, image4)
        self.assertNotEqual(image3, image5)
        self.assertEqual(image5, image6)

    def test_compare_with_multiple_types(self):
        image1 = create_image(b'a', types=["front"], support_types=True, support_multi_types=True)
        image2 = create_image(b'a', types=["front", "booklet"], support_types=True, support_multi_types=True)
        image3 = create_image(b'a', types=["front", "booklet"], support_types=True, support_multi_types=True)
        image4 = create_image(b'b', types=["front", "booklet"], support_types=True, support_multi_types=True)

        self.assertNotEqual(image1, image2)
        self.assertEqual(image2, image3)
        self.assertNotEqual(image2, image4)

    def test_set_data(self):
        imgdata = create_fake_png(b'a')
        imgdata2 = create_fake_png(b'xxx')
        # set data once
        coverartimage = CoverArtImage(data=imgdata2)
        tmp_file = coverartimage.tempfile_filename
        filesize = os.path.getsize(tmp_file)
        # ensure file was written, and check its length
        self.assertEqual(filesize, len(imgdata2))
        self.assertEqual(coverartimage.data, imgdata2)

        # set data again, with another payload
        coverartimage.set_data(imgdata)

        tmp_file = coverartimage.tempfile_filename
        filesize = os.path.getsize(tmp_file)
        # check file length again
        self.assertEqual(filesize, len(imgdata))
        self.assertEqual(coverartimage.data, imgdata)

    def test_delete_file_removed(self):
        payload = b'atest'
        image_ = create_image(payload, comment='1')
        image = create_image(payload, comment='2')
        self.assertIsNotNone(image.datahash._filename)
        data = image.datahash.data
        self.assertEqual(data, b'\x89PNG\r\n\x1a\naaaaIHDR\x00\x00\x00d\x00\x00\x00datest')
        self.assertEqual(image_.datahash.data, data)
        # simulate removal of temporary file by external command
        os.unlink(image.datahash._filename)
        # the following should handle this case without raising an exception
        image.datahash.delete_file()
        self.assertIsNone(image.datahash._filename)
        self.assertIsNone(image.datahash.data)
        with self.assertRaises(CoverArtImageIOError):
            data = image_.data

    def test_coverartimage_image_as_string(self):
        image = CoverArtImage(data=None)
        self.assertEqual(image.imageinfo_as_string(), '')
        image = create_image(b'a')
        self.assertEqual(
            image.imageinfo_as_string(),
            'w=100 h=100 mime=image/png ext=.png datalen=25 file=' +
            image.tempfile_filename
        )

    def test_coverartimage_url_with_query(self):
        image = CoverArtImage(url='http://example.com/image.jpg?size=1024')
        self.assertEqual(image.path, '/image.jpg?size=1024')

    def test_coverartimage_source(self):
        class CAImage(CoverArtImage):
            sourceprefix = 'TEST'
        image = CAImage(url='http://example.com/image.jpg')
        self.assertEqual(image.source, 'TEST: http://example.com/image.jpg')
        image = CAImage()
        self.assertEqual(image.source, 'TEST')

    def test_coverartimage_str_repr(self):
        image = CoverArtImage(url='url',
                              types=['front'], comment='comment')
        image.is_front = True
        self.assertEqual(
            str(image),
            "Image from url of type front and comment 'comment'"
        )
        self.assertEqual(
            repr(image),
            "CoverArtImage(url='url', types=['front'], support_types=False, "
            "support_multi_types=False, is_front=True, comment='comment')"
        )

    def test_save(self):
        metadata = Metadata()
        image = create_image(b'x', types=['back'], support_types=True,
                             support_multi_types=True)
        tmpdir = self.mktmpdir()
        def listdir():
            return os.listdir(tmpdir)
        counters = defaultdict(lambda: 0)

        image.can_be_saved_to_disk = False
        image.save(tmpdir, metadata, counters)
        self.assertEqual(listdir(), [])

        image.can_be_saved_to_disk = True
        image.save(tmpdir, metadata, counters)
        self.assertIn('cover.png', listdir())

        image.save(tmpdir, metadata, counters)
        self.assertIn('cover (1).png', listdir())

        config.setting['caa_image_type_as_filename'] = False
        image.save(tmpdir, metadata, counters)
        self.assertIn('cover (2).png', listdir())

        image.is_front = False
        image.can_be_saved_to_metadata = True
        config.setting['caa_image_type_as_filename'] = True
        image.save(tmpdir, metadata, counters)
        self.assertIn('back.png', listdir())

        tmpdir = self.mktmpdir()
        counters = defaultdict(lambda: 0)
        config.setting['save_images_overwrite'] = True
        image.save(tmpdir, metadata, counters)
        self.assertIn('back.png', listdir())

        # FIXME
        #image.save(tmpdir, metadata, counters)
        #self.assertEqual(len(listdir()), 1)

    def test_normalized_types(self):
        image = create_image(b'a', types=["front", 'back'], support_types=True, support_multi_types=True)
        self.assertEqual(image.normalized_types(), ['back', 'front'])

        image = create_image(b'a')
        self.assertEqual(image.normalized_types(), ['front'])

        image.is_front = False
        self.assertEqual(image.normalized_types(), ['-'])

    def test_types_as_string(self):
        image = create_image(b'a', types=["front", 'back'], support_types=True, support_multi_types=True)
        self.assertEqual(image.types_as_string(translate=False, separator=';'),
                         'back;front')
        # FIXME: translate=True


class LocalFileCoverArtImageTest(PicardTestCase):
    def test_set_file_url(self):
        path = '/some/path/image.jpeg'
        image = LocalFileCoverArtImage(path)
        self.assertEqual(image.url.toString(), 'file://' + path)

    def test_support_types(self):
        path = '/some/path/image.jpeg'
        image = LocalFileCoverArtImage(path)
        self.assertFalse(image.support_types)
        self.assertFalse(image.support_multi_types)
        image = LocalFileCoverArtImage(path, support_types=True)
        self.assertTrue(image.support_types)
        self.assertFalse(image.support_multi_types)
        image = LocalFileCoverArtImage(path, support_multi_types=True)
        self.assertFalse(image.support_types)
        self.assertTrue(image.support_multi_types)

    @unittest.skipUnless(IS_WIN, "windows test")
    def test_windows_path(self):
        path = 'C:\\Music\\somefile.mp3'
        image = LocalFileCoverArtImage(path)
        self.assertEqual(image.url.toLocalFile(), 'C:/Music/somefile.mp3')
