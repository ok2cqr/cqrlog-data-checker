import sys
from os import path
import tools

dxcc_files = [
    'Ambiguous.tbl',
    'AreaOK1RR.tbl',
    'CallResolution.tbl',
    'Country.tab',
    'CountryDel.tab',
    'eqsl.txt',
    'Exceptions.tab',
    'iota.tbl',
    'lotw1.txt',
    'MASTER.SCP',
    'prop_mode.tab',
    'README',
    'sat_name.tab',
    'us_states.tab',
]


def print_help():
    print("""
arguments:
    path to directory with country files  
  
    e.g. ./dxcc_check.bash ~/dxcc_tables
    
    """)


def check_structures(dxcc_data_dir) -> None:
    check_area_ok1rr(dxcc_data_dir, 'AreaOK1RR.tbl')
    check_call_resolution(dxcc_data_dir, 'CallResolution.tbl')
    check_country_tab(dxcc_data_dir, 'Country.tab')
    check_country_tab(dxcc_data_dir, 'CountryDel.tab')
    check_iota_tab(dxcc_data_dir, 'iota.tbl')


def check_area_ok1rr(dxcc_data_dir, dxcc_file) -> None:
    area_ok1rr = path.join(dxcc_data_dir, dxcc_file)
    tools.print_progress("\nProcessing " + dxcc_file + "\n")
    with open(area_ok1rr, 'r') as f:
        for line in f:
            error_messages = []
            parts = line.split('|')
            if len(parts) != 11:
                error_messages.append('Line has to have 11 values separated by |')

            if not (parts[0].strip()):
                error_messages.append('Prefix is missing ')

            check_common_parts(parts, error_messages)

            tools.print_error_messages_with_note(error_messages, line)
    tools.print_note("DONE\n")


def check_call_resolution(dxcc_data_dir, dxcc_file) -> None:
    call_resolution = path.join(dxcc_data_dir, dxcc_file)
    tools.print_progress("Processing " + dxcc_file + "\n")
    with open(call_resolution, 'r') as f:
        for line in f:
            error_messages = []
            if not line.startswith('='):
                error_messages.append('Line has to start with "="')

            parts = line.split('|')
            if len(parts) != 11:
                error_messages.append('Line has to have 11 values separated by |')

            callsigns = parts[0].split(' ')
            if len(callsigns) == 0:
                error_messages.append('Line has no callsigns')

            all_start_with_equals = True
            for callsign in callsigns:
                if not callsign:
                    continue
                if not callsign.startswith('='):
                    all_start_with_equals = False
            if not all_start_with_equals:
                error_messages.append('All callsigns has to start with "="')

            check_common_parts(parts, error_messages)

            tools.print_error_messages_with_note(error_messages, line)
    tools.print_note("DONE\n")


def check_country_tab(dxcc_data_dir, dxcc_file) -> None:
    country_tab = path.join(dxcc_data_dir, dxcc_file)
    tools.print_progress("Processing " + dxcc_file + "\n")
    with open(country_tab, 'r') as f:
        for line in f:
            error_messages = []
            parts = line.split('|')
            if len(parts) != 11:
                error_messages.append('Line has to have 11 values separated by |')

            if not (parts[0].strip()):
                error_messages.append('Prefix is missing ')

            tools.check_continent(parts[2], error_messages)
            tools.check_utc_offset(parts[3], error_messages)
            tools.check_longitude(parts[4], error_messages)
            tools.check_latitude(parts[5], error_messages)
            tools.check_itu_zone(parts[6], error_messages)
            tools.check_waz_zone(parts[7], error_messages)

            dates = parts[-1].strip()
            tools.check_validity_date_format(dates, error_messages)

            tools.print_error_messages_with_note(error_messages, line)
    tools.print_note("DONE\n")


def check_iota_tab(dxcc_data_dir, dxcc_file) -> None:
    iota_tab = path.join(dxcc_data_dir, dxcc_file)
    tools.print_progress("Processing " + dxcc_file + "\n")
    with open(iota_tab, 'r') as f:
        for line in f:
            error_messages = []
            parts = line.split('|')
            iota = parts[0]
            continent, nr = iota.split('-')
            if continent not in tools.continents:
                error_messages.append('Wrong IOTA format: ' + iota)
            if len(nr) != 3:
                error_messages.append('Wrong IOTA format: ' + iota)
            if not tools.is_only_numbers(nr):
                error_messages.append('Wrong IOTA format: ' + iota)
    tools.print_note("DONE\n")


def check_common_parts(parts, error_messages):
    if len(parts[8]):
        error_messages.append('Ninth item in the structure has to be empty, now is ' + parts[8])

    if parts[9] != 'R':
        error_messages.append('Tenth item has to me letter R')

    tools.check_continent(parts[2], error_messages)
    tools.check_utc_offset(parts[3], error_messages)
    tools.check_longitude(parts[4], error_messages)
    tools.check_latitude(parts[5], error_messages)
    tools.check_itu_zone(parts[6], error_messages)
    tools.check_waz_zone(parts[7], error_messages)
    tools.check_adif_dates(parts[10], error_messages)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print_help()
        sys.exit()

    data_dir = sys.argv[1]
    if not path.isdir(data_dir):
        tools.print_error('Directory ' + data_dir + ' does not exist!')
        sys.exit(1)

    all_files_exists = True
    for file in dxcc_files:
        file_with_path = path.join(data_dir, file)
        if not path.isfile(file_with_path):
            tools.print_error('File ' + file_with_path + ' does not exist')
            all_files_exists = False
    if not all_files_exists:
        sys.exit(1)

    check_structures(data_dir)
