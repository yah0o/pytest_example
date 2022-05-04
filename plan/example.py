# remember to set from the testing directory: export PYTHONPATH=.

from plan import Plan
import sys


plan = Plan('test plan')
with open('optional_recording_log.txt', 'w+') as a_file:
    plan.initialize(streams=[sys.stdout, a_file])
    remote = plan.remote(host='ix-c1-60-20.be.core.pw', user='perftest', port=2200, streams=[sys.stdout, a_file])

    plan.echo('checking that python is installed on remote machine')
    output = remote.execute('python -V')
    assert output.stderr.startswith('Python 2.7.5')

    remote.upload('example_upload.py')
    output = remote.execute('python', 'example_upload.py')

    plan.echo('checking example_upload.py output')
    assert output.stdout.startswith('hello world')

    remote.execute('rm', 'example_upload.py')
