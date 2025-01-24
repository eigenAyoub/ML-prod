**Why:** I have been involved in the past 2 years in many ML projects, but none have been focused on production. In my recent project (working with embedding models), I saw a clear potential in building something fun, and serious.

**Goals:**

* Build an AI system that analyzes my local files (PDFs, docs, text) using LLMs, and answer personalized questions.
* I also plan to have a dump of `wikipedia`, to use offline (fine-tune the model on wikipedia).
* Ingest a `github` project (or a dump of files), to get insights?

I basically want to build something that does the following (thanks o1-mini for the scheme):


### Jan 24:

3 main steps:

1. LLM/fastAPI endpoint.
2. Data pipeline: wiki -> embed -> store -> retrieve.
3. port forwarding / ssh tunneling (I will host the LLM in my remote compute pod); and expose it locally - smth weby.

Extra:

* Clean wiki dumps
* Store with chromaDB?
* Fetch top n
* What's a re-ranking loss?


## TODO - later on:

* Add support for CPU inference // when to use vllm?
* Make this a useful thing

Near ones:
* Structures outputs?
* impose it on this.

<details>


## Plan:

1. Set-up.

Deliverables:
* Git repo initialized, Dockerfile for the app, basic CI pipeline for linting & building images.

2. Document Ingestion & Metadata Extraction.

Deliverables:
* Document ingestion pipeline in FastAPI.
* Docker image can be built and run locally to parse various doc types.

3. Embed and store:

Deliverables:
* Vector DB set up.
* End-to-end flow: upload file → parse → embed → store → confirm storage success.

4. Fun, begins. LLM integration.

* Mini-steps
* pick a small model (I can easily go up to 7B).
	* Use [https://huggingface.co/deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B]
* Create you FASTAPI endpoint
* Build  a mini RAG system:  question → retrieve top n chunks from vector DB → feed them into the LLM prompt → final answer

* Try to use: `uvicorn`, `vLLM`.


**Overview:**

* wiki dump ->
* request -> top-n -> LLM -> answer
* web app

**Tools:**

* wiki dump -> huggin face
* chanking -> `langchain.text_splitter`
* embedding model -> some 33M
				  -> my compressed 250M
* vector DB -> ChromaDB/Weaviate


Marketing PR:

* Exposing local LLM through FastAPI endpoint.
* Combine with Kubernetes for managing multiple instances.

* `uvicorn`, `pydantic`, `vllm`
* Eventually host on a AZURE? AWS?



 ┌─────────────────────┐
 │Local File System    │
 │(.pdf, .md , .txt)   │   
 └─────────────────────┘
          |
          v
 ┌─────────────────────┐
 │Data Ingestion       │
 │Pipeline (FastAPI)   │
 │ - pypdf, docx2txt   │
 │ - metadata extract  │
 └─────────────────────┘
          |
          v
 ┌─────────────────────┐
 │Embed & Store        │
 │ - LangChain         │
 │ - Vector DB (Chroma)│
 └─────────────────────┘
          |
          v
 ┌────────────────────────┐
 │Local LLM Server (4-bit)│
 │ - LoRA / GPTQ          │
 │ - HF Transformers      │
 └────────────────────────┘
          |
          v
 ┌─────────────────────────┐
 │FastAPI Endpoint         │
 │"Ask" => RAG -> LLM      │
 │Return Answer + Source   │
 └─────────────────────────┘

</details>


