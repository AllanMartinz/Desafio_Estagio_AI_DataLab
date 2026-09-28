import pandas as pd
import logging
import os
import sys
import time
import subprocess
from datetime import datetime

# Tenta importar matplotlib para evitar erro antes do check_dependencies
try:
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_pdf import PdfPages
except ImportError:
    plt = None
    PdfPages = None

# --- CONFIGURAÇÕES VISUAIS (Cores ANSI) ---
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    ENDC = '\033[0m'

# 1. CONFIGURAÇÃO DE LOG
# O log agora é configurado dinamicamente dentro da função gerar_relatorio
# para garantir que a pasta Relatorios_Gerados exista primeiro.


def print_banner():
    banner = f"""
{Colors.CYAN}{Colors.BOLD}
  ██████╗  █████╗ ██████╗ ██╗
  ██╔══██╗██╔══██╗██╔══██╗██║
  ██████╔╝███████║██████╔╝██║
  ██╔══██╗██╔══██║██╔══██╗██║
  ██████╔╝██║  ██║██║  ██║██║
  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝
    AUTOMAÇÃO DE RELATÓRIOS
{Colors.ENDC}
    """
    print(banner)

def loading_bar(text, duration=1.5):
    print(f"{Colors.BLUE}{text}{Colors.ENDC} ", end="")
    sys.stdout.write("[" + "-" * 20 + "]")
    for i in range(21):
        time.sleep(duration / 20)
        sys.stdout.write(f"\r{Colors.BLUE}{text}{Colors.ENDC} [{'#' * i}{'-' * (20 - i)}] {i*5}%")
        sys.stdout.flush()
    print(f" {Colors.GREEN}OK!{Colors.ENDC}")

def check_dependencies():
    dependencies = ['pandas', 'openpyxl', 'matplotlib']
    missing = []

    for dep in dependencies:
        try:
            __import__(dep)
        except ImportError:
            missing.append(dep)

    if missing:
        print(f"\n{Colors.YELLOW}📦 Dependências faltando: {', '.join(missing)}{Colors.ENDC}")
        loading_bar("Instalando bibliotecas")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", *missing, "-q"])
            # Recarrega matplotlib e PdfPages após a instalação
            global plt
            import matplotlib.pyplot as plt
            from matplotlib.backends.backend_pdf import PdfPages
        except Exception as e:
            print(f"{Colors.RED}Erro ao instalar dependências: {e}{Colors.ENDC}")
            sys.exit(1)
    else:
        loading_bar("Verificando ambiente", duration=0.5)

def validar_colunas(df):
    colunas_obrigatorias = [
        'id_proposta', 'data_entrada', 'canal_origem', 'status_final',
        'etapa_max_funil', 'valor_solicitado', 'valor_imovel'
    ]
    colunas_faltantes = [col for col in colunas_obrigatorias if col not in df.columns]
    if colunas_faltantes:
        raise ValueError(f"O formato do arquivo mudou! Faltam as colunas: {colunas_faltantes}")

def formatar_numero_pontos(valor):
    return f"{valor:,.2f}".replace(',', '.')

def formatar_dec_ponto(valor):
    return f"{valor:.2f}"

def export_to_excel(perda_fin, conversao_canal, folder_path):
    data_hoje = datetime.now().strftime("%Y-%m-%d")
    nome_saida = os.path.join(folder_path, f"Relatorio_{data_hoje}.xlsx")
    with pd.ExcelWriter(nome_saida) as writer:
        perda_fin.to_excel(writer, sheet_name="Dinheiro_Perdido", index=False)
        conversao_canal.to_excel(writer, sheet_name="Conversao_Canais", index=False)
    return nome_saida

def export_to_pdf(perda_fin, conversao_canal, folder_path):
    data_hoje = datetime.now().strftime("%Y-%m-%d")
    nome_saida = os.path.join(folder_path, f"Relatorio_{data_hoje}.pdf")

    with PdfPages(nome_saida) as pdf:
        # Tabela 1: Perda Financeira
        fig, ax = plt.subplots(figsize=(8.5, 11))
        ax.axis('off')
        ax.set_title("Relatório de Perda Financeira por Etapa", fontsize=16, fontweight='bold', pad=20)

        # Preparar dados para a tabela do Matplotlib
        data_perda = [perda_fin.columns.tolist()] + perda_fin.values.tolist()
        table = ax.table(cellText=data_perda, loc='center', cellLoc='center')
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        table.scale(1.2, 1.2)
        pdf.savefig(fig)
        plt.close()

        # Tabela 2: Conversão por Canal
        fig, ax = plt.subplots(figsize=(8.5, 11))
        ax.axis('off')
        ax.set_title("Taxa de Conversão por Canal de Origem", fontsize=16, fontweight='bold', pad=20)

        data_conv = [conversao_canal.columns.tolist()] + conversao_canal.values.tolist()
        table = ax.table(cellText=data_conv, loc='center', cellLoc='center')
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        table.scale(1.2, 1.2)
        pdf.savefig(fig)
        plt.close()

    return nome_saida

