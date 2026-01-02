# KnowledgeBot v25sept - Comprehensive Project Documentation

## Project Overview

**KnowledgeBot** is an intelligent, hybrid RAG (Retrieval-Augmented Generation) assistant designed to answer questions about documents while providing precise source citations. It combines fast, deterministic responses for simple queries with high-quality, context-grounded answers for complex document questions using an improved RAG pipeline with Ollama integration.

***

## 1. List of Features

### Core Features

- **Per-Page PDF Parsing**: Extracts text from PDFs on a page-by-page basis, enabling precise page citations in responses
- **BM25 Retrieval Algorithm**: Implements probabilistic ranking with intelligent synonym expansion and version boost support (e.g., 1.9.0, v1.9.0, 1_9_0)
- **Robust Ollama Client**: Handles both streaming and non-streaming JSON responses with automatic fallback mechanisms
- **Intent-Aware Routing**: Automatically detects query intent (personal info, file listing, project discovery, or document queries)
- **Multi-Format Document Ingestion**: Supports PDF, DOCX, TXT, CSV, XLSX, and MD files
- **Stepwise Instruction Generation**: Recognizes installation/procedure queries and returns numbered, actionable steps
- **Gradio-Based User Interface**: Simple, intuitive web UI with optional Ollama URL configuration
- **Page-Aware Context Composition**: Maintains metadata about source documents and pages for citation
- **Graceful Fallback Mechanisms**: Operates even when BM25 is unavailable or dependencies are missing


### Advanced Features

- Query expansion with synonym dictionary
- Version-aware document matching
- Multiple fallback search strategies (BM25 → Simple Keyword Search)
- Free port detection for UI server
- Configurable model selection (mistral, llama3.2, gemma, etc.)
- Markdown export of responses

***

## 2. Key Advantages Over Available Solutions

| Aspect | KnowledgeBot | Traditional RAG | OpenAI RAG | Enterprise Solutions |
| :-- | :-- | :-- | :-- | :-- |
| **Page Citations** | ✅ Exact page numbers | ❌ Chunk IDs only | ⚠️ Vague references | ⚠️ Limited |
| **Query Routing** | ✅ Intelligent intent detection | ❌ All queries to LLM | ❌ All queries to API | ✅ Available but expensive |
| **Version Awareness** | ✅ Built-in | ❌ No | ❌ No | ❌ Requires config |
| **Local Deployment** | ✅ Ollama (free) | ✅ FAISS/Chroma | ❌ Cloud only | ❌ Cloud/On-prem (expensive) |
| **Cost** | 🟢 Free | 🟢 Free | 🔴 Pay-per-query | 🔴 Expensive |
| **Privacy** | ✅ Complete control | ✅ Local | ❌ Cloud storage | ⚠️ Enterprise agreement |
| **Procedural Answers** | ✅ Numbered steps | ❌ Paragraph form | ❌ Paragraph form | ✅ Available |
| **Multi-Format Support** | ✅ 6+ formats | ⚠️ Limited | ⚠️ Limited | ✅ Extensive |


***

## 3. High-Level Design

### System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         User Interface                           │
│                    Gradio Web Application                        │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ Query Input │ Config Settings │ Model Selection │ Results │ │
│  └────────────────────────────────────────────────────────────┘ │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                  Request Processing Layer                        │
│  ┌──────────────┐      ┌──────────────┐      ┌──────────────┐  │
│  │   Intent     │──────▶│   Query      │──────▶│  Response    │  │
│  │  Detection   │      │  Processor   │      │  Formatter   │  │
│  └──────────────┘      └──────────────┘      └──────────────┘  │
└──────────────────────────┬──────────────────────────────────────┘
                           │
         ┌─────────────────┼─────────────────┐
         ▼                 ▼                 ▼
    ┌──────────┐    ┌──────────┐    ┌──────────┐
    │ Personal │    │  File    │    │   RAG    │
    │  Info    │    │ Listing  │    │ Pipeline │
    │ Handler  │    │ Handler  │    │ Handler  │
    └──────────┘    └──────────┘    └──────────┘
                                          │
                                          ▼
                          ┌───────────────────────────┐
                          │  Document Processing     │
                          │ ┌─────────────────────┐ │
                          │ │ Load & Parse Files  │ │
                          │ │ Chunk Content       │ │
                          │ │ Index with Metadata │ │
                          │ └─────────────────────┘ │
                          └───────────────────────────┘
                                          │
                                          ▼
                          ┌───────────────────────────┐
                          │  BM25 Retrieval Engine    │
                          │ ┌─────────────────────┐ │
                          │ │ Query Expansion     │ │
                          │ │ Version Boosting    │ │
                          │ │ Synonym Matching    │ │
                          │ │ Ranking & Scoring   │ │
                          │ └─────────────────────┘ │
                          └───────────────────────────┘
                                          │
                                          ▼
                          ┌───────────────────────────┐
                          │  Ollama LLM Integration   │
                          │ ┌─────────────────────┐ │
                          │ │ Stream/JSON Handler │ │
                          │ │ Prompt Engineering  │ │
                          │ │ Temperature Control │ │
                          │ │ Context Management  │ │
                          │ └─────────────────────┘ │
                          └───────────────────────────┘
                                          │
                                          ▼
                          ┌───────────────────────────┐
                          │  Page-Cited Response      │
                          │  with Source Metadata     │
                          └───────────────────────────┘
