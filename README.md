# Controle de estoque/almoxarifado

Aplicativo simples de controle de almoxarifado produzido por conta de dois objetivos:
 - Praticar criação de aplicações com interfaces gráficas utilizando o framework Flet.
 - Solicitação da ferramenta por um familiar próximo.

 Como o aplicativo será utilizado por apenas uma pessoa, foi criada uma atenticação para apenas um usuário.

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

## To Do

- Ajustar para modelo MVC
- Fazer a persistencia de dados online, utilizando algo como o firebase
- ajustar os "views" para ficarem mais organizados como o "moviementacoes_view.py"