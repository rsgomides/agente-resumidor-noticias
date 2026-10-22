"""
Módulo de Coleta de Feeds RSS.
Responsável por conectar aos canais de notícias nacionais e internacionais e extrair artigos recentes.
"""

import re
import html
from typing import List, Dict, Any
import feedparser


def limpar_texto_html(texto: str) -> str:
    """Remove tags HTML e decodifica entidades para texto limpo."""
    if not texto:
        return ""
    texto_limpo = re.sub(r"<[^>]+>", "", texto)
    texto_limpo = html.unescape(texto_limpo)
    return " ".join(texto_limpo.split())


def coletar_noticias(feeds: List[Dict[str, str]], limite_por_feed: int = 4) -> List[Dict[str, Any]]:
    """
    Varre a lista de feeds RSS e retorna uma lista unificada de notícias recentes.
    """
    todas_noticias = []

    for feed_info in feeds:
        nome_fonte = feed_info.get("nome", "Desconhecido")
        url_feed = feed_info.get("url", "")
        categoria = feed_info.get("categoria", "Geral")
        regiao = feed_info.get("regiao", "Global")

        try:
            parsed = feedparser.parse(url_feed)
            
            # Verifica se houve erro fatal de rede ou parse
            if parsed.bozo and not parsed.entries:
                print(f"⚠️  [Aviso] Falha ao acessar feed '{nome_fonte}'. Pulando...")
                continue

            artigos_coletados = 0
            for entry in parsed.entries:
                if artigos_coletados >= limite_por_feed:
                    break

                titulo = entry.get("title", "Sem título").strip()
                link = entry.get("link", "").strip()
                data_pub = (
                    entry.get("published") 
                    or entry.get("pubDate") 
                    or entry.get("updated") 
                    or "Recente"
                )
                
                # Obtém o resumo/descrição
                resumo_cru = entry.get("summary") or entry.get("description") or ""
                resumo = limpar_texto_html(resumo_cru)

                if titulo and link:
                    todas_noticias.append({
                        "fonte": nome_fonte,
                        "categoria": categoria,
                        "regiao": regiao,
                        "titulo": titulo,
                        "link": link,
                        "data": data_pub,
                        "resumo_original": resumo[:400] + ("..." if len(resumo) > 400 else "")
                    })
                    artigos_coletados += 1

            flag = "🇧🇷" if regiao == "Brasil" else "🌍"
            print(f"✅ {flag} [{nome_fonte}] Coletadas {artigos_coletados} notícias.")

        except Exception as erro:
            print(f"❌ [Erro] Problema ao ler '{nome_fonte}': {erro}")

    return todas_noticias
