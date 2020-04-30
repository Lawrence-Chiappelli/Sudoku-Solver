resolution = (800, 800)
font_name, font_size = ("Arial", 40)
# freesansbold.ttf would have been preferred
# Comic cans is too large

"""

Please take note of the following critical comments:

Assuming this project will be compiled with pyinstaller, you *MUST* 
use pygame.font.SysFont("a font that actually exists on the system").
If you use pygame.font.Font(), pygame will end up using a package 
called "pkg_resources"- this package is *not* supported by pyinstaller.
So, in the meantime, use SysFont() until pyinstaller supports pkg_resources. 

# http://pyinstaller.47505.x6.nabble.com/Pygame-and-PyInstaller-td2424.html
TODO: https://stackoverflow.com/questions/31546088/check-system-if-font-exists-python-os-agnostic

"""