import streamlit as st
import sqlite3
import pandas as pd
import streamlit.components.v1 as components
import os
import json
import re

# ==============================================================================
# CONFIGURAÇÃO GERAL DA PÁGINA
# ==============================================================================
st.set_page_config(
    page_title="Leitor Bíblico & Linha do Tempo Histórica",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================================================================
# ESTILOS CSS CUSTOMIZADOS (DESIGN UNIFICADO, MODERNO E ELEGANTE)
# ==============================================================================
st.markdown("""
<style>
    /* Variáveis Globais de Cores */
    :root {
        --bg-main: #060911;
        --bg-surface: #0b1120;
        --bg-card: #131c31;
        --border-color: #233252;
        --accent-cyan: #38bdf8;
        --accent-gold: #f59e0b;
        --accent-emerald: #10b981;
        --text-muted: #94a3b8;
    }

    /* Ajuste de Abas do Streamlit & Segmented Control */
    .stTabs [data-baseweb="tab-list"],
    div[data-testid="stSegmentedControl"] {
        gap: 8px;
        background-color: #0b1120;
        padding: 6px 10px;
        border-radius: 12px;
        border: 1px solid #233252;
        display: flex;
        width: 100%;
        margin-bottom: 20px;
    }

    .stTabs [data-baseweb="tab"],
    div[data-testid="stSegmentedControl"] button {
        height: 44px;
        font-size: 0.95rem !important;
        font-weight: 600 !important;
        color: #94a3b8 !important;
        border-radius: 8px !important;
        padding: 0 16px !important;
        background-color: transparent !important;
        border: 1px solid transparent !important;
        transition: all 0.2s ease !important;
    }

    .stTabs [data-baseweb="tab"]:hover,
    div[data-testid="stSegmentedControl"] button:hover {
        color: #f8fafc !important;
        background-color: rgba(56, 189, 248, 0.1) !important;
        border-color: rgba(56, 189, 248, 0.2) !important;
    }

    .stTabs [aria-selected="true"],
    div[data-testid="stSegmentedControl"] button[aria-checked="true"],
    div[data-testid="stSegmentedControl"] button[data-state="on"] {
        background-color: #1a2642 !important;
        color: #38bdf8 !important;
        border-color: #38bdf8 !important;
        border-bottom: 2px solid #38bdf8 !important;
        box-shadow: 0 0 12px rgba(56, 189, 248, 0.25) !important;
    }

    /* Leitor Bíblico */
    .verse-num {
        color: #38bdf8;
        font-size: 0.85em;
        font-weight: bold;
        vertical-align: super;
        margin-right: 6px;
        font-family: 'JetBrains Mono', monospace;
    }
    
    .verse-text {
        font-size: 1.22rem;
        line-height: 1.7;
        margin-bottom: 12px;
        font-family: 'Georgia', serif;
        color: #f1f5f9;
    }

    .book-header {
        font-family: 'Cinzel', 'Georgia', serif;
        font-size: 2.2rem;
        font-weight: 700;
        color: #f8fafc;
        margin-bottom: 4px;
    }

    .translation-sub {
        color: #94a3b8;
        font-size: 0.95rem;
        font-style: italic;
        margin-bottom: 20px;
    }

    /* Botão de Referências Cruzadas (Ícone Sem Borda e Tamanho Ampliado) */
    button[kind="tertiary"] {
        border: none !important;
        background: transparent !important;
        box-shadow: none !important;
        padding: 0px 4px !important;
        min-height: auto !important;
        height: auto !important;
        line-height: 1 !important;
        transition: transform 0.15s ease, background-color 0.15s ease;
    }

    button[kind="tertiary"] p,
    button[kind="tertiary"] span {
        font-size: 1.35rem !important;
        line-height: 1 !important;
        display: inline-block !important;
    }

    button[kind="tertiary"]:hover {
        background: rgba(56, 189, 248, 0.15) !important;
        transform: scale(1.25);
        border-radius: 6px;
    }

    /* Caixa de Referências TSK */
    .ref-box {
        background-color: #131c31;
        border-left: 4px solid #38bdf8;
        padding: 14px;
        margin-top: 12px;
        border-radius: 0 8px 8px 0;
        border: 1px solid #233252;
        border-left-width: 4px;
    }

    .ref-title {
        font-weight: 700;
        color: #38bdf8;
        margin-bottom: 8px;
        font-size: 1rem;
        border-bottom: 1px solid #233252;
        padding-bottom: 4px;
    }

    .ref-item {
        font-size: 0.9rem;
        margin-bottom: 6px;
        color: #cbd5e1;
    }

    /* Context Card de Época */
    .context-card {
        background: linear-gradient(135deg, #0d1527 0%, #15223e 100%);
        border: 1px solid #283a61;
        border-radius: 8px;
        padding: 14px 18px;
        margin-bottom: 20px;
    }

    .context-title {
        font-size: 0.85rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        color: #fbbf24;
        display: flex;
        align-items: center;
        gap: 6px;
        margin-bottom: 6px;
    }

    .context-meta {
        font-size: 0.9rem;
        color: #94a3b8;
        line-height: 1.5;
    }

    /* Badges */
    .badge-chip {
        display: inline-flex;
        align-items: center;
        gap: 4px;
        background: rgba(56, 189, 248, 0.15);
        color: #38bdf8;
        border: 1px solid rgba(56, 189, 248, 0.3);
        border-radius: 12px;
        padding: 2px 8px;
        font-size: 0.75rem;
        font-weight: 600;
        margin-right: 4px;
    }

    .badge-gold {
        background: rgba(245, 158, 11, 0.15);
        color: #fbbf24;
        border-color: rgba(245, 158, 11, 0.3);
    }

    .badge-green {
        background: rgba(16, 185, 129, 0.15);
        color: #34d399;
        border-color: rgba(16, 185, 129, 0.3);
    }

    /* Cards de Personagens */
    .person-card {
        background: #131c31;
        border: 1px solid #233252;
        border-radius: 8px;
        padding: 14px;
        margin-bottom: 12px;
        transition: border-color 0.2s;
    }

    .person-card:hover {
        border-color: #38bdf8;
    }

    .person-name {
        font-size: 1.1rem;
        font-weight: 700;
        color: #f8fafc;
    }

    .person-dates {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.85rem;
        color: #fbbf24;
        margin-bottom: 6px;
    }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# CONEXÃO COM OS BANCOS DE DADOS
# ==============================================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BIBLIA_DB_PATH = os.path.join(BASE_DIR, "biblia.db")
TIMELINE_DB_PATH = os.path.join(BASE_DIR, "timeline.db")

@st.cache_resource
def get_biblia_connection():
    """Conecta ao banco biblia.db decodificando corretamente o texto em UTF-8."""
    if not os.path.exists(BIBLIA_DB_PATH):
        zip_p = os.path.join(BASE_DIR, "biblia.db.zip")
        if os.path.exists(zip_p):
            import zipfile
            with zipfile.ZipFile(zip_p, 'r') as z:
                z.extractall(BASE_DIR)
    conn = sqlite3.connect(BIBLIA_DB_PATH, check_same_thread=False)
    conn.text_factory = lambda b: b.decode('utf-8', errors='replace') if isinstance(b, bytes) else b
    return conn

@st.cache_resource
def get_timeline_connection():
    """Conecta ao banco timeline.db."""
    conn = sqlite3.connect(TIMELINE_DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

conn_biblia = get_biblia_connection()
conn_timeline = get_timeline_connection()

# ==============================================================================
# FUNÇÕES DE ACESSO A DADOS (BIBLIA.DB)
# ==============================================================================
@st.cache_data
def get_languages():
    """Retorna apenas as traduções que possuem texto cadastrado no banco."""
    query = """
        SELECT v.vrs_id, v.Abrev, v.vrs_nome 
        FROM versoes v
        WHERE EXISTS (
            SELECT 1 FROM versiculos ver 
            WHERE ver.ver_vrs_id = v.vrs_id 
              AND ver.ver_texto IS NOT NULL 
              AND length(trim(ver.ver_texto)) > 0
        )
        ORDER BY v.vrs_id
    """
    return pd.read_sql(query, conn_biblia)

@st.cache_data
def get_books(vrs_id):
    """Retorna estritamente os livros que possuem texto para a tradução selecionada."""
    query = f"""
        SELECT DISTINCT l.liv_id as b, l.liv_nome as n 
        FROM livros l
        JOIN versiculos v ON l.liv_id = v.ver_liv_id
        WHERE v.ver_vrs_id = {vrs_id}
          AND v.ver_texto IS NOT NULL
          AND length(trim(v.ver_texto)) > 0
        ORDER BY l.liv_id
    """
    return pd.read_sql(query, conn_biblia)

@st.cache_data
def get_chapters(book_id, vrs_id):
    """Retorna estritamente os capítulos que possuem versículos com texto para o livro e tradução."""
    query = f"""
        SELECT DISTINCT ver_capitulo as c 
        FROM versiculos 
        WHERE ver_liv_id = {book_id} 
          AND ver_vrs_id = {vrs_id}
          AND ver_texto IS NOT NULL
          AND length(trim(ver_texto)) > 0
        ORDER BY c
    """
    res = pd.read_sql(query, conn_biblia)['c'].tolist()
    return res if res else [1]

def get_verses(book_id, chapter, vrs_id):
    """Carrega os versículos com texto válido ordenados por número."""
    query = f"""
        SELECT ver_versiculo as v, ver_texto as t 
        FROM versiculos 
        WHERE ver_liv_id = {book_id} 
          AND ver_capitulo = {chapter} 
          AND ver_vrs_id = {vrs_id}
          AND ver_texto IS NOT NULL
          AND length(trim(ver_texto)) > 0
        ORDER BY v
    """
    return pd.read_sql(query, conn_biblia)

def get_cross_references(book_id, chapter, verse_num, vrs_id):
    if isinstance(vrs_id, int) or (isinstance(vrs_id, str) and str(vrs_id).isdigit()):
        query = f"""
            SELECT l.liv_nome as book_name, v.ver_capitulo as chapter, v.ver_versiculo as verse_num, v.ver_texto as text
            FROM referencias r
            JOIN versiculos v ON v.ver_liv_id = r.destino_liv_id
                             AND v.ver_capitulo = r.destino_capitulo
                             AND v.ver_versiculo >= r.destino_versiculo_start
                             AND v.ver_versiculo <= r.destino_versiculo_end
            JOIN livros l ON v.ver_liv_id = l.liv_id
            WHERE r.origem_liv_id = {int(book_id)} 
              AND r.origem_capitulo = {int(chapter)} 
              AND r.origem_versiculo = {int(verse_num)}
              AND v.ver_vrs_id = {int(vrs_id)}
            ORDER BY r.votos DESC
            LIMIT 10
        """
        return pd.read_sql(query, conn_biblia)
    elif isinstance(vrs_id, str) and vrs_id.startswith("ext:"):
        trans_code = vrs_id.replace("ext:", "")
        db_path = os.path.join(BASE_DIR, "base_biblias", f"{trans_code}.db")
        
        ref_query = f"""
            SELECT r.destino_liv_id, l.liv_nome as default_book_name, r.destino_capitulo, 
                   r.destino_versiculo_start, r.destino_versiculo_end, r.votos
            FROM referencias r
            JOIN livros l ON r.destino_liv_id = l.liv_id
            WHERE r.origem_liv_id = {int(book_id)}
              AND r.origem_capitulo = {int(chapter)}
              AND r.origem_versiculo = {int(verse_num)}
            ORDER BY r.votos DESC
            LIMIT 10
        """
        df_refs = pd.read_sql(ref_query, conn_biblia)
        if df_refs.empty or not os.path.exists(db_path):
            return pd.DataFrame(columns=["book_name", "chapter", "verse_num", "text"])
            
        ext_conn = sqlite3.connect(db_path)
        cur = ext_conn.cursor()
        
        cur.execute(f"SELECT id, name FROM {trans_code}_books")
        b_rows = cur.fetchall()
        b_map = {row[0]: row[1] for row in b_rows}
        
        results = []
        for _, row in df_refs.iterrows():
            dest_b = int(row['destino_liv_id'])
            dest_c = int(row['destino_capitulo'])
            v_start = int(row['destino_versiculo_start'])
            v_end = int(row['destino_versiculo_end'])
            b_name = b_map.get(dest_b, row['default_book_name'])
            
            cur.execute(f"""
                SELECT verse, text FROM {trans_code}_verses
                WHERE book_id = ? AND chapter = ? AND verse >= ? AND verse <= ?
                ORDER BY verse
            """, (dest_b, dest_c, v_start, v_end))
            v_rows = cur.fetchall()
            for vr in v_rows:
                results.append({
                    "book_name": b_name,
                    "chapter": dest_c,
                    "verse_num": vr[0],
                    "text": vr[1]
                })
        ext_conn.close()
        return pd.DataFrame(results)
    return pd.DataFrame(columns=["book_name", "chapter", "verse_num", "text"])

def search_verses(keyword, vrs_id):
    if isinstance(vrs_id, int) or (isinstance(vrs_id, str) and vrs_id.isdigit()):
        query = """
            SELECT l.liv_nome as book_name, v.ver_capitulo as chapter, v.ver_versiculo as verse_num, v.ver_texto as text
            FROM versiculos v
            JOIN livros l ON v.ver_liv_id = l.liv_id
            WHERE v.ver_vrs_id = ? AND v.ver_texto LIKE ?
            ORDER BY v.ver_liv_id, v.ver_capitulo, v.ver_versiculo
            LIMIT 50
        """
        return pd.read_sql(query, conn_biblia, params=(int(vrs_id), f"%{keyword}%"))
    elif isinstance(vrs_id, str) and vrs_id.startswith("ext:"):
        trans_code = vrs_id.replace("ext:", "")
        db_path = os.path.join(BASE_DIR, "base_biblias", f"{trans_code}.db")
        if not os.path.exists(db_path):
            return pd.DataFrame()
        conn = sqlite3.connect(db_path)
        query = f"""
            SELECT b.name as book_name, v.chapter as chapter, v.verse as verse_num, v.text as text
            FROM {trans_code}_verses v
            JOIN {trans_code}_books b ON v.book_id = b.id
            WHERE v.text LIKE ?
            ORDER BY v.book_id, v.chapter, v.verse
            LIMIT 50
        """
        df = pd.read_sql(query, conn, params=(f"%{keyword}%",))
        conn.close()
        return df
    return pd.DataFrame()

@st.cache_data
def get_book_stats(book_id, vrs_id):
    query = f"SELECT COUNT(*) as t FROM versiculos WHERE ver_liv_id={book_id} AND ver_vrs_id={vrs_id}"
    return pd.read_sql(query, conn_biblia).iloc[0]['t']

def get_verses_with_refs(book_id, chapter):
    try:
        q = f"SELECT DISTINCT origem_versiculo FROM referencias WHERE origem_liv_id={book_id} AND origem_capitulo={chapter}"
        return pd.read_sql(q, conn_biblia)['origem_versiculo'].tolist()
    except Exception:
        return []

# ==============================================================================
# CONECTOR UNIVERSAL: BIBLIOTECA GLOBAL DE 141 TRADUÇÕES (BASE_BIBLIAS)
# ==============================================================================
@st.cache_data
def get_catalogo_base_biblias():
    """Carrega o catálogo metadata das 141 bíblias em formato SQLite na pasta base_biblias."""
    p = os.path.join(BASE_DIR, "base_biblias", "catalogo_biblias.json")
    if os.path.exists(p):
        with open(p, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

# Mapeamentos canônicos para bíblias externas
BIB_TO_VULG_MAP = {
    1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8, 9: 9, 10: 10,
    11: 11, 12: 12, 13: 13, 14: 14, 15: 15, 16: 16, 17: 19, 18: 20,
    19: 21, 20: 22, 21: 23, 22: 24, 23: 27, 24: 28, 25: 29, 26: 31,
    27: 32, 28: 33, 29: 34, 30: 35, 31: 36, 32: 37, 33: 38, 34: 39,
    35: 40, 36: 41, 37: 42, 38: 43, 39: 44, 40: 47, 41: 48, 42: 49,
    43: 50, 44: 51, 45: 52, 46: 53, 47: 54, 48: 55, 49: 56, 50: 57,
    51: 58, 52: 59, 53: 60, 54: 61, 55: 62, 56: 63, 57: 64, 58: 65,
    59: 66, 60: 67, 61: 68, 62: 69, 63: 70, 64: 71, 65: 72, 66: 73,
    67: 74, 68: 75, 69: 17, 70: 18, 71: 25, 72: 26, 74: 30, 75: 45,
    76: 46, 78: 76, 86: 77, 87: 78
}

BIB_TO_AVE_MAP = {
    1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8, 9: 9, 10: 10,
    11: 11, 12: 12, 13: 13, 14: 14, 15: 15, 16: 16, 17: 19, 18: 20,
    19: 21, 20: 24, 21: 25, 22: 26, 23: 29, 24: 30, 25: 31, 26: 33,
    27: 34, 28: 35, 29: 36, 30: 37, 31: 38, 32: 39, 33: 40, 34: 41,
    35: 42, 36: 43, 37: 44, 38: 45, 39: 46, 40: 47, 41: 48, 42: 49,
    43: 50, 44: 51, 45: 52, 46: 53, 47: 54, 48: 55, 49: 56, 50: 57,
    51: 58, 52: 59, 53: 60, 54: 61, 55: 62, 56: 63, 57: 64, 58: 65,
    59: 66, 60: 67, 61: 68, 62: 69, 63: 70, 64: 71, 65: 72, 66: 73,
    69: 17, 70: 18, 71: 27, 72: 28, 74: 32, 75: 22, 76: 23
}

def get_external_verses(trans_code, livro_id, capitulo):
    """Lê diretamente versículos do arquivo SQLite na pasta base_biblias."""
    db_path = os.path.join(BASE_DIR, "base_biblias", f"{trans_code}.db")
    if not os.path.exists(db_path):
        return pd.DataFrame(columns=['v', 't'])
    
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute(f"SELECT count(*) FROM {trans_code}_books")
    n_books = cur.fetchone()[0]
    
    target_book_id = livro_id
    if n_books == 78:
        target_book_id = BIB_TO_VULG_MAP.get(livro_id, livro_id)
    elif n_books == 73 and trans_code == "AveMaria":
        target_book_id = BIB_TO_AVE_MAP.get(livro_id, livro_id)
    
    query = f"SELECT verse as v, text as t FROM {trans_code}_verses WHERE book_id = ? AND chapter = ? AND length(trim(text)) > 0 ORDER BY verse"
    df = pd.read_sql(query, conn, params=(target_book_id, capitulo))
    conn.close()
    return df

def get_universal_verses(livro_id, capitulo, vrs_id):
    """Encaminha a busca para biblia.db ou para base_biblias/*.db de forma transparente."""
    if isinstance(vrs_id, int) or (isinstance(vrs_id, str) and vrs_id.isdigit()):
        return get_verses(livro_id, capitulo, int(vrs_id))
    elif isinstance(vrs_id, str) and vrs_id.startswith("ext:"):
        trans_code = vrs_id.replace("ext:", "")
        return get_external_verses(trans_code, livro_id, capitulo)
    return pd.DataFrame(columns=['v', 't'])

@st.cache_data
def get_universal_books(vrs_id):
    """Retorna os livros disponíveis para a tradução selecionada (central ou externa)."""
    if isinstance(vrs_id, int) or (isinstance(vrs_id, str) and vrs_id.isdigit()):
        return get_books(int(vrs_id))
    elif isinstance(vrs_id, str) and vrs_id.startswith("ext:"):
        trans_code = vrs_id.replace("ext:", "")
        db_path = os.path.join(BASE_DIR, "base_biblias", f"{trans_code}.db")
        if not os.path.exists(db_path):
            return get_books(2)
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute(f"SELECT count(*) FROM {trans_code}_books")
        n_books = cur.fetchone()[0]
        conn.close()
        
        if n_books == 78:
            q = "SELECT liv_id as b, liv_nome as n FROM livros WHERE liv_id IN (1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,74,75,76,78,86,87) ORDER BY liv_id"
            return pd.read_sql(q, conn_biblia)
        elif n_books == 73:
            q = "SELECT liv_id as b, liv_nome as n FROM livros WHERE (liv_id BETWEEN 1 AND 66) OR liv_id IN (69,70,71,72,74,75,76) ORDER BY liv_id"
            return pd.read_sql(q, conn_biblia)
        elif n_books <= 39 and trans_code in ("WLC", "MapM", "JPS"):
            q = "SELECT liv_id as b, liv_nome as n FROM livros WHERE liv_id BETWEEN 1 AND 39 ORDER BY liv_id"
            return pd.read_sql(q, conn_biblia)
        elif n_books <= 27 and trans_code in ("TR", "Byz", "StatResGNT"):
            q = "SELECT liv_id as b, liv_nome as n FROM livros WHERE liv_id BETWEEN 40 AND 66 ORDER BY liv_id"
            return pd.read_sql(q, conn_biblia)
        else:
            q = "SELECT liv_id as b, liv_nome as n FROM livros WHERE liv_id BETWEEN 1 AND 66 ORDER BY liv_id"
            return pd.read_sql(q, conn_biblia)
    return get_books(2)

@st.cache_data
def get_universal_chapters(book_id, vrs_id):
    """Retorna os capítulos disponíveis para o livro e tradução selecionados."""
    if isinstance(vrs_id, int) or (isinstance(vrs_id, str) and vrs_id.isdigit()):
        return get_chapters(book_id, int(vrs_id))
    elif isinstance(vrs_id, str) and vrs_id.startswith("ext:"):
        trans_code = vrs_id.replace("ext:", "")
        db_path = os.path.join(BASE_DIR, "base_biblias", f"{trans_code}.db")
        if not os.path.exists(db_path):
            return [1]
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute(f"SELECT count(*) FROM {trans_code}_books")
        n_books = cur.fetchone()[0]
        target_book_id = book_id
        if n_books == 78:
            target_book_id = BIB_TO_VULG_MAP.get(book_id, book_id)
        elif n_books == 73 and trans_code == "AveMaria":
            target_book_id = BIB_TO_AVE_MAP.get(book_id, book_id)
        
        cur.execute(f"SELECT DISTINCT chapter FROM {trans_code}_verses WHERE book_id = ? AND length(trim(text)) > 0 ORDER BY chapter", (target_book_id,))
        res = [r[0] for r in cur.fetchall()]
        conn.close()
        return res if res else [1]
    return [1]

def get_universal_book_stats(book_id, vrs_id):
    """Retorna total de versículos para o livro e versão selecionados."""
    if isinstance(vrs_id, int) or (isinstance(vrs_id, str) and vrs_id.isdigit()):
        return get_book_stats(book_id, int(vrs_id))
    elif isinstance(vrs_id, str) and vrs_id.startswith("ext:"):
        trans_code = vrs_id.replace("ext:", "")
        db_path = os.path.join(BASE_DIR, "base_biblias", f"{trans_code}.db")
        if not os.path.exists(db_path):
            return 0
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute(f"SELECT count(*) FROM {trans_code}_books")
        n_books = cur.fetchone()[0]
        target_book_id = book_id
        if n_books == 78:
            target_book_id = BIB_TO_VULG_MAP.get(book_id, book_id)
        elif n_books == 73 and trans_code == "AveMaria":
            target_book_id = BIB_TO_AVE_MAP.get(book_id, book_id)
        
        cur.execute(f"SELECT count(*) FROM {trans_code}_verses WHERE book_id = ? AND length(trim(text)) > 0", (target_book_id,))
        res = cur.fetchone()[0]
        conn.close()
        return res
    return 0

def get_short_translation_label(name):
    """Extrai uma sigla/rótulo limpo da tradução para cabeçalhos e colunas."""
    if not name: return ""
    name_clean = str(name).replace("🌐 ", "")
    if "[" in name_clean and "]" in name_clean:
        return name_clean.split("[")[-1].replace("]", "").strip()
    if "(" in name_clean and ")" in name_clean:
        return name_clean.split("(")[-1].replace(")", "").strip()
    return name_clean

# ==============================================================================
# FUNÇÕES DE ACESSO A DADOS (TIMELINE.DB) - CONTEXTO HISTÓRICO & PERSONAGENS
# ==============================================================================
@st.cache_data
def get_contexto_livro(nome_livro):
    """Busca os metadados históricos e canônicos do livro no timeline.db."""
    # Mapeamento para nomes padrão
    nome_busca = nome_livro
    if "Samuel" in nome_livro: nome_busca = "Samuel"
    elif "Reis" in nome_livro: nome_busca = "Reis"
    elif "Crônicas" in nome_livro: nome_busca = "Crônicas"

    cur = conn_timeline.cursor()
    cur.execute("SELECT * FROM livros WHERE nome LIKE ? LIMIT 1", (f"%{nome_busca}%",))
    row = cur.fetchone()
    if row:
        livro_id = row["id"]
        cur.execute("SELECT tradicao, status, motivo_justificativa FROM status_canonico WHERE livro_id = ?", (livro_id,))
        status_rows = cur.fetchall()
        return dict(row), [dict(s) for s in status_rows]
    return None, []

@st.cache_data
def get_personagens_por_livro(nome_livro):
    """Retorna os personagens, reis ou profetas bíblicos associados ao livro."""
    cur = conn_timeline.cursor()
    
    tags_map = {
        "Gênesis": ["antediluviano", "patriarca"],
        "Êxodo": ["patriarca", "moises", "exodo"],
        "Levítico": ["patriarca", "arao"],
        "Números": ["patriarca", "moises", "josue"],
        "Deuteronômio": ["patriarca", "moises"],
        "Josué": ["josue", "patriarca"],
        "Juízes": ["juiz"],
        "I Samuel": ["samuel", "saul", "davi", "juiz"],
        "II Samuel": ["davi", "rei_israel"],
        "I Reis": ["salomao", "elias", "acabe", "rei_israel", "rei_juda"],
        "II Reis": ["eliseu", "ezequias", "josias", "rei_israel", "rei_juda", "queda_jerusalem"],
        "Isaías": ["isaias", "profeta", "ezequias", "senaqueribe"],
        "Jeremias": ["jeremias", "profeta", "josias", "zedequias", "exilio"],
        "Ezequiel": ["ezequiel", "profeta", "exilio"],
        "Daniel": ["daniel", "profeta", "exilio", "babilonia", "persia"],
        "Mateus": ["jesus", "joao_batista", "roma"],
        "Marcos": ["jesus", "roma"],
        "Lucas": ["jesus", "joao_batista", "roma"],
        "João": ["jesus", "roma"]
    }
    
    categorias = tags_map.get(nome_livro, [])
    if not categorias:
        return []
    
    placeholders = ",".join(["?"] * len(categorias))
    query = f"""
        SELECT * FROM eventos 
        WHERE categoria IN ({placeholders}) 
           OR tags LIKE ?
        ORDER BY ano_inicio ASC
        LIMIT 8
    """
    params = categorias + [f"%{nome_livro.lower()}%"]
    cur.execute(query, params)
    return [dict(r) for r in cur.fetchall()]

@st.cache_data
def get_todos_personagens():
    """Retorna o catálogo completo de personagens, reis e profetas."""
    cur = conn_timeline.cursor()
    cur.execute("""
        SELECT * FROM eventos 
        WHERE categoria IN ('antediluviano', 'patriarca', 'juiz', 'rei_israel', 'rei_juda', 'profeta')
        ORDER BY ano_inicio ASC
    """)
    return [dict(r) for r in cur.fetchall()]

@st.cache_data
def get_eventos_por_epoca(ano):
    """Busca o confronto dos 4 eixos para um determinado ano."""
    cur = conn_timeline.cursor()
    cur.execute("""
        SELECT e.*, x.codigo as eixo_codigo, x.nome as eixo_nome, x.cor_hex
        FROM eventos e
        JOIN eixos x ON e.eixo_id = x.id
        WHERE ? >= e.ano_inicio AND ? <= COALESCE(e.ano_fim, e.ano_inicio)
        ORDER BY e.eixo_id ASC
    """, (ano, ano))
    return [dict(r) for r in cur.fetchall()]

# Mapeamento para navegação da timeline para o leitor bíblico com ID canônico
PASSAGEM_MAP = {
    "Adão": ("Gênesis", 1, 1),
    "Eva": ("Gênesis", 2, 1),
    "Sete": ("Gênesis", 4, 1),
    "Enoque": ("Gênesis", 5, 1),
    "Matusalém": ("Gênesis", 5, 1),
    "Noé": ("Gênesis", 6, 1),
    "Abraão": ("Gênesis", 12, 1),
    "Isaque": ("Gênesis", 21, 1),
    "Jacó": ("Gênesis", 28, 1),
    "José do Egito": ("Gênesis", 37, 1),
    "Moisés": ("Êxodo", 3, 2),
    "Josué": ("Josué", 1, 6),
    "Débora": ("Juízes", 4, 7),
    "Gideão": ("Juízes", 6, 7),
    "Sansão": ("Juízes", 13, 7),
    "Samuel": ("I Samuel", 3, 9),
    "Rei Saul": ("I Samuel", 9, 9),
    "Rei Davi": ("I Samuel", 16, 9),
    "Rei Salomão": ("I Reis", 1, 11),
    "Rei Acabe": ("I Reis", 16, 11),
    "Rei Ezequias": ("II Reis", 18, 12),
    "Rei Josias": ("II Reis", 22, 12),
    "Profeta Elias": ("I Reis", 17, 11),
    "Profeta Eliseu": ("II Reis", 2, 12),
    "Profeta Isaías": ("Isaías", 1, 23),
    "Profeta Jeremias": ("Jeremias", 1, 24),
    "Profeta Ezequiel": ("Ezequiel", 1, 26),
    "Profeta Daniel": ("Daniel", 1, 27),
    "João Batista": ("Mateus", 3, 40),
    "Jesus": ("Mateus", 5, 40)
}

BOOK_TO_ERA_MAP = {
    1: -2066, 2: -1446, 3: -1446, 4: -1446, 5: -1446,
    6: -1400, 7: -1200, 8: -1100, 9: -1010, 10: -1000,
    11: -970, 12: -853, 13: -1000, 14: -853, 15: -538,
    16: -445, 17: -480, 18: -2000, 19: -1000, 20: -970,
    21: -970, 22: -970, 23: -740, 24: -587, 25: -587,
    26: -587, 27: -587, 40: 30, 41: 30, 42: 30, 43: 30,
    44: 50, 45: 57, 66: 95
}

def abrir_passagem(livro, capitulo, livro_id=None):
    st.session_state["target_nav_livro"] = livro
    st.session_state["target_nav_livro_id"] = livro_id
    st.session_state["target_nav_capitulo"] = capitulo
    st.session_state["aba_ativa"] = "📖 Leitor Bíblico & TSK"
    st.toast(f"📖 Navegando para {livro} {capitulo} no Leitor Bíblico...", icon="📖")

# ==============================================================================
# SIDEBAR DE NAVEGAÇÃO BÍBLICA
# ==============================================================================
st.sidebar.markdown("<h2 style='color:#38bdf8; font-family:Cinzel,serif;'>📖 Leitor Bíblico</h2>", unsafe_allow_html=True)
st.sidebar.caption("Navegue pelas traduções, capítulos e referências cruzadas.")
st.sidebar.divider()

df_idiomas = get_languages()
idiomas_dict = {row['vrs_id']: f"{row['vrs_nome']} ({row['Abrev']})" for _, row in df_idiomas.iterrows()}
idiomas_ids = list(idiomas_dict.keys())

# Catálogo das bíblias em base_biblias
catalogo_base = get_catalogo_base_biblias()
ext_dict = {}
for item in catalogo_base:
    key = f"ext:{item['codigo']}"
    ext_dict[key] = f"🌐 {item['titulo']} [{item['codigo']}]"

idiomas_dict_completo = {**idiomas_dict, **ext_dict}

import unicodedata

def sort_bible_key(opt):
    label = idiomas_dict_completo.get(opt, "")
    limpo = str(label).replace("🌐", "").strip().lower()
    return unicodedata.normalize('NFKD', limpo).encode('ASCII', 'ignore').decode('utf-8')

todas_opcoes_ordenadas = sorted(idiomas_ids + list(ext_dict.keys()), key=sort_bible_key)
opcoes_primarias = todas_opcoes_ordenadas
opcoes_secundarias = [0] + todas_opcoes_ordenadas

default_p_idx = opcoes_primarias.index(2) if 2 in opcoes_primarias else 0

idioma_primario = st.sidebar.selectbox(
    "Tradução Principal:", 
    opcoes_primarias,
    index=default_p_idx,
    format_func=lambda x: idiomas_dict_completo.get(x, str(x)),
    key="sb_idioma_primario"
)

idioma_secundario = st.sidebar.selectbox(
    "Tradução Paralela (Opcional):", 
    opcoes_secundarias,
    format_func=lambda x: "Nenhuma" if x == 0 else idiomas_dict_completo.get(x, str(x)),
    key="sb_idioma_secundario"
)

# Carrega estritamente os livros que EXISTEM COM TEXTO nesta tradução específica
df_livros = get_universal_books(idioma_primario)
livros_dict = dict(zip(df_livros['n'], df_livros['b']))
livros_lista = list(livros_dict.keys())

# Se a tradução não tiver livros válidos (caso de segurança)
if not livros_lista:
    livros_lista = ["Indisponível"]
    livros_dict = {"Indisponível": 1}

# Tratamento seguro de navegação antes da instanciação dos widgets
id_to_book_name = dict(zip(df_livros['b'], df_livros['n']))
if "target_nav_livro_id" in st.session_state and st.session_state["target_nav_livro_id"]:
    target_lid = st.session_state.pop("target_nav_livro_id")
    target_c = st.session_state.pop("target_nav_capitulo", 1)
    st.session_state.pop("target_nav_livro", None)
    if target_lid in id_to_book_name:
        st.session_state["sb_livro"] = id_to_book_name[target_lid]
        st.session_state["sb_capitulo"] = target_c
elif "target_nav_livro" in st.session_state and st.session_state["target_nav_livro"]:
    target_l = st.session_state.pop("target_nav_livro")
    target_c = st.session_state.pop("target_nav_capitulo", 1)
    if target_l in livros_lista:
        st.session_state["sb_livro"] = target_l
        st.session_state["sb_capitulo"] = target_c
    else:
        matched = next((l for l in livros_lista if target_l.lower() in l.lower() or l.lower() in target_l.lower()), None)
        if matched:
            st.session_state["sb_livro"] = matched
            st.session_state["sb_capitulo"] = target_c

# Se o livro atualmente em sessão NÃO existir na tradução selecionada, ajusta para o primeiro disponível
if st.session_state.get("sb_livro") not in livros_lista:
    st.session_state["sb_livro"] = livros_lista[0]

col_livro, col_cap = st.sidebar.columns([3, 2])
with col_livro:
    livro_nome = st.selectbox("Livro:", livros_lista, key="sb_livro")
    livro_id = livros_dict.get(livro_nome, 1)

with col_cap:
    # Carrega estritamente os capítulos que EXISTEM COM TEXTO neste livro para a tradução selecionada
    capitulos = get_universal_chapters(livro_id, idioma_primario)
    if not capitulos:
        capitulos = [1]
    
    # Se o capítulo atualmente em sessão NÃO existir neste livro e tradução, ajusta para o primeiro
    if st.session_state.get("sb_capitulo") not in capitulos:
        st.session_state["sb_capitulo"] = capitulos[0]

    capitulo_selecionado = st.selectbox("Capítulo:", capitulos, key="sb_capitulo")

st.sidebar.divider()
st.sidebar.markdown("<h4 style='color:#f8fafc;'>🔍 Pesquisa Rápida</h4>", unsafe_allow_html=True)
search_query = st.sidebar.text_input("Termo bíblico:", placeholder="Ex: Aliança, Fé, Graça...", key="search_query_input")

st.sidebar.divider()
st.sidebar.info("💡 **Integração:** Use as abas no topo para alternar entre o Texto Sagrado, a Linha do Tempo e o Catálogo de Personagens.")

# Estado de Sessão
if "verso_foco" not in st.session_state:
    st.session_state.verso_foco = 1
if "scroll_to_refs" not in st.session_state:
    st.session_state.scroll_to_refs = False

def ativar_ref(v_num):
    st.session_state.verso_foco = v_num
    st.session_state.scroll_to_refs = True

# ==============================================================================
# ABAS PRINCIPAIS DO APLICATIVO UNIFICADO (NAVEGAÇÃO TOTALMENTE SINCRONIZADA)
# ==============================================================================
LISTA_ABAS = [
    "📖 Leitor Bíblico & TSK", 
    "⏳ Linha do Tempo Histórica Comparada", 
    "⚡ Confronto de Épocas & Impérios", 
    "👤 Personagens, Reis & Profetas"
]

if "aba_ativa" not in st.session_state or st.session_state["aba_ativa"] not in LISTA_ABAS:
    st.session_state["aba_ativa"] = LISTA_ABAS[0]

aba_selecionada = st.segmented_control(
    "Navegação Principal",
    LISTA_ABAS,
    key="aba_ativa",
    label_visibility="collapsed"
)

if not aba_selecionada:
    aba_selecionada = st.session_state["aba_ativa"]

# ==============================================================================
# ABA 1: LEITOR BÍBLICO COM CONTEXTO HISTÓRICO
# ==============================================================================
if aba_selecionada == "📖 Leitor Bíblico & TSK":
    nome_extenso_1 = idiomas_dict_completo.get(idioma_primario, str(idioma_primario))

    # Tratamento de Pesquisa por Palavra-chave
    if search_query:
        st.markdown(f"<div class='book-header'>Pesquisa: '{search_query}'</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='translation-sub'>Tradução: {nome_extenso_1}</div>", unsafe_allow_html=True)
        st.divider()
        
        resultados = search_verses(search_query, idioma_primario)
        if not resultados.empty:
            st.success(f"Encontrados {len(resultados)} versículos para '{search_query}'.")
            
            def ir_para_busca(liv, cap):
                st.session_state["target_nav_livro"] = liv
                st.session_state["target_nav_capitulo"] = cap
                st.session_state["search_query_input"] = ""
                st.toast(f"📖 Navegando para {liv} {cap}...", icon="📖")

            for idx, r in resultados.iterrows():
                col_btn, col_txt = st.columns([1, 4])
                with col_btn:
                    st.button(
                        f"📖 {r['book_name']} {r['chapter']}:{r['verse_num']}", 
                        key=f"btn_s_{idx}",
                        on_click=ir_para_busca,
                        args=(r['book_name'], r['chapter'])
                    )
                with col_txt:
                    st.markdown(f"<div class='verse-text'>{r['text']}</div>", unsafe_allow_html=True)
        else:
            st.warning("Nenhum versículo encontrado com essa palavra na tradução selecionada.")
        st.stop()

    # Cabeçalho do Livro e Estatísticas
    total_capitulos = len(capitulos)
    total_versos = get_universal_book_stats(livro_id, idioma_primario)

    col_t, col_m1, col_m2 = st.columns([3, 1, 1])
    with col_t:
        st.markdown(f"<div class='book-header'>{livro_nome} {capitulo_selecionado}</div>", unsafe_allow_html=True)
        if idioma_secundario == 0:
            st.markdown(f"<div class='translation-sub'>Tradução: {nome_extenso_1}</div>", unsafe_allow_html=True)
        else:
            nome_extenso_2 = idiomas_dict_completo.get(idioma_secundario, str(idioma_secundario))
            st.markdown(f"<div class='translation-sub'>Traduções: {nome_extenso_1} | {nome_extenso_2}</div>", unsafe_allow_html=True)
    with col_m1:
        st.metric("Capítulos no Livro", total_capitulos)
    with col_m2:
        st.metric("Versículos no Livro", total_versos)

    # CARD DE CONTEXTO HISTÓRICO & PERSONAGENS DESTA ÉPOCA (SOLICITADO PELO USUÁRIO)
    meta_livro, status_livro = get_contexto_livro(livro_nome)
    personagens_ep = get_personagens_por_livro(livro_nome)

    with st.expander("🏛️ Contexto Histórico, Época & Personagens Deste Livro", expanded=False):
        col_hist1, col_hist2 = st.columns([2, 1])
        with col_hist1:
            if meta_livro:
                st.markdown(f"**Autor Tradicional:** {meta_livro.get('autor_tradicional', 'N/A')} | **Gênero:** {meta_livro.get('genero_literario', 'N/A')}")
                st.markdown(f"**Data de Composição Crítica:** {meta_livro.get('data_consenso_critico', 'N/A')}")
                if meta_livro.get('resumo'):
                    st.caption(f"{meta_livro['resumo']}")
            else:
                st.markdown(f"Livro canônico histórico da Escritura Sagrada.")

            if personagens_ep:
                st.markdown("**Personagens e Líderes Centrais Desta Época:**")
                chips_html = " ".join([f"<span class='badge-chip badge-gold'>👑 {p['titulo']}</span>" if 'rei' in p['categoria'] else f"<span class='badge-chip'>👤 {p['titulo']}</span>" for p in personagens_ep])
                st.markdown(chips_html, unsafe_allow_html=True)

            if livro_id in BOOK_TO_ERA_MAP:
                era_ano = BOOK_TO_ERA_MAP[livro_id]
                def ir_confronto_livro(ano):
                    st.session_state["custom_ano_confronto"] = int(ano)
                    st.session_state["num_ano_confronto"] = int(ano)
                    st.session_state["aba_ativa"] = "⚡ Confronto de Épocas & Impérios"
                    ano_txt = f"{abs(ano)} a.C." if ano < 0 else f"{ano} d.C."
                    st.toast(f"⚡ Abrindo Confronto de Épocas para {ano_txt}...", icon="⚡")
                st.write("")
                st.button(f"⚡ Explorar Época de {livro_nome} no Confronto Histórico", on_click=ir_confronto_livro, args=(era_ano,), help="Ver o que acontecia nos impérios e mitologias na época deste livro")

        with col_hist2:
            if status_livro:
                st.markdown("**Status Canônico nas Tradições:**")
                for s in status_livro:
                    st.markdown(f"• **{s['tradicao']}:** `{s['status']}`")

    st.divider()

    # Leitura dos Versículos & Referências TSK
    col_texto, col_refs = st.columns([2, 1], gap="large")

    def format_verse_html(v_num, text):
        if not text or text == "<i>[Versículo ausente]</i>" or str(text).startswith("<i>"):
            return f"<div class='verse-text' style='color:#64748b; font-style:italic;'><span class='verse-num'>{v_num}</span>{text}</div>"
        is_hebrew = any('\u0590' <= ch <= '\u05FF' for ch in str(text))
        if is_hebrew:
            return f"<div class='verse-text' dir='rtl' style='text-align:right; font-family:\"SBL Hebrew\", \"Ezra SIL\", \"David\", serif; font-size:1.35rem; line-height:2.0;'><span class='verse-num' style='float:left; margin-left:6px;'>{v_num}</span>{text}</div>"
        return f"<div class='verse-text'><span class='verse-num'>{v_num}</span>{text}</div>"

    with col_texto:
        refs_disponiveis = get_verses_with_refs(livro_id, capitulo_selecionado)
        if idioma_secundario == 0:
            df_versiculos = get_universal_verses(livro_id, capitulo_selecionado, idioma_primario)
            if df_versiculos.empty:
                st.info("Nenhum versículo com texto encontrado para este livro e capítulo nesta tradução.")
                versos_list = []
            else:
                versos_list = df_versiculos['v'].tolist()
                for _, row in df_versiculos.iterrows():
                    v_num = row['v']
                    if v_num in refs_disponiveis:
                        col_txt, col_btn = st.columns([0.94, 0.06])
                        with col_txt:
                            st.markdown(format_verse_html(v_num, row['t']), unsafe_allow_html=True)
                        with col_btn:
                            st.button("🔀", key=f"btn_tsk_{v_num}", on_click=ativar_ref, args=(v_num,), help="Ver referências cruzadas", type="tertiary")
                    else:
                        st.markdown(format_verse_html(v_num, row['t']), unsafe_allow_html=True)
        else:
            df_v1 = get_universal_verses(livro_id, capitulo_selecionado, idioma_primario)
            df_v2 = get_universal_verses(livro_id, capitulo_selecionado, idioma_secundario)
            
            if df_v1.empty and df_v2.empty:
                st.info("Nenhum versículo encontrado para este capítulo nas traduções selecionadas.")
                versos_list = []
            else:
                if df_v1.empty:
                    df_v1 = pd.DataFrame({'v': df_v2['v'], 't': ['<i>[Versículo ausente nesta tradução]</i>'] * len(df_v2)})
                if df_v2.empty:
                    df_v2 = pd.DataFrame({'v': df_v1['v'], 't': ['<i>[Versículo ausente nesta tradução]</i>'] * len(df_v1)})

                df_merged = pd.merge(df_v1[['v', 't']], df_v2[['v', 't']], on='v', how='outer', suffixes=('_1', '_2')).sort_values('v')
                df_merged['v'] = df_merged['v'].astype(int)
                
                c1, c2 = st.columns(2)
                c1.markdown(f"<h4 style='text-align: center; color: #38bdf8;'>{get_short_translation_label(nome_extenso_1)}</h4>", unsafe_allow_html=True)
                c2.markdown(f"<h4 style='text-align: center; color: #38bdf8;'>{get_short_translation_label(nome_extenso_2)}</h4>", unsafe_allow_html=True)
                st.markdown("<hr style='margin-top: 5px; margin-bottom: 15px;'>", unsafe_allow_html=True)
                
                versos_list = df_merged['v'].tolist()
                for _, row in df_merged.iterrows():
                    v_num = row['v']
                    t1 = row['t_1'] if pd.notna(row['t_1']) else "<i>[Versículo ausente]</i>"
                    t2 = row['t_2'] if pd.notna(row['t_2']) else "<i>[Versículo ausente]</i>"
                    
                    if v_num in refs_disponiveis:
                        c1_txt, c_btn, c2_txt = st.columns([0.47, 0.06, 0.47])
                        with c1_txt:
                            st.markdown(format_verse_html(v_num, t1), unsafe_allow_html=True)
                        with c_btn:
                            st.button("🔀", key=f"btn_tsk_d_{v_num}", on_click=ativar_ref, args=(v_num,), help="Ver referências cruzadas", type="tertiary")
                        with c2_txt:
                            st.markdown(format_verse_html(v_num, t2), unsafe_allow_html=True)
                    else:
                        c1_txt, _, c2_txt = st.columns([0.47, 0.06, 0.47])
                        with c1_txt:
                            st.markdown(format_verse_html(v_num, t1), unsafe_allow_html=True)
                        with c2_txt:
                            st.markdown(format_verse_html(v_num, t2), unsafe_allow_html=True)

        # Navegação Sequencial Rápida entre Capítulos (⬅️ Anterior / Próximo ➡️)
        st.markdown("<hr style='margin: 24px 0 16px 0; border-color: #233252;'>", unsafe_allow_html=True)
        col_nav_prev, col_nav_pos, col_nav_next = st.columns([1.2, 1.4, 1.2])
        
        curr_cap_idx = capitulos.index(capitulo_selecionado) if capitulo_selecionado in capitulos else 0
        has_prev_cap = curr_cap_idx > 0
        has_next_cap = curr_cap_idx < len(capitulos) - 1
        
        curr_liv_idx = livros_lista.index(livro_nome) if livro_nome in livros_lista else 0
        can_prev_book = curr_liv_idx > 0
        can_next_book = curr_liv_idx < len(livros_lista) - 1
        
        def mudar_capitulo(novo_cap, novo_livro=None):
            if novo_livro:
                st.session_state["sb_livro"] = novo_livro
            st.session_state["sb_capitulo"] = novo_cap
            
        with col_nav_prev:
            if has_prev_cap:
                p_cap = capitulos[curr_cap_idx - 1]
                st.button(f"⬅️ Cap. {p_cap}", key="btn_nav_prev_cap", on_click=mudar_capitulo, args=(p_cap,), use_container_width=True)
            elif can_prev_book:
                p_liv = livros_lista[curr_liv_idx - 1]
                st.button(f"⏮️ {p_liv}", key="btn_nav_prev_book", on_click=mudar_capitulo, args=(1, p_liv), use_container_width=True, help=f"Ir para o livro anterior ({p_liv})")
                
        with col_nav_pos:
            st.markdown(f"<div style='text-align:center; color:#94a3b8; font-size:0.95rem; font-weight:600; padding-top:6px;'>{livro_nome} {capitulo_selecionado} <span style='font-size:0.8rem; color:#64748b;'>({curr_cap_idx + 1}/{len(capitulos)})</span></div>", unsafe_allow_html=True)
            
        with col_nav_next:
            if has_next_cap:
                n_cap = capitulos[curr_cap_idx + 1]
                st.button(f"Cap. {n_cap} ➡️", key="btn_nav_next_cap", on_click=mudar_capitulo, args=(n_cap,), use_container_width=True)
            elif can_next_book:
                n_liv = livros_lista[curr_liv_idx + 1]
                st.button(f"{n_liv} ⏭️", key="btn_nav_next_book", on_click=mudar_capitulo, args=(1, n_liv), use_container_width=True, help=f"Avançar para o próximo livro ({n_liv})")

        # Recurso de Exportação de Capítulo em Markdown
        st.write("")
        with st.expander("📥 Exportar Este Capítulo para Markdown (.md)", expanded=False):
            md_text = f"# {livro_nome} - Capítulo {capitulo_selecionado}\n\n"
            if idioma_secundario == 0:
                md_text += f"*Tradução: {nome_extenso_1}*\n\n"
                if not df_versiculos.empty:
                    for _, r in df_versiculos.iterrows():
                        md_text += f"**{r['v']}.** {r['t']}\n\n"
            else:
                md_text += f"*Traduções Comparadas: {nome_extenso_1} | {nome_extenso_2}*\n\n"
                md_text += f"| Versículo | {get_short_translation_label(nome_extenso_1)} | {get_short_translation_label(nome_extenso_2)} |\n"
                md_text += "|:---:|:---|:---|\n"
                for _, r in df_merged.iterrows():
                    t1_clean = str(r['t_1']).replace('|', '/')
                    t2_clean = str(r['t_2']).replace('|', '/')
                    md_text += f"| **{r['v']}** | {t1_clean} | {t2_clean} |\n"
            st.download_button(
                label="💾 Baixar Arquivo .md (Obsidian / Notion)",
                data=md_text.encode('utf-8'),
                file_name=f"{livro_nome}_Cap_{capitulo_selecionado}.md",
                mime="text/markdown"
            )

    with col_refs:
        st.markdown("<div id='area-referencias'></div>", unsafe_allow_html=True)
        st.subheader("🔗 Referências Cruzadas (TSK)")
        st.caption("Selecione um versículo para visualizar conexões temáticas da Escritura.")
        
        if versos_list:
            if st.session_state.verso_foco not in versos_list:
                st.session_state.verso_foco = versos_list[0]
                
            verso_foco = st.selectbox("Versículo analisado:", versos_list, key="verso_foco")
            
            if verso_foco:
                refs = get_cross_references(livro_id, capitulo_selecionado, verso_foco, idioma_primario)
                if not refs.empty:
                    st.markdown(f"<div class='ref-box'><div class='ref-title'>Conexões para {livro_nome} {capitulo_selecionado}:{verso_foco}</div>", unsafe_allow_html=True)
                    for _, r in refs.iterrows():
                        st.markdown(f"<div class='ref-item'><b>{r['book_name']} {r['chapter']}:{r['verse_num']}</b> — {r['text'][:90]}...</div>", unsafe_allow_html=True)
                    st.markdown("</div>", unsafe_allow_html=True)
                else:
                    st.write("Nenhuma referência cruzada direta registrada para este versículo.")
        else:
            st.caption("Nenhum versículo disponível neste capítulo.")

# ==============================================================================
# ABA 2: LINHA DO TEMPO HISTÓRICA COMPARADA (VIS-TIMELINE EMBUTIDO)
# ==============================================================================
elif aba_selecionada == "⏳ Linha do Tempo Histórica Comparada":
    # Caminho do HTML gerado da timeline (já possui cabeçalho integrado e estilizado)
    html_timeline_path = os.path.join(BASE_DIR, "timeline_confronto.html")
    
    # Se o HTML não existir, gera a partir do SQLite
    if not os.path.exists(html_timeline_path):
        import gerador_timeline
        gerador_timeline.gerar_timeline_html()

    with open(html_timeline_path, "r", encoding="utf-8") as f:
        html_code = f.read()

    # Renderização responsiva do componente web
    components.html(html_code, height=920, scrolling=True)

# ==============================================================================
# ABA 3: CONFRONTO DE ÉPOCAS & IMPÉRIOS (CONSULTA SINÓPTICA RELACIONAL)
# ==============================================================================
elif aba_selecionada == "⚡ Confronto de Épocas & Impérios":
    st.markdown("<h3 style='color:#fbbf24; font-family:Cinzel,serif;'>⚡ Confronto Simultâneo de Épocas</h3>", unsafe_allow_html=True)
    st.caption("Escolha um momento da história da humanidade e examine instantaneamente o que acontecia nos 4 eixos em paralelo.")

    epocas_predefinidas = [
        ("4004 a.C. — Criação, Adão e Origens", -4004),
        ("2348 a.C. — O Grande Dilúvio e a Arca de Noé", -2348),
        ("2066 a.C. — Era Patriarcal: Nascimento de Isaque", -2066),
        ("1750 a.C. — Código de Hamurabi & Babilônia Antiga", -1750),
        ("1446 a.C. — O Êxodo do Egito e a Lei no Sinai", -1446),
        ("1200 a.C. — Período dos Juízes: Débora e Gideão", -1200),
        ("1010 a.C. — Reinado de Davi e Unificação de Israel", -1010),
        ("970 a.C. — Salomão e Construção do Primeiro Templo", -970),
        ("853 a.C. — Rei Acabe, Profeta Elias e Batalha de Qarqar", -853),
        ("722 a.C. — Queda de Samaria ante o Império Neoassírio", -722),
        ("587 a.C. — Cerco e Destruição de Jerusalém (Cativeiro Babilônico)", -587),
        ("538 a.C. — Edito de Ciro, o Grande e Retorno do Exílio", -538),
        ("250 a.C. — Tradução da Septuaginta (LXX) em Alexandria", -250),
        ("30 d.C. — Ministério e Crucificação de Jesus Cristo sob Pilatos", 30),
        ("70 d.C. — Destruição do 2º Templo por Tito e Guerra Judaica", 70),
        ("393 d.C. — Sínodo de Hipona e Santo Agostinho (Cânon Bíblico)", 393),
        ("1546 d.C. — Concílio de Trento: Fixação Dogmática do Cânon", 1546)
    ]

    # Se recebeu navegação externa de ano (vindo da Aba 4 ou Aba 1)
    if "custom_ano_confronto" in st.session_state:
        st.session_state["num_ano_confronto"] = int(st.session_state.pop("custom_ano_confronto"))
        
    dict_ep = dict(epocas_predefinidas)
    rev_dict_ep = {v: k for k, v in epocas_predefinidas}
    
    ano_atual = st.session_state.get("num_ano_confronto", -587)
    idx_padrao = 10
    if ano_atual in rev_dict_ep:
        idx_padrao = [e[1] for e in epocas_predefinidas].index(ano_atual)

    def on_change_sel_epoca():
        escolhida = st.session_state.get("sel_epoca_predefinida")
        if escolhida in dict_ep:
            st.session_state["num_ano_confronto"] = dict_ep[escolhida]

    col_sel_ep, col_custom_ano = st.columns([3, 1])
    with col_sel_ep:
        epoca_escolhida = st.selectbox(
            "Selecione uma Época Consagrada:", 
            [e[0] for e in epocas_predefinidas],
            index=idx_padrao,
            key="sel_epoca_predefinida",
            on_change=on_change_sel_epoca
        )
    
    with col_custom_ano:
        ano_digitado = st.number_input(
            "Ou digite um ano exato (a.C. negativo):", 
            value=ano_atual, 
            step=10,
            key="num_ano_confronto"
        )
        ano_alvo = int(ano_digitado)

    ano_legivel = f"{abs(ano_alvo)} a.C." if ano_alvo < 0 else f"{ano_alvo} d.C."
    
    col_hdr_ano, col_hdr_btn = st.columns([3, 1])
    with col_hdr_ano:
        st.markdown(f"<h4 style='color:#38bdf8; margin:0; padding-top:6px;'>Exame Sinóptico para o Ano: {ano_legivel}</h4>", unsafe_allow_html=True)
    with col_hdr_btn:
        def ir_para_timeline():
            st.session_state["aba_ativa"] = "⏳ Linha do Tempo Histórica Comparada"
            st.toast(f"⏳ Abrindo Linha do Tempo Histórica...", icon="⏳")
        st.button("⏳ Ver na Linha do Tempo", key="btn_ir_timeline_confronto", on_click=ir_para_timeline, use_container_width=True)
    st.divider()

    eventos_do_ano = get_eventos_por_epoca(ano_alvo)

    def render_cartao_confronto(it, cor_borda="#38bdf8", badge_tipo=None):
        ano_ini = f"{abs(it['ano_inicio'])} a.C." if it['ano_inicio'] < 0 else f"{it['ano_inicio']} d.C."
        ano_fim = f"{abs(it['ano_fim'])} a.C." if it.get('ano_fim') and it['ano_fim'] < 0 else (f"{it['ano_fim']} d.C." if it.get('ano_fim') else "")
        datas = f"{ano_ini} — {ano_fim}" if ano_fim else ano_ini
        
        badge_html = f"<span class='badge-chip'>{badge_tipo}</span>" if badge_tipo else ""
        
        origem = ""
        if it.get('localizacao'): origem = f"📍 {it['localizacao']}"
        elif it.get('cultura_origem'): origem = f"🏺 {it['cultura_origem']}"
        
        wiki_link = ""
        if it.get('wikipedia_url'):
            wiki_link = f"<div style='margin-top:6px;'><a href='{it['wikipedia_url']}' target='_blank' style='font-size:0.8rem; color:#38bdf8; text-decoration:none;'>🌐 Artigo na Wikipédia &rarr;</a></div>"
        
        fontes = ""
        if it.get('fontes_historicas'):
            fontes = f"<div style='font-size:0.78rem; color:#94a3b8; margin-top:4px;'><b>Fontes:</b> {it['fontes_historicas']}</div>"

        st.markdown(f"""
        <div style='background:#131c31; border:1px solid #233252; border-left:3.5px solid {cor_borda}; border-radius:8px; padding:12px; margin-bottom:12px;'>
            <div style='display:flex; justify-content:space-between; align-items:flex-start; gap:4px;'>
                <b style='color:#f8fafc; font-size:0.95rem;'>{it['titulo']}</b>
                {badge_html}
            </div>
            <div style='font-family:\"JetBrains Mono\",monospace; font-size:0.8rem; color:#fbbf24; margin:3px 0 6px 0;'>{datas}</div>
            <div style='font-size:0.86rem; color:#cbd5e1; line-height:1.55; margin-bottom:6px;'>{it['descricao']}</div>
            {f"<div style='font-size:0.8rem; color:#94a3b8;'>{origem}</div>" if origem else ""}
            {fontes}
            {wiki_link}
        </div>
        """, unsafe_allow_html=True)

    col_sec, col_bib, col_mit, col_can = st.columns(4)

    with col_sec:
        st.markdown("<h4 style='color:#0284c7; font-family:Cinzel,serif;'>🏛️ História Secular</h4>", unsafe_allow_html=True)
        sec_itens = [ev for ev in eventos_do_ano if ev['eixo_codigo'] == 'SECULAR']
        if sec_itens:
            for it in sec_itens:
                render_cartao_confronto(it, cor_borda="#0284c7", badge_tipo="IMPÉRIO")
        else:
            st.info("Nenhum grande império dominante registrado para este ano exato.")

    with col_bib:
        st.markdown("<h4 style='color:#d97706; font-family:Cinzel,serif;'>📜 Cronologia Bíblica</h4>", unsafe_allow_html=True)
        bib_itens = [ev for ev in eventos_do_ano if ev['eixo_codigo'] == 'BIBLICO']
        if bib_itens:
            for it in bib_itens:
                badge_cat = f"👑 {it['categoria'].upper()}" if 'rei' in it['categoria'] else f"👤 {it['categoria'].upper()}"
                render_cartao_confronto(it, cor_borda="#d97706", badge_tipo=badge_cat)
                nome_chave = next((k for k in PASSAGEM_MAP.keys() if k.lower() in it['titulo'].lower()), None)
                if nome_chave:
                    liv_target, cap_target, lid_target = PASSAGEM_MAP[nome_chave]
                    st.button(
                        f"📖 Ler no Leitor ({liv_target} {cap_target})",
                        key=f"btn_conf_{it['id']}",
                        on_click=abrir_passagem,
                        args=(liv_target, cap_target, lid_target)
                    )
        else:
            st.info("Nenhum marco bíblico cadastrado exatamente nesta baliza.")

    with col_mit:
        st.markdown("<h4 style='color:#7c3aed; font-family:Cinzel,serif;'>🏺 Mitologias & Mitos</h4>", unsafe_allow_html=True)
        mit_itens = [ev for ev in eventos_do_ano if ev['eixo_codigo'] == 'MITOLOGIA']
        if mit_itens:
            for it in mit_itens:
                render_cartao_confronto(it, cor_borda="#7c3aed", badge_tipo="MITO")
        else:
            st.info("Nenhuma cosmogonia específica datada para este ano.")

    with col_can:
        st.markdown("<h4 style='color:#059669; font-family:Cinzel,serif;'>⛪ Cânon & Concílios</h4>", unsafe_allow_html=True)
        can_itens = [ev for ev in eventos_do_ano if ev['eixo_codigo'] == 'CANON']
        if can_itens:
            for it in can_itens:
                badge_c = "CONCÍLIO" if it['categoria'] == 'concilio' else "CÂNON"
                render_cartao_confronto(it, cor_borda="#059669", badge_tipo=badge_c)
        else:
            st.info("Sem resoluções conciliares formais neste ano.")

# ==============================================================================
# ABA 4: CATÁLOGO DE PERSONAGENS, REIS & PROFETAS COM LINKS BÍBLICOS
# ==============================================================================
elif aba_selecionada == "👤 Personagens, Reis & Profetas":
    st.markdown("<h3 style='color:#38bdf8; font-family:Cinzel,serif;'>👤 Catálogo Histórico de Personagens Bíblicos</h3>", unsafe_allow_html=True)
    st.caption("Consulte Adão a Noé, Grandes Patriarcas, Juízes, Reis de Israel/Judá e Profetas com datas e referências bíblicas.")

    col_f_cat, col_f_busca = st.columns([2, 2])
    with col_f_cat:
        filtro_cat = st.selectbox(
            "Filtrar por Categoria:", 
            [
                "Todas as Categorias", 
                "🌱 Antediluvianos (Adão a Noé)", 
                "⛺ Grandes Patriarcas (Abraão a Josué)", 
                "⚖️ Juízes de Israel (Otniel a Samuel)", 
                "👑 Todos os Reis de Israel & Judá",
                "👑 Reis de Judá (Reino do Sul)",
                "👑 Reis de Israel (Reino do Norte)",
                "🔥 Profetas Bíblicos (Elias a João Batista)"
            ]
        )
    
    with col_f_busca:
        busca_nome = st.text_input("Buscar Personagem:", placeholder="Ex: Davi, Moisés, Isaías, Salomão...")

    todos_personagens = get_todos_personagens()

    # Aplicação de filtros
    personagens_filtrados = []
    for p in todos_personagens:
        cat = p['categoria']
        if filtro_cat.startswith("🌱") and cat != "antediluviano": continue
        if filtro_cat.startswith("⛺") and cat != "patriarca": continue
        if filtro_cat.startswith("⚖️") and cat != "juiz": continue
        if filtro_cat == "👑 Todos os Reis de Israel & Judá" and cat not in ("rei_israel", "rei_juda"): continue
        if filtro_cat == "👑 Reis de Judá (Reino do Sul)" and cat != "rei_juda": continue
        if filtro_cat == "👑 Reis de Israel (Reino do Norte)" and cat != "rei_israel": continue
        if filtro_cat.startswith("🔥") and cat != "profeta": continue

        if busca_nome:
            termo = busca_nome.lower()
            str_p = f"{p['titulo']} {p['subtitulo']} {p['descricao']}".lower()
            if termo not in str_p: continue

        personagens_filtrados.append(p)

    st.markdown(f"**Exibindo {len(personagens_filtrados)} registros:**")
    st.divider()

    def navegar_ao_confronto(ano):
        st.session_state["custom_ano_confronto"] = int(ano)
        st.session_state["num_ano_confronto"] = int(ano)
        st.session_state["aba_ativa"] = "⚡ Confronto de Épocas & Impérios"
        ano_txt = f"{abs(ano)} a.C." if ano < 0 else f"{ano} d.C."
        st.toast(f"⚡ Abrindo Confronto de Épocas para o ano {ano_txt}...", icon="⚡")

    # Exibição em Grid de 2 Colunas
    cols = st.columns(2)
    for idx, p in enumerate(personagens_filtrados):
        col_dest = cols[idx % 2]
        with col_dest:
            ano_ini = f"{abs(p['ano_inicio'])} a.C." if p['ano_inicio'] < 0 else f"{p['ano_inicio']} d.C."
            ano_fim = f"{abs(p['ano_fim'])} a.C." if p['ano_fim'] and p['ano_fim'] < 0 else (f"{p['ano_fim']} d.C." if p['ano_fim'] else "")
            baliza = f"{ano_ini} — {ano_fim}" if ano_fim else ano_ini

            icone_cat = "👤 "
            badge_sub = ""
            if p['categoria'] == 'antediluviano': icone_cat = "🌱 "
            elif p['categoria'] == 'patriarca': icone_cat = "⛺ "
            elif p['categoria'] == 'juiz': icone_cat = "⚖️ "
            elif p['categoria'] == 'rei_juda':
                icone_cat = "👑 "
                badge_sub = "<span class='badge-chip badge-gold' style='margin-left:8px;'>REINO DE JUDÁ (SUL)</span>"
            elif p['categoria'] == 'rei_israel':
                icone_cat = "👑 "
                badge_sub = "<span class='badge-chip' style='margin-left:8px;'>REINO DE ISRAEL (NORTE)</span>"
            elif p['categoria'] == 'profeta': icone_cat = "🔥 "

            st.markdown(f"""
            <div class='person-card'>
                <div class='person-name'>{icone_cat}{p['titulo']} {badge_sub}</div>
                <div class='person-dates'>{baliza}</div>
                <p style='font-size:0.9rem; color:#cbd5e1;'>{p['descricao']}</p>
                <div style='font-size:0.8rem; color:#94a3b8; margin-top:4px;'>
                    <b>Fontes Bíblicas:</b> {p['fontes_historicas'] or 'Tradição Bíblica'}
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Botões de ação coordenada: Leitor Bíblico e Confronto de Épocas
            col_b_ler, col_b_ep = st.columns(2)
            
            nome_chave = next((k for k in PASSAGEM_MAP.keys() if k.lower() in p['titulo'].lower()), None)
            with col_b_ler:
                if nome_chave:
                    liv_target, cap_target, lid_target = PASSAGEM_MAP[nome_chave]
                    st.button(
                        f"📖 Ler ({liv_target} {cap_target})",
                        key=f"btn_p_{p['id']}",
                        on_click=abrir_passagem,
                        args=(liv_target, cap_target, lid_target),
                        use_container_width=True
                    )
                else:
                    st.button(
                        "📖 Abrir no Leitor",
                        key=f"btn_p_{p['id']}",
                        on_click=abrir_passagem,
                        args=("Gênesis", 1, 1),
                        use_container_width=True
                    )
                    
            with col_b_ep:
                st.button(
                    "⚡ Ver no Confronto",
                    key=f"btn_p_ep_{p['id']}",
                    on_click=navegar_ao_confronto,
                    args=(p['ano_inicio'],),
                    use_container_width=True,
                    help=f"Examinar os impérios e eventos mundiais no ano {ano_ini}"
                )

            if p.get('wikipedia_url'):
                st.markdown(f"<a href='{p['wikipedia_url']}' target='_blank' style='font-size:0.8rem; color:#38bdf8; text-decoration:none;'>🌐 Artigo na Wikipédia &rarr;</a>", unsafe_allow_html=True)
            
            st.write("")