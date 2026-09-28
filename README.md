# 📊 Desafio Prático AI - Tratamento de Dados e Extração de Laudos

Este projeto compõe as etapas de análise de dados de propostas de crédito e automação de extração de informações de laudos de avaliação imobiliária utilizando Inteligência Artificial.

## 🚀 Como Rodar o Projeto

O projeto está dividido em dois módulos principais. Ambos foram desenvolvidos para rodar em ambiente Windows.

### 1. Relatório de Proposta de Crédito
Este módulo analisa a base de dados de propostas, realiza a limpeza de dados e gera relatórios de perda financeira e conversão.
*   **Pré-requisitos**: Python instalado e as bibliotecas `pandas`, `openpyxl` e `matplotlib`.
*   **Como executar**:
    1. Navegue até a pasta `1.2.Relatorio_Proposta_Credito`.
    2. Execute o arquivo `Gerar_Relatorio.bat`.
    3. O script abrirá o terminal, solicitará o formato do relatório (Excel, PDF ou Ambos) e salvará os resultados na pasta `Relatorios_Gerados`.

### 2. Projeto Extrator de Laudos
Este módulo utiliza LLMs (Large Language Models) para ler arquivos de texto (.txt) de laudos e extrair dados estruturados para uma planilha Excel.
*   **Opção A - Extração Local (Recomendado)**:
    1. Instale o [Ollama](https://ollama.com/) e baixe o modelo Llama 3.2 (`ollama run llama3.2`).
    2. Navegue até `3.Projeto_Extrator_Laudos/Extrator_Local`.
    3. Execute `Executar_Local.bat`.
*   **Opção B - Extração Nuvem**:
    1. Certifique-se de ter a chave de API do Google Gemini configurada no código.
    2. Navegue até `3.Projeto_Extrator_Laudos/Extrator_Nuvem`.
    3. Execute `Executar_Nuvem.bat`.

---

## 📂 Estrutura de Arquivos

### 📁 `1.2.Relatorio_Proposta_Credito`
*   `automacao_relatorio.py`: Script principal que processa os dados, calcula métricas de funil e gera os arquivos de saída.
*   `Gerar_Relatorio.bat`: Atalho para execução rápida do script de relatório.
*   `Parte1_Analise_Exploratoria.ipynb`: Notebook com a análise inicial, limpeza de dados e validações estatísticas.
*   `proposta_credito.xlsx`: Base de dados bruta de propostas de crédito.
*   `registro_tratamento_dados.txt`: Documentação detalhada de todas as limpezas e correções feitas nos dados.

### 📁 `3.Projeto_Extrator_Laudos`
*   **`Extrator_Local/`**:
    *   `extracao_local.py`: Script que utiliza a biblioteca `ollama` para processar laudos localmente.
    *   `Executar_Local.bat`: Atalho para execução do extrator local.
    *   `laudos_avaliacao/`: Pasta contendo os arquivos `.txt` dos laudos para extração.
*   **`Extrator_Nuvem/`**:
    *   `extracao_nuvem.py`: Script que utiliza a API do `google-genai` para processar laudos na nuvem.
    *   `Executar_Nuvem.bat`: Atalho para execução do extrator em nuvem.
    *   `laudos_avaliacao/`: Pasta contendo os arquivos `.txt` dos laudos para extração.

---

## ⏱️ Tempo de Desenvolvimento

O tempo total investido no desenvolvimento de todas as etapas (Análise Exploratória, Automação de Relatórios, Implementação de Extratores Local e Nuvem e Documentação) foi de aproximadamente **30 horas**.
