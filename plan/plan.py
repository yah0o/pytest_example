import os
import subprocess
import sys

from logger import PlanLogger
from remote import Remote


class Plan(object):

    def __init__(self, plan_name):

        self.__name = plan_name
        self._log = None
        self._env_var = {}

    def initialize(self, streams=None):
        self._env_var = os.environ.copy()
        streams = [sys.stdout] if streams is None else streams
        self._log = PlanLogger(self.__name, streams)

        cwd = os.getcwd()
        self.echo('Adding {} to sys path in order to use local imports'.format(cwd))
        sys.path.append(cwd)

        # python's current directory is located where the script is, not where it is ran from.
        # this makes it so that the current directory is where the plan is called from
        self.cd(self.pwd())

    def echo(self, output, output_color=None):

        return self._log.log(output, output_color=output_color)

    def export(self, key, value):

        self._log.log('export {}={}'.format(key, value), output_color='green')
        self._env_var[key] = str(value)

    def remote(self, host, user, port, streams=None):
        streams = [sys.stdout] if streams is None else streams
        log = PlanLogger('[{}@{}:{}]{}'.format(user, host, port, self.__name), streams)
        plan = Remote(host, user, port, log)
        return plan

    def pwd(self):

        pwd = os.getcwd()
        return pwd

    def cd(self, directory):

        self._log.log('cd {}'.format(directory), output_color='green')
        os.chdir(directory)

    def pip_install(self, *args):

        pip_args = ['pip', 'install'] + list(args)
        self._log.log('pip install {}'.format(' '.join(pip_args)), output_color='green')
        os.system(' '.join(pip_args))

    def execute(self, *args):

        cmd = list(args)

        # for manual any arg with spaces needs to be wrapped in "'s
        self._log.log(' '.join(['\"{}\"'.format(c) if ' ' in c else c for c in cmd]), output_color='green')
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
            env=self._env_var
        )

        try:
            self._log.pipe(process.stdout)
            self._log.pipe(process.stderr)
            return process.wait()

        except KeyboardInterrupt:
            for line in iter(process.stdout.readline, ''):
                self._log.write(line, output_color='red')
            return 1
        except Exception as e:
            self._log.log(e, output_color='red')
            return 2

    def integration_test(
        self,
        tests,
        environment,
        username=None,
        password=None,
        pin=None,
        secret_key=None,
        allure=None,
        reruns=2,
        threads=None,
        marks=None,
        other_args=None
    ):
        args = [
            'pytest',
            tests,
            '--env={}'.format(environment),
            '--skip_pub=1',  # always skip pub because we already did it
            '--disable-warnings',
            '--reruns={}'.format(reruns),
        ]

        if allure is not None:
            args += ['--alluredir', allure]

        if threads is not None:
            args = args + ['-n', threads]
            base_mark = "not notthreadsafe"
        else:
            base_mark = "notthreadsafe"

        args += ['-m', base_mark if marks is None else "{} and {}".format(base_mark, marks)]

        if username is not None:
            args += ['--username', username]
        if password is not None:
            args += ['--password', password]
        if pin is not None:
            args += ['--pin', pin]
        if secret_key is not None:
            args += ['--secret_key', secret_key]

        if other_args is not None:
            args += other_args

        return self.execute(*args)

    def exit(self, status):

        sys.exit(status)
