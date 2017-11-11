#!/usr/bin/env python3.5

"""
Ülesande kirjeldus:
Skript loeb esimese parameetrina antud failist sisse URL-id (sisend.txt) ja nende järel olevad (komaga eraldatud)
sõned. Sõne ja URL eraldatakse, seejärel tehakse päring vastava URLi pihta. Vastuse lähtekoodist otsitakse URLi järel
olnud sõnet. Teise parameetrina antud faili kirjutatakse uuesti URL, otsitav string ning "JAH/EI" vastavalt sellele,
kas otsitav sõne leiti või mitte.
--------------------------------------------------------------
Usage:
Install python 3.5 on your machine.
Run script with SUDO privileges as follows:
./mtseljab.py [INPUT FILE] [OUTPUT FILE]

"""

import sys
import urllib.request
from urllib.request import urlopen


# http://pythoncentral.io/reading-and-writing-to-files-in-python/
# Open output file (if doesn't exist it will be created) and remove all contents.
def clear_out_file(file):
    print("Creating/clearing output file {0}".format(file))
    try:
        file = open(output_file_arg, "w")
        file.truncate()
        file.close()
        print("Success.")
    except OSError:
        print("It was not possible to open/create output file. Check your user privileges.")
        exit(1)


# Read lines, split it by comma, and save pairs to list.
def parse_input_file_to_list(file):
    print("Opening input file {0}".format(file))
    try:
        input_file_object = open(file, "r")
        print("Success")
    except FileNotFoundError as e:
        print("I/O error({0}): {1}".format(e.errno, e.strerror))
        exit(1)
    for line in input_file_object:
        input_lines_list.append(line.strip().split(","))
    input_file_object.close()
    return input_lines_list


# Open and append output file
def writefile(out_file, string):
    try:
        file = open(out_file, "a")
        file.write(string)
        file.close()
    except OSError as error:
        print("I/O error({0}): {1}".format(error.errno, error.strerror))
        exit(1)


# Add "http://" if it's missing, then try to open URL. Handle HTTP and URL errors.
def create_correct_URL(input_link):
    if str(input_link).startswith("http://"):
        URL = input_link
    else:
        URL = "http://" + input_link
    return URL


# Open URL and try to read html
def open_read_url(URL):
    try:
        print("Opening URL {0}".format(URL))
        response = urlopen(URL)
        # print(response.info())
        html = response.read()
        response.close()
        print("Success")
        return html
    except urllib.error.HTTPError as error:
        print("HTTP Connection error ({0}): {1}: {2}".format(URL, error.reason, error.headers))
    except urllib.error.URLError as error:
        print("Oops. URL {0} error occured: {1}".format(item[0], error.reason))


# Search word in html
def search_html(html, word):
    result = ""
    string = str(html)
    if string.find(word) != -1:
        result = "YES"
    else:
        result = "NO"
    return result


# ------------------------ ENGINE -------------------------

# Check if parameter qty is correct
if len(sys.argv) != 1:
    print("Usage:\n ./mtseljab.py [INPUT FILE] [OUTPUT FILE]")
    exit(1)

input_file_arg = "IN.txt"
output_file_arg = "OUT.txt"
input_lines_list = []

# Start run with clearing OUT file
clear_out_file(output_file_arg)

# Try to parse input file
input_lines_list = parse_input_file_to_list(input_file_arg)

# Check if html data is present and search in html
for item in input_lines_list:
    if len(item) == 2:
        URL = create_correct_URL(item[0])
        HTML = open_read_url(URL)
        if HTML == None:
            print("URL {0} is incorrect or cannot be reached. Skipping to next URL.".format(URL))
            out_line = "{0}: {1}: {2}\n".format(item[0], item[1], "URL cannot be reached")
            writefile(output_file_arg, out_line)
        else:
            result = search_html(HTML, item[1])
            out_line = "{0}: {1}: {2}\n".format(item[0], item[1], result)
            writefile(output_file_arg, out_line)
    else:
        result = "NO"
        out_line = "%s: %s \n" % (item[0], "Missing information in input file")
        writefile(output_file_arg, out_line)

print("\nScript finished run successfully")

# ------------------------ ENGINE -------------------------