```


### Three-Tier Architecture

1. **Input Layer (Presentation)**
    - Gradio web interface
    - Accepts queries, file paths, configuration parameters
    - Displays results with source citations
2. **Processing Layer (Business Logic)**
    - Intent detection and routing
    - Document management (loading, parsing, chunking)
    - BM25 ranking and retrieval
    - LLM prompt composition
3. **Output Layer (Response Generation)**
    - Ollama LLM integration
    - Page-aware context composition
    - Response formatting with citations
    - Markdown export capability

***

## 4. Low-Level Design

### Core Components

#### 4.1 custom_tool.py

**Purpose**: Multi-format file ingestion and parsing

**Key Functions**:

- `_read_pdf_per_page()`: Extracts text from PDF files page-by-page
    - Primary method: pdfplumber
    - Fallback: PyPDF2
    - Tracks page numbers for citations
- `_read_docx()`: Parses DOCX documents
    - Extracts paragraph-level text
- `_read_txt()`: Reads plain text files
    - UTF-8 encoding with fallback
- `_read_csv()`: Processes CSV files
    - Uses pandas for structured parsing
    - Handles up to 1000 rows
- `_read_xlsx()`: Parses Excel spreadsheets
    - Extracts data into readable format
- `LocalFileReader()`: Recursive file discovery and ingestion
    - Walks directory tree
    - Supports: .pdf, .docx, .txt, .csv, .xlsx, .md
    - Returns normalized documents with metadata

**Metadata Tracked**:

```python
{
    "content": "extracted text",
    "metadata": {
        "source": "/path/to/file",
        "name": "filename.pdf",
        "type": ".pdf",
        "size": 12345,
        "last_modified": 1672531200,
        "page": 3,  # for PDFs
        "page_count": 10  # for PDFs
    }
}
```


#### 4.2 crew_simple.py

**Purpose**: Core RAG pipeline and LLM integration

**Key Functions**:

1. **Intent Detection** (`_detect_intent()`)
    - Routes queries to appropriate handler
    - Intents: `personal_info`, `list_files`, `list_projects`, `rag_query`
2. **Query Expansion** (`_expand_query_terms()`)
    - Expands keywords using synonym dictionary
    - Recognizes version formats
    - Supports: install/setup, procedure/steps, pod/pods, etc.
3. **Text Chunking** (`_chunk_text()`)
    - Default chunk size: 700 tokens
    - Overlap: 120 tokens
    - Preserves context across chunks
4. **Document Loading** (`_load_documents_from_folder()`)
    - Ingests all supported formats
    - Creates chunks with metadata
    - Tracks chunk IDs and total chunks
5. **BM25 Search** (`_bm25_search()`)
    - Tokenizes corpus
    - Scores documents using BM25 algorithm
    - Applies version boosts (+2.0)
    - Applies keyword boosts for procedure queries (+1.5)
    - Returns top-7 ranked documents
6. **Fallback Search** (`_simple_search()`)
    - Simple keyword matching
    - Overlap-based scoring
    - Phrase bonus calculation
7. **Ollama Integration** (`_ollama_chat_stream_or_json()`)
    - Handles streaming responses
    - Parses JSON responses
    - Robust error handling
    - Timeout management (20s connect, 120s read)
8. **Response Generation** (`_generate_answer_with_ollama()`)
    - Formats context for LLM
    - Detects query type (procedure vs. general)
    - Crafts appropriate prompts
    - Fallback to simple answers if Ollama unavailable

#### 4.3 main.py

**Purpose**: Gradio UI and application orchestration

**Features**:

- Gradio Blocks interface
- Free port detection (starts at 7861)
- Configuration inputs:
    - Query text
    - Knowledge directory path
    - GitHub repo URL (placeholder)
    - Model selection dropdown
    - Ollama URL override
    - Top-K retrieval setting
    - Markdown export option
- Response display with copy button
- Automatic source annotation


### Data Flow Diagram

```
User Query
    ↓
