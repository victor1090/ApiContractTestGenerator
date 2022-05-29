# -*- coding: utf-8 -*-
"""
Created on Sun Jan 30 22:12:50 2022

@author: victo
"""
import json
import sys
from Classes import Base,Objects,Schemas,Paths, Methods, Url, Parameters, Responses
from TestGenerator import *
with open("swaggerPoc2.0.json", encoding='utf-8') as arq:
    dados = json.load(arq)

try:
  definitions = dados["definitions"]
  urls = dados["paths"]
  base_Data = Base(dados["host"],dados["basePath"]) #Capturing Base data of documentation
  list_schemas = [] #List de objects_schemas used as definition
  paths = Paths()
  list_urls = []
  #Interaction to fill the list of objects defined as references
  for key, values in definitions.items():
      list_schemas.append(Schemas(name = key, type = values.get("type"), properties = values.get("properties"), xml = values.get("xml"), required = values.get("required")))
  objects = Objects(schemas=list_schemas)
  #Interaction to fill the paths object which will contain a list of urls and each url will have its objects of methods, parameters, responses
  for key, values in urls.items():
      methods = []
      for method, properties in values.items():
          list_parameters = [] #List of Parameters
          list_responses = [] #List of Responses
          for parameter in properties.get("parameters"):
              list_parameters.append(Parameters(name = parameter["name"], into = parameter.get("in"), description = parameter.get("description"), required = parameter.get("required"), type = parameter.get("type"), schema = parameter.get("schema")))
          for code, response in properties.get("responses").items():
              list_responses.append(Responses(code=code, description = response.get("description"), schemas = response.get("schema")))
          methods.append(Methods(method_type = method, parameters = list_parameters, responses = list_responses))
      #EndFor
      list_urls.append(Url(key, methods))
  #EndFor
  paths.urls = list_urls
except Exception as e:
    print("Error: Unable to process documentation successfully")
    print(e)
    exit()
  
#User interaction
print("Codigo: url")
print("-1: Gerar Todos")
for index, url in enumerate(paths.urls):
    print(f"{index}:{url.url}")
code = int(input("Digite o código do teste a ser gerado:"))
if(code != -1):
    try:
        TestGenerator(base_Data,paths.urls[code],objects)
        print(f"Os testes para a url {paths.urls[code].url} foi gerado na pasta Testes")
    except Exception as e:
        print(f"Não foi possível gerar os testes para a url {paths.urls[code].url}")
        print(e)
else:
    for urls in paths.urls:
        try:
            TestGenerator(base_Data, urls, objects)
            print(f"Os testes para a url {url.url} foi gerado na pasta Testes")
        except Exception as e:
            print(f"Não foi possível gerar os testes para a url {urls.url}")
            print(e)

  









    



    
