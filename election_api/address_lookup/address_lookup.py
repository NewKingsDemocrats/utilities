"""
Utility for interacting with the NY City Election API
"""
import argparse
import csv
import httplib
import json
import os
import time

import requests


CSV_HEADERS = ['nationbuilder_id', 'primary_country_code', 'primary_country', 'primary_state', 'primary_city', 'primary_county',
               'primary_zip', 'primary_address1', 'primary_address2']

OUTPUT_HEADERS = ['assembly_district', 'congress_district', 'council_district', 'election_district',
                  'judicial_district', 'municipal_court_district', 'senate_district']

REQUIRED_FIELDS = ['primary_zip', 'primary_address1']

API_URL = "http://nyc.electionapi.com/psl/pollsiteinfo?streetnumber={street_number}&streetname={street_name}&" \
          "county={county}&postalcode={zip_code}&key={api_key}"

REQUEST_TIMEOUT_S = 30


def lookup_address(api_key, inputs, line_num):
    """
    Parse the csv, and validate all lines
    Look up each line of the CSV
    :param api_key:
    :param inputs: a dict with the value
    :param line_num: the line at which we're parsing
    :return:
    """

    for field in REQUIRED_FIELDS:
        if field not in inputs:
            print "%s not found in address %s... line %d , skipping!" % (field, inputs[:20], line_num)
            return None

    if inputs['primary_county'].lower() != "kings":
        print "NOTE: got a county of '%s' for address on line %d, going to assume this is Kings County instead!" % \
              (inputs['primary_county'], line_num)

    # try to parse out the street number
    addr_pieces = inputs['primary_address1'].split()
    if len(addr_pieces) < 2:
        print "Warning! Couldn't parse a street number from address %s line %d" % (inputs['primary_address1'], line_num)
        return None

    # build the url
    url = API_URL.format(zip_code=inputs['primary_zip'], street_number=addr_pieces[0],
                         street_name=" ".join(addr_pieces[1:]), county='Kings', api_key=api_key)
    print "--> %s" % url
    r = requests.get(url, timeout=REQUEST_TIMEOUT_S)
    if r.status_code != httplib.OK:
        print "Couldn't communicate with the API got status code %d" % r.status_code
        return None

    result_dict = {}
    try:
        obj_js = json.loads(r.content)
        for header in OUTPUT_HEADERS:
            result_dict[header] = obj_js[header]

    except ValueError:
        print "Got unintelligble response from address %s line %d" % (inputs['primary_address1'], line_num)
        return None

    return result_dict


# Main method
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("api_key",
                        help="the API key to the NYC Elections API. In the 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx' "
                             "format")
    parser.add_argument("input_csv_path", help="The full path to the INPUT CSV dataset you're trying to look up")
    parser.add_argument("output_csv_path",
                        help="The full path to where you'd like the OUTPUT CSV to go. e.g 'C:\my_dir\output.csv'")
    args = parser.parse_args()

    # check that the file exists
    if not os.path.isfile(args.input_csv_path):
        print "Election Utils::Couldn't find file %s , please check that your file path " \
              "is correct and try again!" % args.input_csv_path
        exit(-1)

    num_rows_found = 0
    num_tried = 0

    # open the input file
    with open(args.input_csv_path) as in_csvfile:
        reader = csv.DictReader(in_csvfile)

        # create output file
        with open(args.output_csv_path, 'w') as out_csvfile:
            fieldnames = CSV_HEADERS + OUTPUT_HEADERS
            writer = csv.DictWriter(out_csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for row in reader:
                num_tried += 1

                district_values = lookup_address(args.api_key, row, num_tried)
                if district_values:
                    num_rows_found += 1

                    district_values.update(row)
                    writer.writerow(district_values)
                time.sleep(2)

    print "Converted %d rows of a possible %d" % (num_rows_found, num_tried)
