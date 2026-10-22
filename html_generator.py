"""
Módulo de Geração de Interface HTML Interativa.
Cria um dashboard web moderno, responsivo, com suporte a tema escuro/claro,
filtros dinâmicos por região (Brasil / Global), busca em tempo real,
síntese de áudio (TTS) e design estético de alto nível.
"""

from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List


def _renderizar_cards_destaque(destaques: List[Dict[str, Any]], regiao_padrao: str = "Brasil") -> str:
    """Renderiza a lista de cartões analíticos de notícias."""
    html_cards = ""
    for idx, d in enumerate(destaques, 1):
        titulo = d.get("titulo", "Sem título")
        fonte = d.get("fonte", "Fonte")
        regiao = d.get("regiao", regiao_padrao)
        link = d.get("link", "#")
        categoria = d.get("categoria", "Tecnologia")
        resumo = d.get("resumo_executivo", "")
        por_que = d.get("por_que_importa", "")
        pontos = d.get("pontos_chave", [])
        tempo_leitura = d.get("tempo_leitura", "3 min")
        rank_str = f"#{idx:02d}"

        flag = "🇧🇷 Brasil" if regiao == "Brasil" else "🌍 Global"
        classe_regiao = "badge-brasil" if regiao == "Brasil" else "badge-global"

        pontos_html = "".join([f"<li>{p}</li>" for p in pontos])
        resumo_voz = resumo.replace('"', '&quot;').replace("'", "\\'")

        html_cards += f"""
            <article class="news-card" data-titulo="{titulo.lower()}" data-categoria="{categoria.lower()}" data-regiao="{regiao.lower()}">
                <div class="card-top">
                    <div class="meta-badges">
                        <span class="badge-rank">{rank_str}</span>
                        <span class="badge-region {classe_regiao}">{flag}</span>
                        <a href="{link}" target="_blank" class="badge-source">{fonte}</a>
                        <span class="badge-category">{categoria}</span>
                    </div>
                    <div class="read-time">⏱️ {tempo_leitura} de leitura</div>
                </div>

                <h3 class="news-title">{titulo}</h3>
                <p class="news-summary">{resumo}</p>

                <div class="why-it-matters">
                    <div class="why-title">💡 Por que isso importa?</div>
                    <div class="why-desc">{por_que}</div>
                </div>

                <div>
                    <div class="key-points-title">Pontos de Destaque:</div>
                    <ul class="key-points-list">
                        {pontos_html}
                    </ul>
                </div>

                <div class="card-actions">
                    <div class="action-group">
                        <button class="btn-action" onclick="copiarTexto('{link}', 'Link copiado para a área de transferência!')">📋 Copiar Link</button>
                        <button class="btn-action" onclick="ouvirTexto('{resumo_voz}')">🔊 Ouvir Resumo</button>
                    </div>
                    <a href="{link}" target="_blank" class="btn-primary-action">Acessar Matéria Completa ↗</a>
                </div>
            </article>
        """
    return html_cards


MESES_PT = {
    1: "Janeiro", 2: "Fevereiro", 3: "Março", 4: "Abril",
    5: "Maio", 6: "Junho", 7: "Julho", 8: "Agosto",
    9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro"
}


def obter_data_formatada_pt() -> str:
    """Retorna a data atual formatada em português garantido."""
    hoje = datetime.now()
    mes = MESES_PT.get(hoje.month, "")
    return f"{hoje.day} de {mes} de {hoje.year}"


