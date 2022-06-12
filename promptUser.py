# -*- coding: utf-8 -*-
"""
Created on Fri Jun 10 22:29:44 2022

@author: victo
"""

import sys
import json
from GeneratorTest import *
from GeneratorClasses import *

def open_file(file_name):
    try:
        with open(file_name, encoding='utf-8') as arq:
            data = json.load(arq)
            return data
    except Exception as e:
        print("Error: Unable to open file successfully")
        print(e)
        exit()
        
if(len(sys.argv) > 1):
    file_name = sys.argv[1]
    documentation = open_file(file_name)
else:
    file_name = str(input("Enter the file name:"))
    documentation = open_file(file_name)

generatorClasses = GeneratorClasses(documentation)
base_data, paths, objects = generatorClasses.createClasses()

print ("{:<8} {:<15}".format('Code','URL'))
print ("{:<8} {:<15}".format('----','-----------------------------------------\n'))
print ("{:<8} {:<15}".format("-1", "Generate All"))
for index, url in enumerate(paths.urls):
    print ("{:<8} {:<15}".format(index, url.url))
print("\n")
code = int(input("Enter the code of the url to generate the tests:"))
if(code != -1):
    try:
        GeneratorTest(base_data,paths.urls[code],objects)
        folder = paths.urls[code].url.replace("/", "_");
        print(f"The tests for url {paths.urls[code].url} was generated in the Tests/{folder} folder")
    except Exception as e:
        print(f"Error:Could not generate the tests for the url {paths.urls[code].url}" + repr(e))
else:
    for urls in paths.urls:
        try:
            GeneratorTest(base_data, urls, objects)
            folder = url.url.replace("/", "_");
            print(f"The tests for url  {urls.url} was generated in the Tests/{folder} folder")
        except Exception as e:
            print(f"Error:Could not generate the tests for the url {urls.url}" + repr(e))