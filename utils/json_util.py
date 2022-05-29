import os
newline = "\n"
tab = "\t"

class CreateArchivesError(Exception):
    pass

class ClosesArchivesError(Exception):
    pass

def create_arq(diretorio,nome):
    try:
        create_dir(diretorio)
        arq = open(diretorio + "/" + nome+".py", "w")
        return arq
    except Exception as e:
        print(e)
        raise CreateArchivesError("Error creating files")

def create_config(diretorio,nome):
    try: 
        create_dir(diretorio)
        config = open(diretorio + "/" + nome+".json", "w")
        return config
    except Exception as e:
        print(e)
        raise CreateArchivesError("Error creating files")

def create_dir(diretorio):
    try:
        if not os.path.isdir(diretorio):
            os.mkdir(diretorio)
    except Exception as e:
        print(e)
        raise CreateArchivesError("Error creating directory")

def close_arq(arq):
    try:
        arq.close()
    except Exception as e:
        print(e)
        raise ClosesArchivesError("Error trying close archive")
    
def write_imports(arq):
    imports = list()
    imports.append("import unittest" + newline)
    imports.append("import requests"+ newline)
    imports.append("import json5"+ newline)
    imports.append("import sys"+ newline)
    imports.append("import os"+ newline)
    imports.append("sys.path.insert(1, '../util')"+ newline)
    imports.append("from testes_util import *"+ newline +newline)
    arq.writelines(imports)
    
def write_base(arq,name,configName):
    lines = list()
    lines.append(f"class {name}(unittest.TestCase):"+ newline)
    lines.append(f"{tab}def setUp(self):"+ newline)
    lines.append(f"{tab}{tab}self.base_url = get_baseUrl()"+newline)
    lines.append(f"{tab}{tab}with open('{configName}.json', encoding='utf-8') as arq:{newline}")
    lines.append(f"{tab}{tab}{tab}self.dados = json5.load(arq)"+newline+newline)
    arq.writelines(lines)

def initialConfig(config):
    lines = list()
    lines.append("{"+ newline)
    config.writelines(lines)

def finalConfig(config):
    lines = list()
    lines.append("}")
    config.writelines(lines)
    
def create_util(util,host):
    lines = list()
    lines.append("def get_baseUrl():" + newline)
    lines.append(f"{tab}url='{host}'{newline}")
    lines.append(tab +"return url" + newline)
    util.writelines(lines)
    


