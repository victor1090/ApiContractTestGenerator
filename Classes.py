# -*- coding: utf-8 -*-
"""
Created on Sun Jan 30 22:22:16 2022

@author: victo
"""

class Base:
    """ Represents the informations basic of structure documentation  """

    def __init__(self,hostName, basePath):
        self.hostName = hostName
        self.basePath = basePath
    
    def __str__(self):
        return "host:" + str(self.hostName) + ", basePath:" + str(self.basePath)
    
class Objects:
    "Represents the objects presents in documentation"
    def __init__(self, schemas = []):
        self.schemas = schemas
    
    def search(self,name):
        for schema in self.schemas:
            if(schema.name == name):
                return schema
        return
    
class Schemas:
    "Represents the schemas of objects presents in documentation"
    def __init__(self, name, type, properties,  xml = '', required = ''):
        self.name = name
        self.type = type
        self.properties = properties
        self.required = required
        self.xml = xml
    
    def __str__(self):
        return str(self.name)+ "{ xml:" + str(self.xml) + "\ntype:" + str(self.type) +"\nproperties:" + str(self.properties) +"\nrequired:" + str(self.required) +"}"
    
    
class Paths:
    "Represents list of urls presents in documentation"
    def __init__(self, urls = []):
        self.urls = urls
        
    def getByUrl(self, search):
        for url in self.urls:
            if(url.url == search):
                return url
        
class Url:
    "Represents each url and its various methods"
    def __init__(self,url, methods = []):
        self.url = url
        self.methods = methods
    
    def __str__(self):
        resp = str(self.url) + ": {" 
        for method in self.methods:
            resp += str(method) + ", "
        return resp + "}"
            
    def getMethod(self, search):
        for method in self.methods:
            if(method.method_type == search):
                return method
        
class Methods:
    def __init__(self,method_type, parameters= [], responses=[] ):
        self.method_type = method_type
        self.parameters = parameters
        self.responses = responses
        
    def __str__(self):
        resp = str(self.method_type) + ": { parameters:"
        for parameter in self.parameters:
            resp += str(parameter)
        for response in self.responses:
            resp += str(response)
        return resp
    
    def isOnlyRequiredParams(self):
        onlyRequired = True
        for parameter in self.parameters:
            if(parameter.required == False and parameter.into != "header"):
                onlyRequired = False
        return onlyRequired
    
    def searchByRangeCode(self,rangeInitial,rangeFinal):
        for response in self.responses:
            if(response.code.isdigit() and int(response.code) >= rangeInitial and int(response.code) <= rangeFinal):
                return response
        return 
class Parameters:
    "Represents the parameters to be sent in each method"
    def __init__(self,name,into,description='',required=False, type='',schema=''):
        self.name = name
        self.into = into
        self.description = description
        self.required = required
        self.type = type
        self.schema = schema
        
    def __str__(self):
        return str(self.name) + f": {self.into}, {self.description}, {self.required}, {self.type}, {self.schema}"

class Responses:
    "Represents each possible answer to be obtained in a method"
    def __init__(self,code,description='',schemas=''):
        self.code = code
        self.description = description
        self.schemas = schemas
    
    def __str__(self):
        return str(self.code) + ":{ description:"+ str(self.description) + ", schema:" + str(self.schemas) +"}"
