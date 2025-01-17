# Controle de estoque/almoxarifado

Aplicativo simples de controle de almoxarifado produzido por conta de dois objetivos:
 - Praticar criação de aplicações com interfaces gráficas utilizando o framework Flet.
 - Solicitação da ferramenta por um familiar próximo.

## Funcionalidades
![Demonstração](https://github.com/AllanLimaS/AlmoxarifadoControle/blob/master/assets/demonstracao_gif.gif)

- CRUD de item.
- CRuD de pessoa.
- CRud de movimentação de item por pessoa. (saída de item) 

## Criar executável 

- Criar completamente do zero
pyinstaller --onefile --noconsole --add-data "storage\\\estoque.db;storage" app.py
- Criar a partir do arquivo de especificações do pyinstaller 
pyinstaller app.spec

