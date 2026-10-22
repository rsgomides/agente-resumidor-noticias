"""
Módulo de Configuração do Agente Resumidor de Notícias.
Gerencia variáveis de ambiente, canais RSS nacionais (Brasil) e internacionais, e caminhos do projeto.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

# Configurações da API de IA
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite")

# Quantidade de destaques por âmbito (Brasil / Global)
TOP_NEWS_COUNT = int(os.getenv("TOP_NEWS_COUNT", "6"))

# Idioma de saída
LANGUAGE = os.getenv("LANGUAGE", "pt-br")

# Diretório onde os relatórios e páginas HTML são salvos
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Lista completa de Feeds RSS monitorados pelo Agente
DEFAULT_RSS_FEEDS = [
    # -------------------------------------------------------------
    # 🇧🇷 Canais Nacionais mais Relevantes e Conceituados (Brasil)
    # -------------------------------------------------------------
    {
        "nome": "Tecnoblog",
        "url": "https://tecnoblog.net/feed/",
        "regiao": "Brasil",
        "categoria": "Tecnologia & Mercado BR",
        "descricao": "Maior portal independente de tecnologia do Brasil"
    },
    {
        "nome": "TabNews",
        "url": "https://www.tabnews.com.br/recentes/rss",
        "regiao": "Brasil",
        "categoria": "Programação & Engenharia Dev",
        "descricao": "Comunidade de desenvolvedores com foco em conteúdo de valor concreto"
    },
    {
        "nome": "MIT Tech Review Brasil",
        "url": "https://mittechreview.com.br/feed/",
        "regiao": "Brasil",
        "categoria": "IA & Estratégia de Negócios",
        "descricao": "Análises de impacto econômico e governança de IA no mercado nacional"
    },
    {
        "nome": "Startupi",
        "url": "https://startupi.com.br/feed/",
        "regiao": "Brasil",
        "categoria": "Startups & Venture Capital",
        "descricao": "Ecossistema de empreendedorismo, captação e inovação tech"
    },
    {
        "nome": "TI Inside",
        "url": "https://tiinside.com.br/feed/",
        "regiao": "Brasil",
        "categoria": "TI Corporativa & Cloud",
        "descricao": "Notícias corporativas sobre cibersegurança, nuvem e transformação digital"
    },
    {
        "nome": "Canaltech",
        "url": "https://canaltech.com.br/rss/",
        "regiao": "Brasil",
        "categoria": "Notícias Gerais de Tecnologia",
        "descricao": "Cobertura abrangente de hardware, telecom e serviços digitais"
    },

    # -------------------------------------------------------------
    # 🌍 Canais Globais de Fronteira Tecnológica (Internacional)
    # -------------------------------------------------------------
    {
        "nome": "TechCrunch AI",
        "url": "https://techcrunch.com/category/artificial-intelligence/feed/",
        "regiao": "Global",
        "categoria": "IA & Startups Globais",
        "descricao": "Cobertura das principais Big Techs e rodadas globais de IA"
    },
    {
        "nome": "MIT Technology Review Global",
        "url": "https://www.technologyreview.com/feed/",
        "regiao": "Global",
        "categoria": "Pesquisa Científica & Computação",
        "descricao": "Publicação do MIT sobre avanços científicos e modelos de IA"
    },
    {
        "nome": "Wired AI",
        "url": "https://www.wired.com/feed/tag/ai/latest/rss",
        "regiao": "Global",
        "categoria": "Tendências & Sociedade",
        "descricao": "Investigações sobre impactos da IA no mundo e cultura digital"
    },
    {
        "nome": "The Verge Tech",
        "url": "https://www.theverge.com/rss/index.xml",
        "regiao": "Global",
        "categoria": "Ecossistema Tech Global",
        "descricao": "Jornalismo sobre regulação, software e hardware internacional"
    },
]
