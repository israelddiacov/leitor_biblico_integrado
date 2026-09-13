import streamlit as st
import pandas as pd
import sqlite3
import json
import os
import glob

# =====================================================================
# CONFIGURAÇÕES INICIAIS
# =====================================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Dicionário fixo para traduzir o nome do livro no JSON (Inglês) para o liv_id do seu Banco Antigo
ENG_TO_LIV_ID = {
    "Genesis": 1, "Exodus": 2, "Leviticus": 3, "Numbers": 4, "Deuteronomy": 5,
    "Joshua": 6, "Judges": 7, "Ruth": 8, "1 Samuel": 9, "2 Samuel": 10,
    "I Samuel": 9, "II Samuel": 10,
    "1 Kings": 11, "2 Kings": 12, "1 Chronicles": 13, "2 Chronicles": 14,
    "I Kings": 11, "II Kings": 12, "I Chronicles": 13, "II Chronicles": 14,
    "Ezra": 15, "Nehemiah": 16, "Esther": 17, "Job": 18, "Psalms": 19,
    "Proverbs": 20, "Ecclesiastes": 21, "Song of Solomon": 22, "Isaiah": 23,
    "Jeremiah": 24, "Lamentations": 25, "Ezekiel": 26, "Daniel": 27,
    "Hosea": 28, "Joel": 29, "Amos": 30, "Obadiah": 31, "Jonah": 32,
    "Micah": 33, "Nahum": 34, "Habakkuk": 35, "Zephaniah": 36, "Haggai": 37,
    "Zechariah": 38, "Malachi": 39, "Matthew": 40, "Mark": 41, "Luke": 42,
    "John": 43, "Acts": 44, "Romans": 45, "1 Corinthians": 46, "2 Corinthians": 47,
    "I Corinthians": 46, "II Corinthians": 47,
    "Galatians": 48, "Ephesians": 49, "Philippians": 50, "Colossians": 51,
    "1 Thessalonians": 52, "2 Thessalonians": 53, "1 Timothy": 54, "2 Timothy": 55,
    "I Thessalonians": 52, "II Thessalonians": 53, "I Timothy": 54, "II Timothy": 55,
    "Titus": 56, "Philemon": 57, "Hebrews": 58, "James": 59, "1 Peter": 60,
    "2 Peter": 61, "1 John": 62, "2 John": 63, "3 John": 64, "Jude": 65, "Revelation": 66,
    "I Peter": 60, "II Peter": 61, "I John": 62, "II John": 63, "III John": 64, "Revelation of John": 66
}

st.set_page_config(page_title="Construtor de Banco de Dados", layout="centered")

st.title("🛠️ Importador de Dados (JSON -> SQLite)")
st.info("⚠️ O banco selecionado **será atualizado**. Faça um backup do seu SQLite original antes de prosseguir.")

# Pastas padrão sugeridas
default_trans_path = os.path.join(BASE_DIR, 'bible_databases-master', 'formats', 'json')
default_refs_path = os.path.join(BASE_DIR, 'bible_databases-master', 'sources', 'extras')

folder_translations = st.text_input("Caminho da pasta de Traduções Bíblicas (.json):", value=default_trans_path)
folder_refs = st.text_input("Caminho da pasta de Referências Cruzadas (.json):", value=default_refs_path)
file_sqlite = st.text_input("Caminho do Banco SQLite Oficial do Programa:", value=os.path.join(BASE_DIR, 'biblia.db'))

# Busca os arquivos disponíveis na pasta de traduções dinamicamente
arquivos_disponiveis = []
if os.path.exists(folder_translations):
    arquivos_disponiveis = glob.glob(os.path.join(folder_translations, '*.json'))

arquivos_selecionados = st.multiselect(
    "Selecione as Traduções Bíblicas para importar:",
    options=arquivos_disponiveis,
    format_func=lambda x: os.path.basename(x)
)

inserir_refs = st.checkbox("Importar/Atualizar Referências Cruzadas (TSK)", value=True)