def gerar_pagina_html(dados: Dict[str, Any], arquivo_destino: Path) -> Path:
    """
    Gera um arquivo HTML completo com cobertura especializada do Brasil e Global.
    """
    data_formatada = dados.get("data_formatada") or obter_data_formatada_pt()
    data_iso = dados.get("data_iso", datetime.now().strftime("%Y-%m-%d"))
    introducao = dados.get("introducao", "Acompanhe os principais avanços e análises de Inteligência Artificial do dia.")
    
    destaques_br = dados.get("destaques_brasil", [])
    destaques_glob = dados.get("destaques_globais", [])
    radar_rapido = dados.get("radar_rapido", [])
    dica_estudos = dados.get("dica_estudos", "")
    
    total_monitoradas = dados.get("total_monitoradas", 35)
    total_br = dados.get("total_brasil", 20)
    total_glob = dados.get("total_global", 15)
    canais_ativos = dados.get("canais_ativos", 10)
    modelo = dados.get("modelo_utilizado", "Google Gemini")

    cards_br_html = _renderizar_cards_destaque(destaques_br, "Brasil")
    cards_glob_html = _renderizar_cards_destaque(destaques_glob, "Global")

    radar_html = ""
    for r in radar_rapido:
        r_tit = r.get("titulo", "Sem título")
        r_fonte = r.get("fonte", "Geral")
        r_regiao = r.get("regiao", "Global")
        r_link = r.get("link", "#")
        flag = "🇧🇷" if r_regiao == "Brasil" else "🌍"

        radar_html += f"""
            <a href="{r_link}" target="_blank" class="radar-card" data-titulo="{r_tit.lower()}" data-regiao="{r_regiao.lower()}">
                <div class="radar-meta">
                    <span class="radar-source">{flag} {r_fonte}</span>
                    <span style="color: var(--text-muted);">↗</span>
                </div>
                <div class="radar-title">{r_tit}</div>
                <span class="radar-arrow">Ler no {r_fonte}</span>
            </a>
        """

    html_content = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Curadoria Tech & IA — Brasil & Mundo — {data_iso}</title>
    <!-- Fontes Google Modernas -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg-body: #0A0E17;
            --bg-card: rgba(17, 24, 39, 0.75);
            --bg-card-hover: rgba(24, 33, 53, 0.85);
            --border-card: rgba(255, 255, 255, 0.08);
            --border-glow: rgba(99, 102, 241, 0.3);
            --text-primary: #F3F4F6;
            --text-secondary: #9CA3AF;
            --text-muted: #6B7280;
            --accent-primary: #6366F1;
            --accent-secondary: #8B5CF6;
            --accent-cyan: #06B6D4;
            --accent-emerald: #10B981;
            --accent-amber: #F59E0B;
            --accent-brasil: #10B981;
            --tag-bg: rgba(99, 102, 241, 0.15);
            --tag-text: #818CF8;
            --why-bg: rgba(99, 102, 241, 0.08);
            --why-border: #6366F1;
            --font-heading: 'Outfit', -apple-system, BlinkMacSystemFont, sans-serif;
            --font-body: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
            --shadow-glow: 0 10px 30px -10px rgba(99, 102, 241, 0.3);
        }}

        [data-theme="light"] {{
            --bg-body: #F8FAFC;
            --bg-card: rgba(255, 255, 255, 0.9);
            --bg-card-hover: rgba(255, 255, 255, 1);
            --border-card: rgba(226, 232, 240, 0.8);
            --border-glow: rgba(99, 102, 241, 0.25);
            --text-primary: #0F172A;
            --text-secondary: #475569;
            --text-muted: #94A3B8;
            --tag-bg: rgba(99, 102, 241, 0.1);
            --tag-text: #4F46E5;
            --why-bg: rgba(238, 242, 255, 0.8);
            --why-border: #4F46E5;
            --shadow-glow: 0 10px 25px -5px rgba(99, 102, 241, 0.15);
        }}

        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            transition: background-color 0.3s ease, border-color 0.3s ease, color 0.3s ease;
        }}

        body {{
            background-color: var(--bg-body);
            color: var(--text-primary);
            font-family: var(--font-body);
            min-height: 100vh;
            line-height: 1.6;
            background-image: 
                radial-gradient(circle at 10% 15%, rgba(16, 185, 129, 0.12) 0%, transparent 40%),
                radial-gradient(circle at 85% 60%, rgba(99, 102, 241, 0.15) 0%, transparent 40%);
            background-attachment: fixed;
            padding-bottom: 60px;
        }}

        .container {{
            max-width: 1140px;
            margin: 0 auto;
            padding: 0 24px;
        }}

        header {{
            padding: 36px 0 24px 0;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid var(--border-card);
            margin-bottom: 32px;
        }}

        .brand {{
            display: flex;
            align-items: center;
            gap: 14px;
        }}

        .brand-icon {{
            width: 50px;
            height: 50px;
            background: linear-gradient(135deg, #10B981, #6366F1);
            border-radius: 14px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 26px;
            box-shadow: 0 4px 18px rgba(16, 185, 129, 0.4);
        }}

        .brand-title {{
            font-family: var(--font-heading);
            font-size: 23px;
            font-weight: 800;
            letter-spacing: -0.02em;
        }}

        .brand-subtitle {{
            font-size: 13px;
            color: var(--text-secondary);
        }}

        .btn-theme {{
            background: var(--bg-card);
            border: 1px solid var(--border-card);
            color: var(--text-primary);
            padding: 9px 15px;
            border-radius: 10px;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 13px;
            font-weight: 600;
            backdrop-filter: blur(12px);
        }}

        .btn-theme:hover {{
            border-color: var(--accent-primary);
            color: var(--accent-primary);
        }}

        /* Hero Banner */
        .hero-banner {{
            background: linear-gradient(135deg, rgba(16, 185, 129, 0.1), rgba(99, 102, 241, 0.12));
            border: 1px solid var(--border-glow);
            border-radius: 20px;
            padding: 32px;
            margin-bottom: 36px;
            backdrop-filter: blur(16px);
        }}

        .hero-badge {{
            display: inline-flex;
            align-items: center;
            gap: 6px;
            background: rgba(16, 185, 129, 0.15);
            color: #34D399;
            padding: 6px 14px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 16px;
        }}

        .hero-title {{
            font-family: var(--font-heading);
            font-size: 32px;
            font-weight: 800;
            line-height: 1.25;
            margin-bottom: 14px;
            background: linear-gradient(135deg, var(--text-primary) 30%, #34D399);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}

        .hero-desc {{
            font-size: 16px;
            color: var(--text-secondary);
            max-width: 900px;
            margin-bottom: 24px;
            line-height: 1.6;
        }}

        /* Stats Grid */
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(170px, 1fr));
            gap: 14px;
        }}

        .stat-card {{
            background: var(--bg-card);
            border: 1px solid var(--border-card);
            border-radius: 12px;
            padding: 14px 18px;
            display: flex;
            align-items: center;
            gap: 14px;
        }}

        .stat-val {{
            font-family: var(--font-heading);
            font-size: 20px;
            font-weight: 800;
        }}

        .stat-label {{
            font-size: 11px;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.04em;
        }}

        /* Controles: Busca e Filtros */
        .controls-bar {{
            display: flex;
            flex-wrap: wrap;
            justify-content: space-between;
            align-items: center;
            gap: 16px;
            margin-bottom: 32px;
        }}

        .search-box {{
            flex: 1;
            min-width: 280px;
            position: relative;
        }}

        .search-box input {{
            width: 100%;
            background: var(--bg-card);
            border: 1px solid var(--border-card);
            border-radius: 12px;
            padding: 12px 16px 12px 42px;
            color: var(--text-primary);
            font-family: var(--font-body);
            font-size: 14px;
            outline: none;
        }}

        .search-box input:focus {{
            border-color: var(--accent-primary);
            box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.2);
        }}

        .search-icon {{
            position: absolute;
            left: 14px;
            top: 50%;
            transform: translateY(-50%);
            color: var(--text-muted);
        }}

        .filter-pills {{
            display: flex;
            gap: 8px;
            overflow-x: auto;
            padding-bottom: 4px;
        }}

        .pill {{
            background: var(--bg-card);
            border: 1px solid var(--border-card);
            color: var(--text-secondary);
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 13px;
            font-weight: 600;
            cursor: pointer;
            white-space: nowrap;
        }}

        .pill:hover, .pill.active {{
            background: var(--accent-primary);
            color: #FFFFFF;
            border-color: var(--accent-primary);
        }}

        .pill-br.active {{
            background: #059669;
            border-color: #059669;
        }}

        /* Seções de Notícias */
        .scope-header {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin: 36px 0 20px 0;
            padding-bottom: 12px;
            border-bottom: 1px solid var(--border-card);
        }}

        .scope-title {{
            font-family: var(--font-heading);
            font-size: 24px;
            font-weight: 800;
            display: flex;
            align-items: center;
            gap: 10px;
        }}

        .news-grid {{
            display: flex;
            flex-direction: column;
            gap: 28px;
            margin-bottom: 40px;
        }}

        .news-card {{
            background: var(--bg-card);
            border: 1px solid var(--border-card);
            border-radius: 18px;
            padding: 28px;
            backdrop-filter: blur(14px);
            transition: all 0.25s ease;
        }}

        .news-card:hover {{
            background: var(--bg-card-hover);
            border-color: var(--border-glow);
            transform: translateY(-3px);
            box-shadow: var(--shadow-glow);
        }}

        .card-top {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 10px;
            margin-bottom: 16px;
        }}

        .meta-badges {{
            display: flex;
            align-items: center;
            flex-wrap: wrap;
            gap: 8px;
        }}

        .badge-rank {{
            background: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary));
            color: #FFF;
            padding: 4px 10px;
            border-radius: 8px;
            font-size: 11px;
            font-weight: 800;
        }}

        .badge-region {{
            padding: 4px 10px;
            border-radius: 8px;
            font-size: 11px;
            font-weight: 700;
            text-transform: uppercase;
        }}

        .badge-brasil {{
            background: rgba(16, 185, 129, 0.15);
            color: #34D399;
            border: 1px solid rgba(16, 185, 129, 0.3);
        }}

        .badge-global {{
            background: rgba(99, 102, 241, 0.15);
            color: #818CF8;
            border: 1px solid rgba(99, 102, 241, 0.3);
        }}

        .badge-source {{
            background: var(--tag-bg);
            color: var(--tag-text);
            padding: 4px 12px;
            border-radius: 8px;
            font-size: 12px;
            font-weight: 600;
            text-decoration: none;
        }}

        .badge-category {{
            background: rgba(255, 255, 255, 0.05);
            color: var(--text-muted);
            padding: 4px 10px;
            border-radius: 8px;
            font-size: 11px;
            font-weight: 500;
        }}

        .read-time {{
            font-size: 12px;
            color: var(--text-muted);
            display: flex;
            align-items: center;
            gap: 4px;
        }}

        .news-title {{
            font-family: var(--font-heading);
            font-size: 22px;
            font-weight: 700;
            line-height: 1.35;
            margin-bottom: 14px;
        }}

        .news-summary {{
            font-size: 15px;
            color: var(--text-secondary);
            margin-bottom: 20px;
            line-height: 1.6;
        }}

        .why-it-matters {{
            background: var(--why-bg);
            border-left: 4px solid var(--why-border);
            border-radius: 0 12px 12px 0;
            padding: 16px 20px;
            margin-bottom: 20px;
        }}

        .why-title {{
            font-size: 13px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: var(--accent-primary);
            margin-bottom: 6px;
        }}

        .why-desc {{
            font-size: 14px;
            color: var(--text-primary);
            line-height: 1.55;
        }}

        .key-points-title {{
            font-size: 13px;
            font-weight: 600;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.04em;
            margin-bottom: 10px;
        }}

        .key-points-list {{
            list-style: none;
            display: flex;
            flex-direction: column;
            gap: 8px;
            margin-bottom: 22px;
        }}

        .key-points-list li {{
            font-size: 14px;
            color: var(--text-secondary);
            display: flex;
            align-items: flex-start;
            gap: 10px;
        }}

        .key-points-list li::before {{
            content: "✓";
            color: var(--accent-emerald);
            font-weight: 800;
        }}

        .card-actions {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            flex-wrap: wrap;
            gap: 12px;
            padding-top: 16px;
            border-top: 1px solid var(--border-card);
        }}

        .action-group {{
            display: flex;
            align-items: center;
            gap: 10px;
        }}

        .btn-action {{
            background: transparent;
            border: 1px solid var(--border-card);
            color: var(--text-secondary);
            padding: 8px 14px;
            border-radius: 8px;
            font-size: 12px;
            font-weight: 600;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 6px;
        }}

        .btn-action:hover {{
            background: var(--bg-card);
            color: var(--text-primary);
            border-color: var(--text-secondary);
        }}

        .btn-primary-action {{
            background: var(--accent-primary);
            border: 1px solid var(--accent-primary);
            color: #FFFFFF;
            padding: 8px 16px;
            border-radius: 8px;
            font-size: 13px;
            font-weight: 600;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 6px;
            text-decoration: none;
        }}

        .btn-primary-action:hover {{
            background: var(--accent-secondary);
        }}

        /* Radar Rápido */
        .radar-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
            gap: 16px;
            margin-bottom: 48px;
        }}

        .radar-card {{
            background: var(--bg-card);
            border: 1px solid var(--border-card);
            border-radius: 14px;
            padding: 18px 20px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            gap: 12px;
            text-decoration: none;
            color: inherit;
        }}

        .radar-card:hover {{
            border-color: var(--accent-cyan);
            transform: translateY(-2px);
        }}

        .radar-meta {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 11px;
        }}

        .radar-source {{
            color: var(--accent-cyan);
            font-weight: 700;
            text-transform: uppercase;
        }}

        .radar-title {{
            font-size: 14px;
            font-weight: 600;
            color: var(--text-primary);
            line-height: 1.4;
        }}

        .radar-arrow {{
            align-self: flex-end;
            color: var(--text-muted);
            font-size: 12px;
        }}

        /* Dica de Estudos */
        .study-box {{
            background: linear-gradient(135deg, rgba(245, 158, 11, 0.12), rgba(16, 185, 129, 0.08));
            border: 1px solid rgba(245, 158, 11, 0.3);
            border-radius: 18px;
            padding: 28px;
            margin-bottom: 40px;
        }}

        .study-header {{
            display: flex;
            align-items: center;
            gap: 10px;
            font-family: var(--font-heading);
            font-size: 18px;
            font-weight: 700;
            color: var(--accent-amber);
            margin-bottom: 12px;
        }}

        .study-content {{
            font-size: 15px;
            color: var(--text-primary);
            line-height: 1.6;
        }}

        footer {{
            text-align: center;
            padding-top: 32px;
            border-top: 1px solid var(--border-card);
            color: var(--text-muted);
            font-size: 13px;
        }}

        .toast {{
            position: fixed;
            bottom: 24px;
            right: 24px;
            background: var(--accent-emerald);
            color: #FFFFFF;
            padding: 12px 20px;
            border-radius: 10px;
            font-size: 13px;
            font-weight: 600;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
            transform: translateY(100px);
            opacity: 0;
            transition: all 0.3s ease;
            z-index: 999;
        }}

        .toast.show {{
            transform: translateY(0);
            opacity: 1;
        }}

        @media (max-width: 768px) {{
            .hero-title {{ font-size: 26px; }}
            .news-card {{ padding: 20px; }}
            .controls-bar {{ flex-direction: column; align-items: stretch; }}
        }}
    </style>
