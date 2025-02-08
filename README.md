# Controle de estoque/almoxarifado

Aplicativo simples de controle de almoxarifado produzido por conta de dois objetivos:
 - Praticar criação de aplicações com interfaces gráficas utilizando o framework Flet.
 - Solicitação da ferramenta por um familiar próximo.

 Como o aplicativo será utilizado por apenas uma pessoa, foi criada uma atenticação para apenas um usuário.

## Funcionalidades
![Demonstração](https://github.com/AllanLimaS/AlmoxarifadoControle/blob/master/assets/demonstracao_gif.gif)

- CRUD de item.
- CRUD de pessoa.
- CRuD de movimentação de item por pessoa. (saída de item) 
- Impressão de relatório de itens
- Autenticação de usuário (apenas um) para acessar o aplicativo

# Como usar 

## Executável

Para apenas utilizar o aplicativo, disponibilizei duas opções nos 'releases' deste repositório:
- Executável one-file standalone.
Basta baixar e executar.
Há grandes chances de o antivírus emitir um aviso de falso positivo.
- Setup
Nesta opção, o aplicativo será instalado em uma pasta junto com suas dependências, utilizando um assistente de instalação simples.

## Compilar o código-fonte 

Caso queira criar o executável a partir do código-fonte, pode-se utilizar uma das opções a seguir:

### pyinstaller 

O PyInstaller gera o executável rapidamente, mas ao distribuí-lo, frequentemente aciona falsos positivos em diversos antivírus.

- Criar completamente do zero
`pyinstaller --onefile --noconsole --add-data "storage\\\estoque.db;storage" app.py`
- Criar a partir do arquivo de especificações do PyInstaller:
`pyinstaller app.spec`

### Flet

O Flet utiliza o PyInstaller internamente, portanto apresenta os mesmos problemas com antivírus.

`flet pack app.py --name 'Controle de Estoque v1.3' --icon assets\box.ico --product-name 'Controle de Estoque' --product-version 1.3 --copyright 'AllanLimaS 2025'`

### Nuitka

A compilação com Nuitka é mais demorada, mas há menos chances de acionar um falso positivo nos antivírus.

- cria o aplicativo em uma pasta com o executável e suas depedências
`nuitka --standalone --windows-console-mode=disable --windows-icon-from-ico=assets\box.ico --enable-plugin=tk-inter --output-filename='Controle de Estoque' app.py`

- cria o aplicativo com apenas um arquivo ( não funcionou )
`nuitka --onefile --windows-console-mode=disable --windows-icon-from-ico=assets\box.ico --enable-plugin=tk-inter --output-filename='Controle de Estoque' app.py `


## To Do

- Ajustar para modelo MVC
- Fazer a persistencia de dados online, utilizando algo como o firebase