[Check if empty] → Error Message
    ↓ (valid)
Intent Detection
    ├→ personal_info: Load user_preference.txt
    ├→ list_files: List .py/.md files in folder
    ├→ list_projects: Find project directories
    └→ rag_query: Execute RAG Pipeline
              ↓
         Load Documents from Folder
              ↓
         Chunk into 700-token segments
              ↓
         Create BM25 Index
              ↓
         Expand Query Terms (synonyms, versions)
              ↓
         BM25 Ranking
              ↓
         (Fallback to Simple Search if needed)
              ↓
         Retrieve Top-7 Documents
              ↓
         Compose Page-Aware Contexts
              ↓
         Format LLM Prompt
              ↓
         Call Ollama with Streaming
              ↓
         Parse Response (JSON or Stream)
              ↓
         Append Source Citations
              ↓
         Display in UI
              ↓
         (Optional) Save to Markdown
```


***

## 5. Technology Stack \& Component Design

### Technology Stack

| Category | Technology | Purpose |
| :-- | :-- | :-- |
| **UI Framework** | Gradio | Web-based user interface |
| **LLM Inference** | Ollama | Local model serving (mistral, llama3.2, gemma) |
| **Retrieval** | BM25Okapi (rank-bm25) | Document ranking algorithm |
| **PDF Processing** | pdfplumber | Primary PDF text extraction |
| **PDF Fallback** | PyPDF2 | Fallback PDF extraction |
| **Document Processing** | docx, pandas | DOCX and tabular data handling |
| **Runtime** | Python 3.10+ | Language and runtime |
| **Package Manager** | UV | Dependency management (fast alternative to pip) |
| **Environment** | .env | Configuration management (python-dotenv) |

### Component Dependency Graph

```
main.py (UI Entry Point)
├── Gradio
├── socket (port detection)
├── os, sys, warnings
└── crew_simple.py (Processing)
    ├── typing, os, re, json, requests
    ├── rank_bm25.BM25Okapi (optional)
    ├── custom_tool.py (File Loading)
    │   ├── pdfplumber (optional)
    │   ├── PyPDF2 (optional)
    │   ├── docx (optional)
    │   ├── pandas (optional)
    │   └── os, typing
    └── Ollama API (via HTTP requests)
```


### Model Configuration

**Default Configuration**:

```python
Models Supported (in dropdown):
- mistral (default)
- llama3.2
- llama3.2:1b
- llama2
- gemma

Default Ollama Settings:
- temperature: 0.2 (low randomness)
- num_predict: 700 (max tokens)
- num_ctx: 4096 (context window)
```


***

## 6. Implementation \& Deployment

### 6.1 Installation

**Step 1: Install Dependencies**

```bash
# Install package in editable mode
pip install -e .

# Install optional retrieval library
pip install rank-bm25

# Install PDF processing (recommended)
pip install pdfplumber

# Alternative: use UV (faster)
uv pip install -e .
uv pip install rank-bm25 pdfplumber
```

**Step 2: Environment Setup**

```bash
# Create .env file in project root
cat > .env << EOF
OLLAMA_BASE_URL=http://localhost:11434
KB_MODEL=mistral
CREWAI_TELEMETRY_ENABLED=false
KNOWLEDGE_DIR=./knowledge
EOF
```

**Step 3: Prepare Knowledge Base**

```bash
# Create knowledge directory
mkdir -p knowledge

# Add your documents (PDF, DOCX, TXT, etc.)
cp /


<div align="center">⁂</div>

[^1]: https://github.com/kapilgupta86/GenAI_projects/blob/main/knowledge_bot_v25sept/PROJECT_DOCUMENTATION.md```

