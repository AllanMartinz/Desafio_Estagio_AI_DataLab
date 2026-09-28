import os
import json
import pandas as pd
import logging
import time
import sys
import re
from google import genai
from google.genai import types

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

def print_banner():
    banner = f"""
{Colors.CYAN}{Colors.BOLD}
  ██████╗  █████╗ ██████╗ ██╗
  ██╔══██╗██╔══██╗██╔══██╗██║
  ██████╔╝███████║██████╔╝██║
  ██╔══██╗██╔══██║██╔══██╗██║
  ██████╔╝██║  ██║██║  ██║██║
  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝
  EXTRATOR DE LAUDOS - NUVEM
{Colors.ENDC}
    """
    print(banner)

def loading_bar(text, duration=1.0):
    print(f"{Colors.BLUE}{text}{Colors.ENDC} ", end="")
    sys.stdout.write("[" + "-" * 20 + "]")
    for i in range(21):
        time.sleep(duration / 20)
        sys.stdout.write(f"\r{Colors.BLUE}{text}{Colors.ENDC} [{'#' * i}{'-' * (20 - i)}] {i*5}%")
        sys.stdout.flush()
    print(f" {Colors.GREEN}OK!{Colors.ENDC}")

# Configuração de log para auditoria
logging.basicConfig(filename='extracao_nuvem.log', level=logging.INFO, format='%(asctime)s - %(message)s')

# Insira sua chave de API gerada no Google AI Studio
GOOGLE_API_KEY = "sua-chave-aqui(retirado a chave por motivos de segurança)"

PROMPT_SISTEMA = """
Você é um Perito Assistente de IA sênior especializado em auditoria, análise imobiliária e extração de dados jurídicos.
Sua tarefa é analisar laudos de avaliação com extrema atenção aos detalhes.
REQUISITO DE TEMPO: Não tenha pressa. Leia o documento inteiro com extrema calma, reflita passo a passo sobre cada informação e leve o tempo computacional que for necessário para garantir 100% de precisão antes de gerar a resposta.

Você deve extrair os dados e retornar ESTRITAMENTE um JSON válido.

CHAVES DO JSON E REGRAS CRÍTICAS DE EXTRAÇÃO:

1. "tipo_imovel": (string)
   - Regra: Busque exaustivamente por termos que definam o imóvel. Pode estar no meio do texto (ex: "trata-se de um edifício", "casa residencial", "terreno nu", "galpão"). NUNCA deixe nulo se houver qualquer menção ao tipo de construção ou terreno.

2. "endereco": (string)
   - Regra: O endereço completo do imóvel avaliado.

3. "areas": (string)
   - Regra: Extraia todas as menções a áreas (ex: área do terreno, área construída, área privativa).

4. "ano": (inteiro, string ou null)
   - Regra: Extraia o ano de construção exato se houver. Se não houver o ano exato, mas houver menção à idade (ex: "Idade aparente: 11 anos", "aproximadamente 18 anos"), extraia o número da idade ou o texto correspondente para que possamos calcular depois.

5. "valor_avaliacao_real": (string)
   - Regra: Extraia o valor financeiro da avaliação.
   - FORMATAÇÃO OBRIGATÓRIA: Remova TODOS os pontos (.) e vírgulas (,), mantendo apenas os números corridos.
   - REGRA DO EXCEL: Você DEVE obrigatoriamente adicionar 1 (um) espaço em branco no final dos números para forçar a planilha a ler como texto. Exemplo: se o valor for R$ 1.123.000,00, você DEVE retornar exatamente "112300000 ".

6. "matricula": (string)
   - Regra: O número da matrícula do imóvel.
   - REGRA DO EXCEL: Assim como no valor, você DEVE obrigatoriamente adicionar 1 (um) espaço em branco no final do número. Exemplo: se a matrícula for 98765, retorne "98765 ".

7. "onus": (string)
   - Regra: Extraia a seção de ônus, gravames ou observações da matrícula.
   - REGRA DE PREENCHIMENTO: Transcreva EXATAMENTE o que está escrito no laudo, mesmo que seja negativo. Se estiver escrito "sem informação", "nada consta", "não há menção a ônus", "livre e desembaraçado", você DEVE escrever essas frases. NUNCA preencha como null nestes casos.

8. "data_vistoria": (string)
   - Regra: A data em que a vistoria ou avaliação foi realizada.
   - FORMATO PADRÃO BRASILEIRO: Você DEVE formatar a data estritamente como DD/MM/AAAA.
   - Se encontrar traços (ex: 2024-12-05 ou 05-12-2024), você é OBRIGADO a converter para barras (05/12/2024).

9. "responsavel_tecnico": (string)
   - Regra: Procure com o máximo de atenção pelo nome do avaliador, engenheiro, arquiteto ou perito responsável pelo laudo. Verifique assinaturas no final do documento. É inadmissível retornar null se o nome constar no texto.

10. "observacoes": (string)
    - Regra: NOVA COLUNA. Preencha com informações relevantes que não couberam nos campos anteriores, como estado de conservação, divergências documentais, método de avaliação usado ou qualquer outra ressalva importante do perito.

INSTRUÇÕES FINAIS:
- Se, e SOMENTE SE, após procurar no documento inteiro uma informação realmente não existir, use o valor null (nulo padrão do JSON, sem aspas).
- Não inclua blocos de código Markdown (` ```json `), comentários ou qualquer texto fora do JSON. Apenas as chaves e os valores.
"""


