#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 27 17:48:35 2022

@author: victor1090
"""
from utils.file_util import *

newline = "\n"
tab = "\t"
doubletab = tab+tab
string = "str"
integer = "int"
array = "list"
count_test = 0

class TypeNotDefinedError(Exception):
    pass

class ResponseSchemaNotMappedError(Exception):
    pass

class GeneratorTest():
        
    def toType(self,string):
        if(string =="string"):
            return "str"
        elif(string=="integer"):
            return "int"
        elif(string=="array"):
            return "list"
        elif(string=="object"):
            return "dict"
        elif(string=="boolean"):
            return "bool"
        elif(string=="number"):
            return "float"
        else:
            raise TypeNotDefinedError(f"The type {string} used in the documentation is not mapped to python type!")
        
    def mappingObjects(self,schema,recuo):
        lines = list()
        #Mapeando Enums
        if(schema.properties == None and schema.type != None):
            if(schema.xml == None):
                lines.append(f"{recuo}\"{schema.name}\" : \"Insert_Value\"")
            else:
                lines.append(f"{recuo}\"{schema.xml}\" : \"Insert_Value\"")
        else:
            for field, value in schema.properties.items():
                if(value.get("$ref") != None):
                    body_object = value.get("$ref").split("/")
                    body_object = self.objects.search(body_object[-1])
                    internal_object = "\n".join(self.mappingObjects(body_object,recuo+"\t"))
                    lines.append(recuo+"\""+field+"\" : {\n" +internal_object+"},")
                else:
                    lines.append(f"{recuo}\"{field}\" : \"Insert_Value\",")
        return lines
    
    def createAssertsResponseObject(self,schema,subItemHierarquia):
        lines = list()
        #Mapeando Enums
        if(schema.properties == None and schema.type != None):
            type_item = self.toType(schema.type)
            if(subItemHierarquia != ""):
                lines.append(f"{doubletab}self.assertEqual(type(response_data{subItemHierarquia}),{type_item})"+newline)
            else:
                lines.append(f"{doubletab}self.assertIn('{schema.name}',response_data)"+newline)
                lines.append(f"{doubletab}self.assertEqual(type(response_data['{schema.name}']),{type_item})"+newline)
        else:
            for field, value in schema.properties.items():
                if(value.get("$ref") != None):
                    subItem = value.get("$ref").split("/")
                    subItem = self.objects.search(subItem[-1])
                    type_subItem = self.toType(subItem.type)
                    internal_subItem = "".join(self.createAssertsResponseObject(subItem,f"{subItemHierarquia}['{field}']"))
                    if(type_subItem == "dict"):
                        if(subItemHierarquia == ""):
                            lines.append(f"{doubletab}self.assertIn('{field}',response_data)"+newline)
                            lines.append(f"{doubletab}self.assertEqual(type(response_data['{field}']), dict)\n")
                        else:
                            lines.append(f"{doubletab}self.assertIn('{field}',response_data{subItemHierarquia})"+newline)
                            lines.append(f"{doubletab}self.assertEqual(type(response_data{subItemHierarquia}['{field}']), dict)\n")
                        
                    lines.append(f"{doubletab}#Checando Objeto Interno {subItem.name}\n")
                    lines.append(internal_subItem)
                    lines.append(f"{doubletab}#End Check Objeto Interno\n")
                else:
                    type_item = self.toType(value.get('type'))
                    if(subItemHierarquia != ""):
                        lines.append(f"{doubletab}self.assertIn('{field}',response_data{subItemHierarquia})"+newline)
                        lines.append(f"{doubletab}self.assertEqual(type(response_data{subItemHierarquia}['{field}']),{type_item})"+newline)
                    else:
                        lines.append(f"{doubletab}self.assertIn('{field}',response_data)"+newline)
                        lines.append(f"{doubletab}self.assertEqual(type(response_data['{field}']),{type_item})"+newline)
                    #Mapeando Array de Objetos Internos
                    if(value.get("items") != None and value.get("items").get("$ref") != None):
                        subItem = value.get("items").get("$ref").split("/")
                        subItem = self.objects.search(subItem[-1])
                        type_subItem = self.toType(subItem.type)
                        internal_subItem = "".join(self.createAssertsResponseObject(subItem,f"{subItemHierarquia}['{field}']"))
                        lines.append(f"{doubletab}#Checando Array de Objetos Internos {subItem.name}\n")
                        lines.append(internal_subItem)
                        lines.append(f"{doubletab}#End Check\n")
        return lines
    
    def createAssetsAdditionalProperties(self,additional, type_item):
        lines = list()
        try:
            python_type = toType(type_item)
            lines.append(f"{doubletab}self.assertEqual(type(response_data),{python_type}){newline}")
        except Exception as e:
            print("Unable to decipher Schema Additional Properties for response assert generation.")
            raise(e)
        return lines
    
    def createAssetsItems(self,items,type_item):
        lines = list()
        if(type_item =="array"):
            lines.append(f"{doubletab}self.assertEqual(type(response_data), list){newline}")
            if(items.get("$ref")):
                lines.append(f"{doubletab}response_data = response_data[0]{newline}")
        if(items.get("$ref")):
            broker = items["$ref"].split("/")
            object_defined = self.objects.search(broker[-1])
            lines.append("".join(self.createAssertsResponseObject(object_defined,"")))
        return lines
            
    def createAssertsResponseSchemas(self,schema):
        lines = list()
        if(schema.get("$ref")):
            broker = schema["$ref"].split("/")
            object_defined = self.objects.search(broker[-1])
            lines.append("".join(self.createAssertsResponseObject(object_defined,"")))
        else:
            type_schema = schema.get("type")
            if(schema.get("items")):
                lines.append("".join(self.createAssetsItems(schema.get("items"), type_schema)))
            elif(schema.get("additionalProperties")):
                lines.append("".join(self.createAssetsAdditionalProperties(schema.get("additionalProperties"), type_schema)))
            else:
                raise ResponseSchemaNotMappedError(f"The schema of response {schema} used in the documentation is not mapped!")
        return lines
        
               
    def createParameterSchemas(self,schema):
        config_params = ""
        params_body = ""
        deletequote = False
        if(schema.get("$ref")):
            body_object = schema["$ref"].split("/")
            body_object = self.objects.search(body_object[-1])
            params_body += "\n".join(self.mappingObjects(body_object,"\t\t"))
            config_params += "\n".join(self.mappingObjects(body_object,"\t\t")) + newline
        elif(schema.get("type")):
            type_schema = schema.get("type")
            if(schema.get("items") and type_schema == "array"):
                items = schema.get("items")
                config_params += (f"{doubletab}[{newline}")
                params_body += (f"{doubletab}[{newline}")
                if(items.get("$ref")):
                    temp_params, temp_config,_ = self.createParameterSchemas(items)
                    params_body += "\t\t{\n"+temp_params+"\n\t\t}"
                    config_params += "\t\t{\n"+temp_config+"\n\t\t}"
                    deletequote = True
                else:
                    config_params+= (f"{doubletab}{tab}") + '"Insira o dado ' + f"{items.get('type')} no formato {items.get('format')}" + '"\n'
                    params_body+=(f"{doubletab}{tab}'Insira o dado {items.get('type')} no formato {items.get('format')} ")  
                    deletequote = True   
                config_params+=(f"\n{doubletab}]{newline}")
                
        return params_body,config_params, deletequote
 
    def deletequote(self,config):
        #Retirando os caracteres { } , no caso do objeto array
        characters = "{},"
        string = ''.join( x for x in config if x not in characters)
        config = string       
        return config
    
    
    def createTest(self,arq,method,only_params_required,response,config):
        global count_test
        count_test += 1
        lines = list()
        lines.append(f"{tab}#Caso de Teste do Method:{method.method_type}"+newline)
        lines.append(f"{tab}#Espera-se que seja retornado status code = {response.code}"+newline)
        type_test ="sucessfull"  if(int(response.code) < 300 and int(response.code) >199) else "unsucessfull"
        if(only_params_required):
            lines.append(f"{tab}#Onde apenas os parametros obrigatorios s??o enviados na requisi????o"+newline)
        else:
            lines.append(f"{tab}#Onde todos os par??metros(obrigatorios e opcionais) s??o enviados na requisi????o"+newline)
        lines.append(f"{tab}def test{count_test}_{type_test}_{method.method_type}(self):"+newline)
        
        url_request = "http://{self.base_url}"+str(self.url.url)
        parametros = method.parameters
        
        config_params = f"\t\"data{method.method_type}{count_test}\":" +"{\n"
        config_params_paths_variables = ""
        params_query = "\t\tpayload = {"
        params_body = "\t\tdata = {\n"
        params_formData = "\t\tdata = {"
        deletequote = False
        params_var = f"{doubletab}data = self.dados['data{method.method_type}{count_test}']" + newline
        
        for parametro in parametros:
            if(only_params_required == True):
                if(parametro.required == False or parametro.required == None):
                    continue
            if(parametro.into =="query"):
                params_query += f"'{parametro.name}':'Insira o valor aqui' ,"
                config_params += f"{doubletab}\"{parametro.name}\":\"Insira o valor aqui\" ,\n"
            if(parametro.into =="path"):
                config_params_paths_variables += f"{tab}\"{parametro.name}_{method.method_type}{count_test}\":" +"{\n"
                config_params_paths_variables += f"{doubletab}\"{parametro.name}\":\"Insira o valor aqui\" \n"
                config_params_paths_variables += "\t},\n"
                url_request = url_request.replace(parametro.name,f'self.dados["{parametro.name}_{method.method_type}{count_test}"]["{parametro.name}"]')
            if(parametro.into =="formData"):
                params_formData += f"'{parametro.name}':'Insira o valor aqui' ,"
                config_params += f"{doubletab}\"{parametro.name}\":\"Insira o valor aqui\" ,\n"
            if(parametro.into == "body"):
                params_temp,config_temp,deletequote = self.createParameterSchemas(parametro.schema)
                if(deletequote):
                    config_params = self.deletequote(config_params)
                    params_body = self.deletequote(params_body)
                params_body+= str(params_temp)
                config_params+= str(config_temp)
        
        params_query +="}"
        params_formData +="}"
        if(not deletequote):
            params_body += "}"
            config_params += "\t\t},\n"
        
           
        #Verificando se precisa escrever a data no arquivo de configura????o e recuperar no script
        config.write(config_params_paths_variables) #Sem necessidade de verificar, "" caso n??o tenha path variables
        if(len(params_query) > 20 or len(params_formData) > 20 or len(params_body) > 20):
            lines.append(params_var)
            config.writelines(config_params)
        if(len(params_query)> 20):
            lines.append(f"{doubletab}response = requests.{method.method_type}(f'{url_request}',params = data)"+newline)
        elif(len(params_formData) > 20):
            lines.append(f"{doubletab}response = requests.{method.method_type}(f'{url_request}',data = data)"+newline)
        elif(len(params_body) > 20):
            lines.append(f"{doubletab}response = requests.{method.method_type}(f'{url_request}',json = data)"+newline)
        else:
            lines.append(f"{doubletab}response = requests.{method.method_type}(f'{url_request}')"+newline)
            
        #Fim da montagem da requisi????o
        
        #Inicio da montagem das respostas
        lines.append(f"{doubletab}self.assertEqual(response.status_code, {response.code})"+newline)
        if(response.schemas != None):
            lines.append(f"{doubletab}response_data = response.json()"+newline) #Transformando a resposta da request em json
            lines.append("".join(self.createAssertsResponseSchemas(response.schemas)))

        arq.writelines(lines)
        
        
        
    def writeFloor(self):
        lines = []
        lines.append("if __name__ == '__main__':" +newline)
        lines.append(f"{tab}unittest.main()"+newline)
        return lines
    
    def setUp(self):
        try:
            #Directory where the tests were created
            create_dir("Tests")
            #creating a directory with utils file
            utils = create_arq("Tests/util","tests_util")
            create_util(utils,self.base.hostName+self.base.basePath)
            close_arq(utils)
            #Creating the test directory and files
            print("-Creating test directory and files")
            path_arq = self.url.url.replace("/", "_");
            #Sucessfull test
            print("-Creating Success Tests")
            arq = create_arq("Tests/"+path_arq,path_arq+"Sucessfull")
            config = create_config("Tests/"+path_arq,"ConfigurationSucessfull")
            initialConfig(config)
            write_imports(arq)
            write_base(arq,"AutomaticTestSucessfull","ConfigurationSucessfull")
            #Unsucessfull test
            print("-Creating Failure Tests")
            arq2 = create_arq("Tests/"+path_arq,path_arq+"Unsucessfull")
            config2 = create_config("Tests/"+path_arq,"ConfigurationUnsucessfull")
            initialConfig(config2)
            write_imports(arq2)
            write_base(arq2,"AutomaticTestUnsucessfull","ConfigurationUnsucessfull")
            
            for method in self.url.methods:
                responses_sucessfull = method.searchByRangeCode(200, 299)
                responses_unsucessfull = method.searchByRangeCode(400, 599)
                if(len(responses_sucessfull) == 0):
                    print(f"Warning: Incomplete success test generation: no response has been defined for the method: {method.method_type}!")
                if(len(responses_unsucessfull) == 0):
                    print(f"Warning: Incomplete unsuccessful test generation: no response has been defined for the method: {method.method_type}!")
                for response in responses_sucessfull:
                    self.createTest(arq, method, False, response ,config)
                    if(not method.isOnlyRequiredParams()):
                        self.createTest(arq, method, True, response ,config)  
                for response in responses_unsucessfull:
                    self.createTest(arq2, method, False, response, config2)
                    if(not method.isOnlyRequiredParams()):
                        self.createTest(arq2, method, True, response, config2)
            #write floor of archives
            arq.writelines(self.writeFloor())
            arq2.writelines(self.writeFloor())
            endConfig(config)
            endConfig(config2)
            #Closes all archives
            close_arq(arq)
            close_arq(config)
            close_arq(arq2)
            close_arq(config2)
        except Exception as e:
            raise(e)
            
        
    def __init__(self, base, url, objects):
        self.base = base
        self.url = url
        self.objects = objects
        self.setUp()
