KnowledgeBot v25sept - Comprehensive Project Documentation
1. List of Features
Per-page PDF parsing with precise page citation

BM25 retrieval algorithm with synonym expansion and version boost support

Robust Ollama client handling both streaming and non-streaming JSON responses

Intent-aware routing for personal info, file listing, project discovery, and document queries

Multi-format document ingestion (PDF, DOCX, TXT, CSV, XLSX, MD)

Stepwise instruction generation for installation/procedure queries

Gradio-based user interface with optional Ollama URL configuration

Page-aware context composition with metadata tracking

Graceful fallback mechanisms for missing dependencies

2. Key Advantages Over Available Solutions
Accurate Page Citations: Unlike traditional RAG systems, provides exact page numbers in responses

Intelligent Query Routing: Automatically detects query intent to avoid unnecessary LLM calls for simple questions

Version-Aware Retrieval: Understands version formats (1.9.0, v1.9.0, 1_9_0) for better document matching

Procedural Answer Formatting: Recognizes installation/setup queries and returns numbered steps

Lightweight & Extensible: Works with local Ollama instead of requiring cloud APIs

Multi-Format Support: Handles various document types without format-specific configuration

Fallback Mechanisms: Graceful degradation when BM25 unavailable, Ollama issues, or missing dependencies

3. High-Level Design
The system follows a three-tier architecture:

Input Layer: Gradio UI accepts queries, file paths, and configuration parameters

Processing Layer: Intent detection routes queries to appropriate handlers (personal info, file listing, or RAG pipeline)

Output Layer: Generates page-cited answers with source metadata

4. Low-Level Design
Core Components:

custom_tool.py: Multi-format file readers with per-page PDF parsing

crew_simple.py: RAG pipeline with BM25 ranking, query expansion, and Ollama integration

main.py: Gradio UI with free port detection and configuration management

Data Flow: Query → Intent Detection → Document Loading → Chunking → BM25 Ranking → Context Composition → Ollama Generation → Page-Cited Response

5. Technology Stack & Component Design
Framework: Gradio for UI

LLM Inference: Ollama with configurable models (mistral, llama3.2, gemma)

Retrieval: BM25Okapi ranking with synonym expansion

PDF Parsing: pdfplumber (primary) with PyPDF2 fallback

Document Processing: pdfplumber, docx, pandas for multiple formats

Environment: Python 3.10+, UV package manager

6. Implementation & Deployment
Installation:

pip install -e .

pip install pdfplumber rank-bm25

Environment Configuration:

OLLAMA_BASE_URL: Ollama endpoint (e.g., http://ollama:11434)

KB_MODEL: Model name (default: mistral)

CREWAI_TELEMETRY_ENABLED: false

Execution:

python -m knowledge_bot.main

Access at http://0.0.0.0:7861 (or available free port)

7. Key Areas for Improvement & Important Features to Add
Immediate Improvements:

Semantic Search: Add vector embeddings (Chroma, FAISS) alongside BM25

Caching Layer: Implement document cache to avoid re-ingestion

Authentication: Add user authentication and access control

Batch Processing: Support bulk document ingestion and indexing

API Endpoint: Expose REST API alongside Gradio UI

Advanced Features:

Hybrid Search: Combine BM25 + semantic search with weighted ranking

Multi-Language Support: Handle documents and queries in multiple languages

Citation Anchors: Direct links/anchors to exact source locations

Query Analytics: Track usage patterns and optimize retrieval

Document Versioning: Track document versions and update history

Custom Domain Models: Fine-tuned Ollama models for specific domains

Streaming Responses: Stream long responses to UI in real-time

Document Summarization: Auto-generate document summaries on ingestion

To properly document this, manually create the PROJECT_DOCUMENTATION.md file in the knowledge_bot_v25sept folder with the detailed sections above.

github.com favicon
New File at knowledge_bot_v25sept · kapilgupta86/GenAI_projects
