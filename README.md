# ApiContractTestGenerator
Geração automatica de teste de contrato de API a partir da documentação swagger 2.0

## Execução
Parar executar o script de geração automática de teste basta executar o arquivo promptUser.py e inserir a informação referente ao arquivo de documentação que será utilizado para criar os scripts.

Após o processamento da documentação será exibido uma lista de urls.

Para o gerar o teste de uma url especifica basta digitar o número correspondente

Para gerar os testes de todas as urls basta digitar -1.

## Script Gerados
Para cada url será gerado 4 arquivos no caminho ./Testes/url (Onde as "/" do caminho da url seram substituídas por "_" )

Arquivos Gerados:
* ConfigurationSucessfull.json
* ConfigurationUnsucessfull.json
* {url}Sucessfull.py
* {url}Unsucessfull.py

### Arquivo de Configuração
Os arquivos de configuração possuem o esqueleto da entrada de dados necessária para a execução das requisições. È necessário a inserção de dados que sejam condizentes com os existentes na API objetivo.

Por exemplo: Uma requisição GET que necessita de um id para buscar o objeto no banco, o id deverá ser informado no arquivo de configuração no espaço adequado. Da mesma forma no arquivo ConfigurationUnsucessfull deverá ser informado um id errado, caso o objetivo seja a simulação de uma resposta 404 Not Found da API objetivo.

### Esqueleto do arquivo de configuração
Como no mesmo arquivo de testes possuem todas os testes da url e a mesma pode ter vários metodós (GET,POST,PUT), no arquivo de configuração são colocados todos os dados das requisições desses métodos de acordo com o esqueleto abaixo.
```
{
	"{url}_{tipo_metodo}{numero}":{
		"nome_atributo":"Insira o valor aqui" 
	},
	"{url}_{tipo_metodo}{numero}":{
		"nome_atributo":"Insira o valor aqui" 
	},
}
```
Para distinguir qual dado está sendo usando em qual teste basta conferir o número e o tipo. Por exemplo o teste-> teste2_sucessfull_get usará os dados do arquivo de configuração-> {url}get2

### Arquivo de Teste
Os arquivos de teste possuem a chamada de requisição para a API enviando os parametros que serão definidos no arquivo de configuração. A definição da url base que será feita a requisição está definida no arquivo Testes/util/testes_util.py. Todos os arquivos de testes utilizaram essa url para compor a url completa da requisição. 

Essa informação é preenchida com os dados da documentação, caso você queria testar a API em outra url é necessário alterar o arquivo de testes_util.py. **A alteração implica em todos os outros testes utilizando a nova url**.

Após a requisição são definidos vários "asserts" para verificar se a informação retornada da API é condizente com o descrito na documentação. O primeiro "assert" a ser feito é o de status checando se a resposta da requisição é o status esperado. Em seguida são realizados dois "asserts" para cada campo que deveria constar na resposta, um deles checando se o campo está presente na resposta e o segundo verifica se o tipo do campo é o mesmo que foi informado na documentação.
