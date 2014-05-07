from uowmlib import WPCollection, WPConfiguration
from uowmbackends import WPBackendGsettings
import unittest
from shell import shell

class TesCollection(unittest.TestCase):
    def setUp(self):
        self.col = WPCollection([])

    def test_draw(self):
        winner = self.col.draw()
        self.assertIn(winner, self.col.file_list)
    
    def test_dummy(self):
        self.assertEqual(1,1)

class TestGsettings(unittest.TestCase):
    def setUp(self):
        self.col = WPCollection([])
        self.backend = WPBackendGsettings()

    def test_set_wp(self):
        winner = self.col.draw()
        self.backend.set_wallpaper(winner)
        picture_uri = shell(
            "/usr/bin/env gsettings get org.gnome.desktop.background \
            picture-uri").output()[0]
        self.assertEqual("'file://"+winner+"'", picture_uri)

class TestConfiguration(unittest.TestCase):
    def setUp(self):
        self._conf = WPConfiguration("./uowmrc-example")
    
    def test_default_dirs(self):
        self.assertEqual(self._conf.default_dirs, ['/home/pedro/wallpapers'])

    def test_append_default_dirs(self):
        self.assertFalse(self._conf.append_default_dirs)

    def test_log_file(self):
        self.assertEqual(self._conf.log_file, '/home/pedro/.uowm/log')

    def test_no_repeat(self):
        self.assertEqual(self._conf.no_repeat, 20)

    def test_cycle_dirs(self):
        self.assertTrue(self._conf.cycle_dirs)

    def test_backend(self):
        self.assertEqual(self._conf.backend,  "Noop")

if __name__ == '__main__':
    unittest.main()
