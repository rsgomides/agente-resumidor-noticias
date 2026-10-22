# 🤖 Agente Resumidor & Curador de Notícias (Brasil & Global)

Bem-vindo ao projeto do **Agente Autônomo de Curadoria de Notícias de Tecnologia, IA, Programação e Negócios**!

Este agente monitora os 10 veículos de tecnologia mais conceituados do **Brasil** e do **Mundo**, filtra as informações com a inteligência do **Google Gemini**, gera relatórios em Markdown e constrói uma **página web interativa em HTML com síntese de voz**, abrindo-a automaticamente no seu navegador.

---

## 🎯 O que o Agente Faz?

1. **Monitoramento Automatizado:** Conecta-se via RSS a 10 canais renomados:
   * **🇧🇷 Brasil:** [Tecnoblog](https://tecnoblog.net/), [TabNews](https://www.tabnews.com.br/) (devs), [MIT Tech Review Brasil](https://mittechreview.com.br/), [Startupi](https://startupi.com.br/) (startups & VC), [TI Inside](https://tiinside.com.br/) (TI corporativa) e [Canaltech](https://canaltech.com.br/).
   * **🌍 Global:** [TechCrunch AI](https://techcrunch.com/), [Wired AI](https://www.wired.com/), [MIT Technology Review Global](https://www.technologyreview.com/) e [The Verge Tech](https://www.theverge.com/).
2. **Curadoria Inteligente com Gemini:** Seleciona os destaques nacionais e internacionais mais impactantes, analisa "Por que isso importa?" e extrai pontos-chave.
3. **Dashboard Web Interativo:** Gera um arquivo HTML moderno com suporte a tema escuro/claro, filtros dinâmicos, busca instantânea e leitura em voz alta (*Text-to-Speech*).
4. **Rotina Automática Diária:** Possui script pronto para rodar todos os dias às **13:00 (Horário de Brasília)** em segundo plano no Windows.

---

## 🏗️ Estrutura de Arquivos

```text
agente-resumidor-noticias/
├── main.py                    # Script orquestrador central
├── config.py                  # Lista de 10 feeds monitorados e configurações
├── ai_curator.py              # Integração estruturada com Google Gemini + Fallback local
├── rss_fetcher.py             # Coletor e sanitizador de feeds RSS
├── html_generator.py          # Gerador do dashboard web responsivo com áudio TTS
├── executar.bat               # Atalho para rodar manualmente com 1 duplo clique
├── agendar_rotina.bat         # Agenda a execução diária automática às 13:00 no Windows
├── agendar_rotina.ps1         # Script PowerShell de registro da tarefa no Task Scheduler
├── testar_rotina_agora.bat    # Testa o agendamento em segundo plano imediatamente
├── remover_rotina.bat         # Cancela/remove a rotina automática se desejar
├── executar_silencioso.vbs    # Launcher invisível que evita piscar janelas do terminal
├── executar_rotina.bat        # Acionador chamado pelo agendador
├── requirements.txt           # Dependências (feedparser, requests, python-dotenv)
├── .env.example              # Modelo de configuração de chaves
├── .gitignore                # Proteção para não versionar credenciais secretas
└── output/                   # Pasta onde os relatórios são salvos
    ├── curadoria_YYYY-MM-DD.md
    └── curadoria_YYYY-MM-DD.html
```

---

## 🚀 Como Executar

### Opção 1: Execução Manual Imediata
Basta dar um duplo clique no arquivo [`executar.bat`](executar.bat) ou rodar no terminal:
```powershell
.\.venv\Scripts\python.exe main.py
```

### Opção 2: Ativar a Rotina Automática Diária às 13:00
Dê um duplo clique no arquivo [`agendar_rotina.bat`](agendar_rotina.bat).
* O Windows registrará a tarefa no **Agendador de Tarefas**.
* Todo dia, exatamente às **13:00 (Brasília)**, o agente rodará silenciosamente em segundo plano e a página HTML com as novidades do dia surgirá aberta no seu navegador!
* Para testar se o agendamento está funcionando sem esperar até as 13h, dê duplo clique em [`testar_rotina_agora.bat`](testar_rotina_agora.bat).
* Se quiser desativar a rotina no futuro, dê duplo clique em [`remover_rotina.bat`](remover_rotina.bat).

---

## 🔑 Configuração da Chave da API

O projeto vem com uma chave configurada no arquivo `.env`. Caso queira utilizar a sua própria chave gratuita:
1. Obtenha uma chave no [Google AI Studio](https://aistudio.google.com/app/apikey);
2. Abra o arquivo `.env` e configure:
   ```env
   GEMINI_API_KEY=sua_chave_aqui
   GEMINI_MODEL=gemini-3.5-flash-lite
   ```

---

## 📖 Quer Entender Como Tudo Foi Feito?

Consulte a pasta de documentação didática completa:
👉 [**Acessar a Pasta Guia Didático do Projeto**](https://github.com/rsgomides/agente-resumidor-noticias/tree/main/guia-didatico-do-projeto)
