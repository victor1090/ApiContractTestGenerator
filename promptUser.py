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


print("Codigo: url")
print("-1: Gerar Todos")
for index, url in enumerate(paths.urls):
    print(f"{index}:{url.url}")
code = int(input("Digite o código do teste a ser gerado:"))
if(code != -1):
    try:
        GeneratorTest(base_data,paths.urls[code],objects)
        print(f"Os testes para a url {paths.urls[code].url} foi gerado na pasta Testes")
    except Exception as e:
        print(f"Não foi possível gerar os testes para a url {paths.urls[code].url}")
        print(e)
else:
    for urls in paths.urls:
        try:
            GeneratorTest(base_data, urls, objects)
            print(f"Os testes para a url {urls.url} foi gerado na pasta Testes")
        except Exception as e:
            print(f"Não foi possível gerar os testes para a url {urls.url}")
            print(e)