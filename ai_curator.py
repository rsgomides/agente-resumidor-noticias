"""
Módulo do Agente Curador de IA.
Responsável por analisar os artigos coletados (nacionais e globais),
classificar os mais relevantes em cada âmbito e gerar dados estruturados.
"""

import json
from datetime import datetime
from typing import List, Dict, Any
import requests
from config import GEMINI_API_KEY, GEMINI_MODEL, LANGUAGE

MESES_PT = {
    1: "Janeiro", 2: "Fevereiro", 3: "Março", 4: "Abril",
    5: "Maio", 6: "Junho", 7: "Julho", 8: "Agosto",
    9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro"
}


def _curadoria_com_gemini(noticias: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Envia notícias nacionais e globais para a API do Google Gemini com saída JSON estruturada.
    """
    modelos_tentar = [GEMINI_MODEL, "gemini-3.5-flash-lite", "gemini-3.5-flash", "gemini-3.1-flash-lite"]
    modelos_ordenados = []
    for m in modelos_tentar:
        if m and m not in modelos_ordenados:
            modelos_ordenados.append(m)

    # Separa blocos de notícias para o prompt
    bloco_brasil = ""
    bloco_global = ""

    for idx, n in enumerate(noticias, 1):
        bloco = (
            f"[{idx}] Título: {n['titulo']}\n"
            f"    Fonte: {n['fonte']} ({n['categoria']})\n"
            f"    Link: {n['link']}\n"
            f"    Resumo bruto: {n['resumo_original']}\n\n"
        )
        if n.get("regiao") == "Brasil":
            bloco_brasil += bloco
        else:
            bloco_global += bloco

    hoje = datetime.now()
    hoje_str = hoje.strftime("%d/%m/%Y")
    data_formatada = f"{hoje.day} de {MESES_PT[hoje.month]} de {hoje.year}"
    data_iso = hoje.strftime("%Y-%m-%d")

    prompt = f"""
Você é um Agente Autônomo Especialista em Curadoria e Inteligência de Tecnologia, Programação e Negócios.
Data da análise: {hoje_str}. Idioma de saída: {LANGUAGE}.

Receba abaixo as notícias coletadas via RSS, separadas em Brasil e Global:

===================
🇧🇷 NOTÍCIAS DO BRASIL (Startups, Programação, Negócios Tech, Mercado Nacional):
===================
{bloco_brasil}

===================
🌍 NOTÍCIAS GLOBAIS (Fronteira de IA, Modelos, Big Techs, Pesquisa):
===================
{bloco_global}

Sua missão de curadoria:
1. Analise o cenário brasileiro e selecione as 3 notícias mais impactantes para desenvolvedores, startups e profissionais de tecnologia no Brasil.
2. Analise o cenário internacional e selecione as 3 notícias mais relevantes sobre IA e inovação global.
3. Selecione 6 outras notícias secundárias relevantes (misturando Brasil e Global) para o Radar Rápido.
4. Retorne OBRIGATORIAMENTE um objeto JSON estrito com o seguinte esquema:

{{
  "introducao": "Uma síntese executiva motivacional de 2 a 3 frases em português integrando o panorama de tecnologia no Brasil e no mundo.",
  "destaques_brasil": [
    {{
      "titulo": "Título claro e informativo em português",
      "fonte": "Nome da fonte (ex: Tecnoblog, TabNews, Startupi, MIT Tech Review Brasil)",
      "regiao": "Brasil",
      "categoria": "Programação & Dev | Startups & Negócios | IA Corporativa | etc.",
      "link": "URL original da notícia (ATENÇÃO: copie exatamente o link fornecido sem alterar nem encurtar)",
      "tempo_leitura": "3 min",
      "resumo_executivo": "O que aconteceu em 2 ou 3 frases claras e objetivas.",
      "por_que_importa": "Análise crítica do impacto para o mercado, startups e desenvolvedores brasileiros.",
      "pontos_chave": [
        "Fato concreto 1",
        "Fato concreto 2",
        "Fato concreto 3"
      ]
    }}
  ],
  "destaques_globais": [
    {{
      "titulo": "Título traduzido/adaptado para português, claro e informativo",
      "fonte": "Nome da fonte internacional (ex: TechCrunch AI, Wired AI)",
      "regiao": "Global",
      "categoria": "Modelos de IA | Fronteira Tecnológica | Pesquisa",
      "link": "URL original exato",
      "tempo_leitura": "3 min",
      "resumo_executivo": "O que aconteceu em 2 ou 3 frases claras e objetivas.",
      "por_que_importa": "Impacto na tecnologia global e tendências que chegarão ao mercado.",
      "pontos_chave": [
        "Fato concreto 1",
        "Fato concreto 2",
        "Fato concreto 3"
      ]
    }}
  ],
  "radar_rapido": [
    {{
      "titulo": "Título resumido em português",
      "fonte": "Nome da fonte",
      "regiao": "Brasil ou Global",
      "link": "URL original exato",
      "categoria": "Geral"
    }}
  ],
  "dica_estudos": "Uma recomendação prática e acionável de estudo ou teste técnico voltada para carreira tech e agentes de IA."
}}
"""

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ],
        "generationConfig": {
            "responseMimeType": "application/json",
            "temperature": 0.3,
            "maxOutputTokens": 3000,
        }
    }

    ultimo_erro = None
    for modelo in modelos_ordenados:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{modelo}:generateContent?key={GEMINI_API_KEY}"
        try:
            response = requests.post(url, json=payload, headers={"Content-Type": "application/json"}, timeout=50)
            if response.status_code == 200:
                data = response.json()
                raw_json = data["candidates"][0]["content"]["parts"][0]["text"]
                dados_ia = json.loads(raw_json)
                
                print(f"✨ [Gemini] Curadoria completa (Brasil + Global) gerada com sucesso usando '{modelo}'!")
                
                # Metadados operacionais
                dados_ia["data_formatada"] = data_formatada
                dados_ia["data_iso"] = data_iso
                dados_ia["total_monitoradas"] = len(noticias)
                dados_ia["total_brasil"] = sum(1 for n in noticias if n.get("regiao") == "Brasil")
                dados_ia["total_global"] = sum(1 for n in noticias if n.get("regiao") == "Global")
                dados_ia["canais_ativos"] = len(set(n["fonte"] for n in noticias))
                dados_ia["modelo_utilizado"] = f"Google Gemini ({modelo})"
                return dados_ia
            else:
                ultimo_erro = f"HTTP {response.status_code}: {response.text[:120]}"
        except Exception as e:
            ultimo_erro = str(e)

    print(f"⚠️  [Falha na API Gemini]: {ultimo_erro}. Recorrendo ao modo de curadoria local...")
    return _curadoria_local(noticias)


def _curadoria_local(noticias: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Curadoria heurística local quando a API não estiver disponível.
    """
    hoje = datetime.now()
    data_formatada = f"{hoje.day} de {MESES_PT.get(hoje.month, '')} de {hoje.year}"
    data_iso = hoje.strftime("%Y-%m-%d")

    noticias_br = [n for n in noticias if n.get("regiao") == "Brasil"]
    noticias_glob = [n for n in noticias if n.get("regiao") != "Brasil"]

    def extrair_destaques(lista: List[Dict[str, Any]], regiao_padrao: str, qtd: int = 3):
        res = []
        for item in lista[:qtd]:
            res.append({
                "titulo": item["titulo"],
                "fonte": item["fonte"],
                "regiao": regiao_padrao,
                "link": item["link"],
                "categoria": item["categoria"],
                "tempo_leitura": "3 min",
                "resumo_executivo": item["resumo_original"] or "Acesse o artigo completo na fonte original para mais detalhes.",
                "por_que_importa": f"Notícia com impacto direto no ecossistema de tecnologia ({regiao_padrao}).",
                "pontos_chave": [
                    f"Publicado originalmente por {item['fonte']}",
                    f"Data da notícia: {item['data']}",
                    "Selecionada pela relevância em tecnologia e negócios"
                ]
            })
        return res

    destaques_br = extrair_destaques(noticias_br, "Brasil", 3)
    destaques_glob = extrair_destaques(noticias_glob, "Global", 3)

    radar_rapido = []
    for item in (noticias_br[3:6] + noticias_glob[3:6]):
        radar_rapido.append({
            "titulo": item["titulo"],
            "fonte": item["fonte"],
            "regiao": item.get("regiao", "Global"),
            "link": item["link"],
            "categoria": item["categoria"]
        })

    return {
        "data_formatada": data_formatada,
        "data_iso": data_iso,
        "introducao": "Curadoria diária unificada de notícias de tecnologia, negócios e programação com cobertura especializada do mercado brasileiro e global.",
        "destaques_brasil": destaques_br,
        "destaques_globais": destaques_glob,
        "radar_rapido": radar_rapido,
        "dica_estudos": "Acompanhe comunidades como TabNews e portais como Tecnoblog e Startupi para entender como a inovação global se traduz em oportunidades de contratação e projetos no Brasil.",
        "total_monitoradas": len(noticias),
        "total_brasil": len(noticias_br),
        "total_global": len(noticias_glob),
        "canais_ativos": len(set(n["fonte"] for n in noticias)),
        "modelo_utilizado": "Heurística Local (Modo Demonstração)"
    }


def gerar_dados_curadoria(noticias: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Ponto de entrada para obter os dados estruturados da curadoria.
    """
    if not noticias:
        return _curadoria_local([])

    if GEMINI_API_KEY:
        print("🤖 [Agente IA] Analisando notícias nacionais e globais com Google Gemini...")
        return _curadoria_com_gemini(noticias)
    else:
        print("💡 [Agente Local] Chave GEMINI_API_KEY não informada. Executando em Modo Demonstração...")
        return _curadoria_local(noticias)


def formatar_markdown(dados: Dict[str, Any]) -> str:
    """
    Converte os dados estruturados em documento Markdown abrangente com seções de Brasil e Global.
    """
    data_iso = dados.get("data_iso", "")
    introducao = dados.get("introducao", "")
    destaques_br = dados.get("destaques_brasil", [])
    destaques_glob = dados.get("destaques_globais", [])
    radar = dados.get("radar_rapido", [])
    dica = dados.get("dica_estudos", "")

    linhas = [
        f"# 📰 Curadoria Diária de Tecnologia & IA — {data_iso}",
        "",
        introducao,
        "",
        "---",
        "",
        "## 🇧🇷 Destaques Nacionais (Brasil — Startups, Dev & Negócios)",
        ""
    ]

    for d in destaques_br:
        linhas.append(f"### 🔹 [{d.get('titulo', 'Sem título')}]")
        linhas.append(f"- **Fonte:** [{d.get('fonte', 'Fonte')}]({d.get('link', '#')}) | Categoria: `{d.get('categoria', 'Brasil')}`")
        linhas.append(f"- **Resumo Executivo:** {d.get('resumo_executivo', '')}")
        linhas.append(f"- **Por que isso importa?**: {d.get('por_que_importa', '')}")
        linhas.append("- **Pontos-Chave:**")
        for p in d.get("pontos_chave", []):
            linhas.append(f"  - {p}")
        linhas.append("")

    linhas.append("---")
    linhas.append("")
    linhas.append("## 🌍 Destaques Globais (Internacional — Modelos, IA & Big Techs)")
    linhas.append("")

    for d in destaques_glob:
        linhas.append(f"### 🔹 [{d.get('titulo', 'Sem título')}]")
        linhas.append(f"- **Fonte:** [{d.get('fonte', 'Fonte')}]({d.get('link', '#')}) | Categoria: `{d.get('categoria', 'Global')}`")
        linhas.append(f"- **Resumo Executivo:** {d.get('resumo_executivo', '')}")
        linhas.append(f"- **Por que isso importa?**: {d.get('por_que_importa', '')}")
        linhas.append("- **Pontos-Chave:**")
        for p in d.get("pontos_chave", []):
            linhas.append(f"  - {p}")
        linhas.append("")

    if radar:
        linhas.append("---")
        linhas.append("")
        linhas.append("### ⚡ Radar Rápido (Brasil & Mundo)")
        for r in radar:
            flag = "🇧🇷" if r.get("regiao") == "Brasil" else "🌍"
            linhas.append(f"- {flag} [{r.get('fonte', 'Fonte')}] {r.get('titulo', '')} - [Link]({r.get('link', '#')})")
        linhas.append("")

    if dica:
        linhas.append("---")
        linhas.append("")
        linhas.append("### 💡 Dica de Ação para seus Estudos & Carreira")
        linhas.append(dica)
        linhas.append("")

    return "\n".join(linhas)
