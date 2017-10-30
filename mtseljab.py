#!/usr/bin/env python3.5
"""
Ülesande kirjeldus:

Skript loeb esimese parameetrina antud failist sisse URL-id (sisend.txt) ja nende järel olevad (komaga eraldatud)
sõned. Sõne ja URL eraldatakse, seejärel tehakse päring vastava URLi pihta. Vastuse lähtekoodist otsitakse URLi järel
olnud sõnet. Teise parameetrina antud faili kirjutatakse uuesti URL, otsitav string ning "JAH/EI" vastavalt sellele,
kas otsitav sõne leiti või mitte.


http://pythoncentral.io/reading-and-writing-to-files-in-python/
Open file, read lines, split it by comma, and save pairs to list
"""

import sys
import urllib.error
import urllib.request
from urllib.request import urlopen


# Check if parameter qty is correct


if len(sys.argv) != 1:
    print("Usage:\n ./mtseljab.py [INPUT FILE] [OUTPUT FILE]")
    exit(1)

input_file_arg = "IN.txt"
output_file_arg = "OUT.txt"
input_lines_list = []


# http://pythoncentral.io/reading-and-writing-to-files-in-python/
# Open file, read lines, split it by comma, and save pairs to list


def clear_out_file():
    try:
        file = open(output_file_arg, "w")
        file.truncate()
    except OSError:
        print("It was not possible to open/create output file. Check your user privileges.")
        exit(1)


clear_out_file()


def writefile(string):
    try:
        file = open(output_file_arg, "a")
        file.write(string)
        file.close()
    except OSError as error:
        print("I/O error({0}): {1}".format(error.errno, error.strerror))
        exit(1)


# Open input file
try:
    input_file_object = open(input_file_arg, "r")
except FileNotFoundError as e:
    print("I/O error({0}): {1}".format(e.errno, e.strerror))
    exit(1)

# save data to list
for line in input_file_object:
    input_lines_list.append(line.strip().split(","))
input_file_object.close()

# Check items in list, if missing info - display error meesage
for item in input_lines_list:
    if len(item) != 2:
        result = "NO"
        out_line = "%s: %s: %s\n" % (item[0], "Missing info", result)
        writefile(out_line)
    else:
        result = "YES"
        out_line = "{0}: {1}: {2}\n".format(item[0], item[1], result)
        writefile(out_line)

# https://khashtamov.com/ru/python-requests/
for item in input_lines_list:
    if str(item[0]).startswith("http//"):
        try:
            response = urlopen("http://www.neti.eee")
            print(response.info())
            html = response.read()
            response.close()
        except urllib.error.HTTPError as error:
            print("HTTP Connection error ({0}): {1}: {2}".format(error.code, error.reason, error.headers))
        except urllib.error.URLError as error:
            print("Oops. URL Error occured: {0}".format(error.reason))
    else:
        try:
            response = urlopen("http://" + item[0])
            print(response.info())
            html = response.read()
            response.close()
        except urllib.error.HTTPError as error:
            print("HTTP Connection error ({0}): {1}: {2}".format(error.reason, error.reason, error.headers))
        except urllib.error.URLError as error:
            print("Oops. URL {0} error occured: {1}\n".format(item[0], error.reason))
