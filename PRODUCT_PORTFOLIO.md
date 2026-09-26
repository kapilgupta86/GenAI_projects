# Kapil Gupta — Product Portfolio

**Portfolio scope:** 10+ public repositories covering Agentic AI, enterprise AI operations, multimodal automation, investment intelligence, data science, and cloud-native platforms.

---

## Executive Summary

### Core Professional Theme

Building private, domain-specific AI products that automate analysis, decision support, and operational workflows.

**Strongest differentiators:**

- Agentic AI and multi-agent orchestration
- Local and private LLM deployment with Ollama
- Kubernetes, K3s, and infrastructure operations
- RAG and enterprise knowledge assistants
- Multimodal AI (audio, video, documents)
- AI-assisted investment research and trading workflows
- Practical data science and machine learning
- Production-oriented thinking: APIs, deployment, configuration, observability

---

## Portfolio at a Glance

| Repository | Category | Primary User | Maturity |
|---|---|---|---|
| [Log Analysis Agent](https://github.com/kapilgupta86/log_analysis_agent) | AI Kubernetes RCA | SRE, DevOps | **Product Prototype** ⭐ |
| [Claude Trading Skills](https://github.com/kapilgupta86/claude-trading-skills) | AI Trading Toolkit | Investors, Traders | **Advanced Toolkit** ⭐ |
| [GenAI Projects](https://github.com/kapilgupta86/GenAI_projects) | Multi-Agent Portfolio | AI Engineers | **Portfolio Showcase** ⭐ |
| [Audio-Video-to-Text](https://github.com/kapilgupta86/Audio-Video-to-Text) | Meeting Minutes | Teams, Managers | Functional Notebook |
| [Agentic-AI](https://github.com/kapilgupta86/Agentic-AI) | AI Education | AI Engineers | Content Prototype |
| [AI-Stock-Scanner](https://github.com/kapilgupta86/AI-Stock-Scanner) | Stock Screening | Investors | Early Prototype |
| [DS](https://github.com/kapilgupta86/DS) | Data Science | Analysts | Learning Portfolio |
| [GenAI_projects](https://github.com/kapilgupta86/GenAI_projects) | Multi-Agent Labs | Engineers | Active Development |
| [Prompts](https://github.com/kapilgupta86/Prompts) | Experiments | AI Users | Early Stage |
| [DO180-apps](https://github.com/kapilgupta86/DO180-apps) | Container Training | DevOps Learners | Training Repository |
| [logs](https://github.com/kapilgupta86/logs) | Log Dataset | DevOps | Reference Data |

---

## 🌟 Flagship Products

### 1. Log Analysis Agent
**Repository:** [log_analysis_agent](https://github.com/kapilgupta86/log_analysis_agent)

**Problem:** Kubernetes incidents require manual log analysis, taking hours to determine root cause.

**Solution:** AI-powered root-cause-analysis agent that searches Elasticsearch, forms hypotheses, and generates RCA reports automatically.

**Architecture:**
```
User Query → Intent Router → ES Log Search → LLM Reasoning → Reflection Loop → RCA Report
```

**Tech Stack:**
- Python 3.11+
- FastAPI / Uvicorn
- LangChain / LangGraph
- Elasticsearch 8.x
- Ollama (local LLM)
- Kubernetes / K3s
- Docker

**Key Features:**
- ✅ Agentic root-cause-analysis workflow
- ✅ Kubernetes-aware log interpretation
- ✅ Hybrid BM25 + vector search
- ✅ Local LLM support (zero cloud API calls)
- ✅ Reflection loop for evidence gathering
- ✅ FastAPI REST API
- ✅ K3s/Kubernetes deployment ready

**Product Use Cases:**
- Kubernetes incident triage
- Microservice failure investigation
- Telco platform operations
- On-premise SRE support
- Log-based outage analysis

**Product Opportunity:**
Expand into **Enterprise SRE Copilot** with:
- Prometheus/Grafana metrics correlation
- Jaeger/Tempo trace integration
- Recommended remediation commands
- Incident timeline generation
- Postmortem document generation
- Slack/Teams notifications
- Web dashboard

**Target Customers:**
- Telcos
- Platform engineering teams
- Managed service providers
- Regulated enterprises

---

### 2. Claude Trading Skills
**Repository:** [claude-trading-skills](https://github.com/kapilgupta86/claude-trading-skills)

**Problem:** Individual investors need structured research, portfolio review, and trade planning without outsourcing decisions to automated systems.

**Solution:** A Claude Skills-based workflow toolkit that provides disciplined AI-assisted trading process.

**Architecture:**
- Market regime analysis → Portfolio review → Trade planning → Journaling → Performance improvement
- 40+ specialized trading skills
- Operational workflows for different investor goals
- Human decision gates preserved throughout

**Tech Stack:**
- Python 3.9+
- Claude Web Skills
- YAML workflow manifests
- JSON Schema
- yfinance, requests, scipy
- Optional: FMP API, FINVIZ Elite, Alpaca
- Pytest, Ruff, Bandit
- GitHub Pages documentation

**Skill Categories:**
- **Market Regime** (16 skills): Breadth, uptrend, bubble detection
- **Portfolio Management** (6 skills): Allocation, dividend screening, sector rotation
- **Swing Trading** (7 skills): VCP, CANSLIM, breakout planning
- **Trade Planning** (7 skills): Position sizing, technical analysis, options
- **Trade Memory** (6 skills): Journaling, postmortems, performance coaching
- **Strategy Research** (10+ skills): Backtesting, edge detection, scenario analysis
- **Advanced Satellite** (6 skills): Earnings, institutional flows, PEAD

**Product Use Cases:**
- Individual investor portfolio reviews
- Daily market preparation
- Swing-trade candidate discovery
- Dividend portfolio monitoring
- Risk-based position sizing
- Post-trade learning
- Strategy research and backtesting

**Product Opportunity:**
Evolve into **AI Investor Operating System** with:
- Web dashboard for workflow execution
- Portfolio import from brokers
- Interactive skill execution
- Broker integrations (Alpaca, TD Ameritrade, Interactive Brokers)
- Audit trails for investment decisions
- Team/family-office portfolios
- Subscription-based premium data
- Performance attribution analysis

**Target Customers:**
- Individual investors
- Financial researchers
- Investment clubs
- Family offices
- Trading educators

---

### 3. GenAI Projects Multi-Agent Suite
**Repository:** [GenAI_projects](https://github.com/kapilgupta86/GenAI_projects)

**Problem:** Enterprises need demonstrations of how modern AI agents solve real business problems.

**Solution:** A portfolio of 10+ production-ready agent patterns across multiple domains.

**Key Projects:**

#### 3.1 Private Knowledge Bot (Enterprise RAG)
**Problem:** Companies cannot send sensitive documents to cloud AI services.

**Solution:** Local-first RAG assistant using Ollama embeddings and ChromaDB.

**Architecture:**
```
User Documents (PDFs, TXT)
    ↓
Chunking + Ollama Embeddings
    ↓
ChromaDB Vector Store
    ↓
Intent Router (Q&A | Procedural | Directory)
    ↓
CrewAI Agent + Local LLM
    ↓
Response with Citations → Gradio UI
```

**Tech Stack:**
- Ollama (embeddings + LLM)
- ChromaDB
- CrewAI
- Gradio
- YAML configuration
- Python

**Differentiators:**
- 100% local (zero cloud API calls)
- $0/month cost
- GDPR/HIPAA compliant
- Deterministic and reproducible
- Enterprise-ready

**Use Cases:**
- Internal documentation search
- Legal document analysis
- Telco runbook assistance
- Research-paper search
- Private corporate knowledge bases

---

#### 3.2 AI Video Agent
**Problem:** Creating faceless narrated videos takes 4+ hours manually.

**Solution:** Automated pipeline: text → TTS → Wav2Lip lip-sync → HD video (5 minutes).

**Tech Stack:**
- gTTS
- FFmpeg / moviepy
- pydub / librosa
- Wav2Lip
- Kubernetes

**Impact:**
- 80% time savings
- YouTube automation
- Multilingual marketing
- Cost-effective vs D-ID/Synthesia

---

#### 3.3 CrewAI Engineering Team
**Problem:** Software requirements need analysis and design documentation.

**Solution:** Virtual engineering team (Lead, Backend, Frontend, QA) collaborates to generate designs.

**Agents:**
- Engineering Lead: Requirements interpretation, HLD creation
- Backend Engineer: API design, database schema, business logic
- Frontend Engineer: UI/UX design, component architecture
- QA Engineer: Test strategy, edge cases

**Output:** Complete project documentation with HLD, LLD, deployment

---

#### 3.4 Stock Research Crew
**Problem:** Investment research is time-consuming and unstructured.

**Solution:** Multi-agent research workflow generating investment theses.

---

#### 3.5 Audio-Video to Meeting Minutes
**Problem:** Manual note-taking in meetings is inefficient.

**Solution:** Automated pipeline: audio → Whisper transcription → Llama summarization → structured minutes.

**Tech Stack:**
- OpenAI Whisper
- Meta Llama 3.1-8B-Instruct (4-bit quantized)
- moviepy, pydub
- Google Colab
- BitsAndBytes

**Features:**
- Handles long recordings (automatic chunking)
- 4-bit quantization (2GB VRAM only)
- Structured output (decisions, actions, attendees)
- Markdown export

**Use Cases:**
- Meeting minutes automation
- Standup summaries
- Customer call analysis
- Interview transcription
- Lecture summarization

---

**Tech Stack (GenAI Projects):**
- Python
- OpenAI Agents SDK
- Claude
- Anthropic
- CrewAI
- LangChain
- LangGraph
- AutoGen
- MCP
- Semantic Kernel
- Gradio
- Ollama
- ChromaDB
- FastAPI
- Jupyter Notebooks

---

## 📊 Complete Repository Deep-Dives

### Audio-Video-to-Text
**Repository:** [Audio-Video-to-Text](https://github.com/kapilgupta86/Audio-Video-to-Text)

**What:** Jupyter notebook converting audio/video → structured meeting minutes

**Pipeline:**
```
Audio/Video → Audio Extraction → Whisper STT → Transcript
→ Llama-3.1-8B-Instruct (4-bit) → Structured Minutes
→ Markdown (decisions, actions, attendees)
```

**Features:**
- Google Colab support
- Google Drive + file upload + local filesystem
- MP4 audio extraction
- Whisper 25MB chunking
- Llama 3.1 8B summarization
- Markdown output

**Skills Demonstrated:**
- Speech-to-Text (STT)
- Model Quantization (4-bit)
- Audio Processing
- LLM Prompt Engineering
- Multi-model Pipelines
- Colab Orchestration

**Use Cases:**
- Meeting-minute generation
- Engineering standup summaries
- Customer-call analysis
- Lecture transcription
- Podcast summarization

**Product Opportunity:**
Build **Meeting Intelligence SaaS** with:
- Speaker diarization
- Action-item assignment
- Calendar integration
- Searchable history
- CRM integration
- PII redaction
- Export to Jira/Slack/Notion

---

### Agentic-AI
**Repository:** [Agentic-AI](https://github.com/kapilgupta86/Agentic-AI)

**What:** Educational knowledge portal on LLM caching and optimization

**Content:**
- "How LLMs Actually Generate Text — And Every Caching Term"
- "Optimizing L3 Semantic Caching"
- Technical caching documentation

**Technology:** HTML, static web content, GitHub Pages

**Product Concept:**
Developer education platform for LLM performance:
- Token generation mechanics
- Prompt caching
- KV caching
- Semantic caching
- Latency optimization
- Cost reduction strategies

**Product Opportunity:**
Build **LLM Optimization Lab** with:
- Token-generation visualizations
- Prompt-cache hit/miss simulations
- Cost calculators
- Latency benchmarks
- Semantic similarity demos
- Production architecture diagrams

---

### AI-Stock-Scanner
**Repository:** [AI-Stock-Scanner](https://github.com/kapilgupta86/AI-Stock-Scanner)

**What:** AI stock screening and research assistant

**Intended Features:**
- Stock screening
- Candidate discovery
- AI-generated research
- Multi-agent analysis
- Technical/fundamental filtering

**Technology:**
- Python
- Agentic AI patterns
- Stock research workflows
- CrewAI integration likely

**Status:** Early implementation

**Product Opportunity:**
Build standalone **AI Equity Research Assistant** with:
- Fundamental screening
- Technical screening
- News analysis
- Earnings analysis
- Investment thesis generation
- Watchlist monitoring
- Explainable scoring
- Claude Trading Skills integration

---

### Prompts
**Repository:** [Prompts](https://github.com/kapilgupta86/Prompts)

**What:** Prompt engineering and screener experimentation lab

**Status:** Early exploration

**Product Opportunity:**
Formalize into **Prompt Engineering Framework** with:
- Versioned prompts
- Input/output examples
- Evaluation datasets
- Regression tests
- Model comparison
- Cost/latency measurement
- Reusable templates for trading and SRE products

---

### DS (Data Science)
**Repository:** [DS](https://github.com/kapilgupta86/DS)

**Major Projects:**

| Project | Category | Use Case |
|---------|----------|----------|
| House-Price Prediction | Regression ML | Real-estate valuation |
| Fast-Food Analysis | EDA | Consumer analytics |
| Car-Industry Analysis | Business Analytics | Tableau dashboards |
| Mobile-Device Analysis | Data Analysis Capstone | Market research |
| Kubernetes Anomaly Detection | Infrastructure ML | Platform monitoring |
| Advertisement Deep Learning | Deep Learning | Content intelligence |

**Technology:**
- Python
- Jupyter Notebook
- Scikit-learn / PyTorch
- Tableau
- Pandas / NumPy
- Kubernetes monitoring

**Product Opportunity:**
Extract strongest projects into focused case studies:
1. Kubernetes anomaly detection (pairs with Log Analysis Agent)
2. House-price prediction
3. Mobile-device market analysis
4. Automotive business intelligence

---

### DO180-apps
**Repository:** [DO180-apps](https://github.com/kapilgupta86/DO180-apps)

**What:** Red Hat training repository for container and app deployment

**Contents:**
- Node.js sample apps
- PHP Hello World
- To-do application (AngularJS + backend)
- Deep learning notebooks
- Container and infrastructure labs

**Technology:**
- Node.js, PHP, AngularJS
- Apache HTTP Server
- REST API
- Containers / Kubernetes
- Red Hat tooling

**Use Cases:**
- Container training
- Application deployment labs
- OpenShift preparation
- Full-stack application operations

---

### logs
**Repository:** [logs](https://github.com/kapilgupta86/logs)

**What:** Operational log dataset and reference library

**Contents:**
- Sample syslog data
- Machine-check-exception logs
- Architecture diagrams

**Use Cases:**
- Log parser testing
- Elasticsearch ingestion testing
- Observability demonstrations
- Anomaly-detection experimentation
- SRE training
- RCA-agent test fixtures

**Product Opportunity:**
Bundle with Log Analysis Agent as:
- Reproducible test dataset
- Elasticsearch seed-data package
- Regression-test fixture
- Demo environment

---

## 🎯 Cross-Portfolio Product Themes

### Theme 1: Private Enterprise AI
**Combination:**
- Ollama
- Kubernetes/K3s
- Elasticsearch
- ChromaDB
- LangGraph
- RAG

**Potential Products:**
- SRE Copilot
- Telco operations assistant
- Internal knowledge assistant
- Infrastructure troubleshooting
- Secure document intelligence

---

### Theme 2: Domain-Specific AI Agents
**Applied to:**
- Software engineering
- Trading and investment research
- Infrastructure operations
- Sales
- Documents and resumes
- Meeting intelligence
- Video generation

**Key Principle:** Workflow automation and decision support, not generic chatbots.

---

### Theme 3: Multimodal AI
**Covers:**
- Audio
- Video
- Speech
- Text
- Documents
- Images
- Structured data
- Operational logs

---

### Theme 4: Human-in-the-Loop Systems
**Design Principle:** Preserve human control.

**Examples:**
- Trading workflows do not automatically place trades
- SRE workflows generate recommendations
- Engineering agents generate designs
- Research agents support decisions

---

## 🚀 Recommended Flagship Products

### Flagship 1: Enterprise SRE Copilot
**Combines:**
- Log Analysis Agent
- logs dataset
- Kubernetes anomaly detection (from DS)
- Infrastructure GPTs (from GenAI_projects)

**Promise:** Investigate Kubernetes incidents using private AI, correlated logs, metrics, and traces.

**Customers:**
- Telcos
- Platform engineering
- Managed service providers
- Regulated enterprises

---

### Flagship 2: AI Investor Operating System
**Combines:**
- Claude Trading Skills
- AI Stock Scanner
- GenAI stock research crew

**Promise:** Disciplined AI research and portfolio-review system without automated trading.

**Customers:**
- Individual investors
- Financial researchers
- Investment clubs
- Family offices
- Trading educators

---

### Flagship 3: Private Enterprise Knowledge Assistant
**Combines:**
- Knowledge Bot (GenAI_projects)
- Ollama + ChromaDB
- RAG workflows
- Local deployment patterns

**Promise:** Search and reason over private company documents without cloud AI.

**Customers:**
- Enterprises
- Legal teams
- Telcos
- Government
- Research institutions
- Healthcare organizations

---

### Flagship 4: Meeting and Conversation Intelligence
**Combines:**
- Audio-Video-to-Text
- Whisper
- Llama
- Document processing
- Sales automation

**Promise:** Convert meetings, calls, interviews, lectures into searchable summaries and action items.

**Customers:**
- Engineering teams
- Sales organizations
- Consulting firms
- Universities
- Support teams
- Product management

---

## 📋 Technology Stack Summary

| Category | Technologies |
|----------|--------------|
| **LLM Frameworks** | LangChain, LangGraph, CrewAI, AutoGen, Claude |
| **Local LLMs** | Ollama, Llama, Mistral |
| **Vector DBs** | ChromaDB, Elasticsearch |
| **APIs** | FastAPI, Uvicorn, Gradio |
| **Cloud & Container** | Kubernetes, K3s, Docker |
| **Data** | Elasticsearch, Pandas, NumPy |
| **ML/DL** | PyTorch, Scikit-learn, Transformers |
| **Search & NLP** | Whisper, Embeddings, ChromaDB |
| **Integration** | MCP, Tool calling, REST APIs |

---

## 💼 Professional Positioning

### Summary
**An AI solutions architect and product builder focused on secure, domain-specific, agentic AI systems for enterprise operations, investment research, and multimodal automation.**

### Key Strengths
- ✅ Agentic AI orchestration
- ✅ Local-first enterprise security
- ✅ Kubernetes / infrastructure expertise
- ✅ Production-oriented design
- ✅ Multiple domain expertise
- ✅ Human-in-the-loop AI systems
- ✅ Full-stack AI product development

### Best Positioning For
- AI Solutions Architect (enterprises)
- AI Products Manager
- Startup CTO (AI-focused)
- AI Engineering Lead
- Enterprise AI Consultant

---

## 📁 Portfolio Organization

### Production-Oriented Products
1. Log Analysis Agent
2. Claude Trading Skills
3. Knowledge Bot
4. Audio-Video-to-Text

### AI Engineering Demonstrations
1. CrewAI Engineering Team
2. LangGraph Workflows
3. AutoGen Patterns
4. MCP Servers
5. AI Video Agent
6. Infrastructure GPTs

### Data Science & Analytics
1. Kubernetes Anomaly Detection
2. House-Price Prediction
3. Mobile-Device Analysis
4. Automotive Analytics
5. Advertisement Deep Learning

### Learning & Reference
1. Agentic-AI
2. DO180-apps
3. logs
4. Prompts

---

## 🎓 Next Steps

### To Maximize Portfolio Impact:

1. **Prioritize Log Analysis Agent**
   - Add web dashboard
   - Integrate Prometheus + Jaeger
   - Create demo environment
   - Write 3 customer case studies

2. **Enhance Claude Trading Skills**
   - Create investor personas
   - Write workflow tutorials
   - Build comparison matrix vs competitors
   - Develop API/CLI access patterns

3. **Productize Knowledge Bot**
   - Create SaaS deployment guide
   - Add pre-built connectors (Slack, Teams)
   - Write security/compliance docs
   - Develop customer onboarding

4. **Consolidate Repositories**
   - Merge related projects
   - Create unified documentation
   - Standardize deployment
   - Add architecture diagrams

5. **Create Case Studies**
   - Pick 3 strongest products
   - Document real-world scenarios
   - Show before/after metrics
   - Include technical deep-dives

---

## 📞 Contact & Collaboration

**GitHub:** [@kapilgupta86](https://github.com/kapilgupta86)

**Open to:**
- Enterprise AI consulting
- Startup CTO/founder roles
- Product partnerships
- Research collaborations
- Speaking engagements on agentic AI

---

*Last updated: September 2026*
*Portfolio includes 10+ repositories with 100+ projects spanning AI, ML, DevOps, and data science.*