</head>
<body data-theme="dark">

<div class="container">
    <header>
        <div class="brand">
            <div class="brand-icon">🇧🇷</div>
            <div>
                <div class="brand-title">IA & Tech Curator</div>
                <div class="brand-subtitle">Curadoria Inteligente: Brasil & Fronteira Global</div>
            </div>
        </div>
        <div>
            <button class="btn-theme" id="themeToggle" onclick="alternarTema()">
                <span id="themeIcon">☀️</span> Modo Claro
            </button>
        </div>
    </header>

    <!-- Hero / Visão Geral -->
    <section class="hero-banner">
        <div class="hero-badge">⚡ Síntese Estratégica • {data_formatada}</div>
        <h1 class="hero-title">Inteligência de Mercado & Tecnologia</h1>
        <p class="hero-desc">{introducao}</p>
        
        <div class="stats-grid">
            <div class="stat-card">
                <div style="font-size: 24px;">📊</div>
                <div>
                    <div class="stat-val">{total_monitoradas}</div>
                    <div class="stat-label">Artigos Analisados</div>
                </div>
            </div>
            <div class="stat-card">
                <div style="font-size: 24px;">🇧🇷</div>
                <div>
                    <div class="stat-val">{total_br}</div>
                    <div class="stat-label">Notícias Nacionais</div>
                </div>
            </div>
            <div class="stat-card">
                <div style="font-size: 24px;">🌍</div>
                <div>
                    <div class="stat-val">{total_glob}</div>
                    <div class="stat-label">Notícias Globais</div>
                </div>
            </div>
            <div class="stat-card">
                <div style="font-size: 24px;">📰</div>
                <div>
                    <div class="stat-val">{canais_ativos}</div>
                    <div class="stat-label">Veículos Conceituados</div>
                </div>
            </div>
            <div class="stat-card">
                <div style="font-size: 24px;">🤖</div>
                <div>
                    <div class="stat-val" style="font-size: 14px;">{modelo}</div>
                    <div class="stat-label">Motor de IA</div>
                </div>
            </div>
        </div>
    </section>

    <!-- Controles: Busca e Filtros -->
    <div class="controls-bar">
        <div class="search-box">
            <span class="search-icon">🔍</span>
            <input type="text" id="searchInput" placeholder="Filtrar matérias por palavra-chave (ex: startup, dev, agentes, google)..." oninput="filtrarNoticias()">
        </div>
        <div class="filter-pills" id="filterPills">
            <button class="pill active" onclick="filtrarRegiao('todas', this)">🌟 Todos os Destaques</button>
            <button class="pill pill-br" onclick="filtrarRegiao('brasil', this)">🇧🇷 Somente Brasil</button>
            <button class="pill" onclick="filtrarRegiao('global', this)">🌍 Somente Global</button>
            <button class="pill" onclick="filtrarCategoria('programação', this)">💻 Programação & Dev</button>
            <button class="pill" onclick="filtrarCategoria('startup', this)">🚀 Startups & Negócios</button>
        </div>
    </div>

    <!-- Destaques Nacionais (Brasil) -->
    <section id="sectionBrasil">
        <div class="scope-header">
            <h2 class="scope-title"><span>🇧🇷</span> Destaques Nacionais (Brasil Tech, Dev & Startups)</h2>
            <span style="font-size: 13px; color: var(--accent-emerald); font-weight: 700;">{len(destaques_br)} Destaques</span>
        </div>
        <div class="news-grid">
            {cards_br_html}
        </div>
    </section>

    <!-- Destaques Globais (Internacional) -->
    <section id="sectionGlobal">
        <div class="scope-header">
            <h2 class="scope-title"><span>🌍</span> Destaques Globais (Fronteira de IA & Big Techs)</h2>
            <span style="font-size: 13px; color: var(--accent-primary); font-weight: 700;">{len(destaques_glob)} Destaques</span>
        </div>
        <div class="news-grid">
            {cards_glob_html}
        </div>
    </section>

    <!-- Radar Rápido -->
    <section>
        <div class="scope-header">
            <h2 class="scope-title"><span>⚡</span> Radar Rápido (Brasil & Mundo)</h2>
            <span style="font-size: 13px; color: var(--text-muted);">{len(radar_rapido)} notícias</span>
        </div>
        <div class="radar-grid" id="radarGrid">
            {radar_html}
        </div>
    </section>

    <!-- Dica de Estudos -->
    <section class="study-box">
        <div class="study-header">
            <span>💡</span> Dica Estratégica para sua Carreira & Estudos
        </div>
        <div class="study-content">
            {dica_estudos}
        </div>
    </section>

    <footer>
        <p>Curadoria executada pelo <strong>Agente Autônomo de Notícias DIO</strong>.</p>
        <p style="margin-top: 6px; font-size: 11px;">Fontes Nacionais: Tecnoblog • TabNews • MIT Tech Review BR • Startupi • TI Inside • Canaltech</p>
        <p style="margin-top: 2px; font-size: 11px;">Fontes Globais: TechCrunch • Wired • MIT Tech Review • The Verge</p>
    </footer>
