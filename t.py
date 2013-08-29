from uowms import WPCollection, WPBackendGsettings
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

if __name__ == '__main__':
    unittest.main()
