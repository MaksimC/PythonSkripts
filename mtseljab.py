#!/usr/bin/env python3.5

"""
Ülesande kirjeldus:
Skript loeb esimese parameetrina antud failist sisse URL-id (sisend.txt) ja nende järel olevad (komaga eraldatud)
sõned. Sõne ja URL eraldatakse, seejärel tehakse päring vastava URLi pihta. Vastuse lähtekoodist otsitakse URLi järel
olnud sõnet. Teise parameetrina antud faili kirjutatakse uuesti URL, otsitav string ning "JAH/EI" vastavalt sellele,
kas otsitav sõne leiti või mitte.
"""

import sys
import urllib.request
from urllib.request import urlopen


# http://pythoncentral.io/reading-and-writing-to-files-in-python/
def clear_out_file():
    try:
        print("Clearing output file {0}".format(output_file_arg))
        file = open(output_file_arg, "w")
        file.truncate()
        file.close()
        print("Success")
    except OSError:
        print("It was not possible to open/create output file. Check your user privileges.")
        exit(1)


# Open file, read lines, split it by comma, and save pairs to list
def parse_input_file_to_list():
    try:
        print("Opening input file {0}".format(input_file_arg))
        input_file_object = open(input_file_arg, "r")
        print("Success")
    except FileNotFoundError as e:
        print("I/O error({0}): {1}".format(e.errno, e.strerror))
        exit(1)
    for line in input_file_object:
        input_lines_list.append(line.strip().split(","))
    input_file_object.close()
    return input_lines_list


def writefile(string):
    try:
        file = open(output_file_arg, "a")
        file.write(string)
        file.close()
    except OSError as error:
        print("I/O error({0}): {1}".format(error.errno, error.strerror))
        exit(1)


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
        print("HTTP Connection error ({0}): {1}: {2}".format(error.reason, error.reason, error.headers))
    except urllib.error.URLError as error:
        print("Oops. URL {0} error occured: {1}".format(item[0], error.reason))


# Add "http://" if it's missing, then try to open URL. Handle HTTP and URL errors.
def create_correct_URL(input_link):
    if str(input_link).startswith("http://"):
        URL = input_link
    else:
        URL = "http://" + input_link
    return URL


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
clear_out_file()

# Try to parse input file
input_lines_list = parse_input_file_to_list()

# Check if data is present and search in html
for item in input_lines_list:
    if len(item) == 2:
        URL = create_correct_URL(item[0])
        HTML = open_read_url(URL)
        if HTML == None:
            print("URL {0} is incorrect or cannot be reached. Skipping to next URL.".format(URL))
            out_line = "{0}: {1}: {2}\n".format(item[0], item[1], "URL cannot be reached")
            writefile(out_line)
        else:
            result = search_html(HTML, item[1])
            out_line = "{0}: {1}: {2}\n".format(item[0], item[1], result)
            writefile(out_line)
    else:
        result = "NO"
        out_line = "%s: %s \n" % (item[0], "Missing information in input file")
        writefile(out_line)

print("\nScript finished run successfully")

# ------------------------ ENGINE -------------------------