# =========================================================
# ÁREA DE MANUTENÇÃO (Limpeza Sênior)
# =========================================================
with st.expander("🧹 Restauração e Limpeza do Banco (Danger Zone)"):
    st.warning("Esta ação apagará todas as Bíblias JSON e Referências importadas, restaurando o banco aos seus 66 livros originais e 8 versões base.")
    if st.button("Executar Limpeza Profunda"):
        if os.path.exists(file_sqlite):
            try:
                conn_clean = sqlite3.connect(file_sqlite)
                cursor_clean = conn_clean.cursor()
                
                cursor_clean.execute("DELETE FROM versiculos WHERE ver_liv_id > 66 OR ver_vrs_id > 8")
                cursor_clean.execute("DELETE FROM livros WHERE liv_id > 66")
                cursor_clean.execute("DELETE FROM testamentos WHERE tes_id > 2")
                cursor_clean.execute("DELETE FROM versoes WHERE vrs_id > 8")
                cursor_clean.execute("DELETE FROM referencias")
                
                conn_clean.commit()
                cursor_clean.execute("VACUUM") # Recupera o espaço físico no HD e otimiza
                conn_clean.close()
                st.success("✅ Banco limpo e restaurado com sucesso! Espaço em disco recuperado.")
            except Exception as e:
                st.error(f"Erro durante a limpeza: {e}")
        else:
            st.error("Banco de dados não encontrado.")

