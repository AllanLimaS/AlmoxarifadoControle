from fpdf import FPDF
import os
from datetime import datetime
import platform
import subprocess


def abrir_pdf(caminho_pdf):
    """Função para abrir o PDF automaticamente após sua criação."""
    if platform.system() == "Windows":
        os.startfile(caminho_pdf)  # No Windows
    elif platform.system() == "Darwin":  # macOS
        subprocess.run(["open", caminho_pdf])
    else:  # Linux e outros
        subprocess.run(["xdg-open", caminho_pdf])

def gerar_relatorio_itens_simples(lista):

    # Obter a data e hora atuais
    data_hora_atual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    # Criar uma instância do FPDF
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Definir fonte
    pdf.set_font("Arial", size=12)

    # Adicionar data e hora do relatório
    pdf.set_font("Arial", size=10)
    pdf.cell(200, 10, txt=f"Gerado em: {data_hora_atual}   ", ln=True, align="R",)
    pdf.ln(5)  # Linha em branco

    # Título
    pdf.set_font("Arial", style="B", size=20)
    pdf.cell(200, 10, txt="Relatório de Itens", ln=True, align="C")
    pdf.ln(10)  # Linha em branco

    # Cabeçalhos da tabela
    pdf.set_font("Arial", style="B", size=12)
    pdf.cell(100, 10, "Nome do Item", border=1, align="C")
    pdf.cell(50, 10, " ", border=1, align="C")
    pdf.ln()  # Próxima linha

    # Dados da tabela
    pdf.set_font("Arial", size=12)
    for item in lista:
        pdf.cell(100, 10, item[1], border=1, align="C")
        pdf.cell(50, 10, "", border=1, align="C")
        pdf.ln()

    # Salvar o PDF na pasta de relatórios
    output_dir = "relatorios"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    output_path = os.path.join(output_dir, "relatorio_itens.pdf")
    pdf.output(output_path)

    # Abrir o PDF automaticamente
    abrir_pdf(output_path)

    return output_path

def gerar_relatorio_itens(lista):

    # Obter a data e hora atuais
    data_hora_atual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    # Criar uma instância do FPDF
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Definir fonte
    pdf.set_font("Arial", size=12)

    # Adicionar data e hora do relatório
    pdf.set_font("Arial", size=10)
    pdf.cell(200, 10, txt=f"Gerado em: {data_hora_atual}   ", ln=True, align="R",)
    pdf.ln(5)  # Linha em branco

    # Título
    pdf.set_font("Arial", style="B", size=20)
    pdf.cell(200, 10, txt="Relatório de Itens", ln=True, align="C")
    pdf.ln(10)  # Linha em branco

    # Cabeçalhos da tabela
    pdf.set_font("Arial", style="B", size=12)
    pdf.cell(100, 10, "Nome do Item", border=1, align="C")
    pdf.cell(30, 10, "Entrada", border=1, align="C")
    pdf.cell(30, 10, "Saída", border=1, align="C")
    pdf.cell(30, 10, "Total", border=1, align="C")

    pdf.ln()  # Próxima linha

    # Dados da tabela
    pdf.set_font("Arial", size=12)
    for item in lista:
        pdf.cell(100, 10, item[1], border=1, align="C")
        pdf.cell(30, 10, str(item[2]), border=1, align="C")
        pdf.cell(30, 10, str(item[3]), border=1, align="C")
        pdf.cell(30, 10, str(item[2] - item[3]), border=1, align="C")
        pdf.ln()

    # Salvar o PDF na pasta de relatórios
    output_dir = "relatorios"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    output_path = os.path.join(output_dir, "relatorio_itens.pdf")
    pdf.output(output_path)

    # Abrir o PDF automaticamente
    abrir_pdf(output_path)

    return output_path
