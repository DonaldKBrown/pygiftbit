import requests
import subprocess
import sys

from pygiftbit import __version__ as current_version

req = requests.get('https://pypi.python.org/pypi/pygiftbit/json')
server_version = req.json()['info']['version']
exit_code = 0
if current_version != server_version:
    print('Versions differ, publishing.')
    exit_code += subprocess.call(
        ['python', 'setup.py', 'sdist', 'bdist_wheel'],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    exit_code += subprocess.call(
        ['twine', 'check', 'dist/*'],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    exit_code += subprocess.call(
        ['twine', 'upload', '--non-interactive', '--repository-url', 'https://upload.pypi.org/legacy/', 'dist/*'],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
else:
    print('Versions match, skipping publish.')
sys.exit(exit_code)
