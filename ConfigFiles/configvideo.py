from matplotlib import font_manager
import platform


class VideoConfig:

    def __init__(self):
        self.resolution = (800, 800)
        self.font_name, self.font_size = (self._get_font(), 40)

    def _get_font(self):
        """
        :return: "global" font to be drawn
        OS common fonts: http://www.ars-informatica.ca/article.php?article=59
        """

        all_system_fonts = self._process_system_fonts()
        preferred_font = "OpenSans-Bold"
        fallback_font = "Monaco Mac"

        if preferred_font in all_system_fonts:
            return preferred_font
        else:
            return fallback_font


    def _process_system_fonts(self):

        """
        :return: all fonts based on user's operating system

        This GitHub snippet removes the extra characters
        attached the font string, such as slashes and
        any parent directories:

        https://gist.github.com/yoavram/5141090
        """

        fonts = []
        if platform.system() == "Windows":  # TODO: Look into packages that are built for other OS's
            for x in font_manager.win32InstalledFonts():
                x = x[::-1]
                dot = x.find('.')
                slash = x.find('\\')
                x = x[slash - 1:dot:-1]
                fonts += [x]
            fonts.sort()
        return fonts


"""

Please take note of the following critical comments:

Assuming this project will be compiled with pyinstaller, you *MUST* 
use pygame.font.SysFont("a font that actually exists on the system").
If you use pygame.font.Font(), pygame will end up using a package 
called "pkg_resources"- this package is *not* supported by pyinstaller.
So, in the meantime, use SysFont() until pyinstaller supports pkg_resources. 

# http://pyinstaller.47505.x6.nabble.com/Pygame-and-PyInstaller-td2424.html

"""


