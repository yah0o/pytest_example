import sys
import subprocess

output = subprocess.check_output([sys.executable, '-m', 'pip', 'freeze'])
INSTALLED_PACKAGES = [r.decode().split('==')[0] for r in output.split()]

HAS_COLOR_LIBS = 'termcolor' in INSTALLED_PACKAGES and 'colorama' in INSTALLED_PACKAGES
if HAS_COLOR_LIBS:
    import termcolor
    import colorama
    colorama.init()


class PlanLogger(object):

    HEADER_COLOR = 'magenta'

    def __init__(self, header, streams):
        self.__streams = streams
        self.__header = header

    def add_stream(self, stream):
        """
        :param stream:
        :return:
        """

        self.__streams.append(stream)

    def log(self, string, output_color=None):
        """
        :param string:
        :param output_color:
        :return:
        """

        output_color = 'cyan' if output_color is None else output_color
        self.write(self.__header, output_color=PlanLogger.HEADER_COLOR)
        self.write(': ')
        self.writeln(string, output_color)

    def pipe(self, from_stream):
        """
        :param from_stream:
        :return:
        """

        out = None
        while out != '':
            out = from_stream.read(1)
            self.write(out)
        from_stream.close()

    def write(self, content, output_color=None):
        """
        Available text colors:
            red, green, yellow, blue, magenta, cyan, white.

        :param content:
        :param output_color:
        :return:
        """

        for stream in self.__streams:
            if stream is sys.stdout and output_color is not None and HAS_COLOR_LIBS:
                stream.write(termcolor.colored(content, output_color))
            else:
                stream.write(content)
            stream.flush()

    def writeln(self, content, output_color=None):
        """
        :param content:
        :param output_color:
        :return:
        """

        self.write('{}\n'.format(content), output_color)
