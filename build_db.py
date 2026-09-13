import pandas as pd
import sqlite3
import os
import glob
import json

# =====================================================================
# 1. CONFIGURAÇÃO E DIRETÓRIOS
# =====================================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
caminho_csv = os.path.join(BASE_DIR, 'bible_databases-master', 'formats', 'csv')

# Dicionário de tradução nativa
traducao_livros = {
    'Genesis': 'Gênesis', 'Exodus': 'Êxodo', 'Leviticus': 'Levítico', 'Numbers': 'Números',
    'Deuteronomy': 'Deuteronômio', 'Joshua': 'Josué', 'Judges': 'Juízes', 'Ruth': 'Rute',
    '1 Samuel': '1 Samuel', '2 Samuel': '2 Samuel', '1 Kings': '1 Reis', '2 Kings': '2 Reis',
    '1 Chronicles': '1 Crônicas', '2 Chronicles': '2 Crônicas', 'Ezra': 'Esdras', 'Nehemiah': 'Neemias',
    'Esther': 'Ester', 'Job': 'Jó', 'Psalms': 'Salmos', 'Proverbs': 'Provérbios',
    'Ecclesiastes': 'Eclesiastes', 'Song of Solomon': 'Cânticos', 'Isaiah': 'Isaías', 'Jeremiah': 'Jeremias',
    'Lamentations': 'Lamentações', 'Ezekiel': 'Ezequiel', 'Daniel': 'Daniel', 'Hosea': 'Oséias',
    'Joel': 'Joel', 'Amos': 'Amós', 'Obadiah': 'Obadias', 'Jonah': 'Jonas', 'Micah': 'Miquéias',
    'Nahum': 'Naum', 'Habakkuk': 'Habacuque', 'Zephaniah': 'Sofonias', 'Haggai': 'Ageu',
    'Zechariah': 'Zacarias', 'Malachi': 'Malaquias', 'Matthew': 'Mateus', 'Mark': 'Marcos',
    'Luke': 'Lucas', 'John': 'João', 'Acts': 'Atos', 'Romans': 'Romanos', '1 Corinthians': '1 Coríntios',
    '2 Corinthians': '2 Coríntios', 'Galatians': 'Gálatas', 'Ephesians': 'Efésios', 'Philippians': 'Filipenses',
    'Colossians': 'Colossenses', '1 Thessalonians': '1 Tessalonicenses', '2 Thessalonians': '2 Tessalonicenses',
    '1 Timothy': '1 Timóteo', '2 Timothy': '2 Timóteo', 'Titus': 'Tito', 'Philemon': 'Filemom',
    'Hebrews': 'Hebreus', 'James': 'Tiago', '1 Peter': '1 Pedro', '2 Peter': '2 Pedro',
    '1 John': '1 João', '2 John': '2 João', '3 John': '3 João', 'Jude': 'Judas', 'Revelation': 'Apocalipse'
}

livros_english = list(traducao_livros.keys())
book_to_id = {book: i+1 for i, book in enumerate(livros_english)}

print("Iniciando a compilação do banco de dados relacional (Padrão 2025)...")
conn = sqlite3.connect('biblia_app.db')

# =====================================================================
# 2. PROCESSAR LIVROS
# =====================================================================
print("-> Processando estrutura de livros...")
if not os.path.exists(caminho_csv):
    raise FileNotFoundError(f"A pasta '{caminho_csv}' não foi encontrada.")

livros_data = [{'b': i, 'n_pt': pt} for i, pt in enumerate(traducao_livros.values(), start=1)]
pd.DataFrame(livros_data).to_sql('livros', conn, if_exists='replace', index=False)

# =====================================================================
# 3. PROCESSAR REFERÊNCIAS CRUZADAS (Novo Esquema JSON)
# =====================================================================
print("-> Processando Referências Cruzadas (JSON)...")
caminho_extras = os.path.join(BASE_DIR, 'bible_databases-master', 'sources', 'extras')
arquivos_refs = glob.glob(os.path.join(caminho_extras, 'cross_references_*.json'))