def chamar_gemini(texto_laudo):
    # Inicializa o novo cliente oficial do Gemini
    client = genai.Client(api_key=GOOGLE_API_KEY)

    response = client.models.generate_content(
        model='gemini-3.8-flash',
        contents=f"Extraia os dados deste laudo:\n\n{texto_laudo}",
        config=types.GenerateContentConfig(
            system_instruction=PROMPT_SISTEMA,
            response_mime_type="application/json",
            temperature=0.0
        )
    )
    return response.text


def processar_laudos(pasta_laudos):
    resultados = []

    if not os.path.exists(pasta_laudos):
        print(f"{Colors.RED}Erro: A pasta '{pasta_laudos}' não foi encontrada.{Colors.ENDC}")
        return

    arquivos = [f for f in os.listdir(pasta_laudos) if f.endswith(".txt")]

    loading_bar(f"Localizando laudos", duration=0.5)
    print(f"\n{Colors.BOLD}Encontrados {len(arquivos)} laudos para processamento. Iniciando via Nuvem (Gemini)...{Colors.ENDC}\n")

    for arquivo in arquivos:
        caminho = os.path.join(pasta_laudos, arquivo)
        with open(caminho, 'r', encoding='utf-8') as f:
            texto = f.read()

        print(f"Extraindo dados de: {Colors.CYAN}{arquivo}{Colors.ENDC}...", end=" ")
        logging.info(f"Processando: {arquivo}")

        try:
            # 1. Chama o Gemini
            resposta_ia = chamar_gemini(texto)

            # 2. Converte para Dicionário Python
            dados_extraidos = json.loads(resposta_ia)
            dados_extraidos['arquivo_origem'] = arquivo

            # 3. Validação de Qualidade (Fill Rate)
            campos_nulos = sum(1 for v in dados_extraidos.values() if v is None)
            if campos_nulos >= 4:
                dados_extraidos['status_extracao'] = 'REVISÃO HUMANA (Muitos nulos)'
            else:
                dados_extraidos['status_extracao'] = 'SUCESSO'

            resultados.append(dados_extraidos)
            logging.info(f"{arquivo} - SUCESSO")
            print(f"{Colors.GREEN}OK!{Colors.ENDC}")

        except json.JSONDecodeError:
            logging.error(f"Falha de formato no arquivo {arquivo}.")
            print(f"{Colors.RED}Falha ao converter resposta em JSON.{Colors.ENDC}")
            resultados.append({"arquivo_origem": arquivo, "status_extracao": "FALHA - FORMATO INVÁLIDO"})
        except Exception as e:
            logging.error(f"Erro de API no arquivo {arquivo}: {e}")
            print(f"{Colors.RED}Erro de comunicação: {e}{Colors.ENDC}")

            print("\nAguardando 15 segundos para evitar bloqueio de limite da API...")
            time.sleep(15)

    # Exportação para o Excel
    if resultados:
        loading_bar("Gerando planilha final", duration=0.8)
        df_resultados = pd.DataFrame(resultados)
        colunas = ['arquivo_origem', 'status_extracao'] + [col for col in df_resultados.columns if
                                                           col not in ['arquivo_origem', 'status_extracao']]
        df_resultados = df_resultados[colunas]

        df_resultados.to_excel("Base_Laudos_Extraidos.xlsx", index=False)
        print(f"\n{Colors.GREEN}{Colors.BOLD}====================================================")
        print(f"✅ Extração concluída! Verifique o arquivo 'Base_Laudos_Extraidos.xlsx'.")
        print(f"===================================================={Colors.ENDC}\n")
    else:
        print(f"\n{Colors.RED}❌ Nenhum dado extraído.{Colors.ENDC}")


if __name__ == "__main__":
    os.system('') # Habilita cores no CMD do Windows
    print_banner()
    processar_laudos("laudos_avaliacao")
