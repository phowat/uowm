#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

class WPBackendGsettings(object):
    def set_wallpaper(self, wpaper):
        # In case you don't have DBUS_SESSION_BUS_ADDRESS and/or
        # DISPLAY set. export it before running this script. 
        cmd = """\
/usr/bin/env gsettings set \
org.gnome.desktop.background picture-uri "file://{0}"\
        """.format(wpaper)
        os.system(cmd)
        
class WPBackendMate(object):
    def set_wallpaper(self, wpaper):

        cmd = """\
/usr/bin/env mateconftool-2 --set --type=string \
/desktop/mate/background/picture_filename "file://{0}"\
        """.format(wpaper)
        os.system(cmd)
        
class WPBackendXmonad(object):
    # Through feh.
        def set_wallpaper(self, wpaper):
            os.system("/usr/bin/feh --bg-max "+wpaper);

