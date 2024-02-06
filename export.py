from os.path import exists
from bs4 import BeautifulSoup
import requests
import csv
import argparse

HTML_EXPORT_FILE = '.rawhtmlexport'
CSV_FILE = 'lookup.csv'

def _url(base, path):
    if path.startswith('/'):
        return base + path
    else:
        return base + '/' + path

def _lookups_url(base, rows=10000):
    return _url(base, 'vdesigner/lookups.php?rowsp={}'.format(rows))

def _login_url(base):
    return _url(base, 'login.php')

def strip_space(string):
    return string.replace("\xa0", "")

def export_from_switch(**kwargs):
    force = kwargs.get('force', False)
    export_file = kwargs.get('export_file', HTML_EXPORT_FILE)
    user = kwargs.get('user')
    pw = kwargs.get('pass')
    row_count = kwargs.get('rows', 10000)
    switch_url = kwargs.get('switch_url')

    if not user or not pw or not switch_url:
        if not user:
            print("A user argument must be supplied")
        if not pw:
            print("A pass argument must be supplied")
        if not switch_url:
            print("A switch_url argument must be supplied")
        return

    if not exists(export_file) or force:
        with requests.Session() as s, open(export_file, 'wb') as f:
            s.post(_login_url(switch_url), {'user': user, 'pass': pw}, verify=False)

            r = s.get(_lookups_url(switch_url, row_count), verify=False)
            f.write(r.content)

def html_to_csv(**kwargs):
    export_file = kwargs.get("export_file", HTML_EXPORT_FILE)
    csv_file = kwargs.get("csv_file", CSV_FILE)

    with open(export_file, 'r') as f, open(csv_file, 'w', newline='') as c:
        soup = BeautifulSoup(f, features="html.parser")
        writer = csv.writer(c)
        writer.writerow(('group', 'number', 'ani', 'rdnis', 'destination',))
        
        for tag in soup.find_all('tr'):
            if len(tag.findChildren('td')) == 7:
                group = strip_space(tag.findChildren('td')[0].contents[0])
                number = tag.findChildren('td')[1].findAll('a')[0].contents[0]
                ani = strip_space(tag.findChildren('td')[2].contents[0])
                rdnis = strip_space(tag.findChildren('td')[3].contents[0])
                destination = strip_space(tag.findChildren('td')[4].contents[0])

                writer.writerow((group, number, ani, rdnis, destination,))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--force",
        action="store_true",
        help="Forces the creation of the html export file (raw html data from switch) even if it already exists."
    )

    parser.add_argument(
        "--switch-url",
        action="store",
        required=True,
        help="The soft switch URL, which should take the form of https://x.x.x.x - no trailing slash"
    )

    parser.add_argument(
        "--user",
        action="store",
        required=True,
        help="The soft switch username that has sufficient access to the lookup table page."
    )

    parser.add_argument(
        "--password",
        action="store",
        required=True,
        help="The corresponding password."
    )

    parser.add_argument(
        "--html-export-file",
        action="store",
        help="Where the html export file (raw html data from switch) should be stored."
    )

    parser.add_argument(
        "--rows",
        type=int,
        action="store",
        help="The number of rows to request for the soft switch. Defaults to 10,000 rows. Increase the amount if you have more than 10,000 lookup entries."
    )

    parser.add_argument(
        "--out",
        action="store",
        help="The location where the output CSV should be stored.",
        required=True
    )

    args = parser.parse_args()

    extract_args = {'user': args.user, 'pass': args.password, 'switch_url': args.switch_url}

    if args.force:
        extract_args['force'] = True
    
    if args.html_export_file:
        extract_args['export_file'] = args.html_export_file

    if args.rows:
        extract_args['rows'] = args.rows

    csv_args = {'csv_file': args.out}

    if args.html_export_file:
        csv_args['export_file'] = args.html_export_file

    export_from_switch(**extract_args)
    html_to_csv(**csv_args)