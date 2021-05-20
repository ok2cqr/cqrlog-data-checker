import re
import datetime
from rich.console import Console

continents = [
    'AF',
    'AN',
    'AS',
    'EU',
    'NA',
    'OC',
    'SA'
]

console = Console()


def is_number(n) -> bool:
    try:
        float(n)
    except ValueError:
        return False
    return True


def to_int(n) -> int:
    if n.startswith('0'):
        if len(n) > 1:
            n = n[1:]

    return int(n)


def is_only_numbers(n: str) -> bool:
    if re.search("^[0-9]*$", n):
        return True
    return False


def check_date_format(str_date, date_format="%Y/%m/%d") -> bool:
    try:
        datetime.datetime.strptime(str_date, date_format)
        return True
    except ValueError:
        return False


def check_adif_dates(adif_dates, error_messages) -> None:
    if adif_dates.startswith('='):
        adif = adif_dates[1:].strip()
        if not adif.isnumeric():
            error_messages.append('Wrong ADIF format: ' + adif_dates.strip())
    else:
        if '=' not in adif_dates:
            error_messages.append('ADIF information is missing in ' + adif_dates.strip())
        else:
            dates, adif = adif_dates.split('=')
            adif = adif.strip()
            check_validity_date_format(dates, error_messages)

            if not is_number(adif):
                error_messages.append('ADIF number is not correct: ' + adif)


def check_validity_date_format(dates: str, error_messages: list):
    if not dates.strip():
        return None

    if '-' not in dates:
        if not check_date_format(dates):
            error_messages.append('Invalid date1 ' + dates)
    elif dates.startswith('-'):
        if not check_date_format(dates[1:]):
            error_messages.append('Invalid date2 ' + dates[1:])
    elif dates[:-1] == '-':
        if not check_date_format(dates[:-1]):
            error_messages.append('Invalid date3 ' + dates[:-1])
    elif len(dates.split('-')) != 2:
        error_messages.append('Invalid date4 ' + dates)
    else:
        date_from, date_to = dates.split('-')
        if date_from and (not check_date_format(date_from)):
            error_messages.append('Invalid date_from: ' + date_from)
        if date_to and not check_date_format(date_to):
            error_messages.append('Invalid date_to: |' + date_to+'|')


def check_waz_zone(waz_zone, error_messages) -> None:
    if waz_zone:
        if '-' in waz_zone:
            for zone in waz_zone.split('-'):
                if not zone.isnumeric():
                    error_messages.append('WAZ zone has wrong format, it has to be a number, now it is ' + zone)
                else:
                    int_waz = to_int(zone)
                    if not (0 <= int_waz <= 40):
                        error_messages.append('WAZ zone as to be between 1-40, now it is ' + zone)
        else:
            if not waz_zone.isnumeric():
                error_messages.append('WAZ zone has wrong format, it has to be a number, now it is ' + waz_zone)
            else:
                waz = to_int(waz_zone)
                if not (0 <= waz <= 40):
                    error_messages.append('WAZ zone as to be between 1-40, now it is ' + str(waz))


def check_itu_zone(itu_zone, error_messages) -> None:
    if itu_zone:
        if '-' in itu_zone:
            for zone in itu_zone.split('-'):
                if not zone.isnumeric():
                    error_messages.append('ITU zone has wrong format, it has to be a number, now is ' + itu_zone)
                else:
                    int_zone = to_int(zone)
                    if not (0 <= int_zone <= 90):
                        error_messages.append('ITU zone as to be between 1-90, now is ' + zone)
        else:
            if not itu_zone.isnumeric():
                error_messages.append('ITU zone has wrong format, it has to be a number, now is ' + itu_zone)
            else:
                ituz = to_int(itu_zone)
                if not (0 <= ituz <= 90):
                    error_messages.append('ITU zone as to be between 1-90, now is ' + str(ituz))


def check_latitude(latitude, error_messages) -> None:
    if len(latitude):
        if (latitude[-1]) not in ['W', 'E']:
            error_messages.append('Longitude has to end with W or E ' + latitude)


def check_longitude(longitude, error_messages) -> None:
    if len(longitude):
        if longitude[-1] not in ['N', 'S']:
            error_messages.append('Latitude has to end with N or S ' + longitude)

    return error_messages


def check_continent(continent, error_messages) -> None:
    if continent not in continents:
        error_messages.append('Invalid continent ' + continent)


def check_utc_offset(utc_offset, error_messages) -> None:
    if not is_number(utc_offset):
        error_messages.append('Invalid UTC offset ' + utc_offset)


def check_membership_date_format(day, month, year) -> bool:
    if not is_only_numbers(day):
        return False
    if not is_only_numbers(month):
        return False
    if not is_only_numbers(year):
        return False

    if day != '00':
        if to_int(day) > 32:
            return False
    if month != '00':
        if to_int(month) > 12:
            return False

    if 1900 > to_int(year) > 2100:
        return False

    return True


def print_error_messages_with_note(error_messages, note):
    for error_message in error_messages:
        print_error(error_message)
    if error_messages:
        print_note(note)


def print_note(note) -> None:
    console.print(note, style="bold")


def print_error(error_message) -> None:
    console.print(error_message, style="bold red")


def print_progress(message):
    console.print(message, style="bold green underline")