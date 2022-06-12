# -*- coding: utf-8 -*-
"""
Created on Sun Jan 30 22:12:50 2022

@author: victo
"""
from Classes import Base,Objects,Schemas,Paths, Methods, Url, Parameters, Responses

class GeneratorClasses():

    def createClasses(self):
        try:
          definitions = self.documentation["definitions"]
          urls = self.documentation["paths"]
          base_data = Base(self.documentation["host"],self.documentation["basePath"]) #Capturing Base data of documentation
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
          return base_data, paths, objects
        except Exception as e:
            print("Error: Unable to process documentation successfully: "+ repr(e))
            exit()
            
    def __init__(self, documentation):
        self.documentation = documentation
