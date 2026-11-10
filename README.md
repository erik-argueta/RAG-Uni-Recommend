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

## Team Responsibilities
The team responsibilities will be divided by the different stages of the project. Jose will be responsible and lead the data collection and pre-processing; Erik will be responsible for and lead setting up RAG and embeddings; Jerico will be leading the LLM integration and backend; Jose will be responsible for the User Interface and evaluation. Although each member is in charge of a different area, the group will assist one another to ensure that each phase is completed efficiently.

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
