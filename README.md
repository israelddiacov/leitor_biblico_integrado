# 📖 Leitor Bíblico & Linha do Tempo Histórica Comparada

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.63%2B-FF4B4B.svg?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![SQLite](https://img.shields.io/badge/SQLite-Database-003B57.svg?logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE-MIT)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](LICENSE-GPL)
[![Bíblias](https://img.shields.io/badge/Traduções-142%20Versões-emerald.svg)](base_biblias/catalogo_biblias.json)
[![Referências Cruzadas](https://img.shields.io/badge/TSK%20Conexões-432.000%2B-cyan.svg)](biblia.db.zip)

Uma plataforma integrada, moderna e interativa que combina **estudo bíblico aprofundado**, **análise relacional de textos sagrados** e **confronto cronológico com a história mundial e as mitologias contemporâneas**.

---

## 🌟 Principais Recursos

### 1. 📖 Leitor Bíblico Multilíngue (142 Traduções em 58 Idiomas)
* **Biblioteca Universal:** Acesso a 142 Bíblias completas em SQLite, incluindo traduções em português (*Almeida ACF, ARC, AA, Bíblia Ave Maria, Bíblia Livre*), idiomas originais (*Westminster Leningrad Codex Hebraico, Textus Receptus Grego, Septuaginta LXX*), latim (*Vulgata Clementina, Sistina, Stuttgart*), clássicas inglesas (*Wycliffe 1395, Tyndale 1526, Geneva 1599, KJV, ASV*) e dezenas de outros idiomas.
* **Leitura Paralela Lado a Lado:** Compare instantaneamente dois textos bíblicos versículo por versículo com alinhamento visual inteligente.
* **Navegação Contínua:** Botões de rodapé (`⬅️ Cap. Anterior` / `Próximo Cap. ➡️`) com avanço e retrocesso automático entre livros ao chegar no início ou fim de cada livro.
* **Contexto Histórico por Livro:** Card retrátil detalhando autor tradicional, gênero literário, data crítica de composição e líderes contemporâneos.
* **Exportação Markdown (.md):** Baixe qualquer capítulo com um clique, formatado para importação direta no **Obsidian**, **Notion** ou **Logseq**.

### 2. 🔗 Rede de Referências Cruzadas Relacionais (TSK)
* **Mais de 432.000 Conexões:** Baseada no tesouro do conhecimento das Escrituras (*Treasury of Scripture Knowledge*).
* **Botão Discreto `🔀` ao Lado de Cada Verso:** Clique para inspecionar versículos correlacionados tematicamente na coluna lateral de conexões.
* **Suporte Multilíngue Universal:** Conexões funcionam tanto em traduções centrais quanto em qualquer tradução externa via ID canônico.

### 3. ⏳ Linha do Tempo Histórica Comparada (Vis-Timeline Interativo)
* **4 Eixos Sincronizados de Paralelismo Temporal:**
  1. 🏛️ **História Secular & Grandes Impérios** (Egito, Suméria, Babilônia, Assíria, Pérsia, Grécia, Roma).
  2. 📜 **Cronologia Bíblica** (Patriarcas, Juízes, Reis de Judá e Israel, Profetas, Ministério de Jesus).
  3. 🏺 **Mitologias Comparadas** (Cosmogonias, Mitos Mesopotâmicos, Egípcios, Cananeus e Greco-Romanos).
  4. ⛪ **História do Cânon & Concílios** (Sínodos, formação dos manuscritos e definição dogmática).
* **Marcador do Grande Dilúvio (2348 a.C.):** Baliza visual em destaque ciano atravessando todos os eixos de alto a baixo.
* **Sincronizador de Época:** Marcador arrastável interativo para focar em qualquer período da história.
* **Drawer Lateral:** Clique em qualquer bloco para abrir painel retrátil com detalhes, datas e links.

### 4. ⚡ Confronto Simultâneo de Épocas & Impérios
* **Exame Sinóptico Relacional:** Escolha uma das 17 épocas consagradas (de 4004 a.C. até o Concílio de Trento) ou digite qualquer ano da história.
* **Grid de 4 Colunas:** Veja em tempo real o que estava acontecendo ao mesmo tempo no império dominante, no povo de Israel, nos cultos politeístas e nos registros do cânon.
* **Salto Direto:** Botão `📖 Ler no Leitor` leva imediatamente ao texto sagrado com troca automática de aba.

### 5. 👤 Catálogo Biográfico de Personagens, Reis & Profetas
* **Filtros Históricos Especializados:** Filtre por *Antediluvianos*, *Patriarcas*, *Juízes*, *Reis de Judá (Reino do Sul)*, *Reis de Israel (Reino do Norte)* e *Profetas*.
* **Ação Dupla:** Cada personagem possui botões para:
  * `📖 Ler no Leitor`: Abre o livro e capítulo central da vida do personagem.
  * `⚡ Ver no Confronto`: Salta para o ano histórico e examina os impérios contemporâneos.

---

## 🏛️ Arquitetura do Sistema

```
leitor_biblico_integrado/
├── app.py                      # Aplicação central em Streamlit com navegação reativa
├── gerador_timeline.py         # Motor de compilação da linha do tempo Vis-Timeline HTML
├── timeline_confronto.html     # Componente gráfico compilado com os 4 eixos
├── biblia.db.zip               # Banco SQLite central compactado (auto-extraído na 1ª execução)
├── timeline.db                 # Banco relacional de eventos, eixos, personagens e cânon
├── base_biblias/               # 122 Bíblias SQLite individuais em múltiplos idiomas
│   ├── catalogo_biblias.json   # Metadados e catálogo estruturado de todas as Bíblias
│   ├── Wycliffe.db, Tyndale.db, Geneva.db, Vulgate.db, ...
│   └── extras/                 # Referências cruzadas e índices de busca adicionais
├── pyproject.toml              # Dependências gerenciadas via Poetry
├── requirements.txt            # Dependências em formato pip padrão
├── LICENSE                     # Informações de Licenciamento Duplo
├── LICENSE-MIT                 # Licença MIT
└── LICENSE-GPL                 # Licença GNU GPLv3
```

---

## 🚀 Como Executar Localmente

### Pré-requisitos
* **Python 3.10 ou superior** instalado.
* Recomendado: **Poetry** (ou ambiente virtual `venv`).

### Opção 1: Usando Poetry (Recomendado)

```bash
# 1. Clone o repositório
git clone https://github.com/SEU_USUARIO/leitor_biblico_integrado.git
cd leitor_biblico_integrado

# 2. Instale as dependências
poetry install

# 3. Inicie o aplicativo
poetry run streamlit run app.py
```

### Opção 2: Usando Pip e Venv

```bash
# 1. Clone o repositório
git clone https://github.com/SEU_USUARIO/leitor_biblico_integrado.git
cd leitor_biblico_integrado

# 2. Crie e ative o ambiente virtual
python -m venv .venv

# Windows (PowerShell):
.venv\Scripts\Activate.ps1
# Linux / macOS:
source .venv/bin/activate

# 3. Instale os pacotes necessários
pip install -r requirements.txt

# 4. Inicie o aplicativo
streamlit run app.py
```

O aplicativo estará disponível em seu navegador no endereço:
👉 **`http://localhost:8501`**

*(Na primeira execução, o arquivo `biblia.db.zip` será descompactado automaticamente de forma transparente em menos de 2 segundos).*

---

## 📄 Licenciamento Duplo (*Dual Licensing*)

Este projeto é disponibilizado sob **Licenciamento Duplo**. Você tem a liberdade de utilizá-lo sob os termos de qualquer uma das licenças a seguir:

1. **[Licença MIT](LICENSE-MIT)**: Permissiva, ideal para quem deseja utilizar partes do código em projetos próprios, acadêmicos ou comerciais com atribuição.
2. **[GNU General Public License v3.0 (GPL-3.0)](LICENSE-GPL)**: Copyleft, garantindo que qualquer trabalho derivado permaneça de código aberto e livre para toda a comunidade.

---

## 🤝 Contribuições

Contribuições são muito bem-vindas! Se você deseja adicionar novas fontes históricas, refinar datas arqueológicas, melhorar a tradução de interfaces ou sugerir melhorias de UX:

1. Faça um Fork do projeto.
2. Crie sua branch de feature (`git checkout -b feature/minha-melhoria`).
3. Faça commit das suas alterações (`git commit -m 'Adiciona novo recurso'`).
4. Envie para a branch (`git push origin feature/minha-melhoria`).
5. Abra um Pull Request.

---

## ⚖️ Aviso Legal e Direitos Autorais (*Copyright & Disclaimer*)

* **Finalidade do Software:** Este projeto foi desenvolvido com finalidade estritamente **acadêmica, educacional, histórica e de pesquisa teológica comparada**, de código aberto e sem qualquer fim comercial ou lucrativo.
* **Textos em Domínio Público:** Mais de 95% das fontes textuais utilizadas (como o *Texto Massorético Hebraico*, *Textus Receptus Grego*, *Septuaginta LXX*, *Vulgata Latina*, *King James 1611*, *Reina Valera 1909*, *Louis Segond 1910*, entre outras) pertencem integralmente ao **Domínio Público** mundial ou a licenças abertas como **Creative Commons (CC BY-SA)**.
* **Política de Remoção (*Notice and Takedown*):** Se você representa uma editora, sociedade bíblica ou detentor de direitos sobre alguma tradução específica e não deseja que ela conste neste agregador de estudo comparado, favor abrir uma [Issue no GitHub](https://github.com/israelddiacov/leitor_biblico_integrado/issues) informando a versão que procederemos com a **remoção imediata** do arquivo correspondente.
