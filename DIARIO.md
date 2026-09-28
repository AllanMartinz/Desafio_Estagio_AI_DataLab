# DIÁRIO DE BORDO - DESAFIO PRÁTICO AI

## a) Registro de Uso de IA

### Ferramentas Utilizadas
Para o desenvolvimento deste projeto, utilizei um ecossistema de IAs complementares:
*   **Google Gemini**: Utilizado para a concepção inicial da arquitetura dos códigos, estruturação dos prompts de extração e implementação da chamada de API para a versão em nuvem do Extrator de Laudos.
*   **Claude Code**: Ferramenta fundamental para o aprimoramento técnico, refatoração de código, implementação de interfaces visuais (ASCII Art) e automação de tarefas de limpeza e padronização de arquivos.
*   **Ollama (Llama 3.2)**: Implementado como a engine de IA local para garantir a continuidade do processamento de dados sem dependências de cotas externas.
*   **Pandas (Python)**: Embora seja uma biblioteca, a lógica de manipulação de dados foi otimizada via prompts de IA para garantir que a limpeza financeira (ajuste de centavos para reais) fosse precisa.

### Superação de Problemas com IA
A situação mais crítica ocorreu durante a implementação do **Projeto Extrator de Laudos**. Inicialmente, utilizei a API do Google Gemini por ser acessível e poderosa. No entanto, enfrentei dois obstáculos técnicos severos:
1.  **Erro 503 (Service Unavailable)**: O modelo apresentava instabilidade devido a picos de demanda, interrompendo a extração de laudos em lote.
2.  **Erro 429 (Too Many Requests)**: As cotas do plano gratuito foram rapidamente atingidas, impossibilitando a finalização do processamento de todos os documentos.

**Solução**: Para resolver isso, mudei a estratégia de arquitetura. Implementei o **Ollama**, permitindo que o modelo de IA (Llama 3.2) rodasse localmente na minha própria máquina. Isso eliminou a dependência da nuvem, removeu as limitações de cotas de API e garantiu que 100% dos laudos fossem processados com estabilidade e privacidade.

## b) Aprendizado e Evolução

### Conceitos Aprendidos do Zero
Este desafio foi um divisor de águas no meu aprendizado técnico. Eu não possuía experiência prévia com as seguintes ferramentas e conceitos, que aprendi durante a execução do projeto:
*   **Jupyter Notebook**: Aprendi a utilizar o ambiente de notebooks para análise exploratória de dados, permitindo a visualização imediata de tabelas e gráficos.
*   **Biblioteca Pandas**: Dominei a manipulação de DataFrames, a limpeza de dados corrompidos (como a remoção de propostas com idades irreais ou etapas inexistentes) e a exportação de resultados para Excel.
*   **Extração de Dados Estruturados (JSON) via LLM**: Aprendi a criar prompts de sistema rigorosos para forçar modelos de linguagem a retornar dados exclusivamente em formato JSON, permitindo que a IA funcione como um extrator de banco de dados.

**Metodologia**: O aprendizado ocorreu de forma intensiva e prática, utilizando a documentação das bibliotecas e o suporte das IAs Gemini e Claude. Dediquei aproximadamente 30 horas de estudo e desenvolvimento para entregar as quatro etapas do desafio.

### Pontos de Melhoria (Autoavaliação)
Reconheço que a entrega poderia ser aprimorada nos seguintes pontos:
*   **Recursos dos Executáveis**: Embora as automações funcionem perfeitamente, os executáveis `.bat` e os scripts `.py` poderiam ter interfaces de usuário (UI) mais robustas, como menus de navegação mais complexos ou logs de erro mais detalhados para o usuário final.
*   **Validação de Dados**: A parte de extração de laudos poderia contar com uma camada adicional de validação para garantir que a IA não tenha "alucinado" algum dado específico, especialmente em laudos com caligrafia ou formatação complexa.

### Visão de Futuro (Com mais 40 horas)
Se tivesse mais tempo, eu focaria em:
1.  **Dashboard Interativo**: Em vez de apenas exportar para Excel/PDF, criaria um dashboard em Streamlit ou Power BI para visualizar o gargalo do funil de crédito em tempo real.
2.  **Pipeline de Dados Automatizado**: Criaria um fluxo onde o arquivo `.xlsx` de propostas fosse monitorado; assim que um novo arquivo fosse salvo, o relatório seria gerado automaticamente.
3.  **Otimização do Modelo Local**: Realizaria um *fine-tuning* ou usaria técnicas de RAG (Retrieval-Augmented Generation) para tornar a extração de laudos ainda mais precisa, reduzindo a necessidade de revisão humana.

### Pergunta ao Time de Negócios
Se pudesse ter feito uma pergunta antes de começar, seria: 
*"Quais são as métricas de sucesso mais críticas para a diretoria neste momento: a redução do tempo de processamento de cada proposta ou a diminuição do valor financeiro perdido nas etapas iniciais do funil?"*
Saber isso me permitiria priorizar a análise de eficiência operacional versus a análise de perda financeira no relatório final.