if arquivos_refs:
    refs_list = []
    for arquivo in arquivos_refs:
        print(f"   Lendo arquivo: {os.path.basename(arquivo)}")
        with open(arquivo, 'r', encoding='utf-8') as f:
            dados = json.load(f)
            
            for ref in dados.get('cross_references', []):
                from_v = ref['from_verse']
                votes = ref.get('votes', 0)
                from_book_id = book_to_id.get(from_v['book'])
                
                for to_v in ref.get('to_verse', []):
                    to_book_id = book_to_id.get(to_v['book'])
                    
                    # CORREÇÃO CRÍTICA: Lida com versículo único vs intervalo de versículos
                    v_inicio = to_v.get('verse', to_v.get('verse_start'))
                    v_fim = to_v.get('verse_end', v_inicio) 
                    
                    refs_list.append({
                        'origem_livro': from_book_id,
                        'origem_capitulo': from_v['chapter'],
                        'origem_versiculo': from_v['verse'],
                        'destino_livro': to_book_id,
                        'destino_capitulo': to_v['chapter'],
                        'destino_versiculo_inicio': v_inicio,
                        'destino_versiculo_fim': v_fim,
                        'votos': votes
                    })
    
    if refs_list:
        print("   Salvando referências no banco de dados...")
        pd.DataFrame(refs_list).to_sql('referencias', conn, if_exists='replace', index=False)
        print(f"   {len(refs_list)} referências estruturadas com sucesso!")
else:
    print("   [Aviso] Arquivos JSON não encontrados.")

# =====================================================================
# 4. PROCESSAR TEXTOS BÍBLICOS (CSVs)
# =====================================================================
print("-> Mapeando traduções disponíveis (CSV)...")
arquivos_bilias = glob.glob(os.path.join(caminho_csv, '*.csv'))
primeiro_arquivo = True

for arquivo in arquivos_bilias:
    nome_arquivo = os.path.basename(arquivo)
    # Correção: Na branch 2025, o prefixo 't_' pode não existir
    versao = os.path.splitext(nome_arquivo)[0].replace('t_', '').upper()
    print(f"   Carregando tradução: {versao}")
    
    df_temp = pd.read_csv(arquivo)
    
    # Adaptação para o novo formato de CSVs (Branch 2025)
    if 'Book' in df_temp.columns:
        # Cria um mapa numérico para os livros (1 a 66) com base na ordem de aparição no CSV
        livros_unicos = df_temp['Book'].unique()
        mapa_livros = {livro: i+1 for i, livro in enumerate(livros_unicos)}
        
        df_temp['b'] = df_temp['Book'].map(mapa_livros)
        df_temp.rename(columns={'Chapter': 'c', 'Verse': 'v', 'Text': 't'}, inplace=True)
        
        # Cria um ID único combinando Livro, Capítulo e Versículo
        df_temp['id'] = (df_temp['b'] * 1000000) + (df_temp['c'] * 1000) + df_temp['v']

    df_temp['traducao'] = versao
    
    acao = 'replace' if primeiro_arquivo else 'append'
    df_temp[['id', 'b', 'c', 'v', 't', 'traducao']].to_sql('versiculos', conn, if_exists=acao, index=False)
    primeiro_arquivo = False

# =====================================================================
# 5. BANCO EXTRA (Lógica Customizada Mantida)
# =====================================================================
print("-> Verificando traduções extras (biblia_8.sqlite3)...")
caminho_biblia_8 = os.path.join(BASE_DIR, 'biblia_8.sqlite3')

if os.path.exists(caminho_biblia_8):
    conn_8 = sqlite3.connect(caminho_biblia_8)
    query_8 = """
        SELECT (v.ver_vrs_id * 100000) + v.ver_id as id, v.ver_liv_id as b, v.ver_capitulo as c,
               v.ver_versiculo as v, v.ver_texto as t, TRIM(ve.Abrev) as traducao
        FROM versiculos v JOIN versoes ve ON v.ver_vrs_id = ve.vrs_id WHERE ve.vrs_id != 6
    """
    df_biblia_8 = pd.read_sql(query_8, conn_8)
    df_biblia_8['traducao'] = df_biblia_8['traducao'].str.upper()

    try:
        versoes_csv = pd.read_sql("SELECT DISTINCT traducao FROM versiculos", conn)['traducao'].tolist()
    except Exception:
        versoes_csv = []
        
    df_biblia_8['traducao'] = df_biblia_8['traducao'].apply(lambda x: f"{x}_BR" if x in versoes_csv else x)
    df_biblia_8.to_sql('versiculos', conn, if_exists='append', index=False)
    conn_8.close()
    print("   Traduções extras mescladas!")

# =====================================================================
# 6. ÍNDICES DE ALTA PERFORMANCE
# =====================================================================
print("-> Criando índices estruturais no SQLite...")
cursor = conn.cursor()
cursor.execute('CREATE INDEX IF NOT EXISTS idx_busca_texto ON versiculos (traducao, b, c)')
# O índice agora reflete a chave semântica tripla do esquema 2025
cursor.execute('CREATE INDEX IF NOT EXISTS idx_ref_origem ON referencias (origem_livro, origem_capitulo, origem_versiculo)')
cursor.execute('CREATE INDEX IF NOT EXISTS idx_ref_destino ON referencias (destino_livro, destino_capitulo, destino_versiculo_inicio)')
conn.commit()
conn.close()
print("Banco atualizado com sucesso!")