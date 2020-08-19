"""
MIT License

Copyright (c) 2020 Lawrence Chiappelli

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""


class VideoConfig:

    def __init__(self):
        self._resolution = (800, 800)
        self._font_name = "See TODO"  # TODO: Figure out how to grab the specific path of file- returning the string from here will not work in GUI.py
        self._font_size = 40

    def get_font(self, override_font=None):
        """
        :param override_font: override the default font?
        :return: font to be drawn
        OS common fonts: http://www.ars-informatica.ca/article.php?article=59
        """

        if override_font is None:
            return override_font
        return self._font_name

    def get_font_size(self, override_size=None):

        """
        :param override_size: override font size on an individual basis
        :return: font size
        """

        if override_size:
            return override_size
        return self._font_size

    def get_resolution(self):
        return self._resolution


"""

Please take note of the following critical comments:

Assuming this project will be compiled with pyinstaller, you *MUST* 
use pygame.font.SysFont("a font that actually exists on the system").
If you use pygame.font.Font(), pygame will end up using a package 
called "pkg_resources"- this package is *not* supported by pyinstaller.
So, in the meantime, use SysFont() until pyinstaller supports pkg_resources. 

# http://pyinstaller.47505.x6.nabble.com/Pygame-and-PyInstaller-td2424.html

"""


