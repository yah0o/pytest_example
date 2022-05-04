import subprocess
import sys
import os
from pip._internal import main as pip

output = subprocess.check_output([sys.executable, '-m', 'pip', 'freeze'])
INSTALLED_PACKAGES = [r.decode().split('==')[0] for r in output.split()]


class Remote(object):

    @staticmethod
    def create_fabric_connection(host, user, port, log, password=None):
        if 'fabric' not in INSTALLED_PACKAGES:
            log.log('Installing requirement fabric ...')
            try:
                log.log('Trying to "pip install fabric"...')
                pip(['install', 'fabric'])
                import fabric
            except ImportError:
                log.log('Failed to "pip install fabric"...', output_color='red')
                log.log('Trying to "sudo pop install from pip"...')
                os.system("sudo pip install fabric")

        import fabric
        return fabric.Connection(host=host, user=user, port=port, connect_kwargs={
            'password': password,
        })

    def __init__(self, host, user, port, logger):
        self.__log = logger
        self.__connection = Remote.create_fabric_connection(host, user, port, self.__log)

    @property
    def log(self):
        """
        :return:
        """

        return self.__log

    def execute(self, *args):
        """
        :param args:
        :return:
        """
        
        args = ' '.join(args)
        self.__log.log('> {}'.format(args))
        output = self.__connection.run(args, hide=True)

        for line in output.stdout.split('\n'):
            if not line:
                continue
            self.__log.log('stdout: {}'.format(line), output_color='white')
        for line in output.stderr.split('\n'):
            if not line:
                continue
            self.__log.log('stderr: {}'.format(line), output_color='red')

        return output

    def upload(self, file_or_directory, *args, **kwargs):
        """
        :param file_or_directory:
        :param args:
        :param kwargs:
        :return:
        """
        self.__log.log('> uploading: {}'.format(file_or_directory))
        self.__connection.put(file_or_directory, *args, **kwargs)

    def download(self, file_or_directory, *args, **kwargs):
        """
        :param file_or_directory:
        :param args:
        :param kwargs:
        :return:
        """

        self.__log.log('> downloading: {}'.format(file_or_directory))
        return self.__connection.get(file_or_directory, *args, **kwargs)
