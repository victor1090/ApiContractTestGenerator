#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 27 17:48:35 2022

@author: victor1090
"""
from utils.json_util import *

newline = "\n"
tab = "\t"
doubletab = tab+tab
string = "str"
integer = "int"
array = "list"
count_test = 0

class TestGenerator():
        
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
        else:
            print(string)
        
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
        if(type_item =="object"):
            lines.append(f"{doubletab}self.assertEqual(type(response_data),dict){newline}")
        else:
            print("Não foi possível decifrar Schema Additional Properties para a geração de assert de respostas.")
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
    
    
    def createTeste(self,arq,method,only_params_required,range_responses,config):
        global count_test
        count_test += 1
        lines = list()
        lines.append(f"{tab}#Caso de Teste do Methodo:{method.method_type}"+newline)
        
        #Pegando a resposta nessa parte para colocar na descrição do methodo
        responses = method.searchByRangeCode(range_responses[0],range_responses[1])
        if(not responses == None):
            lines.append(f"{tab}#Espera-se que seja retornado status code = {responses.code}"+newline)
        else:
            lines.append(f"{tab}#Espera-se que seja retornado status code = {range_responses[0]}"+newline)
        #Trocar o status code para o status na resposta
        if(only_params_required):
            lines.append(f"{tab}#Onde apenas os parametros obrigatorios são enviados na requisição"+newline)
        else:
            lines.append(f"{tab}#Onde todos os parâmetros(obrigatorios e opcionais) são enviados na requisição"+newline)
        lines.append(f"{tab}def test{count_test}_sucessfull_{method.method_type}(self):"+newline)
        
        url_request = "http://{self.base_url}"+str(self.path.url)
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
        
           
        #Verificando se precisa escrever a data no arquivo de configuração e recuperar no script
        config.write(config_params_paths_variables) #Sem necessidade de verificar, "" caso não tenha path variables
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
            
            
        #Fim da montagem da requisição
        #Inicio da montagem das respostas
        if(not responses == None):
            lines.append(f"{doubletab}self.assertEqual(response.status_code, {responses.code})"+newline)
            if(responses.schemas != None):
                lines.append(f"{doubletab}response_data = response.json()"+newline) #Transformando a resposta da request em json
                lines.append("".join(self.createAssertsResponseSchemas(responses.schemas)))
               # if(len(responses.schemas) > 1):
                  #  print(responses.schemas)
                 #   broker = responses.schemas["items"]["$ref"].split("/")
                #else:
                 #   broker = responses.schemas["$ref"].split("/")
                #schema = self.objects.search(broker[-1])
                #lines.append(f"{doubletab}response_data = response.json()"+newline) #Transformando a resposta da request em json
                #lines.append("".join(self.createAssertsResponse(schema,"")))
        arq.writelines(lines)
        
        
        
    def writeFloor(self):
        lines = []
        lines.append("if __name__ == '__main__':" +newline)
        lines.append(f"{tab}unittest.main()"+newline)
        return lines
    
    def setUp(self):
        #Diretorio onde ficaram os testes criados
        create_dir("Testes")
        #criação de um diretorio com arquivo utils
        utils = create_arq("Testes/util","testes_util")
        create_util(utils,self.base.hostName+self.base.basePath)
        close_arq(utils)
        
        #Criação do diretorio e arquivos do teste
        print("-Criando diretorio e arquivos do teste")
        
        path_arq = self.path.url.replace("/", "_");
        
        #Teste de Sucesso
        print("-Criando Testes de Sucesso")
        arq = create_arq("Testes/"+path_arq,path_arq+"Sucessfull")
        config = create_config("Testes/"+path_arq,"ConfigurationSucessfull")
        initialConfig(config)
        write_imports(arq)
        write_base(arq,"AutomaticTestSucessfull","ConfigurationSucessfull")
        #Teste de Falha
        print("-Criando Testes de Falha")
        arq2 = create_arq("Testes/"+path_arq,path_arq+"Unsucessfull")
        config2 = create_config("Testes/"+path_arq,"ConfigurationUnsucessfull")
        initialConfig(config2)
        write_imports(arq2)
        write_base(arq2,"AutomaticTestUnsucessfull","ConfigurationUnsucessfull")
        #Ranges os responses
        range_sucessfull = [200,299]
        range_unsucessfull = [400,599]
        for method in self.path.methods:
            self.createTeste(arq,method,False,range_sucessfull,config)
            self.createTeste(arq2,method,False,range_unsucessfull,config2)
            if(not method.isOnlyRequiredParams()):
                self.createTeste(arq,method,True,range_sucessfull,config)   
                self.createTeste(arq2,method,True,range_unsucessfull,config2)
        
        #Rodapé dos arquivos
        arq.writelines(self.writeFloor())
        arq2.writelines(self.writeFloor())
        finalConfig(config)
        finalConfig(config2)
        
        
        close_arq(arq)
        close_arq(config)
        close_arq(arq2)
        close_arq(config2)
    
    
        
        
    
        
        
    
        
    def __init__(self, base, path, objects):
        self.base = base
        self.path = path
        self.objects = objects
        self.setUp()
        
        
    
    
        




