# What should the directory structure look like for this project?
• For this project, I’d use a small Python layout organized around the pipeline described in the README: collecting catalog data, cleaning and
  chunking it, indexing it in ChromaDB, retrieving relevant material, and presenting grounded recommendations.
 
  final-proj/
  ├── README.md
  ├── pyproject.toml
  ├── uv.lock
  ├── .env.example
  ├── .gitignore
  ├── data/
  │   ├── raw/              # downloaded catalogs; usually gitignored
  │   ├── processed/        # cleaned, normalized catalog records
  │   └── sample/           # small, safe-to-commit examples for development
  ├── chroma/               # local vector database; gitignored
  ├── src/
  │   └── university_recommender/
  │       ├── __init__.py
  │       ├── config.py     # environment variables and settings
  │       ├── ingestion/    # catalog collection and parsing
  │       ├── processing/   # cleaning, metadata, and chunking
  │       ├── embeddings.py
  │       ├── retrieval.py
  │       ├── recommendations.py
  │       └── interface.py  # UI or API entry point
  ├── scripts/              # commands to ingest, index, and run the app
  ├── tests/
  │   ├── test_processing.py
  │   └── test_retrieval.py
  └── docs/                 # architecture, data sources, and evaluation notes
 
  Keep the source code in one importable package, and make each data stage explicit (raw → processed → ChromaDB). That should make it easier
  for teammates to work on ingestion, retrieval, and the interface independently.
  
  A few practical notes for the current repo:
 
  • main.py can stay as a small launcher, or move into src/university_recommender/ once the app grows.
  • Use pyproject.toml as the dependency source of truth; the README’s requirements.txt commands refer to a file that isn’t currently present.
  • Keep .venv, API keys, downloaded catalogs, and the local ChromaDB store out of Git. Commit only small sample data that you’re allowed to redistribute.
 
  You don’t need to create all these directories immediately. Start with src/university_recommender/, scripts/, and tests/, then add the data folders when ingestion is
  underway.

