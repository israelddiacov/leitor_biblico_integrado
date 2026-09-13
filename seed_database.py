"""
Script de inicialização e povoamento (Seed) do Banco de Dados SQLite
da Timeline Histórica Bíblica Comparada com:
1. Adão, Eva e descendentes antediluvianos até o Dilúvio (nascimento e morte).
2. Patriarcas bíblicos pós-dilúvio e grandes patriarcas (Abraão a Josué).
3. Juízes de Israel (Shofetim: Otniel a Samuel).
4. Reis da Monarquia Unida, de Israel e de Judá.
5. Profetas de Israel e Judá (Elias a Malaquias e João Batista).
6. Eixos Seculares, Mitologias Contemporâneas, Livros e Concílios.
"""

import sqlite3
import os
import sys

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

DB_PATH = "timeline.db"
SCHEMA_PATH = "schema.sql"

def inicializar_banco():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        print(f"Banco de dados '{DB_PATH}' reiniciado.")

    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")
    cursor = conn.cursor()

    # 1. Executar Schema
    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        cursor.executescript(f.read())
    print("[OK] Schema SQL aplicado com sucesso.")

    # 2. Eixos
    eixos = [
        (1, 'SECULAR', 'História Secular & Impérios', '🏛️', '#0284c7', 1),
        (2, 'BIBLICO', 'Cronologia Bíblica & Personagens', '📜', '#d97706', 2),
        (3, 'MITOLOGIA', 'Mitologias & Cosmogonias', '🏺', '#7c3aed', 3),
        (4, 'CANON', 'Manuscritos, Cânon & Concílios', '⛪', '#059669', 4)
    ]
    cursor.executemany("""
        INSERT INTO eixos (id, codigo, nome, icone, cor_hex, ordem_exibicao)
        VALUES (?, ?, ?, ?, ?, ?)
    """, eixos)

    eventos = []

    # =========================================================================
    # EIXO 1: HISTÓRIA SECULAR & GRANDES IMPÉRIOS
    # =========================================================================
    eventos.extend([
        (
            1, "Império Antigo Egípcio (Era das Pirâmides)", "Dinastias III a VI (Mênfis)",
            -2686, 1, 1, -2181, 12, 31, "range", 50, "imperio", "Egito",
            "Consolidação do Estado egípcio centralizado e ereção das grandes pirâmides de Gizé (Quéops, Quéfren e Miquerinos).",
            "Cânon Real de Turim; Papiro de Westcar; Manetão (Aegyptiaca).",
            "https://en.wikipedia.org/wiki/Old_Kingdom_of_Egypt",
            "Mênfis / Gizé (Egito)", 29.9792, 31.1342, "egito,piramides,farao,imperio"
        ),
        (
            1, "Império Paleobabilônico (Hamurabi)", "Dinastia Amorita de Babilônia",
            -1792, 1, 1, -1750, 12, 31, "range", 10, "imperio", "Babilônia",
            "Hamurabi unifica as cidades-estado sumério-acádias da Mesopotâmia e promulga seu monumental código legal gravado em estela de diorito.",
            "Código de Hamurabi (Louvre, Sb 8); Cartas Reais de Mari.",
            "https://en.wikipedia.org/wiki/First_Babylonian_Empire",
            "Babilônia (Mesopotâmia)", 32.5363, 44.4208, "babilonia,hamurabi,leis,mesopotamia"
        ),
        (
            1, "Império Neoassírio (Hegemonia Militar)", "De Tiglath-Pileser III à queda de Nínive",
            -745, 1, 1, -612, 8, 1, "range", 5, "imperio", "Assíria",
            "Monarquia imperialista altamente militarizada; introduziu transferências populacionais em massa e conquistou o Levante e Egito.",
            "Anais Reais Assírios; Prisma de Senaqueribe (Museu Britânico); Reliefs de Laquis.",
            "https://en.wikipedia.org/wiki/Neo-Assyrian_Empire",
            "Nínive / Assur (Iraque)", 36.3596, 43.1528, "assiria,ninive,guerra,senaqueribe"
        ),
        (
            1, "Império Neobabilônico (Nabucodonosor II)", "Dinastia Caldeia e Domínio Mesopotâmico",
            -626, 1, 1, -539, 10, 29, "range", 0, "imperio", "Babilônia",
            "Restauração do poder caldeu, florescimento arquitetônico (Porta de Ishtar), vitórias sobre o Egito na Batalha de Carquemis (-605) e cerco e destruição de Jerusalém.",
            "Crônicas Babilônicas (ABC 5 - Crônica de Jerusalém); Cilindro de Nabucodonosor.",
            "https://en.wikipedia.org/wiki/Neo-Babylonian_Empire",
            "Babilônia", 32.5363, 44.4208, "babilonia,nabucodonosor,exilio,carquemis"
        ),
        (
            1, "Império Aquemênida (Persa)", "Fundado por Ciro, o Grande até Alexandre",
            -550, 1, 1, -330, 1, 1, "range", 2, "imperio", "Pérsia",
            "Primeiro império global da Antiguidade, célebre por sua administração em satrapias, sistema de estradas reais e edito de tolerância e repatriação religiosa.",
            "Cilindro de Ciro (BM 90920); Inscrição de Behistun de Dario I; Heródoto.",
            "https://en.wikipedia.org/wiki/Achaemenid_Empire",
            "Persépolis / Susa / Pasárgada", 29.9344, 52.8914, "persia,ciro,dario,tolerancia"
        ),
        (
            1, "Império Macedônio & Diádocos Helenísticos", "Alexandre Magno e os Reinos Selêucida e Ptolomaico",
            -336, 1, 1, -63, 1, 1, "range", 1, "imperio", "Grécia/Macedônia",
            "Conquista do Oriente Próximo por Alexandre, o Grande, promovendo a helenização, a universalização do grego Koiné e a fundação de Alexandria.",
            "Arriano (Anábase); Diodoro Sículo; Políbio.",
            "https://en.wikipedia.org/wiki/Hellenistic_period",
            "Alexandria / Antioquia / Pela", 31.2001, 29.9187, "grecia,alexandre,helenismo,koine"
        ),
        (
            1, "Império Romano (Pax Romana)", "De Otávio Augusto à Queda do Ocidente",
            -27, 1, 1, 476, 9, 4, "range", 0, "imperio", "Roma",
            "Estrutura imperial universal no Mediterrâneo; pacificação de rotas comerciais e expansão jurídica sobre a Judeia provincial durante as origens do cristianismo.",
            "Res Gestae Divi Augusti; Tácito (Anais); Suetônio (Vidas dos Césares).",
            "https://en.wikipedia.org/wiki/Roman_Empire",
            "Roma (Itália)", 41.9028, 12.4964, "roma,augusto,pax_romana,imperio"
        )
    ])

    # =========================================================================
    # EIXO 2: CRONOLOGIA BÍBLICA - ANTEDILUVIANOS (Adão a Noé - Gn 5)
    # =========================================================================
    eventos.extend([
        (
            2, "Adão (Vida: 930 anos)", "Criação e Primeiro Homem",
            -4004, 1, 1, -3074, 12, 31, "range", 50, "antediluviano", "Origens",
            "Criado por Deus no sexto dia da criação; expulso do Jardim do Éden após a queda; viveu 930 anos segundo o Texto Massorético (Gênesis 5:3-5).",
            "Gênesis 1-5; Lucas 3:38.", "https://en.wikipedia.org/wiki/Adam",
            "Jardim do Éden / Mesopotâmia", 31.0, 47.0, "adao,criacao,antediluviano,origens"
        ),
        (
            2, "Eva (Mãe de Todos os Viventes)", "Primeira Mulher",
            -4004, 1, 1, -3074, 12, 31, "range", 50, "antediluviano", "Origens",
            "Formada da costela de Adão para ser sua adjutora idônea; mãe de Caim, Abel e Sete; 'mãe de todos os viventes' (Gênesis 3:20).",
            "Gênesis 2-4.", "https://en.wikipedia.org/wiki/Eve",
            "Jardim do Éden / Mesopotâmia", 31.0, 47.0, "eva,antediluviano,origens"
        ),
        (
            2, "Sete (Vida: 912 anos)", "Substituto de Abel e Linhagem Piedosa",
            -3874, 1, 1, -2962, 12, 31, "range", 50, "antediluviano", "Origens",
            "Nascido quando Adão tinha 130 anos, após a morte de Abel; dele procede a linhagem dos justos que invocaram o nome do Senhor (Gn 4:26, 5:6-8).",
            "Gênesis 4:25, 5:6-8; 1 Crônicas 1:1.", "https://en.wikipedia.org/wiki/Seth",
            "Mesopotâmia", 31.5, 46.5, "sete,antediluviano,linhagem"
        ),
        (
            2, "Enos (Vida: 905 anos)", "Início da Invocação Pública a Yahweh",
            -3769, 1, 1, -2864, 12, 31, "range", 50, "antediluviano", "Origens",
            "Filho de Sete, nascido quando este tinha 105 anos. Em seus dias começou-se a invocar solenemente o nome do Senhor (Gn 4:26, 5:9-11).",
            "Gênesis 5:9-11; Lucas 3:38.", "https://en.wikipedia.org/wiki/Enos_(biblical_figure)",
            "Mesopotâmia", 31.5, 46.5, "enos,antediluviano"
        ),
        (
            2, "Cainã (Vida: 910 anos)", "Patriarca Antediluviano",
            -3679, 1, 1, -2769, 12, 31, "range", 50, "antediluviano", "Origens",
            "Filho de Enos, gerado quando este tinha 90 anos; viveu 910 anos (Gênesis 5:12-14).",
            "Gênesis 5:12-14; 1 Crônicas 1:2.", "https://en.wikipedia.org/wiki/Kenan",
            "Mesopotâmia", 31.5, 46.5, "caina,antediluviano"
        ),
        (
            2, "Maalalel (Vida: 895 anos)", "Patriarca Antediluviano",
            -3609, 1, 1, -2714, 12, 31, "range", 50, "antediluviano", "Origens",
            "Filho de Cainã, gerado aos 70 anos; viveu 895 anos e gerou a Jarede (Gênesis 5:15-17).",
            "Gênesis 5:15-17; Lucas 3:37.", "https://en.wikipedia.org/wiki/Mahalalel",
            "Mesopotâmia", 31.5, 46.5, "maalalel,antediluviano"
        ),
        (
            2, "Jarede (Vida: 962 anos)", "Segundo Homem Mais Longevo",
            -3544, 1, 1, -2582, 12, 31, "range", 50, "antediluviano", "Origens",
            "Filho de Maalalel; viveu 962 anos, sendo o segundo patriarca mais longevo de toda a Bíblia, superado apenas por Matusalém (Gênesis 5:18-20).",
            "Gênesis 5:18-20; 1 Crônicas 1:2.", "https://en.wikipedia.org/wiki/Jared_(biblical_figure)",
            "Mesopotâmia", 31.5, 46.5, "jarede,antediluviano"
        ),
        (
            2, "Enoque (Vida: 365 anos - Arrebatado)", "Andou com Deus e Não Viu a Morte",
            -3382, 1, 1, -3017, 12, 31, "range", 50, "antediluviano", "Origens",
            "Filho de Jarede; andou intimamente com Deus por 300 anos após gerar Matusalém e 'desapareceu, porque Deus o levou' (arrebatamento sem experimentar a morte física).",
            "Gênesis 5:21-24; Hebreus 11:5; Judas 1:14.", "https://en.wikipedia.org/wiki/Enoch_(ancestor_of_Noah)",
            "Mesopotâmia", 31.5, 46.5, "enoque,arrebatamento,antediluviano"
        ),
        (
            2, "Matusalém (Vida: 969 anos)", "O Homem Mais Velho da História Bíblica",
            -3317, 1, 1, -2348, 12, 31, "range", 50, "antediluviano", "Origens",
            "Filho de Enoque; homem de maior longevidade registrada nas Escrituras (969 anos). Segundo a cronologia bíblica masorética, faleceu no próprio ano do Dilúvio.",
            "Gênesis 5:25-27; 1 Crônicas 1:3.", "https://en.wikipedia.org/wiki/Methuselah",
            "Mesopotâmia", 31.5, 46.5, "matusalem,longevidade,diluvio,antediluviano"
        ),
        (
            2, "Lameque (Vida: 777 anos)", "Pai do Patriarca Noé",
            -3130, 1, 1, -2353, 12, 31, "range", 50, "antediluviano", "Origens",
            "Filho de Matusalém; profetizou ao dar o nome a Noé: 'Este nos consolará dos nossos trabalhos e da fadiga de nossas mãos' (Gênesis 5:28-31). Faleceu 5 anos antes do Dilúvio.",
            "Gênesis 5:28-31; Lucas 3:36.", "https://en.wikipedia.org/wiki/Lamech_(father_of_Noah)",
            "Mesopotâmia", 31.5, 46.5, "lameque,pai_noe,antediluviano"
        ),
        (
            2, "Noé (Vida: 950 anos)", "A Arca e a Aliança do Arco-Íris",
            -2948, 1, 1, -1998, 12, 31, "range", 50, "antediluviano", "Mesopotâmia / Ararate",
            "Homem justo e íntegro entre seus contemporâneos; construiu a Arca por ordem divina para salvar sua família e os animais do Dilúvio quando tinha 600 anos; viveu mais 350 anos após o cataclismo.",
            "Gênesis 6-9; Hebreus 11:7; 1 Pedro 3:20.", "https://en.wikipedia.org/wiki/Noah",
            "Monte Ararate", 39.7025, 44.2992, "noe,arca,diluvio,alianca,antediluviano"
        ),
        (
            2, "O Grande Dilúvio Universal", "Ano 600 da Vida de Noé",
            -2348, 2, 17, -2347, 2, 27, "range", 50, "narrativa", "Global / Mesopotâmia",
            "As fontes do grande abismo se romperam e as comportas dos céus se abriram por 40 dias e 40 noites; águas prevaleceram por 150 dias até a Arca repousar nos Montes de Ararate.",
            "Gênesis 7-8; Tabuinha XI de Gilgamesh (Utnapishtim).", "https://en.wikipedia.org/wiki/Genesis_flood_narrative",
            "Montes de Ararate", 39.7025, 44.2992, "diluvio,cataclisma,arca,ararate"
        ),
        (
            2, "Sem (Vida: 600 anos)", "Filho de Noé e Progenitor dos Semitas",
            -2446, 1, 1, -1846, 12, 31, "range", 50, "patriarca", "Oriente Próximo",
            "Filho de Noé que cobriu a nudez do pai; recebeu a bênção patriarcal de onde procedem Abraão e a linhagem messiânica (povos semitas).",
            "Gênesis 9:26-27, 10:21-31, 11:10-11.", "https://en.wikipedia.org/wiki/Shem",
            "Oriente Próximo", 32.0, 44.0, "sem,semitas,linhagem_abencoadas"
        )
    ])

    # =========================================================================
    # EIXO 2: CRONOLOGIA BÍBLICA - GRANDES PATRIARCAS (Abraão a Josué)
    # =========================================================================
    eventos.extend([
        (
            2, "Abraão (Vida: 175 anos)", "Pai da Fé e Aliança Abraâmica",
            -2166, 1, 1, -1991, 12, 31, "range", 25, "patriarca", "Ur / Canaã",
            "Chamado por Deus para sair de Ur dos Caldeus para a terra prometida de Canaã; pai de Ismael e Isaque; recebeu a promessa de que nele seriam benditas todas as famílias da terra.",
            "Gênesis 12-25; Romanos 4; Gálatas 3.", "https://en.wikipedia.org/wiki/Abraham",
            "Ur / Harã / Hebrom", 31.5292, 35.0938, "abraao,alianca,pai_da_fe,canaa,patriarca"
        ),
        (
            2, "Sara (Vida: 127 anos)", "Matriarca da Promessa e Mãe de Isaque",
            -2156, 1, 1, -2029, 12, 31, "range", 25, "patriarca", "Canaã / Hebrom",
            "Esposa estéril de Abraão que deu à luz Isaque aos 90 anos de idade pelo poder da promessa divina; sepultada na caverna de Macpela em Hebrom.",
            "Gênesis 17:15-21, 18, 21, 23; 1 Pedro 3:6.", "https://en.wikipedia.org/wiki/Sarah",
            "Hebrom (Caverna de Macpela)", 31.5247, 35.1107, "sara,matriarca,macpela,patriarca"
        ),
        (
            2, "Ismael (Vida: 137 anos)", "Primogênito de Abraão com Agar",
            -2080, 1, 1, -1943, 12, 31, "range", 25, "patriarca", "Deserto de Parã",
            "Filho de Abraão com a serva egípcia Agar; pai de doze príncipes e progenitor tradicional dos povos árabes no deserto.",
            "Gênesis 16, 21:8-21, 25:12-18.", "https://en.wikipedia.org/wiki/Ishmael",
            "Deserto de Parã", 29.0, 34.5, "ismael,agar,arabes,patriarca"
        ),
        (
            2, "Isaque (Vida: 180 anos)", "Filho da Promessa e Sacrifício no Moriá",
            -2066, 1, 1, -1886, 12, 31, "range", 25, "patriarca", "Canaã / Berseba",
            "Gerado aos 100 anos de Abraão; oferecido no Monte Moriá onde Deus proveu o cordeiro; casou-se com Rebeca e foi pai de Esaú e Jacó.",
            "Gênesis 21-28, 35:27-29; Hebreus 11:17-20.", "https://en.wikipedia.org/wiki/Isaac",
            "Berseba / Hebrom", 31.2589, 34.7997, "isaque,moria,alianca,patriarca"
        ),
        (
            2, "Jacó / Israel (Vida: 147 anos)", "O Suplantador que Lutou com Deus",
            -2006, 1, 1, -1859, 12, 31, "range", 25, "patriarca", "Canaã / Egito",
            "Filho de Isaque; comprou o direito de primogenitura; após lutar com o anjo em Peniel teve seu nome mudado para Israel; gerou os doze patriarcas das doze tribos; faleceu no Egito.",
            "Gênesis 25-50; Oseias 12:3-4.", "https://en.wikipedia.org/wiki/Jacob",
            "Bete-el / Peniel / Goshen", 30.5, 31.5, "jaco,israel,tribos,peniel,patriarca"
        ),
        (
            2, "Levi (Vida: 137 anos)", "Progenitor da Tribo Sacerdotal",
            -1928, 1, 1, -1791, 12, 31, "range", 25, "patriarca", "Canaã / Egito",
            "Terceiro filho de Jacó e Lia; dele descende a linhagem sacerdotal levítica, incluindo Moisés, Arão e os sacerdotes do Templo.",
            "Gênesis 29:34, 34, 49:5-7; Êxodo 6:16.", "https://en.wikipedia.org/wiki/Levi",
            "Egito (Goshen)", 30.5, 31.5, "levi,levitas,sacerdocio,patriarca"
        ),
        (
            2, "Judá (Linhagem Real Davídica)", "Patriarca da Tribo Real",
            -1925, 1, 1, -1800, 12, 31, "range", 30, "patriarca", "Canaã / Egito",
            "Quarto filho de Jacó; intercedeu por Benjamim diante de José; recebeu a bênção profética de que o cetro não se apartaria de seus pés até que viesse Siló (Messias).",
            "Gênesis 29:35, 37, 43, 44, 49:8-12; Mateus 1:1-3.", "https://en.wikipedia.org/wiki/Judah_(son_of_Jacob)",
            "Hebrom / Goshen", 31.5, 35.1, "juda,cetro,linhagem_real,leao_de_juda,patriarca"
        ),
        (
            2, "José do Egito (Vida: 110 anos)", "Governador do Egito e Salvador de Israel",
            -1915, 1, 1, -1805, 12, 31, "range", 25, "patriarca", "Canaã / Egito",
            "Filho amado de Jacó e Raquel; vendido pelos irmãos; interpretou os sonhos do Faraó e foi elevado a grão-vizir do Egito, preservando a família durante a fome; pai de Efraim e Manassés.",
            "Gênesis 37-50; Salmo 105:16-22.", "https://en.wikipedia.org/wiki/Joseph_(Genesis)",
            "Avaris / Mênfis (Egito)", 30.7871, 31.8214, "jose,egito,governador,farao,patriarca"
        ),
        (
            2, "Moisés (Vida: 120 anos)", "O Libertador, Legislador e Profeta da Lei",
            -1526, 1, 1, -1406, 12, 31, "range", 30, "patriarca", "Egito / Sinai / Nebo",
            "Salvo das águas do Nilo; viveu 40 anos na corte egípcia, 40 anos como pastor em Midiã e 40 anos conduzindo Israel pelo deserto; recebeu o Decálogo no Sinai e compôs a Torá.",
            "Êxodo, Levítico, Números, Deuteronômio; Deuteronômio 34:1-12; Atos 7:20-40.", "https://en.wikipedia.org/wiki/Moses",
            "Monte Sinai / Monte Nebo", 31.7683, 35.7253, "moises,lei,sinai,exodo,tora,patriarca"
        ),
        (
            2, "Arão (Vida: 123 anos)", "Primeiro Sumo Sacerdote de Israel",
            -1529, 1, 1, -1406, 12, 31, "range", 30, "patriarca", "Egito / Deserto / Hor",
            "Irmão mais velho de Moisés e seu porta-voz diante do Faraó; consagrado como o primeiro Sumo Sacerdote de Yahweh, inaugurando o sacerdócio aarônico permanente; faleceu no Monte Hor.",
            "Êxodo 4:14, 28-29; Números 20:22-29.", "https://en.wikipedia.org/wiki/Aaron",
            "Monte Hor", 30.3167, 35.4167, "arao,sumo_sacerdote,tabernaculo,patriarca"
        ),
        (
            2, "Josué filho de Num (Vida: 110 anos)", "Comandante da Conquista de Canaã",
            -1485, 1, 1, -1375, 12, 31, "range", 30, "patriarca", "Canaã / Jericó",
            "Sucessor de Moisés na liderança de Israel; cruzou o Rio Jordão a pés enxutos, comandou a queda das muralhas de Jericó e conduziu a divisão da terra prometida entre as doze tribos.",
            "Livro de Josué; Deuteronômio 31:7-8; Josué 24:29.", "https://en.wikipedia.org/wiki/Joshua",
            "Jericó / Timnate-Sera", 31.8706, 35.4439, "josue,conquista,jerico,canaa,patriarca"
        )
    ])

    # =========================================================================
    # EIXO 2: CRONOLOGIA BÍBLICA - JUÍZES DE ISRAEL (Shofetim)
    # =========================================================================
    eventos.extend([
        (
            2, "Otniel (Primeiro Juiz de Israel)", "Libertação contra o Rei da Mesopotâmia",
            -1374, 1, 1, -1334, 12, 31, "range", 20, "juiz", "Judá / Hebrom",
            "Sobrinho de Calebe; sobre ele veio o Espírito do Senhor para libertar Israel da opressão de Cuchã-Risataim, rei da Mesopotâmia; a terra repousou por 40 anos.",
            "Juízes 3:7-11; Josué 15:17.", "https://en.wikipedia.org/wiki/Othniel",
            "Hebrom / Debir", 31.4333, 34.9833, "otniel,juiz,calebe,libertacao"
        ),
        (
            2, "Eúde (Segundo Juiz de Israel)", "O Libertador Canhoto contra Eglom de Moabe",
            -1316, 1, 1, -1236, 12, 31, "range", 20, "juiz", "Benjamim / Jericó",
            "Benjamita canhoto que assassinou em audiência secreta o obeso rei Eglom de Moabe com um punhal de dois gumes, pondo fim a 18 anos de tirania moabita.",
            "Juízes 3:12-30.", "https://en.wikipedia.org/wiki/Ehud",
            "Cidade das Palmeiras (Jericó)", 31.8706, 35.4439, "eude,juiz,moabe,benjamim"
        ),
        (
            2, "Débora e Baraque (Quarto Juiz de Israel)", "A Profetisa e a Derrota de Sísera",
            -1209, 1, 1, -1169, 12, 31, "range", 20, "juiz", "Efraim / Monte Tabor",
            "Única juíza mulher de Israel; julgava sob a palmeira entre Ramá e Betel; convocou Baraque e juntos desbarataram os 900 carros de ferro de Sísera no ribeiro de Quisom.",
            "Juízes 4-5 (O Cântico de Débora, um dos textos poéticos mais arcaicos da Bíblia).",
            "https://en.wikipedia.org/wiki/Deborah",
            "Monte Tabor / Rio Quisom", 32.6869, 35.3889, "debora,baraque,sisera,tabor,juiz"
        ),
        (
            2, "Gideão / Jerubaal (Quinto Juiz de Israel)", "A Vitória dos 300 contra os Midianitas",
            -1162, 1, 1, -1122, 12, 31, "range", 20, "juiz", "Manassés / Vale de Jezreel",
            "Derrubou o altar de Baal de seu pai; provou a vontade de Deus com a lã e o orvalho; derrotou o exército colossal de Midiã com apenas 300 guerreiros armados de tochas e trombetas.",
            "Juízes 6-8; Hebreus 11:32.", "https://en.wikipedia.org/wiki/Gideon",
            "Fonte de Harode / Vale de Jezreel", 32.5486, 35.3850, "gideao,300_homens,midianitas,juiz"
        ),
        (
            2, "Jefté (Oitavo Juiz de Israel)", "Vitória sobre Amom e o Voto Trágico",
            -1074, 1, 1, -1068, 12, 31, "range", 15, "juiz", "Gileade",
            "Guerreiro valoroso exilado pelos irmãos; convocado pelos anciãos de Gileade para repelir os amonitas; fez um voto solene que envolveu sua única filha; julgou Israel por 6 anos.",
            "Juízes 11-12; Hebreus 11:32.", "https://en.wikipedia.org/wiki/Jephthah",
            "Gileade / Mizpá", 32.2, 35.8, "jefte,voto,amon,gileade,juiz"
        ),
        (
            2, "Sansão (Vida e Juizado: 20 anos)", "O Nazireu de Força Prodigiosa contra os Filisteus",
            -1075, 1, 1, -1055, 12, 31, "range", 15, "juiz", "Dã / Gaza / Soreque",
            "Nazireu de Deus desde o ventre cuja força sobre-humana residia no voto de consagração; matou um leão com as mãos e 1.000 filisteus com uma queixada de jumento; traído por Dalila, derrubou o templo de Dagom em Gaza.",
            "Juízes 13-16; Hebreus 11:32.", "https://en.wikipedia.org/wiki/Samson",
            "Zorá / Gaza / Vale de Soreque", 31.5, 34.45, "sansao,dalila,filisteus,gaza,juiz"
        ),
        (
            2, "Eli (Sumo Sacerdote e Juiz por 40 anos)", "Liderança Sacerdotal em Siló",
            -1107, 1, 1, -1067, 12, 31, "range", 15, "juiz", "Siló",
            "Sacerdote da linhagem de Itamar; julgou Israel por 40 anos e criou o menino Samuel no Tabernáculo de Siló; faleceu aos 98 anos ao saber que a Arca da Aliança havia sido capturada pelos filisteus.",
            "1 Samuel 1-4.", "https://en.wikipedia.org/wiki/Eli_(biblical_figure)",
            "Siló (Samaria)", 32.0556, 35.2894, "eli,silo,tabernaculo,arca,juiz"
        ),
        (
            2, "Samuel (Vida: ~78 anos)", "Último dos Juízes e Primeiro Grande Profeta Monárquico",
            -1090, 1, 1, -1012, 12, 31, "range", 15, "juiz", "Ramá / Siló / Mispá",
            "Consagrado por sua mãe Ana; ouviu a voz audível de Deus ainda jovem em Siló; liderou a restauração espiritual de Israel e a derrota dos filisteus em Ebenézer; ungiu os dois primeiros reis: Saul e Davi.",
            "1 Samuel 1-25; Atos 3:24; Hebreus 11:32.", "https://en.wikipedia.org/wiki/Samuel",
            "Ramá de Benjamim", 31.8542, 35.2319, "samuel,profeta,juiz,uncao_saul_davi"
        )
    ])

    # =========================================================================
    # EIXO 2: CRONOLOGIA BÍBLICA - REIS DA MONARQUIA UNIDA E REINOS DIVIDIDOS
    # =========================================================================
    eventos.extend([
        # --- MONARQUIA UNIDA ---
        (
            2, "Rei Saul (Reinado: 40 anos)", "Primeiro Rei de Todo Israel",
            -1050, 1, 1, -1010, 12, 31, "range", 10, "rei_israel", "Gibeá de Benjamim",
            "Umgido por Samuel a pedido do povo; homem de porte imponente da tribo de Benjamim; obteve vitórias militares contra os amonitas e filisteus, mas desobedeceu na guerra contra os amalequitas; pereceu na Batalha do Monte Gilboa.",
            "1 Samuel 9-31; 1 Crônicas 10.", "https://en.wikipedia.org/wiki/Saul",
            "Gibeá / Monte Gilboa", 32.5028, 35.4194, "saul,primeiro_rei,gilboa,monarquia_unida"
        ),
        (
            2, "Rei Davi (Vida: 70 anos / Reinado: 40 anos)", "O Homem Segundo o Coração de Deus",
            -1040, 1, 1, -970, 12, 31, "range", 5, "rei_israel", "Hebrom / Jerusalém",
            "Pastor de Belém que derrotou o gigante Golias; ungiu como rei sobre Judá em Hebrom (-1010) e depois sobre todo Israel (-1003); conquistou a fortaleza jebuseia de Sião, fundando a Cidade de Davi; autor da maioria dos Salmos.",
            "1 e 2 Samuel; 1 Crônicas 11-29; Inscrição de Tel Dã ('Casa de Davi').",
            "https://en.wikipedia.org/wiki/David",
            "Jerusalém (Monte Sião)", 31.7767, 35.2345, "davi,salmos,jerusalem,casa_de_davi,monarquia"
        ),
        (
            2, "Rei Salomão (Reinado: 40 anos)", "Sabedoria Lendária e Construtor do Templo",
            -990, 1, 1, -931, 12, 31, "range", 5, "rei_israel", "Jerusalém",
            "Filho de Davi e Bate-Seba; orou pedindo sabedoria para julgar o povo; edificou o monumental Primeiro Templo de Jerusalém no Monte Moriá; expandiu frotas comerciais até Társis e Ofir; compôs Provérbios, Eclesiastes e Cantares.",
            "1 Reis 1-11; 2 Crônicas 1-9.", "https://en.wikipedia.org/wiki/Solomon",
            "Jerusalém (Monte Moriá)", 31.7780, 35.2354, "salomao,primeiro_templo,sabedoria,moria"
        ),

        # --- REINO DO NORTE (ISRAEL / SAMARIA) ---
        (
            2, "Rei Jeroboão I (Reinado: 22 anos)", "Cisma das 10 Tribos e Culto em Betel e Dã",
            -931, 1, 1, -910, 12, 31, "range", 2, "rei_israel", "Siquém / Tirza / Samaria",
            "Líder da revolta do norte contra os pesados tributos de Roboão; estabeleceu bezerros de ouro em Betel e Dã para impedir que seus súditos peregrinassem ao Templo de Jerusalém, originando o infame 'pecado de Jeroboão'.",
            "1 Reis 11:26-40, 12-14.", "https://en.wikipedia.org/wiki/Jeroboam",
            "Siquém / Betel / Dã", 32.2133, 35.2819, "jeroboao,cisma,bezerros_de_ouro,reino_norte"
        ),
        (
            2, "Rei Onri (Reinado: 12 anos)", "Fundador da Dinastia Onrida e Construtor de Samaria",
            -885, 1, 1, -874, 12, 31, "range", 2, "rei_israel", "Samaria",
            "Comandante militar que tomou o poder; comprou a colina de Samaria e edificou a nova e fortificada capital do Reino do Norte; mencionado internacionalmente na célebre Estela de Mesa como soberano poderoso sobre Moabe.",
            "1 Reis 16:21-28; Estela de Mesa (Pedra Moabita no Louvre).",
            "https://en.wikipedia.org/wiki/Omri",
            "Samaria (Sebaste)", 32.2770, 35.1906, "onri,samaria,estela_de_mesa,dinastia_onrida"
        ),
        (
            2, "Rei Acabe (Reinado: 22 anos)", "Casamento com Jezabel e Batalha de Qarqar",
            -874, 1, 1, -853, 12, 31, "range", 1, "rei_israel", "Samaria / Jezreel",
            "Filho de Onri; desposou a princesa fenícia Jezabel de Tiro e promoveu o culto a Baal; enfrentou a oposição implacável do profeta Elias; liderou uma coalizão com 2.000 carros de guerra contra o imperador Salmaneser III na Batalha de Qarqar (-853).",
            "1 Reis 16:29 - 22:40; Monólito de Curque (British Museum).",
            "https://en.wikipedia.org/wiki/Ahab",
            "Samaria / Jezreel / Qarqar", 35.7333, 36.3833, "acabe,jezabel,elias,qarqar,assiria"
        ),
        (
            2, "Rei Jeú (Reinado: 28 anos)", "Extermínio da Casa de Acabe e Tributo à Assíria",
            -841, 1, 1, -814, 12, 31, "range", 1, "rei_israel", "Jezreel / Samaria",
            "Ungido por ordem de Eliseu; executou Jorão de Israel, Acazias de Judá e mandou lançar Jezabel da torre; expurgou os sacerdotes de Baal; retratado ajoelhado prestando tributo a Salmaneser III no Obelisco Negro de Nimrud.",
            "2 Reis 9-10; Obelisco Negro de Salmaneser III (Museu Britânico).",
            "https://en.wikipedia.org/wiki/Jehu",
            "Samaria / Jezreel", 32.2770, 35.1906, "jeu,obelisco_negro,jezabel,salmaneser"
        ),
        (
            2, "Rei Jeroboão II (Reinado: 41 anos)", "Idade de Ouro Econômica e Expansão do Norte",
            -793, 1, 1, -753, 12, 31, "range", 2, "rei_israel", "Samaria",
            "Monarca de maior longevidade e poder militar no Reino do Norte; recuperou fronteiras desde Hamate até o Mar Morto; prosperidade atestada pelos Óstracos de Samaria, contemporâneo dos profetas Amós e Oseias.",
            "2 Reis 14:23-29; Amós 6; Oseias 1:1; Óstracos de Samaria.",
            "https://en.wikipedia.org/wiki/Jeroboam_II",
            "Samaria", 32.2770, 35.1906, "jeroboao_ii,prosperidade,amos,oseias,samaria"
        ),
        (
            2, "Rei Oseias (Último Rei de Israel: 732-722 a.C.)", "Queda de Samaria e Fim do Reino do Norte",
            -732, 1, 1, -722, 12, 31, "range", 0, "rei_israel", "Samaria",
            "Assassinou Peca com apoio assírio; rebelou-se contra Salmaneser V buscando aliança com o faraó egípcio So; Samaria foi sitiada por 3 anos e conquistada por Sargão II em 722 a.C., selando a dispersão das 10 tribos.",
            "2 Reis 17:1-6; Anais de Sargão II em Corsabade.",
            "https://en.wikipedia.org/wiki/Hoshea",
            "Samaria", 32.2770, 35.1906, "oseias,queda_samaria,assiria,deportacao,reino_norte"
        ),

        # --- REINO DO SUL (JUDÁ / DINASTIA DAVÍDICA) ---
        (
            2, "Rei Roboão (Reinado: 17 anos)", "Filho de Salomão e Invasão de Sisaque",
            -931, 1, 1, -913, 12, 31, "range", 2, "rei_juda", "Jerusalém",
            "Rejeitou o conselho dos anciãos e agravou os tributos, causando a cisão das 10 tribos; no quinto ano de seu reinado, o faraó Sisaque I (Sheshenq I) saqueou os tesouros do Templo de Jerusalém.",
            "1 Reis 12, 14:21-31; Reliefs de Shoshenq I no Templo de Karnak.",
            "https://en.wikipedia.org/wiki/Rehoboam",
            "Jerusalém", 31.7767, 35.2345, "roboao,sisaque,karnak,cisma,juda"
        ),
        (
            2, "Rei Asa (Reinado: 41 anos)", "Grande Reforma Religiosa em Judá",
            -911, 1, 1, -870, 12, 31, "range", 2, "rei_juda", "Jerusalém",
            "Neto de Roboão; coração reto diante do Senhor; removeu os altares dos deuses estranhos, derrubou os postes sagrados e depôs sua própria avó Maaca por causa de um ídolo obsceno.",
            "1 Reis 15:9-24; 2 Crônicas 14-16.", "https://en.wikipedia.org/wiki/Asa_of_Judah",
            "Jerusalém", 31.7767, 35.2345, "asa,reforma,juda,idolatria"
        ),
        (
            2, "Rei Josafá (Reinado: 25 anos)", "Piedade, Justiça e Vitória pela Adoração",
            -870, 1, 1, -848, 12, 31, "range", 2, "rei_juda", "Jerusalém",
            "Enviou príncipes e levitas para ensinar a Lei de Deus em todas as cidades de Judá; estabeleceu juízes íntegros; alcançou vitória espetacular sobre a confederação moabita e amonita através de louvor sagrado.",
            "1 Reis 22; 2 Crônicas 17-20.", "https://en.wikipedia.org/wiki/Jehoshaphat",
            "Jerusalém / En-Gedi", 31.4500, 35.3833, "josafa,ensino_da_lei,louvor,vitoria,juda"
        ),
        (
            2, "Rei Joás de Judá (Reinado: 40 anos)", "O Rei Menino Salvo da Usurpadora Atalia",
            -835, 1, 1, -796, 12, 31, "range", 2, "rei_juda", "Jerusalém",
            "Escondido no Templo pelo sumo sacerdote Joiada durante o massacre promovido pela rainha Atalia; coroado aos 7 anos de idade; promoveu a grande restauração arquitetônica do Templo de Salomão.",
            "2 Reis 11-12; 2 Crônicas 23-24.", "https://en.wikipedia.org/wiki/Jehoash_of_Judah",
            "Jerusalém (Templo)", 31.7780, 35.2354, "joas,atalia,joiada,reparo_templo,juda"
        ),
        (
            2, "Rei Uzias / Azarias (Reinado: 52 anos)", "Prosperidade Tecnológica, Força Militar e Lepra",
            -790, 1, 1, -739, 12, 31, "range", 2, "rei_juda", "Jerusalém",
            "Reinou longamente com grande sucesso militar contra filisteus e árabes; desenvolveu engenhos mecânicos para projetar flechas e pedras em Jerusalém; no auge de seu orgulho, usurpou as funções sacerdotais entrando no Templo para queimar incenso, sendo ferido de lepra.",
            "2 Reis 15:1-7; 2 Crônicas 26; Isaías 6:1; Inscrição Funerária de Uzias.",
            "https://en.wikipedia.org/wiki/Uzziah",
            "Jerusalém", 31.7767, 35.2345, "uzias,lepra,tecnologia,isaias,juda"
        ),
        (
            2, "Rei Acaz (Reinado: 16 anos)", "Guerra Siro-Efraimita e Submissão à Assíria",
            -735, 1, 1, -715, 12, 31, "range", 2, "rei_juda", "Jerusalém",
            "Monarca idólatra que sacrificou o próprio filho no fogo no vale de Ben-Hinom; rejeitou o sinal de fé oferecido pelo profeta Isaías (a profecia de Emanuel em Isaías 7); pagou tributo a Tiglath-Pileser III para atacar Damasco e Samaria.",
            "2 Reis 16; 2 Crônicas 28; Isaías 7; Selo Bulla do Rei Acaz.",
            "https://en.wikipedia.org/wiki/Ahaz",
            "Jerusalém", 31.7767, 35.2345, "acaz,emanuel,isaias,siro_efraimita,assiria,juda"
        ),
        (
            2, "Rei Ezequias (Reinado: 29 anos)", "O Cerco de Senaqueribe e o Túnel de Siloé",
            -715, 1, 1, -686, 12, 31, "range", 1, "rei_juda", "Jerusalém",
            "Piedoso reformador; destruiu a serpente de bronze Neustã transformada em ídolo; perfurou o impressionante Túnel de Siloé na rocha viva (533 metros) para assegurar água durante o cerco assírio de 701 a.C.; Jerusalém foi milagrosamente poupada.",
            "2 Reis 18-20; Isaías 36-39; Prisma de Senaqueribe; Inscrição de Siloé (Museu de Istambul).",
            "https://en.wikipedia.org/wiki/Hezekiah",
            "Jerusalém (Túnel de Siloé)", 31.7725, 35.2356, "ezequias,siloe,senaqueribe,milagre,juda"
        ),
        (
            2, "Rei Manassés (Reinado: 55 anos)", "O Reinado Mais Longo e Idólatra de Judá",
            -697, 1, 1, -642, 12, 31, "range", 1, "rei_juda", "Jerusalém",
            "Filho de Ezequias; reconstruiu altares a Baal, adorou o exército dos céus e derramou sangue inocente em profusão; aprisionado e levado em cadeias à Babilônia pelos assírios, arrependeu-se amargamente em oração e foi restaurado.",
            "2 Reis 21; 2 Crônicas 33; Oração de Manassés; Anais de Assurbanipal.",
            "https://en.wikipedia.org/wiki/Manasseh_of_Judah",
            "Jerusalém", 31.7767, 35.2345, "manasses,arrependimento,oracao_manasses,juda"
        ),
        (
            2, "Rei Josias (Reinado: 31 anos)", "Achado do Livro da Lei e Morte em Megido",
            -640, 1, 1, -609, 12, 31, "range", 1, "rei_juda", "Jerusalém / Megido",
            "Coroado aos 8 anos; aos 18 anos promoveu reforma profunda quando o sumo sacerdote Hilquias encontrou o rolo da Lei no Templo (622 a.C.); expurgou todo culto idólatra e celebrou uma Páscoa sem paralelo; tombou na Batalha de Megido contra o Faraó Neco II.",
            "2 Reis 22-23; 2 Crônicas 34-35; Jeremias 22:15-16.",
            "https://en.wikipedia.org/wiki/Josiah",
            "Jerusalém / Tel Megido", 32.5850, 35.1844, "josias,livro_da_lei,megido,pascoa,reforma,juda"
        ),
        (
            2, "Rei Joaquim / Jeconias", "Primeira Deportação e Cativeiro em Babilônia",
            -598, 12, 9, -597, 3, 16, "range", 0, "rei_juda", "Jerusalém / Babilônia",
            "Reinou por apenas 3 meses e 10 dias; Nabucodonosor sitiou Jerusalém em 597 a.C. e levou Joaquim, sua mãe e 10.000 artesãos e guerreiros cativos para Babilônia (entre eles o profeta Ezequiel); mais tarde foi libertado da prisão pelo rei Evil-Merodaque.",
            "2 Reis 24:8-17; Crônica Babilônica ABC 5; Tabuletas de Ração de Joaquim em Berlim.",
            "https://en.wikipedia.org/wiki/Jeconiah",
            "Jerusalém / Babilônia", 32.5363, 44.4208, "jeconias,primeira_deportacao,nabucodonosor,juda"
        ),
        (
            2, "Rei Zedequias (Último Rei de Judá: 597-586 a.C.)", "Queda Definitiva de Jerusalém e Cegueira em Ribla",
            -597, 1, 1, -586, 7, 29, "range", 0, "rei_juda", "Jerusalém / Ribla / Babilônia",
            "Último monarca davídico a reinar em Jerusalém; rebelou-se imprudentemente contra a Babilônia; após cerco devastador de 18 meses, a cidade sucumbiu; viu seus filhos serem executados diante de si em Ribla, teve seus olhos vazados e foi arrastado em correntes de bronze para morrer na Babilônia.",
            "2 Reis 24:18 - 25:7; Jeremias 39, 52; 2 Crônicas 36:11-21.",
            "https://en.wikipedia.org/wiki/Zedekiah",
            "Jerusalém / Ribla", 34.4500, 36.5667, "zedequias,queda_jerusalem,fim_monarquia,babilônia,juda"
        )
    ])

    # =========================================================================
    # EIXO 2: CRONOLOGIA BÍBLICA - PROFETAS DE ISRAEL E JUDÁ
    # =========================================================================
    eventos.extend([
        (
            2, "Profeta Elias, o Tesbita", "O Confronto no Monte Carmelo e a Carruagem de Fogo",
            -900, 1, 1, -849, 12, 31, "range", 10, "profeta", "Gileade / Monte Carmelo",
            "Profeta do Reino do Norte; ordenou a seca por 3 anos e meio; desafiou e venceu os 450 profetas de Baal no Monte Carmelo com fogo descido do céu; arrebatado aos céus em um redemoinho com uma carruagem e cavalos de fogo.",
            "1 Reis 17-19, 21; 2 Reis 1-2; Malaquias 4:5; Mateus 17:1-3.", "https://en.wikipedia.org/wiki/Elijah",
            "Monte Carmelo / Rio Jordão", 32.7389, 35.0444, "elias,carmelo,fogo_do_ceu,carruagem,profeta"
        ),
        (
            2, "Profeta Eliseu", "Porção Dobrada do Espírito e Milagres em Israel",
            -890, 1, 1, -800, 12, 31, "range", 10, "profeta", "Samaria / Rio Jordão",
            "Sucessor de Elias; recebeu porção dobrada de seu espírito; realizou inúmeros milagres (cura de Naamã o sírio da lepra, ressurreição do filho da sunamita, flutuação do machado de ferro); conselheiro espiritual de reis durante 60 anos.",
            "1 Reis 19:16-21; 2 Reis 2-13; Lucas 4:27.", "https://en.wikipedia.org/wiki/Elisha",
            "Samaria / Suném / Jericó", 32.2770, 35.1906, "eliseu,milagres,naama,sunamita,profeta"
        ),
        (
            2, "Profeta Jonas", "A Missão a Nínive e o Grande Peixe",
            -785, 1, 1, -760, 12, 31, "range", 10, "profeta", "Gate-Hefer / Nínive",
            "Profeta do norte sob Jeroboão II; tentou fugir de seu chamado embarcando para Társis; engolido por um grande peixe, orou e foi expelido; pregou o juízo em Nínive, capital assíria, resultando em arrependimento coletivo.",
            "Livro de Jonas; 2 Reis 14:25; Mateus 12:39-41.", "https://en.wikipedia.org/wiki/Jonah",
            "Nínive (Mossul, Iraque)", 36.3596, 43.1528, "jonas,ninive,arrependimento,peixe,profeta"
        ),
        (
            2, "Profeta Amós de Tecoa", "Voz da Justiça Social e Retidão Moral",
            -760, 1, 1, -750, 12, 31, "range", 5, "profeta", "Tecoa (Judá) / Betel",
            "Pastor e cultivador de sicômoros do sul; enviado por Deus ao próspero e idólatra Reino do Norte sob Jeroboão II; denunciou a opressão aos pobres e hipocrisia cúltica: 'Corra, porém, a justiça como as águas, e a retidão, como um ribeiro perene' (Amós 5:24).",
            "Livro de Amós; Atos 7:42-43.", "https://en.wikipedia.org/wiki/Amos_(prophet)",
            "Betel / Tecoa", 31.6167, 35.2167, "amos,justica_social,betel,profeta"
        ),
        (
            2, "Profeta Oseias", "O Amor Incondicional de Deus e a Esposa Infiel",
            -755, 1, 1, -715, 12, 31, "range", 10, "profeta", "Reino do Norte (Israel)",
            "Instruído por Deus a desposar Gômer, mulher infiel, como alegoria viva do adultério espiritual de Israel com ídolos pagãos; profetizou a ruína iminente de Samaria combinada com a promessa da reconciliação compassiva de Yahweh.",
            "Livro de Oseias; Romanos 9:25-26.", "https://en.wikipedia.org/wiki/Hosea",
            "Samaria", 32.2770, 35.1906, "oseias,amor_de_deus,gomer,reconciliacao,profeta"
        ),
        (
            2, "Profeta Isaías de Jerusalém (Proto-Isaías)", "O Santo de Israel e o Rei Messias",
            -765, 1, 1, -686, 12, 31, "range", 10, "profeta", "Jerusalém",
            "Cortesão e teólogo monumental em Jerusalém sob os reis Uzias, Jotão, Acaz e Ezequias; teve a visão de Deus no Templo ('Santo, Santo, Santo'); profetizou o nascimento do Emanuel (7:14) e o Príncipe da Paz (9:6); segundo a tradição judaica foi serrado ao meio sob Manassés.",
            "Livro de Isaías 1-39; 2 Reis 19-20; Hebreus 11:37.", "https://en.wikipedia.org/wiki/Isaiah",
            "Jerusalém", 31.7767, 35.2345, "isaias,emanuel,santo_de_israel,serafins,profeta"
        ),
        (
            2, "Profeta Miqueias de Moresete", "A Origem Eterna do Messias em Belém",
            -740, 1, 1, -690, 12, 31, "range", 10, "profeta", "Moresete-Gate / Jerusalém",
            "Profeta camponês das colinas de Judá; defendeu agricultores espoliados pelos poderosos de Jerusalém; imortalizou a profecia do Messias: 'E tu, Belém-Efrata, de ti me sairá aquele que há de reinar em Israel, cujas saídas são desde a eternidade' (Miquéias 5:2).",
            "Livro de Miqueias; Jeremias 26:18; Mateus 2:5-6.", "https://en.wikipedia.org/wiki/Micah_(prophet)",
            "Moresete / Belém", 31.6000, 34.9000, "miqueias,belem,messias,moresete,profeta"
        ),
        (
            2, "Profeta Naum de Elcos", "O Juízo Final sobre a Sanguinária Nínive",
            -660, 1, 1, -612, 12, 31, "range", 10, "profeta", "Judá / Nínive",
            "Predisse com vivacidade poética impressionante a queda catastrófica de Nínive (-612 a.C.), a capital do Império Assírio, vingando as nações oprimidas por sua crueldade militar.",
            "Livro de Naum.", "https://en.wikipedia.org/wiki/Nahum",
            "Elcos / Nínive", 36.3596, 43.1528, "naum,ninive,queda_ninive,juizo,profeta"
        ),
        (
            2, "Profeta Sofonias", "O Grande e Terrível Dia do Senhor",
            -640, 1, 1, -621, 12, 31, "range", 10, "profeta", "Jerusalém",
            "Bisneto do piedoso rei Ezequias; profetizou nos primórdios do reinado de Josias, preparando espiritualmente a corte e a nação para as reformas purificadoras após décadas de degradação sob Manassés.",
            "Livro de Sofonias.", "https://en.wikipedia.org/wiki/Zephaniah",
            "Jerusalém", 31.7767, 35.2345, "sofonias,dia_do_senhor,reforma_josias,profeta"
        ),
        (
            2, "Profeta Habacuque", "O Justo Viverá pela Fé diante da Invasão Caldeia",
            -612, 1, 1, -589, 12, 31, "range", 5, "profeta", "Jerusalém",
            "Filósofo-profeta que dialoga honestamente com Deus sobre o mistério da providência: como o Todo-Poderoso podia usar os perversos babilônios (caldeus) para punir Judá? Recebe a resposta canônica: 'O justo viverá pela sua fé' (Hab 2:4).",
            "Livro de Habacuque; Romanos 1:17; Gálatas 3:11.", "https://en.wikipedia.org/wiki/Habakkuk",
            "Jerusalém", 31.7767, 35.2345, "habacuque,fe,caldeus,soberania,profeta"
        ),
        (
            2, "Profeta Jeremias (O Profeta Chorão)", "Quarenta Anos de Advertência, a Nova Aliança e o Exílio",
            -645, 1, 1, -570, 12, 31, "range", 5, "profeta", "Anatote / Jerusalém / Egito",
            "Chamado desde o ventre sob Josias; advertiu incessantemente contra falsas seguranças cúlticas; foi lançado em cisternas de lama por oficiais rebeldes; testemunhou com lágrimas o incêndio de Jerusalém e a deportação; profetizou o cativeiro de 70 anos e a Nova Aliança gravada no coração (Jr 31:31).",
            "Livro de Jeremias; Lamentações; 2 Crônicas 36:21-22.", "https://en.wikipedia.org/wiki/Jeremiah",
            "Anatote / Jerusalém / Tafnes (Egito)", 31.8167, 35.2667, "jeremias,nova_alianca,exilio,lamentacoes,profeta"
        ),
        (
            2, "Profeta Ezequiel", "O Vale de Ossos Secos e a Glória no Rio Quebar",
            -622, 1, 1, -565, 12, 31, "range", 5, "profeta", "Babilônia (Rio Quebar)",
            "Sacerdote de 25 anos deportado com o rei Joaquim em 597 a.C.; aos 30 anos contemplou a carruagem da glória divina na Babilônia; realizou dramatizações proféticas chocantes; profetizou a ressurreição nacional no vale de ossos secos (Ez 37) e a visão do novo Templo sagrado.",
            "Livro de Ezequiel.", "https://en.wikipedia.org/wiki/Ezekiel",
            "Tel-Abibe (Rio Quebar, Babilônia)", 32.1, 45.0, "ezequiel,ossos_secos,novo_templo,quebar,profeta"
        ),
        (
            2, "Profeta Daniel (Belsazar / Ciro)", "A Cova dos Leões e as Visões dos Quatro Impérios Mundiais",
            -620, 1, 1, -536, 12, 31, "range", 5, "profeta", "Babilônia / Susa",
            "Nobre judeu levado adolescente à Babilônia em 605 a.C.; manteve-se fiel recusando a comida real; decifrou os sonhos da estátua dos impérios mundiais e a escrita na parede para Belsazar; salvo milagrosamente da cova dos leões famintos sob Dario o Medo; revelou as 70 semanas messiânicas.",
            "Livro de Daniel; Mateus 24:15; Hebreus 11:33.", "https://en.wikipedia.org/wiki/Daniel_(biblical_figure)",
            "Babilônia / Susa (Pérsia)", 32.1892, 48.2578, "daniel,cova_dos_leoes,estatua,70_semanas,profeta"
        ),
        (
            2, "Profeta Ageu", "A Glória da Segunda Casa e o Apelo à Reconstrução",
            -520, 8, 1, -520, 12, 31, "point", 0, "profeta", "Jerusalém Pós-Exílica",
            "Desafiou com veemência a indiferença dos repatriados que viviam em casas apaineladas enquanto a casa de Deus jazia em ruínas; profetizou: 'A glória desta última casa será maior do que a da primeira' (Ageu 2:9).",
            "Livro de Ageu; Esdras 5:1, 6:14.", "https://en.wikipedia.org/wiki/Haggai",
            "Jerusalém", 31.7767, 35.2345, "ageu,reconstrucao_templo,esdras,segundo_templo,profeta"
        ),
        (
            2, "Profeta Zacarias", "O Rei Humilde Montado em um Jumento e as 30 Moedas de Prata",
            -520, 1, 1, -480, 12, 31, "range", 5, "profeta", "Jerusalém",
            "Contemporâneo de Ageu e Zorobabel; suas visões noturnas descortinam a restauração cósmica e sacerdotal de Jerusalém; profetizou a entrada triunfal do Rei montado num jumentinho (Zc 9:9), o preço da traição por 30 moedas de prata (11:12) e 'olharão para aquele a quem traspassaram' (12:10).",
            "Livro de Zacarias; Mateus 21:4-5, 27:9; João 19:37.", "https://en.wikipedia.org/wiki/Zechariah_(Hebrew_prophet)",
            "Jerusalém", 31.7767, 35.2345, "zacarias,messias,trinta_moedas,segundo_templo,profeta"
        ),
        (
            2, "Profeta Malaquias", "O Mensageiro da Aliança e a Promessa de Elias",
            -450, 1, 1, -430, 12, 31, "range", 5, "profeta", "Jerusalém",
            "Último dos profetas do Antigo Testamento; repreendeu o sacerdócio corrompido e dízimos negligenciados nos dias de Neemias; encerrou o cânon hebraico profetizando o Sol da Justiça e o envio de Elias precursor antes do grande Dia do Senhor.",
            "Livro de Malaquias; Mateus 11:10-14.", "https://en.wikipedia.org/wiki/Malachi",
            "Jerusalém", 31.7767, 35.2345, "malaquias,mensageiro,dizimos,ultimo_profeta_at,profeta"
        ),
        (
            2, "João Batista (O Precursor do Messias)", "A Voz que Clama no Deserto e o Batismo no Jordão",
            -5, 1, 1, 29, 8, 29, "range", 1, "profeta", "Deserto da Judeia / Rio Jordão",
            "Filho do sacerdote Zacarias e Isabel; viveu no deserto trajado de pelos de camelo alimentando-se de gafanhotos e mel silvestre; batizou as multidões e o próprio Jesus no Jordão proclamando o Cordeiro de Deus; degolado na fortaleza de Maquero por Herodes Antipas.",
            "Mateus 3, 11, 14; Marcos 1, 6; Lucas 1, 3; Flávio Josefo (Antiguidades XVIII.5.2).",
            "https://en.wikipedia.org/wiki/John_the_Baptist",
            "Rio Jordão / Fortaleza de Maquero", 31.5647, 35.6319, "joao_batista,precursor,batismo,jordao,maquero,profeta"
        )
    ])

    # Eventos Centrais Bíblicos Adicionais
    eventos.extend([
        (
            2, "Vida e Ministério de Jesus de Nazaré", "Crucificação sob Pôncio Pilatos",
            -4, 1, 1, 30, 4, 7, "range", 3, "narrativa", "Judeia/Galileia",
            "Nascimento (~6-4 a.C. sob Herodes), ministério na Galileia e Judeia, condenação por ordem do prefeito romano Pôncio Pilatos em Jerusalém e surgimento do movimento cristão.",
            "Evangelhos de Marcos, Mateus, Lucas e João; Tácito (Anais XV.44); Josefo (Ant. XVIII.3.3).",
            "https://en.wikipedia.org/wiki/Jesus",
            "Galileia / Jerusalém", 31.7767, 35.2345, "jesus,cristianismo,evangelho,pilatos"
        ),
        (
            2, "Queda de Jerusalém e Destruição do Segundo Templo", "Primeira Guerra Judaico-Romana (Tito)",
            70, 4, 1, 70, 9, 8, "point", 0, "batalha", "Roma/Judeia",
            "General Tito sitia e incendeia o Segundo Templo de Jerusalém; dispersão da nação judaica, fim do sacerdócio sacrificial saduceu e consolidação do judaísmo rabínico em Jâmnia.",
            "Flávio Josefo (A Guerra dos Judeus); Arco de Tito no Fórum Romano.",
            "https://en.wikipedia.org/wiki/Siege_of_Jerusalem_(70_CE)",
            "Jerusalém", 31.7780, 35.2354, "queda_templo,tito,roma,guerra_judaica,jamnia"
        )
    ])

    # =========================================================================
    # EIXO 3: MITOLOGIAS & COSMOGONIAS
    # =========================================================================
    eventos.extend([
        (
            3, "Enûma Eliš (Cosmogonia Babilônica da Criação)", "Marduk e o Triunfo sobre o Caos Primordial de Tiamat",
            -1800, 1, 1, -1100, 1, 1, "range", 200, "mito", "Babilônia",
            "Épico em 7 tábuas recitado anualmente no festival do Ano Novo (Akitu). Marduk divide o corpo do monstro aquático Tiamat para erigir o firmamento e a terra; confronto estilístico com Gênesis 1.",
            "7 Tabuletas Cuneiformes da Biblioteca Real de Nínive.",
            "https://en.wikipedia.org/wiki/En%C3%BBma_Eli%C5%A1",
            "Babilônia / Nínive", 32.5363, 44.4208, "enuma_elish,marduk,tiamat,cosmogonia,akitu"
        ),
        (
            3, "Epopeia de Gilgamesh e o Dilúvio Mesopotâmico", "A Tabuinha XI de Utnapishtim e a Arca",
            -2100, 1, 1, -1200, 1, 1, "range", 150, "mito", "Suméria/Babilônia",
            "Obra monumental da literatura mesopotâmica; a Tábua XI traz a narrativa do dilúvio mandado pelos deuses e a salvação de Utnapishtim em uma embarcação vedada com betume, paralela a Gênesis 6-9.",
            "Tabuletas cuneiformes decifradas por George Smith em 1872 (Museu Britânico).",
            "https://en.wikipedia.org/wiki/Epic_of_Gilgamesh",
            "Uruk / Nínive", 31.3222, 45.6361, "gilgamesh,diluvio,utnapishtim,arca,mesopotamia"
        ),
        (
            3, "Cosmogonia de Heliópolis e o Mito de Osíris", "Atum, o Oceano Nun e a Ressurreição no Duat",
            -2400, 1, 1, -1000, 1, 1, "range", 200, "mito", "Egito",
            "O deus solar Atum auto-emerge das águas caóticas primordiais de Nun gerando a Enéade sagrada; o ciclo de Osíris, Ísis e Hórus fundamenta a doutrina do julgamento da alma (Psicostasia).",
            "Textos das Pirâmides (Saqqara); Papiro de Ani (Livro dos Mortos).",
            "https://en.wikipedia.org/wiki/Ancient_Egyptian_creation_myths",
            "Heliópolis / Tebas (Egito)", 30.1290, 31.3060, "egito,atum,osiris,nun,livro_dos_mortos"
        ),
        (
            3, "Ciclo Cananeu de Baal (Textos de Ugarit)", "Baal-Hadad contra Yam (Mar Caótico) e Mot (Morte)",
            -1400, 1, 1, -1200, 1, 1, "range", 100, "mito", "Cananeia/Ugarit",
            "Mitologia da costa levantina encontrada em Ras Shamra; o deus El e o deus das tempestades Baal em conflito cósmico com as forças marinhas e da seca; contextualiza os anátemas dos profetas bíblicos.",
            "Tabuletas alfabéticas cuneiformes de Ras Shamra (Ugarit, 1929).",
            "https://en.wikipedia.org/wiki/Baal_Cycle",
            "Ras Shamra (Ugarit, Síria)", 35.6022, 35.7825, "ugarit,baal,cananeu,ras_shamra,el"
        ),
        (
            3, "Teogonia de Hesíodo (Cosmogonia Grega)", "Do Caos Primordial à Soberania Olímpica de Zeus",
            -730, 1, 1, -700, 1, 1, "range", 30, "mito", "Grécia",
            "Poema épico genealógico grego: nascimento do cosmos a partir do Caos primordial, Terra (Gaia) e Amor (Eros); castração de Urano por Cronos e a Titanomaquia que coroa Zeus.",
            "Texto poético em hexâmetro dactílico de Hesíodo.",
            "https://en.wikipedia.org/wiki/Theogony",
            "Beócia / Monte Hélicon (Grécia)", 38.3750, 23.3200, "hesiodo,teogonia,zeus,caos,grecia"
        ),
        (
            3, "Cultos de Mistério Greco-Romanos & Mitraísmo", "Mistérios Eleusinos, Ísis e o Culto Solar de Mitra",
            -300, 1, 1, 350, 1, 1, "range", 50, "mito", "Grécia/Roma",
            "Religiões iniciáticas de salvação pessoal e imortalidade da alma; o culto a Mitra com o sacrifício do touro cósmico (tauroctonia) tornou-se a religião militar mais difundida do Império Romano.",
            "Mitreus arqueológicos de Óstia e Roma; Apuleio (O Asno de Ouro XI).",
            "https://en.wikipedia.org/wiki/Mithraism",
            "Roma / Óstia / Eleusis", 41.9028, 12.4964, "misterios,mitra,eleusis,iniciacao,roma"
        )
    ])

    # =========================================================================
    # EIXO 4: MANUSCRITOS, CÂNON & CONCÍLIOS
    # =========================================================================
    eventos.extend([
        (
            4, "Tradução da Septuaginta (LXX)", "A Bíblia Hebraica traduzida para o Grego Koiné",
            -250, 1, 1, -132, 1, 1, "range", 30, "manuscrito", "Alexandria (Judaísmo Helenístico)",
            "Tradução da Torá e livros históricos/poéticos para o grego em Alexandria sob mecenato dos Ptolomeus; incluiu livros deuterocanônicos e tornou-se a base textual citada pelos apóstolos do NT.",
            "Carta de Aristeias; Prólogo grego do Eclesiástico (132 a.C.).",
            "https://en.wikipedia.org/wiki/Septuagint",
            "Alexandria (Egito)", 31.2001, 29.9187, "septuaginta,lxx,alexandria,grego_koine"
        ),
        (
            4, "Manuscritos do Mar Morto (Comunidade de Qumran)", "A mais antiga biblioteca bíblica descoberta",
            -250, 1, 1, 68, 6, 1, "range", 20, "manuscrito", "Judeia/Qumran",
            "Mais de 900 manuscritos hebraicos e aramaicos em 11 cavernas; atesta o texto bíblico com mil anos de antecedência ao Códice de Leningrado e preserva obras como 1 Enoque e Jubileus.",
            "Grande Rolo de Isaías (1QIsaa); Regra da Comunidade (1QS); Rolo do Templo (11Q19).",
            "https://en.wikipedia.org/wiki/Dead_Sea_Scrolls",
            "Cavernas de Qumran (Mar Morto)", 31.7410, 35.4590, "qumran,mar_morto,manuscritos,rolos"
        ),
        (
            4, "Cânon de Marcião e Fragmento Muratoriano", "Primeiras catalogações formais de livros do NT",
            144, 1, 1, 200, 12, 31, "range", 25, "manuscrito", "Roma",
            "A heresia de Marcião em Roma (144 d.C.) rejeita todo o Antigo Testamento e restringe o NT a Lucas e 10 epístolas de Paulo; em réplica, a Igreja formula listas canônicas como o Cânon Muratoriano.",
            "Fragmento Muratoriano (Códice do séc. VII na Bibl. Ambrosiana de Milão).",
            "https://en.wikipedia.org/wiki/Muratorian_fragment",
            "Roma (Itália)", 41.9028, 12.4964, "muratori,marciao,canon_nt,heresias"
        ),
        (
            4, "Concílio de Roma (382 d.C.)", "Decreto Damasino sobre o Cânon Bíblico Ocidental",
            382, 1, 1, 382, 12, 31, "box", 0, "concilio", "Igreja Ocidental",
            "Sínodo sob o Papa Dâmaso I, com São Jerônimo como secretário; estabelece o cânon bíblico ocidental com os 73 livros (incluindo deuterocanônicos) e encomenda a revisão da Bíblia Latina (Vulgata).",
            "Decretum Damasi / Decretum Gelasianum de libris recipiendis et non recipiendis.",
            "https://en.wikipedia.org/wiki/Council_of_Rome",
            "Roma (Itália)", 41.9028, 12.4964, "concilio_roma,damaso,jeronimo,vulgata,canon"
        ),
        (
            4, "Sínodo de Hipona (393) e Concílios de Cartago (397 e 419)", "Fixação Canônica com Santo Agostinho",
            393, 1, 1, 397, 8, 28, "range", 0, "concilio", "Igreja Norte-Africana",
            "Sob a liderança de Aurélio de Cartago e Santo Agostinho, a Igreja Africana promulga no Cânon 36 a lista oficial de 46 livros do AT e 27 do NT, solicitando confirmação da sé episcopal de Roma.",
            "Breviarium Hipponense; Atas do III Concílio de Cartago (397); Codex Canonum Ecclesiae Africanae.",
            "https://en.wikipedia.org/wiki/Councils_of_Carthage",
            "Hipona e Cartago (Norte da África)", 36.9000, 7.7667, "hipona,cartago,agostinho,canon_africano"
        ),
        (
            4, "Concílio de Florença (1442 d.C.)", "Bula Cantate Domino para a União com os Coptas",
            1442, 2, 4, 1442, 2, 4, "box", 0, "concilio", "Igreja Católica / União Oriental",
            "O Papa Eugênio IV sela a comunhão com a Igreja Copta do Egito e decreta formalmente a lista completa dos 73 livros inspirados do Antigo e do Novo Testamento.",
            "Bula Papal Cantate Domino (Denzinger 1334-1336).",
            "https://en.wikipedia.org/wiki/Council_of_Florence",
            "Florença (Itália)", 43.7696, 11.2558, "florenca,cantate_domino,eugenio_iv,uniao_coptas"
        ),
        (
            4, "Concílio de Trento (1546 d.C. - 4ª Sessão)", "Definição Dogmática Solene com Anátema contra a Reforma",
            1546, 4, 8, 1546, 4, 8, "box", 0, "concilio", "Igreja Católica (Contrarreforma)",
            "Em resposta à distinção protestante feita por Lutero, os Padres Conciliares definem sob anátema a igual autoridade e inspiração divina de todos os 73 livros com todas as suas partes tal como contidos na Vulgata Latina.",
            "Decretum de Canonicis Scripturis, Sessão IV do Concílio de Trento.",
            "https://en.wikipedia.org/wiki/Council_of_Trent",
            "Trento (Itália)", 46.0711, 11.1211, "trento,dogma,anatema,contrarreforma,lutero"
        ),
        (
            4, "Sínodo de Jerusalém / Belém (1672 d.C.)", "Confissão de Fé de Dositeu (Igreja Ortodoxa)",
            1672, 3, 16, 1672, 3, 20, "box", 0, "concilio", "Igreja Ortodoxa Oriental",
            "Convocado pelo Patriarca Dositeu de Jerusalém para repelir teses calvinistas infiltradas; ratifica no Decreto 18 a plena canonicidade dos Anaginoskomena (Sabedoria, Eclesiástico, Tobias, Judite, etc.).",
            "Confissão de Dositeu, Decreto 18 (Sínodo de Belém/Jerusalém).",
            "https://en.wikipedia.org/wiki/Synod_of_Jerusalem_(1672)",
            "Jerusalém / Belém", 31.7054, 35.2024, "ortodoxia,dositeu,jerusalem,anaginoskomena"
        )
    ])

    cursor.executemany("""
        INSERT INTO eventos (
            eixo_id, titulo, subtitulo,
            ano_inicio, mes_inicio, dia_inicio,
            ano_fim, mes_fim, dia_fim,
            tipo_tempo, incerteza_anos, categoria, cultura_origem,
            descricao, fontes_historicas, wikipedia_url, localizacao, latitude, longitude, tags
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, eventos)
    print(f"[OK] {len(eventos)} eventos e personagens históricos inseridos.")

    # 4. Livros Bíblicos e Apócrifos
    livros = [
        (
            "Gênesis", "Bereshit (בְּרֵאשִׁית)", "AT", "Torá/Pentateuco", "Hebraico",
            "Moisés (tradicional)", -1440, -500, "Fontes JEDP unificadas na redação sacerdotal pós-exílica (~séc. VI a.C.)",
            "https://en.wikipedia.org/wiki/Book_of_Genesis",
            "Origens cósmicas, dilúvio primordial, narrativas patriarcais (Abraão a José) e a escolha da linhagem da aliança."
        ),
        (
            "Êxodo", "Shemot (שְׁמוֹת)", "AT", "Torá/Pentateuco", "Hebraico",
            "Moisés (tradicional)", -1440, -500, "Tradições mosaicas pré-monárquicas codificadas na redação sacerdotal",
            "https://en.wikipedia.org/wiki/Book_of_Exodus",
            "Libertação do cativeiro egípcio, travessia do Mar Vermelho, outorga do Decálogo no Monte Sinai e tabernáculo."
        ),
        (
            "Isaías", "Yeshayahu (יְשַׁעְיָהוּ)", "AT", "Profético", "Hebraico",
            "Isaías filho de Amoz e discípulos (Proto, Dêutero e Trito-Isaías)", -740, -515, "Divisão crítica em 3 períodos: caps 1-39 (século VIII a.C.), caps 40-55 (exílio), caps 56-66 (pós-exílio)",
            "https://en.wikipedia.org/wiki/Book_of_Isaiah",
            "Julgamento sobre Judá e nações, oráculos messiânicos (Emanuel, Servo Sofredor) e promessa de consolo e restauração."
        ),
        (
            "Salmos", "Tehilim (תְּהִלִּים)", "AT", "Sapiencial/Poético", "Hebraico",
            "Davi, Asafe, Filhos de Corá e anônimos", -1000, -300, "Antologia poética e litúrgica compilada progressivamente ao longo de séculos",
            "https://en.wikipedia.org/wiki/Psalms",
            "Hinário sagrado de Israel em 150 poemas divididos em 5 livros: súplicas, louvores cósmicos, arrependimento e salmos reais messiânicos."
        ),
        (
            "Tobias", "Tobi (Τωβίθ)", "INTERTESTAMENTARIO", "Histórico/Edificante", "Aramaico/Hebraico (preservado em Grego)",
            "Anônimo judeu da Diáspora", -225, -175, "Composição helenística tardia; fragmentos hebraicos e aramaicos encontrados em Qumran (4Q196-200)",
            "https://en.wikipedia.org/wiki/Book_of_Tobit",
            "Narra a piedade de Tobit na Assíria, a jornada curativa de seu filho Tobias guiado pelo arcanjo Rafael e o exorcismo de Asmodeu."
        ),
        (
            "Judite", "Ioudith (Ἰουδίθ)", "INTERTESTAMENTARIO", "Histórico/Narrativo", "Hebraico original perdido (preservado na Septuaginta)",
            "Anônimo judeu da Judeia", -150, -100, "Escrito durante a resistência macabeia em grego ou hebraico",
            "https://en.wikipedia.org/wiki/Book_of_Judith",
            "A virtuosa viúva Judite infiltra-se no acampamento do general invasor Holofernes e o decapita, salvando a cidade de Betúlia e o Templo."
        ),
        (
            "Sabedoria de Salomão", "Sophia Salomonis (Σοφία Σαλoμῶντος)", "INTERTESTAMENTARIO", "Sapiencial", "Grego Koiné",
            "Pseudo-Salomão (sábio judeu alexandrino)", -100, -30, "Composto em Alexandria; obra-prima do judaísmo helenístico filosófico",
            "https://en.wikipedia.org/wiki/Book_of_Wisdom",
            "Tratado sapiencial que exalta a Sabedoria personificada emanada de Deus, defende a imortalidade da alma e ataca a idolatria pagã."
        ),
        (
            "Eclesiástico (Sirácida)", "Hokmat Ben Sira (Σοφία Ἰησοῦ Σειράχ)", "INTERTESTAMENTARIO", "Sapiencial", "Hebraico (traduzido ao Grego em 132 a.C.)",
            "Jesus Ben Sira (Yeshua ben Eleazar ben Sira)", -190, -175, "Original hebraico escrito em Jerusalém; prólogo grego do neto em Alexandria em 132 a.C.",
            "https://en.wikipedia.org/wiki/Sirach",
            "Compêndio monumental de ética prática, temor de Deus, amizade, família e elogio aos antepassados ilustres de Israel."
        ),
        (
            "Baruc", "Baruch (Βαρούχ)", "INTERTESTAMENTARIO", "Profético/Exortativo", "Hebraico/Aramaico (preservado em Grego)",
            "Atribuído a Baruc ben Nerias (secretário de Jeremias)", -200, -60, "Composição pós-exílica com adições helenísticas (inclui a Carta de Jeremias)",
            "https://en.wikipedia.org/wiki/Book_of_Baruch",
            "Oração penitencial do cativeiro, reflexão sobre a Sabedoria divina manifestada na Torá e mensagem consoladora para Jerusalém."
        ),
        (
            "1 Macabeus", "Makkabaion A (Μακκαβαίων Αʹ)", "INTERTESTAMENTARIO", "Histórico", "Hebraico original perdido (preservado em Grego)",
            "Historiador oficial da corte dos príncipes asmoneus", -104, -63, "Redigido na Judeia sob João Hircano I",
            "https://en.wikipedia.org/wiki/1_Maccabees",
            "Crônica militar e política da insurreição de Matatias e da liderança de Judas Macabeu contra a tirania selêucida até a fundação da dinastia asmoneia."
        ),
        (
            "2 Macabeus", "Makkabaion B (Μακκαβαίων Βʹ)", "INTERTESTAMENTARIO", "Histórico/Teológico", "Grego Koiné",
            "Jasão de Cirene (compilado por autor anônimo)", -124, -60, "Epítome em grego retórico de cinco volumes originais de Jasão de Cirene",
            "https://en.wikipedia.org/wiki/2_Maccabees",
            "Foca na teologia do martírio, na ressurreição corpórea dos justos, na oração em favor dos mortos (2 Mac 12) e na criação ex-nihilo."
        ),
        (
            "3 Macabeus", "Makkabaion C (Μακκαβαίων Γʹ)", "INTERTESTAMENTARIO", "Histórico/Narrativo", "Grego Koiné",
            "Judeu alexandrino", -100, -50, "Narrativa helenística sobre o reinado de Ptolomeu IV Filopátor",
            "https://en.wikipedia.org/wiki/3_Maccabees",
            "Relata a tentativa de profanação do Templo pelo faraó ptolomaico e o milagroso livramento dos judeus de Alexandria condenados ao pisoteio por elefantes embriagados."
        ),
        (
            "Oração de Manassés", "Proseuche Manasse (Προσευχὴ Μανασσῆ)", "INTERTESTAMENTARIO", "Poético/Penitencial", "Grego Koiné",
            "Atribuído ao Rei Manassés de Judá (2 Crônicas 33)", -150, 50, "Hino penitencial helenístico preservado nas Odes da Septuaginta",
            "https://en.wikipedia.org/wiki/Prayer_of_Manasseh",
            "Súplica de profundo arrependimento proferida em cadeias na Babilônia, ressaltando que a misericórdia de Deus supera a multidão dos pecados."
        ),
        (
            "Salmo 151", "Psalmos 151 (Ψαλμὸς 151)", "INTERTESTAMENTARIO", "Poético", "Hebraico (encontrado em 11QPs de Qumran)",
            "Atribuído a Davi", -200, -100, "Salmo presente na Septuaginta grega e confirmado em hebraico nos Rolos do Mar Morto",
            "https://en.wikipedia.org/wiki/Psalm_151",
            "Davi relata sua juventude humilde pastoreando ovelhas, a unção por Samuel e a vitória decepando o gigante Golias com sua própria espada."
        ),
        (
            "Evangelho de Mateus", "Kata Matthaion (Κατὰ Μαθθαῖον)", "NT", "Evangelho", "Grego Koiné",
            "Apóstolo Mateus (Levi)", 70, 85, "Composto após a queda do Segundo Templo para uma comunidade judaico-cristã",
            "https://en.wikipedia.org/wiki/Gospel_of_Matthew",
            "Retrata Jesus como o Messias davídico e novo Moisés no Sermão da Montanha, cumpridor rigoroso de toda a Lei e Profetas."
        ),
        (
            "Epístola aos Romanos", "Pros Romaious (Πρὸς Ῥωμαίους)", "NT", "Epístola", "Grego Koiné",
            "Apóstolo Paulo de Tarso", 56, 58, "Escrita em Corinto durante sua terceira viagem missionária",
            "https://en.wikipedia.org/wiki/Epistle_to_the_Romans",
            "Magna Carta da teologia paulina: justificação universal pela fé em Cristo, graça, redenção, eleição de Israel e ética comunitária."
        ),
        (
            "Apocalipse de João", "Apokalypsis Ioannou (Ἀποκάλυψις Ἰωάννου)", "NT", "Apocalíptico", "Grego Koiné",
            "João em Patmos", 90, 96, "Redigido durante as perseguições imperiais sob Domiciano",
            "https://en.wikipedia.org/wiki/Book_of_Revelation",
            "Visões proféticas do Cordeiro imolado, juízos cósmicos sobre a Besta e Babilônia, e o triunfo final com a descida da Nova Jerusalém."
        ),
        (
            "Evangelho de Tomé", "Evangelho Copta de Tomé", "APOCRIFO_NT", "Ditos / Gnóstico", "Copta (original grego fragmentário em Oxirrinco)",
            "Pseudo-Tomé (comunidade gnóstica)", 130, 180, "Coleção de 114 sentenças secretas; redescoberto na Biblioteca de Nag Hammadi em 1945",
            "https://en.wikipedia.org/wiki/Gospel_of_Thomas",
            "Rejeita a redenção histórica pela crucificação e prega o despertar gnóstico do divino interior para superar a morte."
        ),
        (
            "Didaquê (Ensino dos Doze Apóstolos)", "Didache (Διδαχή)", "APOCRIFO_NT", "Manual Litúrgico Eclesiástico", "Grego Koiné",
            "Líderes anônimos da Igreja Apostólica", 70, 110, "Mais antigo catecismo cristão primitivo; manuscrito redescoberto em Istambul em 1873 por Bryennios",
            "https://en.wikipedia.org/wiki/Didache",
            "A Doutrina dos Dois Caminhos (Vida e Morte), fórmulas batismais por imersão/aspersão, jejum semanal, oração do Pai Nosso e a Eucaristia."
        ),
        (
            "Pastor de Hermas", "Poimen tou Herma (Ποιμὴν τοῦ Ἑρμᾶ)", "APOCRIFO_NT", "Apocalíptico/Alegórico", "Grego Koiné",
            "Hermas de Roma", 130, 155, "Texto altamente estimado na Igreja Antiga (presente no Códice Sinaítico junto ao NT)",
            "https://en.wikipedia.org/wiki/The_Shepherd_of_Hermas",
            "Série de visões, mandamentos morais e parábolas concedidas por um anjo em trajes pastoris sobre a possibilidade de penitência pós-batismal."
        )
    ]

    cursor.executemany("""
        INSERT INTO livros (
            nome, nome_original, testamento, genero_literario, idioma_original,
            autor_tradicional, ano_composicao_inicio, ano_composicao_fim,
            data_consenso_critico, wikipedia_url, resumo
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, livros)
    print(f"[OK] {len(livros)} livros bíblicos e apócrifos inseridos.")

    # 5. Status Canônico
    status_regras = [
        ("Gênesis", [
            ("JUDAICA", "CANONICO", "Primeiro livro da Torá (Tanakh)."),
            ("PROTESTANTE", "CANONICO", "Primeiro livro canônico do Antigo Testamento."),
            ("CATOLICA", "CANONICO", "Livro plenamente canônico e inspirado."),
            ("ORTODOXA", "CANONICO", "Livro plenamente canônico e inspirado.")
        ]),
        ("Êxodo", [
            ("JUDAICA", "CANONICO", "Segundo livro da Torá."),
            ("PROTESTANTE", "CANONICO", "Livro canônico histórico da Lei."),
            ("CATOLICA", "CANONICO", "Livro plenamente canônico."),
            ("ORTODOXA", "CANONICO", "Livro plenamente canônico.")
        ]),
        ("Isaías", [
            ("JUDAICA", "CANONICO", "Nevi'im (Profetas)."),
            ("PROTESTANTE", "CANONICO", "Profeta Maior canônico."),
            ("CATOLICA", "CANONICO", "Profeta Maior canônico."),
            ("ORTODOXA", "CANONICO", "Profeta Maior canônico.")
        ]),
        ("Salmos", [
            ("JUDAICA", "CANONICO", "Ketuvim (Escritos Sagrados)."),
            ("PROTESTANTE", "CANONICO", "Hinário canônico em 150 salmos."),
            ("CATOLICA", "CANONICO", "Hinário canônico fundamental da Liturgia."),
            ("ORTODOXA", "CANONICO", "Saltério canônico litúrgico.")
        ]),
        ("Tobias", [
            ("JUDAICA", "APOCRIFO", "Não incluído no cânon hebraico masorético."),
            ("PROTESTANTE", "APOCRIFO", "Classificado por Lutero como livro apócrifo: não igual às Escrituras, mas útil para leitura."),
            ("CATOLICA", "DEUTEROCANONICO", "Canônico dogmático sob anátema (Concílio de Trento, 1546)."),
            ("ORTODOXA", "ANAGINOSKOMENA", "Canônico (Anaginoskomena) pelo Sínodo de Jerusalém (1672).")
        ]),
        ("Judite", [
            ("JUDAICA", "APOCRIFO", "Excluído da Bíblia Hebraica."),
            ("PROTESTANTE", "APOCRIFO", "Apócrifo instrutivo sem força dogmática."),
            ("CATOLICA", "DEUTEROCANONICO", "Canônico dogmático (Trento)."),
            ("ORTODOXA", "ANAGINOSKOMENA", "Canônico na tradição da Septuaginta grega.")
        ]),
        ("Sabedoria de Salomão", [
            ("JUDAICA", "APOCRIFO", "Composição em grego alexandrino; fora do Tanakh."),
            ("PROTESTANTE", "APOCRIFO", "Apócrifo intertestamentário sem base para doutrina."),
            ("CATOLICA", "DEUTEROCANONICO", "Canônico e divinamente inspirado."),
            ("ORTODOXA", "ANAGINOSKOMENA", "Canônico (Anaginoskomena).")
        ]),
        ("Eclesiástico (Sirácida)", [
            ("JUDAICA", "APOCRIFO", "Citado no Talmude como obra de sabedoria, mas excluído do cânon bíblico."),
            ("PROTESTANTE", "APOCRIFO", "Apócrifo de elevado teor ético-moral."),
            ("CATOLICA", "DEUTEROCANONICO", "Canônico dogmático confirmado em Hipona, Cartago e Trento."),
            ("ORTODOXA", "ANAGINOSKOMENA", "Canônico e amplamente usado na teologia patrística.")
        ]),
        ("Baruc", [
            ("JUDAICA", "APOCRIFO", "Fora do cânon masorético."),
            ("PROTESTANTE", "APOCRIFO", "Livro apócrifo ligado a Jeremias."),
            ("CATOLICA", "DEUTEROCANONICO", "Canônico (inclui a Epístola de Jeremias no cap. 6)."),
            ("ORTODOXA", "ANAGINOSKOMENA", "Canônico na Septuaginta.")
        ]),
        ("1 Macabeus", [
            ("JUDAICA", "APOCRIFO", "História venerada de Hanucá, porém sem inspiração profética no Tanakh."),
            ("PROTESTANTE", "APOCRIFO", "Apócrifo com imenso valor para a história do período intertestamentário."),
            ("CATOLICA", "DEUTEROCANONICO", "Canônico dogmático pleno."),
            ("ORTODOXA", "ANAGINOSKOMENA", "Canônico pleno.")
        ]),
        ("2 Macabeus", [
            ("JUDAICA", "APOCRIFO", "Fora do cânon hebraico."),
            ("PROTESTANTE", "APOCRIFO", "Apócrifo rejeitado dogmaticamente por Lutero devido à doutrina do sufrágio pelos mortos."),
            ("CATOLICA", "DEUTEROCANONICO", "Canônico dogmático pleno (apoio bíblico para oração pelos defuntos)."),
            ("ORTODOXA", "ANAGINOSKOMENA", "Canônico pleno.")
        ]),
        ("3 Macabeus", [
            ("JUDAICA", "APOCRIFO", "Fora do cânon judaico."),
            ("PROTESTANTE", "APOCRIFO", "Pseudepígrafo histórico."),
            ("CATOLICA", "APOCRIFO", "Não aceito nem listado nos concílios ocidentais."),
            ("ORTODOXA", "ANAGINOSKOMENA", "Canônico na Bíblia Ortodoxa Grega e Eslava.")
        ]),
        ("Oração de Manassés", [
            ("JUDAICA", "APOCRIFO", "Fora do Tanakh."),
            ("PROTESTANTE", "APOCRIFO", "Apêndice apócrifo."),
            ("CATOLICA", "APOCRIFO", "Não dogmático; preservado apenas em apêndice da Vulgata Clementina para não se perder."),
            ("ORTODOXA", "ANAGINOSKOMENA", "Canônico, incorporado nas Odes litúrgicas.")
        ]),
        ("Salmo 151", [
            ("JUDAICA", "APOCRIFO", "Não numerado no Saltério de 150 salmos masoréticos."),
            ("PROTESTANTE", "APOCRIFO", "Não reconhecido."),
            ("CATOLICA", "APOCRIFO", "Não consta no cânon dogmático da Vulgata."),
            ("ORTODOXA", "ANAGINOSKOMENA", "Canônico no Saltério da Septuaginta.")
        ]),
        ("Evangelho de Mateus", [
            ("JUDAICA", "REJEITADO", "Literatura do Novo Testamento não reconhecida pelo judaísmo."),
            ("PROTESTANTE", "CANONICO", "Primeiro livro do Novo Testamento."),
            ("CATOLICA", "CANONICO", "Livro apostólico plenamente canônico."),
            ("ORTODOXA", "CANONICO", "Livro apostólico plenamente canônico.")
        ]),
        ("Epístola aos Romanos", [
            ("JUDAICA", "REJEITADO", "Epístola apostólica cristã."),
            ("PROTESTANTE", "CANONICO", "Centro da soteriologia da Reforma."),
            ("CATOLICA", "CANONICO", "Epístola apostólica canônica."),
            ("ORTODOXA", "CANONICO", "Epístola apostólica canônica.")
        ]),
        ("Apocalipse de João", [
            ("JUDAICA", "REJEITADO", "Apocalíptica cristã."),
            ("PROTESTANTE", "CANONICO", "Último livro canônico do NT."),
            ("CATOLICA", "CANONICO", "Dogmaticamente canônico (Cartago, Florença e Trento)."),
            ("ORTODOXA", "CANONICO", "Reconhecido no cânon, porém tradicionalmente não lido na Divina Liturgia bizantina.")
        ]),
        ("Evangelho de Tomé", [
            ("JUDAICA", "REJEITADO", "Texto gnóstico herético."),
            ("PROTESTANTE", "REJEITADO", "Apócrifo gnóstico pseudepígrafo."),
            ("CATOLICA", "REJEITADO", "Condenado como herético pelos primeiros Padres da Igreja."),
            ("ORTODOXA", "REJEITADO", "Condenado como espúrio e fora da sucessão apostólica.")
        ]),
        ("Didaquê (Ensino dos Doze Apóstolos)", [
            ("JUDAICA", "REJEITADO", "Manual eclesiástico cristão."),
            ("PROTESTANTE", "APOCRIFO", "Texto dos Padres Apostólicos de grande valor histórico, mas fora do cânon bíblico."),
            ("CATOLICA", "APOCRIFO", "Documento patrístico venerável, mas não Escritura inspirada."),
            ("ORTODOXA", "APOCRIFO", "Patrístico primordial respeitado, porém não canônico.")
        ]),
        ("Pastor de Hermas", [
            ("JUDAICA", "REJEITADO", "Sem relação com a Bíblia."),
            ("PROTESTANTE", "APOCRIFO", "Apócrifo/Patrístico não inspirado."),
            ("CATOLICA", "APOCRIFO", "Excluído expressamente pelo Cânon Muratoriano e Atanásio da lista de livros divinamente inspirados."),
            ("ORTODOXA", "APOCRIFO", "Respeitado na patrística antiga, porém fora do cânon bíblico.")
        ])
    ]

    for nome_livro, tradicoes in status_regras:
        cursor.execute("SELECT id FROM livros WHERE nome = ?", (nome_livro,))
        row = cursor.fetchone()
        if row:
            livro_id = row[0]
            for tradicao, status, motivo in tradicoes:
                cursor.execute("""
                    INSERT INTO status_canonico (livro_id, tradicao, status, motivo_justificativa)
                    VALUES (?, ?, ?, ?)
                """, (livro_id, tradicao, status, motivo))

    print(f"[OK] {len(status_regras) * 4} status canônicos catalogados.")

    # 6. Concílios
    concilios = [
        (
            "Concílio de Roma (382 d.C.)", 382, None, "Roma", "Itália",
            41.9028, 12.4964, "Papa Dâmaso I", "São Jerônimo (consultor e tradutor da Vulgata)",
            "Convocado em Roma sob o Papa Dâmaso I durante as controvérsias arianas e apolinaristas.",
            "Primeira lista canônica do Ocidente latino preservada no Decretum Damasi, contendo os 46 livros do AT (com deuterocanônicos) e os 27 do NT. Dâmaso comissiona São Jerônimo para revisar os manuscritos latinos antigos e traduzir as Escrituras a partir do hebraico e grego originais (origem da Vulgata).",
            "Decretum Damasi / Decretum Gelasianum de libris recipiendis et non recipiendis.",
            "https://en.wikipedia.org/wiki/Council_of_Rome", 0
        ),
        (
            "Sínodo de Hipona (393 d.C.)", 393, None, "Hipona Regius (Annaba)", "Argélia (África Proconsular)",
            36.9000, 7.7667, "Aurélio de Cartago e Santo Agostinho (como presbítero influente)", "Bispos católicos da África",
            "Reunião plenária dos bispos norte-africanos para regularizar a disciplina eclesiástica e a liturgia.",
            "Aprovou o Breviarium Hipponense que estipulou que 'nada além das Escrituras canônicas seja lido na igreja sob o título de Escrituras divinas'. Fixou a lista de 46 livros do AT e 27 do NT, orientando envio das resoluções à Sé de Roma para confirmação.",
            "Breviarium Hipponense", "https://en.wikipedia.org/wiki/Synod_of_Hippo", 0
        ),
        (
            "III Concílio de Cartago (397 d.C.)", 397, None, "Cartago (Túnis)", "Tunísia",
            36.8529, 10.3217, "Aurélio de Cartago e Santo Agostinho (já bispo de Hipona)", "Bispos norte-africanos",
            "Ratificação e publicação formal dos cânones de Hipona para todas as províncias eclesiásticas do Ocidente.",
            "O famoso Cânon 36 (ou 47 em algumas compilações) lista nominalmente os 46 livros do Antigo Testamento (incluindo Tobias, Judite, Sabedoria, Eclesiástico, Baruc e os 2 livros dos Macabeus) e os 27 livros do Novo Testamento, determinando comunicação formal ao Bispo de Roma.",
            "Atas do III Concílio de Cartago (397)", "https://en.wikipedia.org/wiki/Councils_of_Carthage", 0
        ),
        (
            "Concílio de Florença (1442 d.C.)", 1442, None, "Florença", "Itália",
            43.7696, 11.2558, "Papa Eugênio IV", "Prelados católicos latinos e delegação copta do Egito",
            "17º Concílio Ecumênico da Igreja Católica; buscava restaurar a plena comunhão doutrinária com as igrejas do Oriente.",
            "A solene Bula Papal 'Cantate Domino' (4 de fevereiro de 1442) proclamou que um e o mesmo Deus inspirou os profetas do AT e os apóstolos do NT, enumerando de forma exaustiva o cânon de 73 livros.",
            "Bula Papal Cantate Domino (Denzinger 1334-1336)", "https://en.wikipedia.org/wiki/Council_of_Florence", 0
        ),
        (
            "Concílio de Trento (1546 d.C. - 4ª Sessão)", 1546, 1563, "Trento", "Itália",
            46.0711, 11.1211, "Papa Paulo III / Legados Cardeais Del Monte e Marcello Cervini", "Padres Conciliares e Teólogos da Cristandade",
            "19º Concílio Ecumênico; principal marco da Contrarreforma Católica para responder às teses da Reforma Protestante.",
            "Em 8 de abril de 1546, o decreto 'De Canonicis Scripturis' estabelece como artigo de FÉ DOGMÁTICA a igual reverência e inspiração divina de todos os 73 livros com todas as suas partes tal como contidos na Vulgata Latina, pronunciando solene ANÁTEMA contra quem recusar recebê-los.",
            "Decretum de Canonicis Scripturis (Sessio IV)", "https://en.wikipedia.org/wiki/Council_of_Trent", 1
        )
    ]

    for c in concilios:
        cursor.execute("SELECT id FROM eventos WHERE titulo LIKE ?", (f"%{c[0].split('(')[0].strip()}%",))
        ev_row = cursor.fetchone()
        evento_id = ev_row[0] if ev_row else None

        cursor.execute("""
            INSERT INTO concilios (
                evento_id, nome, ano, ano_fim, cidade, regiao,
                coordenadas_lat, coordenadas_lon, papa_ou_lideranca,
                participantes_principais, contexto_historico,
                decisoes_canonicidade, documento_oficial, wikipedia_url, anatemas_declarados
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (evento_id, c[0], c[1], c[2], c[3], c[4], c[5], c[6], c[7], c[8], c[9], c[10], c[11], c[12], c[13]))

    print(f"[OK] {len(concilios)} concílios históricos registrados com contexto dogmático e coordenadas.")

    # 7. Resoluções Conciliares Detalhadas por Livro
    cursor.execute("SELECT id FROM concilios WHERE nome LIKE '%Trento%'")
    trento_id = cursor.fetchone()[0]

    cursor.execute("SELECT id FROM concilios WHERE nome LIKE '%Cartago%'")
    cartago_id = cursor.fetchone()[0]

    livros_alvo = [
        ("Tobias", "DEUTEROCANONICO_ACEITO", "Declarado sagrado e canônico sob anátema."),
        ("Judite", "DEUTEROCANONICO_ACEITO", "Confirmado no catálogo solene tridentino."),
        ("1 Macabeus", "DEUTEROCANONICO_ACEITO", "Aceito integralmente como canônico."),
        ("2 Macabeus", "DEUTEROCANONICO_ACEITO", "Aceito integralmente, repudiando a exclusão de Lutero."),
        ("Sabedoria de Salomão", "DEUTEROCANONICO_ACEITO", "Ratificado como Escritura divinamente inspirada."),
        ("Pastor de Hermas", "EXCLUIDO_APOCRIFO", "Explicitamente não incluído no catálogo bíblico.")
    ]

    for nome_l, pos, trecho in livros_alvo:
        cursor.execute("SELECT id FROM livros WHERE nome = ?", (nome_l,))
        l_row = cursor.fetchone()
        if l_row:
            livro_id = l_row[0]
            cursor.execute("""
                INSERT INTO concilio_livro_decisoes (concilio_id, livro_id, posicionamento, trecho_decreto)
                VALUES (?, ?, ?, ?)
            """, (trento_id, livro_id, pos, f"Trento (1546): {trecho}"))
            if pos != "EXCLUIDO_APOCRIFO":
                cursor.execute("""
                    INSERT INTO concilio_livro_decisoes (concilio_id, livro_id, posicionamento, trecho_decreto)
                    VALUES (?, ?, ?, ?)
                """, (cartago_id, livro_id, pos, f"Cartago (397): Cânon 36 - Lido como Escritura canônica."))

    conn.commit()
    conn.close()
    print("Sucesso: Banco de dados 'timeline.db' criado e povoado com sucesso total!")

if __name__ == "__main__":
    inicializar_banco()
