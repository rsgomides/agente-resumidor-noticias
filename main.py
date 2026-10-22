"""
Ponto de entrada do Agente Resumidor & Curador de Notícias.
Orquestra a coleta de feeds RSS, a síntese inteligente com IA e a geração
dos relatórios em Markdown e da página interativa em HTML (abrindo no navegador).
"""

import sys
import webbrowser
from datetime import datetime
from pathlib import Path

# Garante suporte a UTF-8 no terminal Windows para emojis e acentos
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

from config import DEFAULT_RSS_FEEDS, OUTPUT_DIR
from rss_fetcher import coletar_noticias
from ai_curator import gerar_dados_curadoria, formatar_markdown
from html_generator import gerar_pagina_html


def executar_agente():
    print("=" * 65)
    print("🤖 AGENTE RESUMIDOR & CURADOR DE NOTÍCIAS DE IA")
    print("=" * 65)
    print(f"📡 Monitorando {len(DEFAULT_RSS_FEEDS)} canais RSS de tecnologia...")
    
    # 1. Coleta das notícias
    noticias = coletar_noticias(DEFAULT_RSS_FEEDS, limite_por_feed=4)
    print(f"\n📊 Total de notícias coletadas: {len(noticias)}")
    
    if not noticias:
        print("❌ Nenhuma notícia encontrada. Verifique sua conexão com a internet.")
        sys.exit(1)

    # 2. Curadoria e Síntese Inteligente (Agente IA)
    dados_curadoria = gerar_dados_curadoria(noticias)

    # 3. Salvar o arquivo Markdown na pasta de saída
    data_arquivo = datetime.now().strftime("%Y-%m-%d")
    arquivo_md = OUTPUT_DIR / f"curadoria_{data_arquivo}.md"
    relatorio_md = formatar_markdown(dados_curadoria)
    
    with open(arquivo_md, "w", encoding="utf-8") as f:
        f.write(relatorio_md)

    # 4. Gerar e salvar a página HTML rica
    arquivo_html = OUTPUT_DIR / f"curadoria_{data_arquivo}.html"
    gerar_pagina_html(dados_curadoria, arquivo_html)

    print("\n" + "=" * 65)
    print("🎉 CURADORIA CONCLUÍDA COM SUCESSO!")
    print(f"📄 Relatório Markdown: {arquivo_md}")
    print(f"🌐 Página Web Interativa: {arquivo_html}")
    print("=" * 65)

    # 5. Abrir a página HTML automaticamente no navegador padrão
    try:
        print("🚀 Abrindo a página de notícias no seu navegador...")
        webbrowser.open(arquivo_html.as_uri())
    except Exception as e:
        print(f"⚠️  Não foi possível abrir o navegador automaticamente: {e}")
    print()


if __name__ == "__main__":
    executar_agente()
