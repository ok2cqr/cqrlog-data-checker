import sys
from os import path
import tools
from pathlib import Path as Path


def print_help():
    print("""
arguments:
    path to directory with membership files  

    e.g. ./members_check.bash ~/membership

    """)


def check_structure(filename):
    tools.print_progress("Processing " + str(filename) + "\n")
    with open(filename, 'r') as f:
        line_number = 0
        for line in f:
            line_number += 1
            error_messages = []
            if line_number < 3:
                continue

            parts = line.split(';')
            if len(parts) == 0:
                error_messages.append('Line number ' + str(line_number) + ' has wrong format: ' + line)

            if len(parts) < 3:
                continue

            # file should include at least start date
            if parts[2] == '-':
                continue

            start_date = parts[2].split('-')
            year, month, day = '1900', '1', '1'
            if len(start_date) == 2:
                year, month = start_date
            elif len(start_date) == 3:
                year, month, day = start_date
            else:
                error_messages.append('Line number ' + str(line_number) + ' has wrong date format: ' + line)
                continue

            if not tools.check_membership_date_format(day, month, year):
                error_messages.append('Line number ' + str(line_number) + ' has wrong date format: ' + line)

            tools.print_error_messages_with_note(error_messages, line)
    tools.print_note("DONE\n")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print_help()
        sys.exit()

    data_dir = sys.argv[1]
    if not path.isdir(data_dir):
        tools.print_error('Directory ' + data_dir + ' does not exist!')
        sys.exit(1)

    p = Path(data_dir)
    p.glob('*.txt')
    for file in p.glob('*.txt'):
        check_structure(file)
