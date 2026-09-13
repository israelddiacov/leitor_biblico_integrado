"""
Gerador de Linha do Tempo Comparativa Interativa (Python + SQLite + vis-timeline)
Eixos: História Secular, Cronologia Bíblica, Mitologias e Manuscritos/Concílios
Interface compacta com menus drop down, rótulos encolhidos e calibração de zoom.
"""

import sqlite3
import json
import os
import sys
import re

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

DB_PATH = "timeline.db"
OUTPUT_HTML = "timeline_confronto.html"

def formatar_ano_iso(ano, mes=1, dia=1):
    mes = mes if mes and 1 <= mes <= 12 else 1
    dia = dia if dia and 1 <= dia <= 31 else 1
    if ano < 0:
        return f"-{abs(ano):06d}-{mes:02d}-{dia:02d}"
    else:
        return f"{ano:04d}-{mes:02d}-{dia:02d}"

def ano_para_legivel(ano):
    if ano < 0:
        return f"{abs(ano)} a.C."
    elif ano == 0:
        return "1 a.C."
    else:
        return f"{ano} d.C."

def carregar_dados_sqlite():
    if not os.path.exists(DB_PATH):
        raise FileNotFoundError(f"Banco de dados '{DB_PATH}' não encontrado. Execute seed_database.py primeiro.")

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # 1. Carregar Eixos (Card elegante com título, subtítulo e ícone sem repetição)
    cursor.execute("SELECT * FROM eixos ORDER BY ordem_exibicao ASC")
    eixos_raw = cursor.fetchall()
    
    meta_eixos = {
        'SECULAR': {
            'titulo': 'História Secular',
            'subtitulo': 'Impérios & Civilizações',
            'icone': '🏛️',
            'cor': '#0284c7'
        },
        'BIBLICO': {
            'titulo': 'Cronologia Bíblica',
            'subtitulo': 'Patriarcas, Reis & Profetas',
            'icone': '📜',
            'cor': '#d97706'
        },
        'MITOLOGIA': {
            'titulo': 'Mitologias Antigas',
            'subtitulo': 'Cosmogonias & Poemas',
            'icone': '🏺',
            'cor': '#7c3aed'
        },
        'CANON': {
            'titulo': 'Cânon & Concílios',
            'subtitulo': 'Manuscritos & Sínodos',
            'icone': '⛪',
            'cor': '#059669'
        }
    }

    grupos = []
    for e in eixos_raw:
        cod = e['codigo']
        meta = meta_eixos.get(cod, {
            'titulo': re.sub(r'^[^\w\s]+', '', e['nome']).strip(),
            'subtitulo': '',
            'icone': e['icone'] or '📌',
            'cor': e['cor_hex'] or '#38bdf8'
        })
        
        titulo = meta['titulo']
        subtitulo = meta['subtitulo']
        cor = meta['cor']

        content_html = (
            f"<div class='eixo-card' style='--eixo-cor: {cor};' title='{titulo} — {subtitulo}'>"
            f"  <div class='eixo-bar' style='background: {cor};'></div>"
            f"  <div class='eixo-textos'>"
            f"    <div class='eixo-titulo'>{titulo}</div>"
            f"    <div class='eixo-subtitulo'>{subtitulo}</div>"
            f"  </div>"
            f"</div>"
        )

        grupos.append({
            "id": e["id"],
            "codigo": cod,
            "content": content_html,
            "order": e["ordem_exibicao"],
            "cor": cor
        })

    # 2. Carregar Concílios
    cursor.execute("""
        SELECT c.*, e.titulo as evento_titulo
        FROM concilios c
        LEFT JOIN eventos e ON c.evento_id = e.id
    """)
    concilios_map = {}
    for c in cursor.fetchall():
        concilios_map[c["id"]] = dict(c)
        if c["evento_id"]:
            concilios_map[f"ev_{c['evento_id']}"] = dict(c)

    # 3. Carregar Livros e Status Canônicos
    cursor.execute("""
        SELECT l.*,
            MAX(CASE WHEN s.tradicao = 'JUDAICA' THEN s.status END) as status_judaica,
            MAX(CASE WHEN s.tradicao = 'JUDAICA' THEN s.motivo_justificativa END) as motivo_judaica,
            MAX(CASE WHEN s.tradicao = 'PROTESTANTE' THEN s.status END) as status_protestante,
            MAX(CASE WHEN s.tradicao = 'PROTESTANTE' THEN s.motivo_justificativa END) as motivo_protestante,
            MAX(CASE WHEN s.tradicao = 'CATOLICA' THEN s.status END) as status_catolica,
            MAX(CASE WHEN s.tradicao = 'CATOLICA' THEN s.motivo_justificativa END) as motivo_catolica,
            MAX(CASE WHEN s.tradicao = 'ORTODOXA' THEN s.status END) as status_ortodoxa,
            MAX(CASE WHEN s.tradicao = 'ORTODOXA' THEN s.motivo_justificativa END) as motivo_ortodoxa
        FROM livros l
        LEFT JOIN status_canonico s ON l.id = s.livro_id
        GROUP BY l.id
    """)
    livros_rows = cursor.fetchall()
    livros_list = [dict(row) for row in livros_rows]

    # 4. Carregar Eventos e Personagens
    cursor.execute("""
        SELECT e.*, x.codigo as eixo_codigo, x.cor_hex as eixo_cor
        FROM eventos e
        JOIN eixos x ON e.eixo_id = x.id
        ORDER BY e.ano_inicio ASC
    """)
    eventos_rows = cursor.fetchall()

    itens = []
    for ev in eventos_rows:
        eixo_cod = ev["eixo_codigo"]
        tipo_vis = "box" if ev["tipo_tempo"] == "box" or ev["ano_fim"] is None else "range"
        
        cat = ev["categoria"]
        class_name = f"item-{eixo_cod.lower()} cat-{cat}"
        
        # Remove qualquer emoji prefixado no título original para evitar duplicatas
        titulo_puro = re.sub(r'^[^\w\s\(\)]+', '', ev['titulo']).strip()
        
        icone_prefixo = ""
        if cat == "antediluviano": icone_prefixo = "🌱 "
        elif cat == "patriarca": icone_prefixo = "⛺ "
        elif cat == "juiz": icone_prefixo = "⚖️ "
        elif cat in ("rei_israel", "rei_juda"): icone_prefixo = "👑 "
        elif cat == "profeta": icone_prefixo = "🔥 "
        elif cat == "concilio": icone_prefixo = "⛪ "
        elif cat == "mito": icone_prefixo = "🏺 "
        elif cat == "imperio": icone_prefixo = "🏛️ "

        concilio_info = concilios_map.get(f"ev_{ev['id']}")

        item_dict = {
            "id": f"ev_{ev['id']}",
            "group": ev["eixo_id"],
            "content": f"<span class='item-titulo'>{icone_prefixo}{titulo_puro}</span>",
            "start": formatar_ano_iso(ev["ano_inicio"], ev["mes_inicio"], ev["dia_inicio"]),
            "type": tipo_vis,
            "className": class_name,
            "meta": {
                "tipo_item": "evento",
                "titulo": titulo_puro,
                "subtitulo": ev["subtitulo"] or "",
                "eixo_codigo": eixo_cod,
                "categoria": cat,
                "cultura": ev["cultura_origem"] or "",
                "ano_inicio": ev["ano_inicio"],
                "ano_fim": ev["ano_fim"],
                "data_legivel": f"{ano_para_legivel(ev['ano_inicio'])}" + (f" até {ano_para_legivel(ev['ano_fim'])}" if ev["ano_fim"] else ""),
                "incerteza": ev["incerteza_anos"],
                "descricao": ev["descricao"],
                "fontes": ev["fontes_historicas"] or "",
                "wikipedia_url": ev["wikipedia_url"] or "",
                "localizacao": ev["localizacao"] or "",
                "latitude": ev["latitude"],
                "longitude": ev["longitude"],
                "tags": ev["tags"] or "",
                "concilio": concilio_info
            }
        }
        if ev["ano_fim"]:
            item_dict["end"] = formatar_ano_iso(ev["ano_fim"], ev["mes_fim"], ev["dia_fim"])

        itens.append(item_dict)

    # 5. Adicionar Livros Bíblicos
    for livro in livros_list:
        if livro["ano_composicao_inicio"]:
            ano_fim = livro["ano_composicao_fim"] or livro["ano_composicao_inicio"] + 20
            nome_livro_puro = re.sub(r'^[^\w\s]+', '', livro['nome']).strip()
            itens.append({
                "id": f"livro_{livro['id']}",
                "group": 4,
                "content": f"<span class='item-livro'>📖 {nome_livro_puro}</span>",
                "start": formatar_ano_iso(livro["ano_composicao_inicio"]),
                "end": formatar_ano_iso(ano_fim),
                "type": "range",
                "className": f"item-livro-bloco testamento-{livro['testamento'].lower()} cat-livro",
                "meta": {
                    "tipo_item": "livro",
                    "titulo": nome_livro_puro,
                    "subtitulo": f"Original: {livro['nome_original']} ({livro['idioma_original']})",
                    "eixo_codigo": "CANON",
                    "categoria": "livro",
                    "testamento": livro["testamento"],
                    "genero": livro["genero_literario"],
                    "idioma": livro["idioma_original"],
                    "autor_tradicional": livro["autor_tradicional"],
                    "data_legivel": f"Composição estimada: {ano_para_legivel(livro['ano_composicao_inicio'])} a {ano_para_legivel(ano_fim)}",
                    "ano_inicio": livro["ano_composicao_inicio"],
                    "ano_fim": ano_fim,
                    "consenso_critico": livro["data_consenso_critico"],
                    "descricao": livro["resumo"] or "",
                    "wikipedia_url": livro["wikipedia_url"] or "",
                    "status_canonico": {
                        "JUDAICA": {"status": livro["status_judaica"], "motivo": livro["motivo_judaica"]},
                        "PROTESTANTE": {"status": livro["status_protestante"], "motivo": livro["motivo_protestante"]},
                        "CATOLICA": {"status": livro["status_catolica"], "motivo": livro["motivo_catolica"]},
                        "ORTODOXA": {"status": livro["status_ortodoxa"], "motivo": livro["motivo_ortodoxa"]}
                    }
                }
            })

    conn.close()
    return grupos, itens, livros_list

