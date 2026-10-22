# 🚀 Módulo 5: Personalização e Próximos Passos de Evolução

Agora que você compreende como o agente funciona, veja como você pode personalizá-lo para atender exatamente às suas preferências e como levá-lo para o próximo nível.

---

## 1. Como Adicionar Novos Canais de Notícias

Para incluir um novo blog, portal ou newsletter que você goste, abra o arquivo [`config.py`](../agente-resumidor-noticias/config.py) e adicione um novo bloco dentro da lista `DEFAULT_RSS_FEEDS`:

```python
{
    "nome": "Seu Portal Favorito",
    "url": "https://url-do-feed-rss.com/feed",
    "regiao": "Brasil",  # ou "Global"
    "categoria": "IA & Startups",
    "descricao": "Breve descrição do portal"
},
```

> **Dica:** Quase todo blog em WordPress disponibiliza RSS nativo simplesmente adicionando `/feed` ao final da URL (exemplo: `https://meublog.com/feed`).

---

## 2. Como Mudar o Horário da Execução Automática

Se você preferir receber a curadoria às **08:00 da manhã** antes de começar a trabalhar, ao invés das 13:00:

1. Abra o arquivo [`agendar_rotina.ps1`](../agente-resumidor-noticias/agendar_rotina.ps1);
2. Altere a linha:
   ```powershell
   $trigger = New-ScheduledTaskTrigger -Daily -At 13:00
   ```
   para:
   ```powershell
   $trigger = New-ScheduledTaskTrigger -Daily -At 08:00
   ```
3. Dê um duplo clique no arquivo [`agendar_rotina.bat`](../agente-resumidor-noticias/agendar_rotina.bat) para atualizar o agendamento no Windows!

---

## 3. Ideias de Evolução para Desenvolver suas Habilidades

Aqui estão três desafios graduais para você praticar o que aprendeu:

### Desafio 1: Notificação em Bot do Telegram 📲
* **Como fazer:** Crie um bot gratuito no Telegram com o [@BotFather](https://t.me/BotFather), pegue seu Token e Chat ID.
* No `main.py`, adicione uma função simples com `requests.post()` para enviar o resumo das 3 principais notícias do Brasil direto no seu celular todo dia às 13:00.

### Desafio 2: Envio para um Canal do Discord 🎮
* **Como fazer:** No Discord, crie um *Webhook* nas configurações do seu servidor e envie uma requisição HTTP contendo os pontos-chave da matéria formatados com *Embeds*.

### Desafio 3: Suporte a Transcrição de Podcasts de Tecnologia 🎙️
* **Como fazer:** Use bibliotecas como `pytube` ou feeds RSS de áudio e passe o áudio para um modelo como o **Whisper** ou o **Gemini multimodal** transcrever e resumir episódios dos seus podcasts favoritos.
