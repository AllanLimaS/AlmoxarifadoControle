# Controle de estoque/almoxarifado
Aplicativo simples de controle de almoxarifado produzido por conta de dois objetivos:
 - Praticar criação de aplicações com interfaces gráficas utilizando o framework Flet.
 - Solicitação da ferramenta por um familiar próximo.

## Funcionalidades
- CRUD de item.
- CRuD de pessoa.
- CRud de movimentação de item por pessoa. (saída de item) 

## Executar 

Para que o aplicativo funcione, é necessário ter uma pasta "storage" no local do executável, para que seja criado o arquivo de banco de dados. 

## Criar executável 

- Criar completamente do zero
pyinstaller --onefile --noconsole --add-data "storage\\\estoque.db;storage" app.py
- Criar a partir do arquivo de especificações do pyinstaller 
pyinstaller app.spec