def gerar_relatorio(caminho_arquivo):
    try:
        print_banner()
        check_dependencies()

        # Menu de Opções
        print(f"\n{Colors.BOLD}Selecione o formato do relatório:{Colors.ENDC}")
        print(f" {Colors.CYAN}[1]{Colors.ENDC} Gerar apenas Excel (.xlsx)")
        print(f" {Colors.CYAN}[2]{Colors.ENDC} Gerar apenas PDF (.pdf)")
        print(f" {Colors.CYAN}[3]{Colors.ENDC} Gerar Ambos (Excel e PDF)")
        print(f" {Colors.CYAN}[4]{Colors.ENDC} Sair")

        opcao = input(f"\nEscolha uma opção: ").strip()

        if opcao == '4':
            print("Saindo...")
            return
        if opcao not in ['1', '2', '3']:
            print(f"{Colors.RED}Opção inválida!{Colors.ENDC}")
            return

        logging.info("--- INICIANDO ROTINA SEMANAL DE RELATÓRIO ---")

        if not os.path.exists(caminho_arquivo):
            raise FileNotFoundError(f"Arquivo '{caminho_arquivo}' não encontrado na pasta.")

        # Criar pasta de relatórios
        folder_path = "Relatorios_Gerados"
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            logging.info(f"Pasta {folder_path} criada.")

        # Configuração de Log dinâmica (Move o log para dentro da pasta)
        log_path = os.path.join(folder_path, 'execucao_relatorio.log')
        for handler in logging.root.handlers[:]:
            logging.root.removeHandler(handler)
        logging.basicConfig(
            filename=log_path,
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        logging.info(f"Log configurado em: {log_path}")


        loading_bar("Lendo arquivo bruto")
        df = pd.read_excel(caminho_arquivo)

        loading_bar("Validando integridade")
        validar_colunas(df)

        loading_bar("Limpando e tratando dados")
        df['valor_solicitado_reais'] = df['valor_solicitado'] / 100
        df_limpo = df[df['etapa_max_funil'] <= 6].copy()
        df_limpo['canal_origem'] = df_limpo['canal_origem'].astype(str).str.strip().str.capitalize()

        loading_bar("Calculando métricas")
        # Métrica 1: Perda por etapa
        perdidas = df_limpo[df_limpo['status_final'] != 'Contratada']
        perda_fin = perdidas.groupby(['etapa_max_funil', 'status_final'])['valor_solicitado_reais'].sum().reset_index()
        perda_fin = perda_fin.sort_values(by='valor_solicitado_reais', ascending=False)
        perda_fin['valor_solicitado_reais'] = perda_fin['valor_solicitado_reais'].apply(formatar_numero_pontos)

        # Métrica 2: Conversão por canal
        df_limpo['sucesso'] = df_limpo['status_final'].apply(lambda x: 1 if x == 'Contratada' else 0)
        conversao_canal = (df_limpo.groupby('canal_origem')['sucesso'].mean() * 100).reset_index()
        conversao_canal.rename(columns={'sucesso': 'conversao_%'}, inplace=True)
        conversao_canal['conversao_%'] = conversao_canal['conversao_%'].apply(formatar_dec_ponto)

        arquivos_gerados = []

        if opcao in ['1', '3']:
            loading_bar("Exportando para Excel")
            xlsx_path = export_to_excel(perda_fin, conversao_canal, folder_path)
            arquivos_gerados.append(xlsx_path)

        if opcao in ['2', '3']:
            loading_bar("Exportando para PDF")
            pdf_path = export_to_pdf(perda_fin, conversao_canal, folder_path)
            arquivos_gerados.append(pdf_path)

        logging.info(f"SUCESSO! Arquivos gerados: {arquivos_gerados}")

        print(f"\n{Colors.GREEN}{Colors.BOLD}====================================================")
        print(f"✅ SUCESSO! Relatórios gerados com êxito:")
        for arq in arquivos_gerados:
            print(f"  - {arq}")
        print(f"===================================================={Colors.ENDC}\n")

    except Exception as erro:
        logging.error(f"FALHA NA EXECUÇÃO: {erro}")
        print(f"\n{Colors.RED}{Colors.BOLD}❌ [ERRO FATAL] O relatório não pôde ser gerado.")
        print(f"Detalhe do erro: {erro}{Colors.ENDC}\n")

if __name__ == "__main__":
    os.system('')
    gerar_relatorio('proposta_credito.xlsx')