if st.button("Importar Dados Selecionados"):
    if not os.path.exists(folder_refs):
        st.error("Por favor, verifique se a pasta de referências cruzadas existe.")
    elif not os.path.exists(file_sqlite):
        st.error(f"Banco de dados não encontrado em {file_sqlite}")
    else:
        try:
            conn = sqlite3.connect(file_sqlite)
            
            # Lógica Sênior: Função inteligente para criar livros apócrifos ou extras em tempo real
            def get_or_create_book(book_name, db_conn, db_cursor):
                if not book_name: return None
                b_id = ENG_TO_LIV_ID.get(book_name)
                if b_id: return b_id
                
                # Verifica se o livro já foi criado dinamicamente nesta sessão ou já existia
                db_cursor.execute("SELECT liv_id FROM livros WHERE liv_nome = ?", (book_name,))
                res = db_cursor.fetchone()
                if res:
                    ENG_TO_LIV_ID[book_name] = res[0]
                    return res[0]
                    
                db_cursor.execute("SELECT MAX(liv_id) FROM livros")
                max_l = db_cursor.fetchone()[0]
                new_liv_id = (max_l + 1) if max_l else 1
                
                db_cursor.execute("SELECT tes_id FROM testamentos WHERE tes_id = 3")
                if not db_cursor.fetchone():
                    db_cursor.execute("INSERT INTO testamentos (tes_id, tes_nome, Abrev) VALUES (3, 'Apócrifos / Extras', 'AP')")
                    
                db_cursor.execute("SELECT MAX(liv_posicao) FROM livros WHERE liv_tes_id = 3")
                max_p = db_cursor.fetchone()[0]
                new_pos = (max_p + 1) if max_p else 1
                
                abrev = book_name[:3].upper()
                db_cursor.execute("INSERT INTO livros (liv_id, liv_tes_id, liv_posicao, liv_nome, liv_abreviado) VALUES (?, ?, ?, ?, ?)",
                               (new_liv_id, 3, new_pos, book_name, abrev))
                db_conn.commit()
                ENG_TO_LIV_ID[book_name] = new_liv_id
                return new_liv_id

            # Pega o próximo ID disponível globalmente para versiculos para garantir inserção correta
            cursor = conn.cursor()
            cursor.execute("SELECT MAX(ver_id) FROM versiculos")
            max_ver_id_row = cursor.fetchone()[0]
            prox_ver_id = (max_ver_id_row + 1) if max_ver_id_row else 1
            
            # =========================================================
            # 1. IMPORTAR TEXTOS BÍBLICOS JSON
            # =========================================================
            st.write("📜 **Passo 1:** Processando Traduções Bíblicas...")
            arquivos_biblias = arquivos_selecionados
            
            novas_versoes_importadas = 0
            if arquivos_biblias:
                progresso_json = st.progress(0)
                texto_status = st.empty()
                
                for idx, arquivo in enumerate(arquivos_biblias):
                    nome_arquivo = os.path.basename(arquivo)
                    
                    # Leitura do JSON hierárquico
                    with open(arquivo, 'r', encoding='utf-8') as f:
                        biblia_json = json.load(f)
                        
                    # Extrai o nome da tradução do nó principal ou do nome do arquivo
                    versao = biblia_json.get("translation", nome_arquivo).split(':')[0].strip().upper()
                    versao_nome_completo = biblia_json.get("translation", nome_arquivo).strip()
                    texto_status.text(f"Carregando tradução: {versao}...")
                    
                    # Verifica se a versão já existe, se não, cadastra e gera um ID
                    df_vrs = pd.read_sql(f"SELECT vrs_id FROM versoes WHERE Abrev = '{versao}'", conn)
                    if df_vrs.empty:
                        cursor.execute("SELECT MAX(vrs_id) FROM versoes")
                        max_v_id = cursor.fetchone()[0]
                        novo_vrs_id = (max_v_id + 1) if max_v_id else 1
                        
                        # Insere na tabela 'versoes' do SQLite antigo
                        cursor.execute("INSERT INTO versoes (vrs_id, vrs_nome, Abrev) VALUES (?, ?, ?)", (novo_vrs_id, versao_nome_completo, versao))
                        conn.commit()
                        vrs_id_atual = novo_vrs_id
                        novas_versoes_importadas += 1
                    else:
                        vrs_id_atual = df_vrs.iloc[0]['vrs_id']
                        
                    linhas_insercao = []
                    for book in biblia_json.get("books", []):
                        book_name = book.get("name")
                        liv_id = get_or_create_book(book_name, conn, cursor)
                        if not liv_id: continue
                        
                        for chapter in book.get("chapters", []):
                            c_id = chapter.get("chapter")
                            
                            for verse in chapter.get("verses", []):
                                linhas_insercao.append({
                                    "ver_id": prox_ver_id,
                                    "ver_vrs_id": vrs_id_atual,
                                    "ver_liv_id": liv_id,
                                    "ver_capitulo": c_id,
                                    "ver_versiculo": verse.get("verse"),
                                    "ver_texto": verse.get("text")
                                })
                                prox_ver_id += 1
                    
                    # Faz o append na tabela versículos
                    df_temp = pd.DataFrame(linhas_insercao)
                    df_temp.to_sql('versiculos', conn, if_exists='append', index=False)
                    
                    progresso_json.progress((idx + 1) / len(arquivos_biblias))
                
                texto_status.empty()
                st.success(f"✔️ {novas_versoes_importadas} nova(s) tradução(ões) importada(s) com sucesso para o banco principal!")
            else:
                st.warning(f"⚠️ Nenhuma tradução (.json) selecionada para importar.")

            # =========================================================
            # 2. IMPORTAR REFERÊNCIAS CRUZADAS (JSON aninhado)
            # =========================================================
            if inserir_refs:
                st.write("🔗 **Passo 2:** Processando Referências Cruzadas...")
                arquivos_refs = glob.glob(os.path.join(folder_refs, '*.json'))
                
                refs_list = []
                for arquivo in arquivos_refs:
                    with open(arquivo, 'r', encoding='utf-8') as f:
                        ref_data = json.load(f)
                        
                    for ref in ref_data.get("cross_references", []):
                        from_v = ref.get("from_verse", {})
                        origem_liv_id = get_or_create_book(from_v.get("book"), conn, cursor)
                        if not origem_liv_id: continue
                        
                        # Como "to_verse" é um array, iteramos os destinos
                        for to_v in ref.get("to_verse", []):
                            destino_liv_id = get_or_create_book(to_v.get("book"), conn, cursor)
                            if not destino_liv_id: continue
                            
                            refs_list.append({
                                "origem_liv_id": origem_liv_id,
                                "origem_capitulo": from_v.get("chapter"),
                                "origem_versiculo": from_v.get("verse"),
                                "destino_liv_id": destino_liv_id,
                                "destino_capitulo": to_v.get("chapter"),
                                "destino_versiculo_start": to_v.get("verse_start"),
                                "destino_versiculo_end": to_v.get("verse_end"),
                                "votos": ref.get("votes", 0)
                            })
                            
                if refs_list:
                    # Limpa as referências anteriores antes de inserir as novas (sem dropar a tabela para não perder índices)
                    cursor.execute("DELETE FROM referencias")
                    conn.commit()
                    
                    df_refs = pd.DataFrame(refs_list)
                    df_refs.to_sql('referencias', conn, if_exists='append', index=False)
                    st.success(f"✔️ {len(refs_list)} referências cruzadas cadastradas com sucesso!")

            conn.close()
            st.balloons()
            st.success(f"🎉 Importação e Atualização finalizadas com sucesso no banco `{file_sqlite}`!")

        except Exception as e:
            st.error(f"Ocorreu um erro ao processar os arquivos: {e}")