def gerar_timeline_html():
    grupos, itens, livros = carregar_dados_sqlite()

    html_content = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Timeline Histórica Bíblica Comparada: Adão a Cristo, Concílios, Impérios & Mitos</title>
  
  <!-- Vis-Timeline -->
  <script type="text/javascript" src="https://unpkg.com/vis-timeline@latest/standalone/umd/vis-timeline-graph2d.min.js"></script>
  <link href="https://unpkg.com/vis-timeline@latest/styles/vis-timeline-graph2d.min.css" rel="stylesheet" type="text/css" />

  <!-- Google Fonts: Inter & JetBrains Mono -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">

  <style>
    :root {{
      --bg-main: #060911;
      --bg-surface: #0b1120;
      --bg-card: #131c31;
      --bg-card-hover: #1c2844;
      --border-color: #233252;
      --border-highlight: #38bdf8;
      --text-primary: #f8fafc;
      --text-secondary: #94a3b8;
      --text-muted: #64748b;
      
      --color-secular: #0284c7;
      --color-biblico: #d97706;
      --color-mitologia: #7c3aed;
      --color-canon: #059669;
      --color-accent: #38bdf8;
    }}

    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}

    body {{
      font-family: 'Inter', sans-serif;
      background-color: var(--bg-main);
      color: var(--text-primary);
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      overflow-x: hidden;
    }}

    /* HEADER INTEGRADO */
    header {{
      background: linear-gradient(180deg, #0d1527 0%, #060911 100%);
      border-bottom: 1px solid var(--border-color);
      padding: 10px 18px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 10px;
    }}

    .brand {{
      display: flex;
      align-items: center;
      gap: 10px;
      flex-wrap: wrap;
    }}

    .brand-tag {{
      background: rgba(56, 189, 248, 0.12);
      color: #38bdf8;
      border: 1px solid rgba(56, 189, 248, 0.3);
      padding: 3px 8px;
      border-radius: 12px;
      font-size: 10px;
      font-weight: 700;
      letter-spacing: 0.5px;
      text-transform: uppercase;
    }}

    .brand h1 {{
      font-family: 'Cinzel', serif;
      font-size: 16px;
      font-weight: 700;
      letter-spacing: 0.4px;
      background: linear-gradient(90deg, #38bdf8, #818cf8, #fbbf24);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      margin: 0;
    }}

    .brand p {{
      font-size: 11px;
      color: var(--text-secondary);
      margin: 0;
    }}

    .header-stats {{
      display: flex;
      gap: 6px;
      align-items: center;
      flex-wrap: wrap;
    }}

    .stat-badge {{
      background: rgba(19, 28, 49, 0.7);
      border: 1px solid var(--border-color);
      border-radius: 14px;
      padding: 3px 8px;
      font-size: 10.5px;
      display: flex;
      align-items: center;
      gap: 4px;
      color: var(--text-secondary);
    }}

    .stat-badge b {{
      color: var(--color-accent);
    }}

    /* TOOLBAR COM MENUS DROPDOWN MODERNOS */
    .controls-bar {{
      background: var(--bg-surface);
      border-bottom: 1px solid var(--border-color);
      padding: 8px 20px;
      display: flex;
      flex-wrap: wrap;
      gap: 12px;
      align-items: center;
      justify-content: space-between;
    }}

    .dropdown-container {{
      display: flex;
      align-items: center;
      gap: 10px;
      flex-wrap: wrap;
    }}

    .control-item {{
      display: flex;
      align-items: center;
      gap: 6px;
    }}

    .control-label {{
      font-size: 11px;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      color: var(--text-muted);
      white-space: nowrap;
    }}

    .modern-select {{
      background: #131c31;
      border: 1px solid var(--border-color);
      color: var(--text-primary);
      padding: 6px 10px;
      border-radius: 6px;
      font-size: 12px;
      font-family: inherit;
      outline: none;
      cursor: pointer;
      transition: all 0.2s;
      min-width: 170px;
    }}

    .modern-select:hover {{
      border-color: var(--border-highlight);
      background: #1a2642;
    }}

    .modern-select:focus {{
      border-color: var(--color-accent);
      box-shadow: 0 0 0 2px rgba(56, 189, 248, 0.2);
    }}

    .btn-toggle-labels {{
      background: #131c31;
      border: 1px solid var(--border-color);
      color: var(--text-secondary);
      padding: 6px 10px;
      border-radius: 6px;
      font-size: 11.5px;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 5px;
      transition: all 0.2s;
    }}

    .btn-toggle-labels:hover {{
      background: #1a2642;
      color: var(--text-primary);
      border-color: var(--border-highlight);
    }}

    .search-input {{
      background: #131c31;
      border: 1px solid var(--border-color);
      color: var(--text-primary);
      padding: 6px 12px;
      border-radius: 6px;
      font-size: 12px;
      width: 210px;
      outline: none;
      transition: border-color 0.2s;
    }}

    .search-input:focus {{
      border-color: var(--color-accent);
      box-shadow: 0 0 0 2px rgba(56, 189, 248, 0.2);
    }}

    /* MARCADOR SINCRONIZADOR DE ÉPOCA */
    .epoch-scrubber-bar {{
      background: linear-gradient(90deg, #090e1a 0%, #1e1b4b 50%, #090e1a 100%);
      border-bottom: 1px solid #3730a3;
      padding: 6px 20px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-wrap: wrap;
      gap: 10px;
    }}

    .scrubber-indicator {{
      display: flex;
      align-items: center;
      gap: 8px;
    }}

    .scrubber-title {{
      font-size: 11px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.6px;
      color: #a5b4fc;
      display: flex;
      align-items: center;
      gap: 5px;
    }}

    .scrubber-year {{
      font-family: 'JetBrains Mono', monospace;
      font-size: 14px;
      font-weight: 700;
      color: #38bdf8;
      background: rgba(0,0,0,0.5);
      padding: 2px 8px;
      border-radius: 5px;
      border: 1px solid #38bdf8;
    }}

    .epoch-summary-grid {{
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 8px;
      flex: 1;
      max-width: 900px;
    }}

    .epoch-track-pill {{
      background: rgba(11, 17, 32, 0.85);
      border: 1px solid var(--border-color);
      border-radius: 5px;
      padding: 3px 7px;
      font-size: 10.5px;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
    }}

    .epoch-track-pill span {{
      color: var(--text-muted);
      font-size: 9px;
      font-weight: 700;
      display: block;
    }}

    /* MAIN APP BODY */
    .app-body {{
      display: flex;
      flex: 1;
      height: calc(100vh - 195px);
      min-height: 520px;
      position: relative;
    }}

    #timeline-container {{
      flex: 1;
      height: 100%;
      background: #060911;
      border-right: 1px solid var(--border-color);
      position: relative;
    }}

    /* VIS-TIMELINE OVERRIDES: RÓTULOS ENCOLHIDOS E FONTE REFINADA */
    .vis-timeline {{
      border: none !important;
      font-family: 'Inter', sans-serif !important;
    }}

    .vis-panel.vis-center, .vis-panel.vis-left, .vis-panel.vis-right, .vis-panel.vis-top, .vis-panel.vis-bottom {{
      border-color: var(--border-color) !important;
    }}

    /* RÓTULOS LATERAIS DOS EIXOS: CARDS REFINADOS E ELEGANTES */
    .vis-panel.vis-left {{
    /* RÓTULOS LATERAIS DOS EIXOS: SEM ÍCONES, COR SINCRONIZADOR DE ÉPOCA (#a5b4fc) */
    .vis-panel.vis-left {{
      width: 180px !important;
      min-width: 180px !important;
      max-width: 180px !important;
      transition: width 0.25s ease;
    }}

    .vis-labelset .vis-label {{
      background: #0b1120 !important;
      border-bottom: 1px solid var(--border-color) !important;
      border-right: 1px solid var(--border-color) !important;
      padding: 6px 10px !important;
      display: flex !important;
      align-items: center !important;
      width: 180px !important;
      min-width: 180px !important;
      max-width: 180px !important;
      box-sizing: border-box !important;
      transition: width 0.25s ease;
    }}

    .eixo-card {{
      display: flex;
      align-items: center;
      gap: 10px;
      width: 100%;
      box-sizing: border-box;
    }}

    .eixo-bar {{
      width: 4px;
      height: 28px;
      border-radius: 2px;
      flex-shrink: 0;
      box-shadow: 0 0 8px var(--eixo-cor);
    }}

    .eixo-textos {{
      display: flex;
      flex-direction: column;
      min-width: 0;
      overflow: hidden;
    }}

    .eixo-titulo {{
      font-family: 'Inter', sans-serif;
      font-size: 12px;
      font-weight: 700;
      color: #a5b4fc !important; /* Mesma cor do texto 'Sincronizador de Época' */
      letter-spacing: 0.3px;
      line-height: 1.3;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }}

    .eixo-subtitulo {{
      font-size: 9.5px;
      font-weight: 500;
      color: #94a3b8;
      line-height: 1.2;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
      margin-top: 2px;
    }}

    /* MODO ULTRA COMPACTO */
    body.labels-ultra-compact .vis-panel.vis-left,
    body.labels-ultra-compact .vis-labelset .vis-label {{
      width: 36px !important;
      min-width: 36px !important;
      max-width: 36px !important;
      padding: 4px 2px !important;
    }}

    body.labels-ultra-compact .eixo-card {{
      justify-content: center;
      padding: 0;
    }}

    body.labels-ultra-compact .eixo-textos {{
      display: none !important;
    }}

    body.labels-ultra-compact .eixo-bar {{
      width: 5px;
      height: 30px;
    }}

    .vis-time-axis .vis-text {{
      color: #94a3b8 !important;
      font-family: 'JetBrains Mono', monospace !important;
      font-size: 10.5px !important;
    }}

    /* MARCADOR SINCRONIZADOR DE ÉPOCA (ARRASTÁVEL) */
    .vis-custom-time.marcador-epoca {{
      background-color: #f43f5e !important;
      width: 2px !important;
      cursor: ew-resize !important;
      z-index: 100 !important;
    }}

    .vis-custom-time.marcador-epoca:after {{
      content: '📍 Época';
      position: absolute;
      top: 0;
      left: 4px;
      background: #f43f5e;
      color: #fff;
      font-size: 9px;
      font-weight: 700;
      padding: 1px 4px;
      border-radius: 3px;
      white-space: nowrap;
    }}

    /* MARCADOR DO DILÚVIO: LINHA AZUL CLARA DE ALTO A BAIXO */
    .vis-custom-time.marcador-diluvio {{
      background-color: #38bdf8 !important; /* Azul claro */
      width: 2.5px !important;
      z-index: 95 !important;
      box-shadow: 0 0 10px rgba(56, 189, 248, 0.8) !important;
      pointer-events: none;
    }}

    .vis-custom-time.marcador-diluvio:after {{
      content: '🌊 O DILÚVIO (2348 a.C.)';
      position: absolute;
      top: 2px;
      left: 4px;
      background: linear-gradient(135deg, #0284c7, #0369a1);
      color: #f0f9ff;
      border: 1px solid #38bdf8;
      font-size: 9.5px;
      font-weight: 700;
      padding: 2px 7px;
      border-radius: 4px;
      white-space: nowrap;
      pointer-events: none;
      box-shadow: 0 2px 6px rgba(0,0,0,0.6);
    }}
      pointer-events: none;
    }}

    /* TEXTOS QUE CABEM DENTRO DAS BARRAS */
    .vis-item {{
      border-radius: 4px !important;
      font-size: 11px !important;
      color: #ffffff !important;
      cursor: pointer !important;
      min-width: 18px !important;
      height: 23px !important;
      display: flex !important;
      align-items: center !important;
      transition: transform 0.1s ease, box-shadow 0.1s ease !important;
    }}

    .vis-item .vis-item-content {{
      padding: 1px 5px !important;
      font-size: 10.5px !important;
      font-weight: 500 !important;
      letter-spacing: 0.1px !important;
      line-height: 18px !important;
      white-space: nowrap !important;
      overflow: hidden !important;
      text-overflow: ellipsis !important;
    }}

    .vis-item:hover {{
      transform: translateY(-1px);
      box-shadow: 0 4px 12px rgba(0,0,0,0.7) !important;
      z-index: 50 !important;
    }}

    .vis-item:hover .vis-item-content {{
      overflow: visible !important;
    }}

    .vis-item.vis-selected {{
      border-color: #38bdf8 !important;
      box-shadow: 0 0 0 2px #38bdf8, 0 6px 18px rgba(56, 189, 248, 0.4) !important;
    }}

    /* Categorias */
    .cat-antediluviano {{ background: linear-gradient(135deg, #065f46 0%, #047857 100%) !important; border: 1px solid #34d399 !important; }}
    .cat-patriarca {{ background: linear-gradient(135deg, #b45309 0%, #d97706 100%) !important; border: 1px solid #fbbf24 !important; }}
    .cat-juiz {{ background: linear-gradient(135deg, #1d4ed8 0%, #2563eb 100%) !important; border: 1px solid #60a5fa !important; }}
    .cat-rei_israel, .cat-rei_juda {{ background: linear-gradient(135deg, #854d0e 0%, #a16207 100%) !important; border: 1px solid #fde047 !important; }}
    .cat-profeta {{ background: linear-gradient(135deg, #be123c 0%, #e11d48 100%) !important; border: 1px solid #fda4af !important; }}
    .item-secular {{ background: linear-gradient(135deg, #0369a1 0%, #0284c7 100%) !important; border: 1px solid #38bdf8 !important; }}
    .item-mitologia {{ background: linear-gradient(135deg, #6d28d9 0%, #7c3aed 100%) !important; border: 1px solid #c084fc !important; }}
    .cat-concilio {{ background: linear-gradient(135deg, #047857 0%, #10b981 100%) !important; border: 2px solid #6ee7b7 !important; font-weight: 700 !important; }}
    .item-livro-bloco {{ background: #131c31 !important; border: 1px dashed #64748b !important; }}

    /* Status Canônico */
    .status-canonico-destaque {{ border: 2px solid #10b981 !important; box-shadow: 0 0 8px rgba(16, 185, 129, 0.4) !important; }}
    .status-deuterocanonico-destaque {{ border: 2px solid #8b5cf6 !important; box-shadow: 0 0 8px rgba(139, 92, 246, 0.4) !important; }}
    .status-apocrifo-destaque {{ border: 1px dashed #f59e0b !important; opacity: 0.75 !important; }}
    .status-rejeitado-destaque {{ border: 1px solid #ef4444 !important; opacity: 0.3 !important; filter: grayscale(80%) !important; }}

    /* SIDEBAR DRAWER */
    .sidebar-drawer {{
      width: 420px;
      background: var(--bg-surface);
      display: flex;
      flex-direction: column;
      overflow-y: auto;
      border-left: 1px solid var(--border-color);
    }}

    .drawer-header {{
      padding: 14px 18px;
      background: #0d1527;
      border-bottom: 1px solid var(--border-color);
      position: sticky;
      top: 0;
      z-index: 20;
    }}

    .drawer-header h2 {{
      font-size: 14.5px;
      font-weight: 700;
      color: var(--text-primary);
    }}

    .drawer-body {{
      padding: 16px 18px;
      display: flex;
      flex-direction: column;
      gap: 14px;
      font-size: 12.5px;
      line-height: 1.55;
      color: #cbd5e1;
    }}

    .detail-card {{
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      border-radius: 7px;
      padding: 12px 14px;
      display: flex;
      flex-direction: column;
      gap: 7px;
    }}

    .card-title {{
      font-size: 10px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.8px;
      color: var(--color-accent);
      display: flex;
      align-items: center;
      gap: 5px;
    }}

    .badge {{
      display: inline-flex;
      align-items: center;
      gap: 4px;
      padding: 2px 7px;
      border-radius: 4px;
      font-size: 10px;
      font-weight: 600;
    }}

    .badge-secular {{ background: rgba(2, 132, 199, 0.2); color: #38bdf8; border: 1px solid #0284c7; }}
    .badge-biblico {{ background: rgba(217, 119, 6, 0.2); color: #fbbf24; border: 1px solid #d97706; }}
    .badge-mitologia {{ background: rgba(124, 58, 237, 0.2); color: #c084fc; border: 1px solid #7c3aed; }}
    .badge-canon {{ background: rgba(5, 150, 105, 0.2); color: #34d399; border: 1px solid #059669; }}

    .wiki-btn {{
      display: inline-flex;
      align-items: center;
      gap: 7px;
      background: #131c31;
      color: #38bdf8;
      border: 1px solid #38bdf8;
      border-radius: 6px;
      padding: 7px 12px;
      font-size: 11.5px;
      font-weight: 600;
      text-decoration: none;
      transition: all 0.2s;
      margin-top: 4px;
    }}

    .wiki-btn:hover {{
      background: #38bdf8;
      color: #060911;
    }}

    .canon-table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 11px;
      margin-top: 4px;
    }}

    .canon-table th, .canon-table td {{
      padding: 5px 7px;
      text-align: left;
      border-bottom: 1px solid var(--border-color);
    }}

    .canon-table th {{
      color: var(--text-muted);
      font-weight: 600;
      background: rgba(11, 17, 32, 0.6);
    }}

    .status-pill {{
      display: inline-block;
      padding: 2px 5px;
      border-radius: 4px;
      font-size: 9px;
      font-weight: 700;
      text-transform: uppercase;
    }}

    .status-CANONICO {{ background: #064e3b; color: #6ee7b7; border: 1px solid #059669; }}
    .status-DEUTEROCANONICO {{ background: #4c1d95; color: #c4b5fd; border: 1px solid #7c3aed; }}
    .status-ANAGINOSKOMENA {{ background: #1e1b4b; color: #a5b4fc; border: 1px solid #6366f1; }}
    .status-APOCRIFO {{ background: #78350f; color: #fcd34d; border: 1px solid #d97706; }}
    .status-REJEITADO {{ background: #450a0a; color: #fca5a5; border: 1px solid #dc2626; }}

    footer {{
      background: #060911;
      border-top: 1px solid var(--border-color);
      padding: 6px 20px;
      font-size: 10.5px;
      color: var(--text-muted);
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 6px;
    }}

    @media (max-width: 1024px) {{
      .epoch-summary-grid {{ display: none; }}
      .app-body {{ flex-direction: column; height: auto; }}
      #timeline-container {{ height: 480px; }}
      .sidebar-drawer {{ width: 100%; }}
    }}
  </style>
</head>
<body>

  <!-- HEADER INTEGRADO -->
  <header>
    <div class="brand">
      <span class="brand-tag">Sincronismo Histórico</span>
      <h1>Linha do Tempo Comparada de 4 Eixos</h1>
      <p>4004 a.C. a 1546 d.C. • 112 Registros Conectados</p>
    </div>
    <div class="header-stats">
      <div class="stat-badge">🌱 <b>Adão a Noé</b></div>
      <div class="stat-badge">⛺ <b>Patriarcas</b></div>
      <div class="stat-badge">⚖️ <b>Juízes</b></div>
      <div class="stat-badge">👑 <b>Reis</b></div>
      <div class="stat-badge">🔥 <b>Profetas</b></div>
      <div class="stat-badge">⛪ <b>Cânon & Concílios</b></div>
    </div>
  </header>

  <!-- TOOLBAR COM MENUS DROPDOWN (SUBSTITUINDO CHIPS E BOTÕES EXCESSIVOS) -->
  <div class="controls-bar">
    <div class="dropdown-container">
      
      <!-- 1. Dropdown de Filtro Temático -->
      <div class="control-item">
        <label for="select-categoria" class="control-label">🏷️ Categoria:</label>
        <select id="select-categoria" class="modern-select" onchange="filtrarCategoria(this.value)">
          <option value="TODOS">🌐 Todos os Registros ({len(itens)})</option>
          <option value="antediluviano">🌱 Antediluvianos (Adão a Noé)</option>
          <option value="patriarca">⛺ Grandes Patriarcas (Abraão a Josué)</option>
          <option value="juiz">⚖️ Juízes de Israel (Otniel a Samuel)</option>
          <option value="rei">👑 Reis de Israel & Judá</option>
          <option value="profeta">🔥 Profetas (Elias a João Batista)</option>
          <option value="imperio">🏛️ Grandes Impérios Seculares</option>
          <option value="mito">🏺 Mitologias & Cosmogonias</option>
          <option value="concilio">⛪ Concílios & Sínodos</option>
          <option value="livro">📖 Livros Bíblicos & Cânon</option>
        </select>
      </div>

      <!-- 2. Dropdown de Salto Rápido de Época -->
      <div class="control-item">
        <label for="select-salto" class="control-label">⚡ Salto Histórico:</label>
        <select id="select-salto" class="modern-select" onchange="if(this.value) executarSalto(this.value)">
          <option value="">🎯 Pular para uma Época...</option>
          <option value="-4004,600">🌱 4004 a.C. — Adão & Eva (Origens)</option>
          <option value="-2348,400">🌊 2348 a.C. — O Grande Dilúvio & Noé</option>
          <option value="-2066,350">⛺ 2066 a.C. — Era Patriarcal (Abraão & Isaque)</option>
          <option value="-1750,300">🏺 1750 a.C. — Hamurabi & Babilônia</option>
          <option value="-1446,250">📜 1446 a.C. — Êxodo de Moisés & Sinai</option>
          <option value="-1200,200">⚖️ 1200 a.C. — Débora, Gideão & Juízes</option>
          <option value="-1010,200">👑 1010 a.C. — Monarquia Unida (Rei Davi)</option>
          <option value="-853,150">⚔️ 853 a.C. — Acabe, Elias & Batalha de Qarqar</option>
          <option value="-722,120">⚡ 722 a.C. — Queda de Samaria ante Assíria</option>
          <option value="-587,120">🔥 587 a.C. — Queda de Jerusalém & Exílio</option>
          <option value="-538,120">📜 538 a.C. — Edito de Ciro & Retorno</option>
          <option value="-250,150">📖 250 a.C. — Septuaginta LXX & Qumran</option>
          <option value="30,60">✝️ 30 d.C. — Jesus Cristo & Império Romano</option>
          <option value="70,60">🏛️ 70 d.C. — Queda do 2º Templo por Tito</option>
          <option value="393,80">⛪ 393 d.C. — Hipona & Santo Agostinho</option>
          <option value="1546,80">⚜️ 1546 d.C. — Concílio de Trento</option>
        </select>
      </div>

      <!-- 3. Dropdown de Tradição Canônica -->
      <div class="control-item">
        <label for="select-tradicao" class="control-label">📖 Cânon:</label>
        <select id="select-tradicao" class="modern-select" onchange="filtrarTradicao(this.value)" style="min-width: 140px;">
          <option value="TODAS">🌐 Todas as Tradições</option>
          <option value="CATOLICA">⛪ Católica (73 Livros)</option>
          <option value="PROTESTANTE">📖 Protestante (66 Livros)</option>
          <option value="ORTODOXA">☦️ Ortodoxa (76+ Livros)</option>
          <option value="JUDAICA">✡️ Judaica / Tanakh (24)</option>
        </select>
      </div>

      <!-- 4. Botão para Encolher / Expandir Rótulos do Lado Esquerdo -->
      <button class="btn-toggle-labels" id="btn-toggle-labels" onclick="toggleRótulos()" title="Alterna entre rótulos compactos e ultra-encolhidos">
        <span id="icone-toggle-labels">◀</span> <span id="texto-toggle-labels">Encolher Rótulos</span>
      </button>

    </div>

    <!-- Busca Rápida -->
    <div class="control-item">
      <input type="text" id="campo-busca" class="search-input" placeholder="🔍 Buscar nome, rei, livro..." onkeyup="buscarTimeline(this.value)">
    </div>
  </div>

  <!-- MARCADOR SINCRONIZADOR DE ÉPOCA -->
  <div class="epoch-scrubber-bar">
    <div class="scrubber-indicator">
      <div class="scrubber-title">⚡ Sincronizador de Época:</div>
      <div id="display-ano-marcador" class="scrubber-year">-1010 a.C.</div>
    </div>
    <div class="epoch-summary-grid">
      <div class="epoch-track-pill" id="pill-secular">
        <span>🏛️ SECULAR</span>
        <b id="txt-secular">Carregando...</b>
      </div>
      <div class="epoch-track-pill" id="pill-biblico">
        <span>📜 BÍBLICO</span>
        <b id="txt-biblico">Carregando...</b>
      </div>
      <div class="epoch-track-pill" id="pill-mitologia">
        <span>🏺 MITOLOGIAS</span>
        <b id="txt-mitologia">Carregando...</b>
      </div>
      <div class="epoch-track-pill" id="pill-canon">
        <span>⛪ CÂNON & CONCÍLIOS</span>
        <b id="txt-canon">Carregando...</b>
      </div>
    </div>
  </div>

  <!-- CORPO PRINCIPAL -->
  <div class="app-body">
    <div id="timeline-container"></div>

    <aside class="sidebar-drawer" id="sidebar-drawer">
      <div class="drawer-header">
        <h2 id="drawer-titulo">Selecione um Personagem ou Evento</h2>
      </div>
      <div class="drawer-body" id="drawer-body">
        <div class="detail-card">
          <div class="card-title">ℹ️ Navegação Otimizada</div>
          <p>• <b>Zoom Calibrado:</b> O zoom inicial foi focado para que os nomes e datas caibam confortavelmente dentro das barras de cada personagem e império.</p>
          <p>• <b>Rótulos Encolhidos:</b> Os títulos do lado esquerdo foram compactados. Use o botão <b>◀ Encolher Rótulos</b> para ocultar os textos e ver apenas os ícones.</p>
          <p>• <b>Menus Dropdown:</b> Use os menus suspensos superiores para saltar instantaneamente de época ou isolar grupos (Patriarcas, Juízes, Reis ou Profetas).</p>
        </div>
      </div>
    </aside>
  </div>

  <!-- FOOTER -->
  <footer>
    <div>Cronologia bíblica estruturada com base no Texto Massorético (Gn 5 e 11), Edwin Thiele e verificação na <b>Wikipédia</b>.</div>
    <div>Total: <b>{len(itens)} registros</b> sincronizados no SQLite.</div>
  </footer>

  <!-- SCRIPT JS -->
  <script type="text/javascript">
    const RAW_GROUPS = {json.dumps(grupos, ensure_ascii=False)};
    const RAW_ITEMS = {json.dumps(itens, ensure_ascii=False)};
    const RAW_LIVROS = {json.dumps(livros, ensure_ascii=False)};

    const groupsDataSet = new vis.DataSet(RAW_GROUPS);
    const itemsDataSet = new vis.DataSet(RAW_ITEMS);

    const container = document.getElementById('timeline-container');
    
    // ZOOM INICIAL CALIBRADO:
    // Uma janela de ~530 anos (-1050 a.C. a -520 a.C.) onde os textos cabem perfeitamente
    // dentro das barras (Davi, Salomão, reis de Israel e Judá, profetas e impérios contemporâneos).
    const options = {{
      stack: true,
      stackSubgroups: true,
      horizontalScroll: true,
      zoomKey: 'ctrlKey',
      start: '-001050-01-01',
      end: '-000520-01-01',
      min: '-004200-01-01',
      max: '2050-01-01',
      orientation: 'top',
      showCurrentTime: false,
      margin: {{
        item: {{ horizontal: 6, vertical: 6 }},
        axis: 8
      }}
    }};

    const timeline = new vis.Timeline(container, itemsDataSet, groupsDataSet, options);

    const MARCADOR_ID = 'marcador-epoca';
    timeline.addCustomTime('-001010-01-01', MARCADOR_ID);
    timeline.setCustomTimeTitle('Arraste para sincronizar a data nos 4 trilhos', MARCADOR_ID);

    // Linha azul clara contínua de alto a baixo marcando o Dilúvio (2348 a.C.)
    const DILUVIO_ID = 'marcador-diluvio';
    timeline.addCustomTime('-002348-01-01', DILUVIO_ID);
    timeline.setCustomTimeTitle('🌊 O Grande Dilúvio e a Arca de Noé (2348 a.C.)', DILUVIO_ID);

    function formatarAnoLegivel(ano) {{
      if (ano < 0) return `${{Math.abs(ano)}} a.C.`;
      if (ano === 0) return `1 a.C.`;
      return `${{ano}} d.C.`;
    }}

    function atualizarConfrontoEpoca(dataCustomTime) {{
      const d = new Date(dataCustomTime);
      const ano = d.getFullYear();
      document.getElementById('display-ano-marcador').innerText = formatarAnoLegivel(ano);

      let secularAtivo = 'Nenhum grande império dominante cadastrado';
      let biblicoAtivo = 'Sem personagem central registrado neste ponto';
      let mitologiaAtiva = 'Nenhum mito proeminente datado';
      let canonAtivo = 'Sem concílios ou manuscritos formais';

      const biblicosAtivos = [];

      RAW_ITEMS.forEach(item => {{
        const meta = item.meta;
        if (!meta) return;
        const ini = meta.ano_inicio;
        const fim = meta.ano_fim || meta.ano_inicio;

        if (ano >= ini && ano <= fim) {{
          if (meta.eixo_codigo === 'SECULAR') secularAtivo = meta.titulo;
          else if (meta.eixo_codigo === 'BIBLICO') biblicosAtivos.push(meta.titulo);
          else if (meta.eixo_codigo === 'MITOLOGIA') mitologiaAtiva = meta.titulo;
          else if (meta.eixo_codigo === 'CANON') canonAtivo = meta.titulo;
        }}
      }});

      if (biblicosAtivos.length > 0) {{
        biblicoAtivo = biblicosAtivos.slice(0, 2).join(' • ');
        if (biblicosAtivos.length > 2) biblicoAtivo += ` (+${{biblicosAtivos.length - 2}})`;
      }}

      const elSec = document.getElementById('txt-secular');
      const elBib = document.getElementById('txt-biblico');
      const elMit = document.getElementById('txt-mitologia');
      const elCan = document.getElementById('txt-canon');

      elSec.innerText = secularAtivo; elSec.parentElement.title = secularAtivo;
      elBib.innerText = biblicoAtivo; elBib.parentElement.title = biblicosAtivos.join(', ') || biblicoAtivo;
      elMit.innerText = mitologiaAtiva; elMit.parentElement.title = mitologiaAtiva;
      elCan.innerText = canonAtivo; elCan.parentElement.title = canonAtivo;
    }}

    timeline.on('timechange', function (properties) {{
      if (properties.id === MARCADOR_ID) {{
        atualizarConfrontoEpoca(properties.time);
      }} else if (properties.id === DILUVIO_ID) {{
        timeline.setCustomTime('-002348-01-01', DILUVIO_ID);
      }}
    }});

    atualizarConfrontoEpoca(new Date('-001010-01-01'));

    // Execução do Salto pelo Dropdown
    function executarSalto(valor) {{
      if (!valor) return;
      const partes = valor.split(',');
      const ano = parseInt(partes[0], 10);
      const range = parseInt(partes[1], 10);

      const startIso = formatarAnoIsoJS(ano - Math.floor(range / 2));
      const endIso = formatarAnoIsoJS(ano + Math.ceil(range / 2));
      timeline.setWindow(startIso, endIso, {{ animation: {{ duration: 600, easingFunction: 'easeInOutQuad' }} }});
      
      const marcadorIso = formatarAnoIsoJS(ano);
      timeline.setCustomTime(marcadorIso, MARCADOR_ID);
      atualizarConfrontoEpoca(marcadorIso);
    }}

    function formatarAnoIsoJS(ano) {{
      if (ano < 0) return `-${{String(Math.abs(ano)).padStart(6, '0')}}-01-01`;
      return `${{String(ano).padStart(4, '0')}}-01-01`;
    }}

    // Alternar Rótulos Ultra Encolhidos (Modo Compacto de Ícones)
    let ultraCompacto = false;
    function toggleRótulos() {{
      ultraCompacto = !ultraCompacto;
      document.body.classList.toggle('labels-ultra-compact', ultraCompacto);
      const icone = document.getElementById('icone-toggle-labels');
      const texto = document.getElementById('texto-toggle-labels');
      if (icone) icone.innerText = ultraCompacto ? '▶' : '◀';
      if (texto) texto.innerText = ultraCompacto ? 'Expandir Rótulos' : 'Encolher Rótulos';
      setTimeout(() => {{
        timeline.redraw();
      }}, 50);
    }}

    // Filtro pelo Dropdown de Categorias
    function filtrarCategoria(cat) {{
      if (cat === 'TODOS') {{
        itemsDataSet.clear();
        itemsDataSet.add(RAW_ITEMS);
        return;
      }}

      const filtrados = RAW_ITEMS.filter(it => {{
        const meta = it.meta || {{}};
        if (cat === 'rei') return meta.categoria === 'rei_israel' || meta.categoria === 'rei_juda';
        return meta.categoria === cat;
      }});

      itemsDataSet.clear();
      itemsDataSet.add(filtrados);
    }}

    // Filtro pelo Dropdown de Tradição Canônica
    function filtrarTradicao(tradicao) {{
      const itensAtualizados = RAW_ITEMS.map(it => {{
        const copy = Object.assign({{}}, it);
        if (copy.meta && copy.meta.tipo_item === 'livro' && copy.meta.status_canonico) {{
          const stObj = copy.meta.status_canonico[tradicao];
          const st = stObj ? stObj.status : null;

          if (tradicao === 'TODAS') {{
            copy.className = `item-livro-bloco testamento-${{copy.meta.testamento.toLowerCase()}}`;
          }} else if (st === 'CANONICO') {{
            copy.className = 'item-livro-bloco status-canonico-destaque';
          }} else if (st === 'DEUTEROCANONICO' || st === 'ANAGINOSKOMENA') {{
            copy.className = 'item-livro-bloco status-deuterocanonico-destaque';
          }} else if (st === 'APOCRIFO') {{
            copy.className = 'item-livro-bloco status-apocrifo-destaque';
          }} else if (st === 'REJEITADO') {{
            copy.className = 'item-livro-bloco status-rejeitado-destaque';
          }}
        }}
        return copy;
      }});

      itemsDataSet.clear();
      itemsDataSet.add(itensAtualizados);
    }}

    function buscarTimeline(termo) {{
      termo = termo.toLowerCase().trim();
      if (!termo) {{
        itemsDataSet.clear();
        itemsDataSet.add(RAW_ITEMS);
        return;
      }}

      const filtrados = RAW_ITEMS.filter(it => {{
        const meta = it.meta || {{}};
        const strBusca = `${{meta.titulo}} ${{meta.subtitulo}} ${{meta.descricao}} ${{meta.cultura}} ${{meta.tags}}`.toLowerCase();
        return strBusca.includes(termo);
      }});

      itemsDataSet.clear();
      itemsDataSet.add(filtrados);
    }}

    // Drawer de Detalhes
    timeline.on('select', function (properties) {{
      if (properties.items.length === 0) return;
      const itemId = properties.items[0];
      const item = itemsDataSet.get(itemId);
      if (!item || !item.meta) return;

      const meta = item.meta;
      const drawerTitulo = document.getElementById('drawer-titulo');
      const drawerBody = document.getElementById('drawer-body');

      drawerTitulo.innerHTML = `${{meta.titulo}}`;

      let html = '';

      // Badges
      html += `<div style="display:flex; gap:6px; flex-wrap:wrap;">`;
      html += `<span class="badge badge-${{meta.eixo_codigo.toLowerCase()}}">${{meta.eixo_codigo}}</span>`;
      html += `<span class="badge" style="background:#131c31; color:#38bdf8; border:1px solid #38bdf8;">${{meta.categoria.toUpperCase()}}</span>`;
      if (meta.cultura) html += `<span class="badge" style="background:#131c31; color:#94a3b8;">📍 ${{meta.cultura}}</span>`;
      html += `</div>`;

      // Datas
      html += `
        <div class="detail-card">
          <div class="card-title">⏳ Cronologia & Baliza Histórica</div>
          <p><b>${{meta.data_legivel}}</b></p>
          ${{meta.subtitulo ? `<p style="color:#94a3b8; font-size:11.5px;">${{meta.subtitulo}}</p>` : ''}}
          ${{meta.incerteza ? `<p style="font-size:11px; color:var(--text-muted)">Incerteza historiográfica: &plusmn;${{meta.incerteza}} anos</p>` : ''}}
        </div>
      `;

      // Concílio
      if (meta.concilio) {{
        const c = meta.concilio;
        html += `
          <div class="detail-card" style="border-left: 3px solid var(--color-canon);">
            <div class="card-title">⛪ Metadados do Concílio</div>
            <p><b>Cidade/Região:</b> ${{c.cidade}}, ${{c.regiao}}</p>
            <p><b>Liderança:</b> ${{c.papa_ou_lideranca || 'N/A'}}</p>
            <p><b>Participantes:</b> ${{c.participantes_principais || 'N/A'}}</p>
            <p><b>Documento Oficial:</b> <code>${{c.documento_oficial || 'Atas'}}</code></p>
            <p><b>Anátema Dogmático:</b> ${{c.anatemas_declarados ? '<span style="color:#ef4444; font-weight:700">SIM (Sob anátema)</span>' : 'Não'}}</p>
            <div style="background:rgba(0,0,0,0.3); padding:8px; border-radius:6px; margin-top:4px;">
              <b>Decisões Canônicas:</b>
              <p style="font-size:11.5px; margin-top:3px;">${{c.decisoes_canonicidade}}</p>
            </div>
          </div>
        `;
      }}

      // Livro Bíblico
      if (meta.tipo_item === 'livro' && meta.status_canonico) {{
        html += `
          <div class="detail-card">
            <div class="card-title">📜 Metadados Literários & Canônicos</div>
            <p><b>Testamento:</b> ${{meta.testamento}} | <b>Gênero:</b> ${{meta.genero}}</p>
            <p><b>Idioma Original:</b> ${{meta.idioma}}</p>
            <p><b>Autor Tradicional:</b> ${{meta.autor_tradicional}}</p>
            <p><b>Crítica Textual:</b> ${{meta.consenso_critico}}</p>
            
            <div style="margin-top:6px;">
              <b style="font-size:11px; color:var(--color-accent)">Status nas 4 Tradições:</b>
              <table class="canon-table">
                <thead>
                  <tr>
                    <th>Tradição</th>
                    <th>Status</th>
                    <th>Contexto Histórico</th>
                  </tr>
                </thead>
                <tbody>
                  ${{Object.entries(meta.status_canonico).map(([trad, data]) => `
                    <tr>
                      <td><b>${{trad}}</b></td>
                      <td><span class="status-pill status-${{data.status}}">${{data.status}}</span></td>
                      <td style="font-size:10px; color:#94a3b8;">${{data.motivo || '-'}}</td>
                    </tr>
                  `).join('')}}
                </tbody>
              </table>
            </div>
          </div>
        `;
      }}

      // Síntese
      html += `
        <div class="detail-card">
          <div class="card-title">📖 Resumo & Contexto Histórico</div>
          <p>${{meta.descricao}}</p>
          ${{meta.fontes ? `<p style="font-size:11px; margin-top:6px; color:#94a3b8"><b>Fontes Primárias:</b> ${{meta.fontes}}</p>` : ''}}
          ${{meta.localizacao ? `<p style="font-size:11px; color:#94a3b8"><b>Localização:</b> ${{meta.localizacao}}</p>` : ''}}
        </div>
      `;

      // Wikipedia Link
      if (meta.wikipedia_url) {{
        html += `
          <a href="${{meta.wikipedia_url}}" target="_blank" rel="noopener noreferrer" class="wiki-btn">
            🌐 Ver Artigo Verificado na Wikipédia &rarr;
          </a>
        `;
      }}

      drawerBody.innerHTML = html;
    }});
  </script>
</body>
</html>
"""

    with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"[OK] Linha do tempo visual gerada com sucesso em '{OUTPUT_HTML}'!")
    print(f"     Itens processados: {len(itens)} | Grupos: {len(grupos)} | Livros: {len(livros)}")

if __name__ == "__main__":
    gerar_timeline_html()
    if "--serve" in sys.argv:
        import http.server
        import socketserver
        PORT = 8000
        Handler = http.server.SimpleHTTPRequestHandler
        print(f"\n🚀 Servidor web local iniciado em http://localhost:{PORT}/timeline_confronto.html")
        print("Pressione Ctrl+C para encerrar o servidor.")
        with socketserver.TCPServer(("", PORT), Handler) as httpd:
            try:
                httpd.serve_forever()
            except KeyboardInterrupt:
                print("\n🛑 Servidor encerrado.")