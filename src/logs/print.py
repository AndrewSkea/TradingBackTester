import sys
import os

log_path = os.environ.get('LOG_FILE_PATH')


def _print(text):
    sys.stdout.write(str(text) + '\n')
    with open(log_path, 'a') as open_file:
        open_file.write("\n{}".format(text))
