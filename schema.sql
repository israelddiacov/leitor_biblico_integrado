-- ==============================================================================
-- SCHEMA RELACIONAL SQLITE: TIMELINE HISTÓRICO-BÍBLICA COMPARADA
-- Eixos: História Secular, Cronologia Bíblica, Mitologias e Cânon/Concílios
-- ==============================================================================

PRAGMA foreign_keys = ON;

-- 1. Tabela de Eixos / Trilhas Paralelas (Swimlanes)
CREATE TABLE IF NOT EXISTS eixos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo TEXT UNIQUE NOT NULL,             -- ex: 'SECULAR', 'BIBLICO', 'MITOLOGIA', 'CANON'
    nome TEXT NOT NULL,                      -- ex: 'História Secular & Grandes Impérios'
    icone TEXT,                              -- ex: '🏛️', '📜', '🏺', '⛪'
    cor_hex TEXT NOT NULL,                   -- ex: '#0284c7', '#d97706', '#7c3aed', '#059669'
    ordem_exibicao INTEGER NOT NULL DEFAULT 1
);

-- 2. Tabela Central de Eventos e Períodos Temporais
-- Suporta datas a.C. com inteiros negativos (ex: -586) e precisão de mês/dia
CREATE TABLE IF NOT EXISTS eventos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    eixo_id INTEGER NOT NULL,
    titulo TEXT NOT NULL,
    subtitulo TEXT,
    
    -- Balizas temporais de início (ano negativo = a.C.)
    ano_inicio INTEGER NOT NULL,
    mes_inicio INTEGER NOT NULL DEFAULT 1 CHECK (mes_inicio BETWEEN 1 AND 12),
    dia_inicio INTEGER NOT NULL DEFAULT 1 CHECK (dia_inicio BETWEEN 1 AND 31),
    
    -- Balizas temporais de fim (NULL para eventos pontuais / 'box')
    ano_fim INTEGER,
    mes_fim INTEGER DEFAULT 1 CHECK (mes_fim IS NULL OR mes_fim BETWEEN 1 AND 12),
    dia_fim INTEGER DEFAULT 1 CHECK (dia_fim IS NULL OR dia_fim BETWEEN 1 AND 31),
    
    tipo_tempo TEXT NOT NULL DEFAULT 'range' CHECK (tipo_tempo IN ('range', 'box', 'point')),
    incerteza_anos INTEGER DEFAULT 0,       -- Margem de incerteza em anos (+/- X anos)
    
    categoria TEXT NOT NULL,                 -- ex: 'imperio', 'batalha', 'narrativa', 'mito', 'manuscrito', 'concilio'
    cultura_origem TEXT,                     -- ex: 'Mesopotâmia', 'Egito', 'Pérsia', 'Grécia', 'Roma', 'Israel'
    
    descricao TEXT NOT NULL,
    fontes_historicas TEXT,                  -- Citações primárias: Josefo, Heródoto, Tabuletas Cuneiformes, etc.
    wikipedia_url TEXT,                      -- Link direto para artigo verificado na Wikipedia
    localizacao TEXT,                        -- Cidade, região ou bacia geográfica
    latitude REAL,
    longitude REAL,
    tags TEXT,                               -- Tags separadas por vírgula para filtragem
    
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (eixo_id) REFERENCES eixos(id) ON DELETE RESTRICT
);

-- 3. Tabela de Livros Bíblicos e Apócrifos (Metadados Literários)
CREATE TABLE IF NOT EXISTS livros (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT UNIQUE NOT NULL,               -- ex: 'Gênesis', '1 Macabeus', 'Evangelho de Tomé'
    nome_original TEXT,                      -- ex: 'Bereshit' (בְּרֵאשִׁית), 'Génesis' (Γένεσις)
    testamento TEXT NOT NULL CHECK (testamento IN ('AT', 'NT', 'INTERTESTAMENTARIO', 'APOCRIFO_NT', 'PSEUDEPIGRAFO')),
    genero_literario TEXT NOT NULL,          -- ex: 'Torá/Pentateuco', 'Histórico', 'Sapiencial', 'Profético', 'Evangelho', 'Epístola', 'Apocalíptico'
    idioma_original TEXT NOT NULL,           -- 'Hebraico', 'Aramaico', 'Grego Koiné', 'Copta', 'Latim'
    
    autor_tradicional TEXT,                  -- Atribuição confessional tradicional (ex: 'Moisés', 'Paulo')
    ano_composicao_inicio INTEGER,           -- Estimativa crítica da alta/baixa crítica textual
    ano_composicao_fim INTEGER,
    data_consenso_critico TEXT,              -- Resumo explicativo (ex: 'Sec. VI a.C. compilação sacerdotal pós-exílica')
    wikipedia_url TEXT,                      -- Link direto da Wikipedia
    resumo TEXT
);

