# RAG University Recommendation
## Program Authors:
* Erik Argueta
* Jerico Avila
* Jose Cervantes 

## Project Background
California has a total of thirty-three universities, each with different courses depending on the major. Selecting the best-fitting university can be difficult because it requires reviewing each school’s catalog. This problem can be solved with an application that records the user’s preferences and interests in the field they want to study and analyzes universities’ courses to inform the user which school would benefit them most. This application would use Retrieval-Augmented Generation (RAG) to fetch information from official UC and CSU catalogs to generate personalized comparisons between universities. The model would analyze course descriptions and degree requirements to help users make an informed decision about which path best aligns with their educational goals.  

## Goals and Objectives 
Our group plans to compile data on academic catalogs obtained from the universities’ official websites; this information will consist of academic programs, course descriptions, any prerequisites, and degree requirements. We will then clean the collected information and reorganize it into a smaller form. While our initial goal is to record all universities in California, we may have to narrow it to the UC schools or to schools within a specific radius. The project will be developed using libraries and APIs like ChromaDB and the NRP OpenAI keys we were given for this course. Our group will compile the catalog collections, process the text, develop the retrieval logic, and build the user interface. 

## Steps and Procedures 
Our group will begin with gathering academic catalog information from universities’ websites in California; we may use a web scraper for this process. We will then process and clean the collected data. Next, we will use OpenAI’s text embedding model to convert the information into vectors, which will then be stored in a ChromaDB collection. Using the user’s input on their field of interest, the model will generate university comparisons and provide a supported recommendation based on the catalog information. We will evaluate the model’s retrieval relevance and accuracy by submitting different types of user inputs.

## Dependencies  (update as needed)


# Roles and Responsibilities 
1. Web Scraping and Data Collection 
    Collect degree information from CSUF and later nearby CSUs.
	* Develop/Utilize Python web scrapers 
	* Extract majors, courses, descriptions, and degree requirements 
	* Standardize the cllected information into JSON 
	* Preserve university names and catalog URLs  
    * Deliverable: Structured dataset contatining university degree information.

2. Data Processing & Vector Database 
    Transform the collected information into something RAG system can search.
	* Clean and preprocess scraped data.
	* Develop and test chunking strategies. 
	* Generate embeddings using an embedding model.
	* Store embeddings and metadata in **Chroma**  
	* Evaluate retrieval relevance.  
    * Deliverable: A functioning Chroma vector database that returns relevant university information.  

3. RAG Pipeline & LLM Integration  
    Build the recommendation system that interacts with the user. 
	* Accept users' academic interests and preferences.
	* Translate those preferences into retrieval queries. 
	* Retrieve relevant information from **Chroma**.  
	* Integrate the OpenAI API to generate comparisons. 
	* Ensure recommendations cite the university catalogs.  
    * Deliverable: A functioning RAG backend tha tcompares universities using retrieved information.

4. Front-End Development 


# JSON Structure
We will use 2 JSON record types to help the recommendation system: **Course Records** and **Degree Requirements**  

## Course Records 
```JSON 
{
  "id": "university-a-cs-101-2026",
  "record_type": "course",
  "university": "University A",
  "department": "Computer Science",
  "course_code": "CS 101",
  "course_title": "Artificial Intelligence",
  "description": "An introduction to AI, machine learning, and search algorithms.",
  "units": 3,
  "prerequisites": ["CS 100"],
  "catalog_year": "2026-2027",
  "source_url": "https://example.edu/courses/cs101"
}
```

## Degree Requirements
```JSON 
{
  "id": "university-a-bs-cs-2026",
  "record_type": "degree_program",
  "university": "University A",
  "major": "Computer Science",
  "degree": "Bachelor of Science",
  "catalog_year": "2026-2027",
  "total_units": 120,
  "core_courses": [
    "CS 100",
    "CS 101",
    "CS 200"
  ],
  "elective_courses": [
    "CS 310",
    "CS 320"
  ],
  "concentrations": [
    "Artificial Intelligence",
    "Cybersecurity"
  ],
  "source_url": "https://example.edu/programs/computer-science"
}
```

# Project Structure 
 ```
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
 ```


# Misc
## How to Initialize
* If using uv, run the following within the project's home directory:  
`uv pip install -r requirements.txt`

* If using pip, run the following in within the project's home directory:  
`pip install -r requirements.txt`

## NRP API Key
This project reads the NRP LLM key from your local environment, not from source code.

The client uses `https://ellm.nrp-nautilus.io/v1`, model `gpt-oss`, and
`client.chat.completions.create(...)`.

Set the key in your terminal or `~/.bashrc`:

```bash
export NRP_API_KEY="your_nrp_api_key_here"
```

If you edited `~/.bashrc`, reload it with `source ~/.bashrc`. Start the GUI
from that same terminal:

## Python .venv
Please don't forget to create your venv as `.venv`  
Otherwise, please include the venv within .gitignore  

## Branching  
Please work in a different branch until you're ready to merge with main.  
Please notify the group when a push has been made on the main branch.