</div>

<div class="toast" id="toast">Notificação</div>

<script>
    function alternarTema() {{
        const body = document.body;
        const currentTheme = body.getAttribute('data-theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        body.setAttribute('data-theme', newTheme);
        
        const btn = document.getElementById('themeToggle');
        if (newTheme === 'light') {{
            btn.innerHTML = '<span>🌙</span> Modo Escuro';
        }} else {{
            btn.innerHTML = '<span>☀️</span> Modo Claro';
        }}
    }}

    function filtrarNoticias() {{
        const termo = document.getElementById('searchInput').value.toLowerCase();
        const cards = document.querySelectorAll('.news-card');
        const radarCards = document.querySelectorAll('.radar-card');

        cards.forEach(card => {{
            const tit = card.getAttribute('data-titulo') || '';
            const cat = card.getAttribute('data-categoria') || '';
            const reg = card.getAttribute('data-regiao') || '';
            if (tit.includes(termo) || cat.includes(termo) || reg.includes(termo)) {{
                card.style.display = 'block';
            }} else {{
                card.style.display = 'none';
            }}
        }});

        radarCards.forEach(card => {{
            const tit = card.getAttribute('data-titulo') || '';
            if (tit.includes(termo)) {{
                card.style.display = 'flex';
            }} else {{
                card.style.display = 'none';
            }}
        }});
    }}

    function filtrarRegiao(regiao, elemento) {{
        document.querySelectorAll('.pill').forEach(p => p.classList.remove('active'));
        elemento.classList.add('active');

        const secBrasil = document.getElementById('sectionBrasil');
        const secGlobal = document.getElementById('sectionGlobal');
        const radarCards = document.querySelectorAll('.radar-card');

        if (regiao === 'todas') {{
            secBrasil.style.display = 'block';
            secGlobal.style.display = 'block';
            radarCards.forEach(c => c.style.display = 'flex');
        }} else if (regiao === 'brasil') {{
            secBrasil.style.display = 'block';
            secGlobal.style.display = 'none';
            radarCards.forEach(c => {{
                c.style.display = (c.getAttribute('data-regiao') === 'brasil') ? 'flex' : 'none';
            }});
        }} else if (regiao === 'global') {{
            secBrasil.style.display = 'none';
            secGlobal.style.display = 'block';
            radarCards.forEach(c => {{
                c.style.display = (c.getAttribute('data-regiao') === 'global') ? 'flex' : 'none';
            }});
        }}
    }}

    function filtrarCategoria(categoria, elemento) {{
        document.querySelectorAll('.pill').forEach(p => p.classList.remove('active'));
        elemento.classList.add('active');

        document.getElementById('sectionBrasil').style.display = 'block';
        document.getElementById('sectionGlobal').style.display = 'block';

        const cards = document.querySelectorAll('.news-card');
        cards.forEach(card => {{
            const cat = (card.getAttribute('data-categoria') || '').toLowerCase();
            const tit = (card.getAttribute('data-titulo') || '').toLowerCase();
            if (cat.includes(categoria) || tit.includes(categoria)) {{
                card.style.display = 'block';
            }} else {{
                card.style.display = 'none';
            }}
        }});
    }}

    function copiarTexto(texto, mensagem) {{
        navigator.clipboard.writeText(texto).then(() => {{
            mostrarToast(mensagem);
        }}).catch(() => {{
            mostrarToast('Erro ao copiar.');
        }});
    }}

    let synthUtterance = null;
    function ouvirTexto(texto) {{
        if (!('speechSynthesis' in window)) {{
            mostrarToast('Seu navegador não suporta leitura de voz nativa.');
            return;
        }}

        if (window.speechSynthesis.speaking) {{
            window.speechSynthesis.cancel();
            mostrarToast('Leitura pausada.');
            return;
        }}

        synthUtterance = new SpeechSynthesisUtterance(texto);
        synthUtterance.lang = 'pt-BR';
        synthUtterance.rate = 1.05;
        synthUtterance.onstart = () => mostrarToast('Reproduzindo resumo em áudio...');
        synthUtterance.onend = () => mostrarToast('Fim da leitura.');
        window.speechSynthesis.speak(synthUtterance);
    }}

    function mostrarToast(msg) {{
        const toast = document.getElementById('toast');
        toast.innerText = msg;
        toast.classList.add('show');
        setTimeout(() => toast.classList.remove('show'), 3000);
    }}
</script>
</body>
</html>
"""

    with open(arquivo_destino, "w", encoding="utf-8") as f:
        f.write(html_content)

    return arquivo_destino