-- 4. Status Canônico por Tradição
CREATE TABLE IF NOT EXISTS status_canonico (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    livro_id INTEGER NOT NULL,
    tradicao TEXT NOT NULL CHECK (tradicao IN ('JUDAICA', 'PROTESTANTE', 'CATOLICA', 'ORTODOXA')),
    status TEXT NOT NULL CHECK (status IN ('CANONICO', 'DEUTEROCANONICO', 'ANAGINOSKOMENA', 'APOCRIFO', 'REJEITADO')),
    motivo_justificativa TEXT,
    FOREIGN KEY (livro_id) REFERENCES livros(id) ON DELETE CASCADE,
    UNIQUE(livro_id, tradicao)
);

-- 5. Concílios, Sínodos e Marcos de Canonicidade
CREATE TABLE IF NOT EXISTS concilios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    evento_id INTEGER,                       -- Vinculação direta com a timeline visual
    nome TEXT UNIQUE NOT NULL,               -- ex: 'Sínodo de Hipona (393)', 'Concílio de Trento (1546)'
    ano INTEGER NOT NULL,
    ano_fim INTEGER,                         -- Caso dure vários anos (ex: Trento 1545-1563)
    cidade TEXT NOT NULL,
    regiao TEXT NOT NULL,
    coordenadas_lat REAL,
    coordenadas_lon REAL,
    papa_ou_lideranca TEXT,                  -- ex: 'Papa Dâmaso I', 'Santo Agostinho', 'Papa Paulo III'
    participantes_principais TEXT,
    contexto_historico TEXT NOT NULL,
    decisoes_canonicidade TEXT NOT NULL,
    documento_oficial TEXT,                  -- ex: 'Decretum de Canonicis Scripturis'
    anatemas_declarados INTEGER DEFAULT 0 CHECK (anatemas_declarados IN (0, 1)),
    wikipedia_url TEXT,                      -- Link verificado na Wikipedia
    FOREIGN KEY (evento_id) REFERENCES eventos(id) ON DELETE SET NULL
);

-- 6. Tabela Associativa de Resoluções Conciliares por Livro (Cruzamento Canônico Fino)
CREATE TABLE IF NOT EXISTS concilio_livro_decisoes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    concilio_id INTEGER NOT NULL,
    livro_id INTEGER NOT NULL,
    posicionamento TEXT NOT NULL CHECK (posicionamento IN ('CONFIRMADO_CANONICO', 'DEUTEROCANONICO_ACEITO', 'LEITURA_DEVOCIONAL_SEM_DOGMA', 'EXCLUIDO_APOCRIFO', 'CONDENADO_HERETICO')),
    trecho_decreto TEXT,
    FOREIGN KEY (concilio_id) REFERENCES concilios(id) ON DELETE CASCADE,
    FOREIGN KEY (livro_id) REFERENCES livros(id) ON DELETE CASCADE,
    UNIQUE(concilio_id, livro_id)
);

-- ==============================================================================
-- ÍNDICES ESTRATÉGICOS PARA OTIMIZAÇÃO TEMPORAL
-- ==============================================================================

-- 1. Busca primária de viewport do vis-timeline:
-- Colisão com janela [view_start, view_end]: ano_inicio <= :fim AND (ano_fim >= :inicio OR ano_fim IS NULL)
CREATE INDEX IF NOT EXISTS idx_eventos_temporal 
ON eventos (ano_inicio, ano_fim);

-- 2. Busca combinada por Trilha/Eixo + Janela Temporal (crucial para filtros visuais de swimlane)
CREATE INDEX IF NOT EXISTS idx_eventos_eixo_temporal 
ON eventos (eixo_id, ano_inicio, ano_fim);

-- 3. Filtragem por categoria de evento (ex: 'imperio', 'concilio', 'mito') com ordenação temporal
CREATE INDEX IF NOT EXISTS idx_eventos_categoria_tempo 
ON eventos (categoria, ano_inicio);

-- 4. Busca de livros por época de composição estimada
CREATE INDEX IF NOT EXISTS idx_livros_composicao 
ON livros (ano_composicao_inicio, ano_composicao_fim);

-- 5. Otimização de junção para filtros canônicos (exibir livros por tradição e status)
CREATE INDEX IF NOT EXISTS idx_status_canonico_busca 
ON status_canonico (tradicao, status);

-- 6. Otimização para concílios por data
CREATE INDEX IF NOT EXISTS idx_concilios_ano 
ON concilios (ano);
