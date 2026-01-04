
# 🚀 **KAPIL GUPTA - COMPLETE GenAI \& LLM PORTFOLIO SHOWCASE**

**Version:** 2.0 (Validated \& Updated)
**Date:** January 4, 2026
**GitHub:** [@kapilgupta86](https://github.com/kapilgupta86)

***

## 📋 **TABLE OF CONTENTS**

1. Executive Summary
2. Project Inventory (with validated URLs)
3. Detailed Architecture \& Skills Matrix
4. Framework Coverage \& Tech Stack
5. Deployment Guide
6. Monetization Angles
7. Key Differentiators
8. Next Steps \& Action Items

***

## **SECTION 1: EXECUTIVE SUMMARY**

You are showcasing **10+ production-ready GenAI projects** that span:

✅ **Advanced Agent Frameworks** – CrewAI, LangGraph, AutoGen, MCP

✅ **Multimodal AI** – Video generation (Wav2Lip), Speech-to-text (Whisper), Audio synthesis

✅ **Enterprise RAG** – Local inference (Ollama), Vector DBs (Chroma), Intent routing

✅ **Production Ops** – Kubernetes deployment, containerization, scalable pipelines

✅ **Domain Expertise** – Stock market analysis, infra/DevOps AI, sales automation

✅ **Full-Stack Thinking** – From notebooks → APIs → SaaS-ready products

**Target Audience:** GenAI Engineers, AI Architects, Startup Founders, Tech Leads
**Best For:** Startups, enterprises seeking local-first AI, telco/edge computing roles

***

## **SECTION 2: COMPLETE PROJECT INVENTORY**

### **Main Repository Structure**

| Folder | Purpose | Status | Last Update |
| :-- | :-- | :-- | :-- |
| **GenAI_projects** | Parent repo (monorepo) | ✅ Active | Jan 4, 2026 |
| **Audio-Video-to-Text** | Separate standalone repo | ✅ Active | Jan 2, 2026 |

### **All Projects with Direct Links**

#### **🎬 MULTIMODAL PROJECTS**

| \# | Project | Path | URL | Tech Stack |
| :-- | :-- | :-- | :-- | :-- |
| 1 | **AI Video Agent** | `/AIVideoProject_30sept` | [View](https://github.com/kapilgupta86/GenAI_projects/tree/main/AIVideoProject_30sept) | Wav2Lip, FFmpeg, TTS, K8s |
| 2 | **Audio-Video to Minutes** | Separate repo | [View](https://github.com/kapilgupta86/Audio-Video-to-Text) | Whisper, Llama-3.1-8B, moviepy |

#### **🤖 RAG \& AGENT PROJECTS**

| \# | Project | Path | URL | Tech Stack |
| :-- | :-- | :-- | :-- | :-- |
| 3 | **Knowledge Bot** | `/knowledge_bot_v25sept` | [View](https://github.com/kapilgupta86/GenAI_projects/tree/main/knowledge_bot_v25sept) | CrewAI, Ollama, Chroma, Gradio |
| 4 | **CrewAI Eng. Team** | `/3_crew/engineering_team` | [View](https://github.com/kapilgupta86/GenAI_projects/tree/main/3_crew/engineering_team) | CrewAI, YAML, multi-agent SDLC |
| 5 | **LangGraph Flows** | `/4_langgraph` | [View](https://github.com/kapilgupta86/GenAI_projects/tree/main/4_langgraph) | LangGraph, state machines |
| 6 | **AutoGen Patterns** | `/5_autogen` | [View](https://github.com/kapilgupta86/GenAI_projects/tree/main/5_autogen) | AutoGen, agent collaboration |

#### **💼 DOMAIN-SPECIFIC PROJECTS**

| \# | Project | Path | URL | Tech Stack |
| :-- | :-- | :-- | :-- | :-- |
| 7 | **Stock Research Crew** | `/stock-research-crew` | [View](https://github.com/kapilgupta86/GenAI_projects/tree/main/stock-research-crew) | RAG, agents, finance domain |
| 8 | **Sales Email Automation** | `/Project Sales Email Automation` | [View](https://github.com/kapilgupta86/GenAI_projects/tree/main/Project%20Sales%20Email%20Automation) | Email gen, personalization |
| 9 | **Infra GPTs** | `/Infragpts` | [View](https://github.com/kapilgupta86/GenAI_projects/tree/main/Infragpts) | K8s diags, AIOps, runbooks |

#### **🔧 FOUNDATIONAL \& TOOL PROJECTS**

| \# | Project | Path | URL | Tech Stack |
| :-- | :-- | :-- | :-- | :-- |
| 10 | **Resume Chatbot** | `/resume_conversion_chatbot` | [View](https://github.com/kapilgupta86/GenAI_projects/tree/main/resume_conversion_chatbot) | Prompt eng., Streamlit/Gradio |
| 11 | **MCP Servers** | `/6_mcp` | [View](https://github.com/kapilgupta86/GenAI_projects/tree/main/6_mcp) | Model Context Protocol |
| 12 | **OpenAI Labs** | `/2_openai` | [View](https://github.com/kapilgupta86/GenAI_projects/tree/main/2_openai) | GPT APIs, prompts |
| 13 | **Deep Research Agent** | `/Deep Research` | [View](https://github.com/kapilgupta86/GenAI_projects/blob/main/Deep%20Research/document.txt) | Multi-hop reasoning design doc |
| 14 | **Foundations** | `/1_foundations` | [View](https://github.com/kapilgupta86/GenAI_projects/tree/main/1_foundations) | Educational notebooks |


***

## **SECTION 3: DETAILED PROJECT DEEP-DIVES**

### **PROJECT 1: AI VIDEO AGENT** 🎬

**🔗 URL:** https://github.com/kapilgupta86/GenAI_projects/tree/main/AIVideoProject_30sept

**⏱️ Problem:** Convert text script → HD lip-synced video in 5 minutes (vs manual editing: 4+ hours)

**🏗️ ARCHITECTURE DIAGRAM:**

```
Script (text)
    ↓
Text-to-Speech (gTTS)
    ↓ MP3 Audio
Audio Chunking & Normalization (FFmpeg, pydub, librosa)
    ↓ WAV segments
Lip-Sync Generation (Wav2Lip deep learning)
    ↓ Video frames
Audio-Video Muxing (FFmpeg)
    ↓
Final MP4 (H.264 + AAC, HD 720p/1080p)
```

**💡 KEY DIFFERENTIATORS:**


| Feature | Your Solution | Industry Standard (D-ID, Synthesia) |
| :-- | :-- | :-- |
| **Cost** | \$0/month (self-hosted) | \$50-500/month per video |
| **Privacy** | Fully on-prem | Cloud-dependent |
| **Long-form** | Supports 2-10 min videos | 60-90 sec per frame |
| **Customization** | Direct model control | Black-box APIs |
| **Deployment** | Kubernetes-native | SaaS only |
| **Setup** | 30 min (containerized) | 5 min (API key) |

**🛠️ TECH STACK:**

```
Frontend: CLI / Python script
Processing Pipeline:
  - Audio: gTTS → MP3 → FFmpeg (normalize, resample) → WAV segments
  - Video: Wav2Lip (PyTorch) → inference → frame seq
  - Muxing: ffmpeg-python → final MP4
Infrastructure: Docker container, Kubernetes pod
Languages: Python 3.9+
Key Libs: moviepy, librosa, numpy, torch, wav2lip-gfpgan
```

**📊 SKILLS SHOWCASED:**


| Skill | Depth | Evidence |
| :-- | :-- | :-- |
| Deep Learning Pipelines | ⭐⭐⭐⭐⭐ | Wav2Lip model inference, inference optimization |
| Audio Engineering | ⭐⭐⭐⭐⭐ | TTS, PCM conversion, normalization, chunking |
| Video Codecs \& FFmpeg | ⭐⭐⭐⭐ | H.264, AAC, container format, bitrate control |
| Kubernetes MLOps | ⭐⭐⭐⭐ | Container images, resource limits, dependency pinning |
| Python Packaging | ⭐⭐⭐⭐ | Version conflicts (numpy/librosa/torch), lock files |
| Production Hardening | ⭐⭐⭐⭐ | Error handling, fallbacks, extensive logging |

**📈 BUSINESS IMPACT:**

- ✅ **80% time savings** on video creation (4 hours → 5 min)
- ✅ **Enables YouTube automation** (explainers, tutorials, multilingual ads)
- ✅ **Cost reduction** for content creators/agencies
- ✅ **Scalable** via Kubernetes (batch processing 100s of videos)

**🎯 IDEAL USE CASES:**

- Educational content (explainer videos, tutorials)
- Multilingual ads (hindi/english variants)
- Meeting recaps with AI presenter
- Training videos with talking head
- Social media automation (short-form + long-form)

***

### **PROJECT 2: KNOWLEDGE BOT – HYBRID RAG** 🧠

**🔗 URL:** https://github.com/kapilgupta86/GenAI_projects/tree/main/knowledge_bot_v25sept

**⏱️ Problem:** Build a **private, local knowledge assistant** that reads your docs and answers—without OpenAI/cloud APIs.

**🏗️ ARCHITECTURE DIAGRAM:**

```
User Documents (PDFs, TXT, Markdown)
    ↓ [Chunking & Embedding]
Vector Store (Chroma DB)
    ↓
User Query
    ↓
[Intent Router]
├─ Q&A mode → Retrieval-Augmented Generation
├─ Procedural → Step-by-step instructions
├─ Directory → List all docs
└─ Profile → Personal info ("who am I?")
    ↓
[CrewAI Agent]
    ├─ Retrieve relevant chunks
    ├─ Chain-of-thought reasoning
    └─ Generate grounded answer
    ↓
Response (with citations)
    ↓
Gradio UI / CLI / API
```

**💡 KEY DIFFERENTIATORS:**


| Aspect | Your Solution | Competitors |
| :-- | :-- | :-- |
| **Inference** | 100% local (Ollama) | OpenAI, Claude APIs |
| **Privacy** | Zero external calls | Cloud-dependent |
| **Cost** | \$0/month | \$0.01-0.10 per query |
| **Intent Routing** | Reduces hallucinations | Generic retrieval |
| **Enterprise Ready** | On-prem data residency | SaaS only |
| **Customization** | Full model/prompt control | Limited |

**🛠️ TECH STACK:**

```
Embedding: Ollama (mxbai-embed, all-MiniLM)
Vector DB: ChromaDB (persistent storage)
LLM: Ollama-hosted (Llama-3.1-8B, Mistral)
Agent: CrewAI (agents, tasks, tools)
Intent Router: Custom Python classifier
UI: Gradio (web interface)
CLI: CrewAI CLI (`crewai run`)
Config: YAML (declarative task/agent definitions)
```

**📊 SKILLS SHOWCASED:**


| Skill | Depth | Evidence |
| :-- | :-- | :-- |
| RAG Architecture | ⭐⭐⭐⭐⭐ | Chunking, embeddings, vector search, citations |
| CrewAI Framework | ⭐⭐⭐⭐⭐ | Agents, tasks, Knowledge source API, YAML config |
| Intent Classification | ⭐⭐⭐⭐ | NLP routing, handler specialization |
| Local LLM Inference | ⭐⭐⭐⭐⭐ | Ollama, quantization, resource optimization |
| Gradio Development | ⭐⭐⭐⭐ | UI components, file upload, streaming |
| Vector DB Design | ⭐⭐⭐⭐ | Chroma persistence, semantic search |

**📈 BUSINESS IMPACT:**

- ✅ **100% private** knowledge base (no API calls)
- ✅ **5-10x cheaper** than OpenAI at scale
- ✅ **Meets data compliance** (GDPR, on-prem deployments)
- ✅ **Instant answers** from company docs
- ✅ **Reproducible** (same model version = same answers)

**🎯 IDEAL USE CASES:**

- **Enterprise:** Internal documentation bot (HR policies, tech docs)
- **Legal:** Case law / contract analysis
- **Customer Support:** Product docs + FAQ automation
- **R\&D:** Paper/research knowledge base
- **Telco:** Operations manuals, runbooks

***

### **PROJECT 3: RESUME CONVERSION CHATBOT** 📄

**🔗 URL:** https://github.com/kapilgupta86/GenAI_projects/tree/main/resume_conversion_chatbot

**⏱️ Problem:** Convert generic resume → job-specific, ATS-optimized content in seconds.

**🏗️ SIMPLE ARCHITECTURE:**

```
Resume Upload (PDF/TXT)
    ↓
Text Extraction
    ↓
[Prompt Templates]
├─ Summary template (2-3 lines)
├─ Bullets template (STAR method, action verbs)
├─ Skills template (categorized)
└─ LinkedIn template (narrative)
    ↓
LLM Processing (GPT-4 / Claude / local)
    ↓
Structured Output (JSON / Markdown)
    ↓
Web App (Streamlit / Gradio)
```

**💡 KEY DIFFERENTIATORS:**


| Aspect | Your Solution | Manual Rewriting |
| :-- | :-- | :-- |
| **Speed** | 30 sec / resume | 30 min / resume |
| **Consistency** | Template-driven | Varies by person |
| **Scalability** | 1000s at once | One-by-one |
| **Cost** | \$5-20 SaaS model | \$50-100 hr consulting |
| **Productization** | Ready-to-deploy | Just a script |

**🛠️ TECH STACK:**

```
PDF Extraction: pdfplumber / PyPDF2
Text Processing: string manipulation
Prompt Templates: Jinja2
LLM Backend: OpenAI / Claude / local
Web Framework: Streamlit or Gradio
Deployment: HF Spaces / Streamlit Cloud / GitHub Pages
Output Format: JSON / Markdown
```

**📊 SKILLS SHOWCASED:**


| Skill | Depth |
| :-- | :-- |
| Prompt Engineering | ⭐⭐⭐⭐ |
| Domain Knowledge (HR/ATS) | ⭐⭐⭐⭐ |
| PDF Extraction |  |

