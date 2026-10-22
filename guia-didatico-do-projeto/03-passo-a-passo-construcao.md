# 🔨 Módulo 3: Passo a Passo da Construção (Do Zero à Produção)

Neste capítulo, você verá o passo a passo exato de como este projeto foi concebido e programado. Você pode seguir este roteiro para reproduzir o projeto do zero ou para criar seus próprios agentes autônomos.

---

## Passo 1: Isolamento do Ambiente de Desenvolvimento

### O erro mais comum de iniciantes:
Instalar pacotes diretamente no Python global do sistema com `pip install pacote`. Com o tempo, projetos diferentes exigem versões conflitantes e quebram o ambiente da máquina.

### Como fizemos corretamente:
1. Criamos um ambiente virtual isolado chamado `.venv`:
   ```powershell
   python -m venv .venv
   ```
2. Criamos o arquivo [`requirements.txt`](../agente-resumidor-noticias/requirements.txt) listando apenas o essencial:
   ```text
   feedparser>=6.0.11
   python-dotenv>=1.0.1
   requests>=2.31.0
   ```
3. Instalamos os pacotes diretamente no ambiente virtual:
   ```powershell
   .\.venv\Scripts\pip install -r requirements.txt
   ```
4. Criamos um arquivo [`.gitignore`](../agente-resumidor-noticias/.gitignore) para impedir que a pasta `.venv/` e as chaves do `.env` subam para o GitHub.

---

## Passo 2: Mapeamento de Fontes e Configurações em `config.py`

Separamos todas as variáveis de configuração em um módulo dedicado ([`config.py`](../agente-resumidor-noticias/config.py)):

* **Por que fazer isso:** Se amanhã você quiser adicionar um novo feed RSS ou alterar o modelo de IA, você não precisa mexer no código de lógica do robô; basta editar a lista em `config.py`.
* Mapeamos **10 portais conceituados**:
  * **Nacionais:** Tecnoblog, TabNews (devs), MIT Tech Review Brasil, Startupi, TI Inside e Canaltech.
  * **Globais:** TechCrunch AI, MIT Technology Review Global, Wired AI e The Verge.

---

## Passo 3: Criação do Coletor de Dados em `rss_fetcher.py`

O papel do [`rss_fetcher.py`](../agente-resumidor-noticias/rss_fetcher.py) é ser o "sensor" do agente.

### Desafios resolvidos nesta etapa:
1. **Limpeza de HTML:** Artigos de RSS costumam vir com tags feias como `<p>`, `<a>`, `&nbsp;`. Criamos a função `limpar_texto_html()` com expressões regulares (`re.sub`) e decodificador de entidades (`html.unescape`) para transformar o texto em texto puro.
2. **Tolerância a falhas:** Se um site estiver fora do ar ou bloquear a conexão, o robô não trava: ele emite um aviso no console e continua processando os outros 9 canais com tranquilidade.

---

## Passo 4: O "Cérebro" do Agente em `ai_curator.py`

Esta é a etapa onde a mágica da inteligência artificial acontece:

### A Engenharia de Prompt:
Montamos um prompt especializado que:
1. Recebe a lista bruta das 40 notícias;
2. Instrui o Gemini com o papel: *"Você é um Agente Especialista em Curadoria de Tecnologia..."*;
3. Exige a classificação separada de **Destaques Nacionais (Brasil)** e **Destaques Globais**;
4. Obriga a extração de um campo valioso: **"Por que isso importa?"** (análise de impacto para o leitor);
5. Solicita a sugestão de uma **Dica Prática de Estudos**.

### Saída Estruturada com JSON Mode:
Configuramos a API com:
```python
"generationConfig": {
    "responseMimeType": "application/json",
    "temperature": 0.3
}
```
Isso força o modelo a entregar um JSON perfeito que o Python converte instantaneamente para um dicionário com `json.loads()`.

### Modo de Contingência (*Fallback*):
E se a internet cair ou o usuário não tiver chave de API configurada? O módulo conta com a função `_curadoria_local()` que usa heurísticas locais de palavras-chave para montar o relatório mesmo sem IA.

---

## Passo 5: Geração da Interface Web em `html_generator.py`

Para transformar os dados em uma experiência incrível para o usuário:

1. Desenhamos um layout com **Glassmorphism** e cores refinadas (fundos escuros obsidian, toques de esmeralda para o Brasil e índigo para o Global);
2. Adicionamos a tag `<meta name="viewport">` para garantir responsividade no celular;
3. Criamos em **JavaScript puro**:
   * O sistema de alternância entre Modo Claro e Escuro;
   * O sintetizador de voz com `window.speechSynthesis` para ler as matérias em voz alta;
   * O filtro dinâmico de busca por texto e botões de filtro (`🇧🇷 Somente Brasil`, `🌍 Somente Global`).

---

## Passo 6: O Orquestrador Central em `main.py`

O [`main.py`](../agente-resumidor-noticias/main.py) amarra todas as pontas em uma sequência lógica:
1. Imprime o banner no console;
2. Chama o coletor (`coletar_noticias`);
3. Chama o cérebro (`gerar_dados_curadoria`);
4. Salva a versão em Markdown (`output/curadoria_YYYY-MM-DD.md`);
5. Salva a versão em HTML (`output/curadoria_YYYY-MM-DD.html`);
6. Dispara o navegador do sistema com `webbrowser.open()`.

---

## Passo 7: Automação e Facilidade de Uso

Para que ninguém precise abrir o terminal e digitar comandos:
* Criamos o [`executar.bat`](../agente-resumidor-noticias/executar.bat) para rodar com **duplo clique**;
* Criamos o agendamento no Windows com [`agendar_rotina.bat`](../agente-resumidor-noticias/agendar_rotina.bat) para disparar todos os dias às **13:00** silenciosamente via [`executar_silencioso.vbs`](../agente-resumidor-noticias/executar_silencioso.vbs).
