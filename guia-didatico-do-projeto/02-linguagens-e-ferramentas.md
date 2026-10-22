# 🛠️ Módulo 2: Linguagens, Ferramentas e Bibliotecas Utilizadas

Para construir um agente robusto e que funcione perfeitamente no computador de qualquer usuário, selecionamos tecnologias modernas, leves e consolidadas.

Abaixo, explicamos detalhadamente **qual tecnologia foi usada, por que foi escolhida e o papel exato que ela desempenha no projeto**.

---

## 1. Linguagem Principal: Python 3.13

### Por que Python?
Python é o padrão da indústria para Inteligência Artificial, automação e ciência de dados. Sua sintaxe limpa permite que o foco do desenvolvedor fique na lógica do agente, sem se perder em burocracias de sintaxe.

### Recursos nativos utilizados:
* **`pathlib.Path`**: Gerencia caminhos de pastas e arquivos de forma segura, funcionando tanto no Windows (`\`) quanto no Linux/Mac (`/`).
* **`json`**: Serializa e converte respostas estruturadas entre a IA e o código.
* **`datetime`**: Controla datas, carimbos de tempo e nomenclatura de arquivos diários (`curadoria_2026-10-22.md`).
* **`re` e `html`**: Sanitizam textos, removendo tags HTML indesejadas que vêm nos feeds RSS.
* **`webbrowser`**: Dispara a abertura automática da página HTML no navegador padrão do sistema operacional.
* **`sys.stdout.reconfigure(encoding="utf-8")`**: Evita erros clássicos de codificação (`UnicodeEncodeError`) no terminal do Windows ao imprimir emojis e acentos.

---

## 2. Motor de Inteligência Artificial: Google Gemini API

### O modelo: `gemini-3.5-flash-lite`
* **Por que foi escolhido:** É um dos modelos mais rápidos e modernos do Google, com latência ultrabaixa (menos de 3 segundos para ler 40 notícias) e camada gratuita generosa no [Google AI Studio](https://aistudio.google.com/).
* **Recurso-chave: Saída JSON Estruturada (`responseMimeType: "application/json"`)**
  * Em vez de pedir para a IA retornar um texto livre (que pode variar e quebrar o código), forçamos o modelo a responder estritamente no formato JSON definido por nós.
  * Isso garante que os campos `titulo`, `fonte`, `por_que_importa`, `pontos_chave` e `link` sempre venham organizados para alimentar o Markdown e o HTML com perfeição.

---

## 3. Bibliotecas Externas (Instaladas no `.venv`)

As dependências foram mantidas intencionalmente leves e sem dependências pesadas de compilação em C++:

### `feedparser` (v6.0.14)
* **Função:** Lê e interpreta feeds nos formatos RSS 2.0 e Atom de qualquer site ou blog.
* **Por que é essencial:** Cada site publica seu RSS com pequenas diferenças de tags. O `feedparser` normaliza tudo em um dicionário Python uniforme (`entry.title`, `entry.link`, `entry.summary`).

### `requests` (v2.34.2)
* **Função:** Realiza as chamadas HTTP seguras (POST e GET) para a API do Google Gemini.
* **Por que foi preferido ao SDK pesado:** A chamada direta via REST API com `requests` é extremamente estável, tem zero dependências conflitantes com versões novas do Python (como Python 3.13) e nos dá controle total sobre cabeçalhos e timeouts.

### `python-dotenv` (v1.2.4)
* **Função:** Carrega variáveis de ambiente a partir do arquivo secreto `.env`.
* **Segurança:** Garante que a sua chave `GEMINI_API_KEY` nunca seja escrita diretamente no código fonte, protegendo você contra vazamentos acidentais no GitHub.

---

## 4. Tecnologias da Interface Web (Dashboard HTML)

Ao invés de instalar frameworks pesados como React ou Next.js (que exigiriam Node.js, `npm`, compilações e servidores locais rodando), criamos uma **página web única, autossuficiente e instantânea**:

### HTML5 Semântico
* Uso de tags limpas (`<article>`, `<header>`, `<section>`, `<footer>`) que organizam a hierarquia da informação.

### CSS3 Moderno (Sem Tailwind / Sem Frameworks)
* **Glassmorphism:** Uso de `backdrop-filter: blur(16px)` com fundos semitransparentes `rgba(17, 24, 39, 0.75)` para criar o visual elegante de vidro fosco.
* **Variáveis CSS (`--var`):** Permitem alternar entre Modo Escuro (*Dark Mode Obsidian*) e Modo Claro com suavidade.
* **CSS Grid & Flexbox:** Layout responsivo que se adapta perfeitamente do monitor ultrawide à tela do celular.
* **Tipografia:** Google Fonts com as fontes modernas **Plus Jakarta Sans** (leitura do corpo) e **Outfit** (títulos expressivos).

### JavaScript Vanilla (Nativo do Navegador)
* **Filtros e Busca em Tempo Real:** Escuta o evento `oninput` do teclado e filtra os cartões de notícias sem precisar recarregar a página.
* **Web Speech API (`SpeechSynthesisUtterance`):** Utiliza a inteligência de voz nativa do próprio navegador do usuário para transformar texto em fala (*Text-to-Speech*) em português com o botão "🔊 Ouvir Resumo".
* **Clipboard API (`navigator.clipboard`):** Permite copiar o link original da matéria com feedback visual de notificação (*toast*).

---

## 5. Ferramentas de Automação do Sistema (Windows)

Para que o agente não dependa de comandos manuais no terminal, implementamos a automação nativa do Windows:

| Ferramenta | Arquivo | Papel no Projeto |
| :--- | :--- | :--- |
| **PowerShell** | [`agendar_rotina.ps1`](../agente-resumidor-noticias/agendar_rotina.ps1) | Registra a tarefa diária no Agendador de Tarefas do Windows com os privilégios corretos. |
| **Agendador de Tarefas (*Task Scheduler*)** | Gerenciado pelo Windows | Dispara o fluxo diariamente às 13:00 (horário de Brasília). |
| **VBScript** | [`executar_silencioso.vbs`](../agente-resumidor-noticias/executar_silencioso.vbs) | Executa o processo de forma silenciosa em segundo plano, sem abrir janelas pretas do terminal na tela do usuário. |
| **Batch Script** | [`executar.bat`](../agente-resumidor-noticias/executar.bat) | Atalho de 1 clique para quem quiser rodar manualmente a qualquer momento. |

---

## 📊 Resumo do Stack Tecnológico

```text
Camada de Coleta:       RSS/Atom + Feedparser + Python 3.13
Camada de Inteligência: Google Gemini API (gemini-3.5-flash-lite) + JSON Schema
Camada de Persistência: Markdown (.md) + HTML5/CSS3/JS
Camada de Apresentação: Navegador Web (Chrome/Edge/Brave/Firefox) + Web Speech API
Camada de Automação:    Windows Task Scheduler + PowerShell + VBScript
```
