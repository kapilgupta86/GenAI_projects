# Kapil Gupta — GenAI Product Portfolio

This portfolio is a precise inventory of the actual AI and agentic projects present in the `GenAI_projects` repository and related work in your GitHub profile. It goes beyond generic summaries and captures the real project names, use cases, technologies, and product thinking reflected in the code and folders.

---

## Executive Summary

This repository is not a single product; it is a full portfolio of AI product experiments, agent patterns, and domain-specific automation solutions. The strongest themes are:

- Agentic AI / multi-agent systems
- Local-first enterprise RAG
- Multimodal AI (video, audio, documents)
- Infrastructure and DevOps AI copilots
- Investment research automation
- Automation for sales, documentation, and business workflows
- AI systems that combine local models, APIs, and frameworks like LangGraph, AutoGen, CrewAI, and MCP

The portfolio shows a clear product direction: building AI systems that are practical, domain-specific, and often private-first rather than generic chatbots.

---

## Portfolio Inventory

The following are the real project areas present in `GenAI_projects` and related repositories:

| # | Project / Folder | Category | Status | Product Lens |
|---|---|---|---|---|
| 1 | `AIVideoProject_30sept` | Multimodal AI | Active | AI video generation |
| 2 | `knowledge_bot_local22sept` | Enterprise RAG | Active | Local knowledge assistant |
| 3 | `knowledge_bot_v25sept` | Enterprise RAG | Active | Local enterprise copilot |
| 4 | `3_crew` | Multi-agent systems | Active | CrewAI team simulation |
| 5 | `stock-research-crew` | Domain expert agent | Active | AI stock research assistant |
| 6 | `Project Sales Email Automation` | Business automation | Active | Sales outreach automation |
| 7 | `resume_conversion_chatbot` | Document automation | Active | Resume conversion and extraction |
| 8 | `Infragpts` | DevOps / infra AI | Active | Infrastructure Copilot |
| 9 | `4_langgraph` | Agent orchestration | Active | Stateful agent flows |
| 10 | `5_autogen` | Agent orchestration | Active | AutoGen patterns |
| 11 | `6_mcp` | Tool integration | Active | MCP servers and tool use |
| 12 | `2_openai` | AI foundation / labs | Active | OpenAI experiments |
| 13 | `Deep Research` | Research / design documents | Active | AI research design |
| 14 | `1_foundations` | AI foundations | Active | Learning and foundational patterns |
| 15 | `guides` | Learning content | Active | Applied AI education |
| 16 | `setup` | Environment setup | Active | Local AI setup and onboarding |
| 17 | `Audio-Video-to-Text` | External repo | Active | Meeting transcribe + summarize |
| 18 | `log_analysis_agent` | External repo | Active | SRE log RCA AI |
| 19 | `claude-trading-skills` | External repo | Active | AI trading workflow toolkit |
| 20 | `AI-Stock-Scanner` | External repo | Active | AI stock discovery |

---

## 1) AI Video Agent

Project folder: `AIVideoProject_30sept`

### What it does
This project automates the creation of faceless videos from text prompts and scripts. It turns written content into a generated voiceover, syncs face or avatar motion to speech, and exports a final video.

### Product idea
A low-cost AI content creation engine for:
- YouTube automation
- Product explainers
- Social media clips
- Multilingual marketing videos
- Internal training content

### Technology stack
- Python
- gTTS / text-to-speech
- FFmpeg
- moviepy
- pydub
- librosa
- Wav2Lip / lip-sync workflows
- Kubernetes-based deployment patterns

### Product use cases
- Faceless video publishing
- Multilingual ad creation
- Educational content generation
- AI presenter workflows
- Rapid content production for digital channels

---

## 2) Knowledge Bot – Local Enterprise RAG

Project folders:
- `knowledge_bot_local22sept`
- `knowledge_bot_v25sept`

### What it does
This is a private, local-first knowledge assistant that can ingest documents and answer questions grounded in those documents. The system is designed to work without sending documents to external cloud APIs.

### Product idea
A secure internal knowledge bot for enterprises and regulated businesses.

### Technology stack
- Ollama
- ChromaDB
- CrewAI
- Python
- PDF/Text document ingestion
- Local embeddings
- Gradio or CLI-based interface

### Key features
- Local-first document search
- Knowledge grounding from PDFs and documents
- Intent routing and retrieval
- Private AI experience
- Reduced cloud dependency

### Product use cases
- Internal documentation search
- Policy and SOP retrieval
- Legal document Q&A
- Telco runbook search
- Engineering knowledge base
- Research paper exploration
- Secure enterprise internal copilots

---

## 3) CrewAI Engineering Team

Project folder: `3_crew`

### What it does
This is a multi-agent simulation of a software engineering team. Different agents specialize in roles like engineering lead, backend engineer, frontend engineer, and QA engineer.

### Product idea
An AI-powered software design and specification engine.

### Technology stack
- CrewAI
- Python
- YAML-based agent/task config
- LLMs (OpenAI or local models)
- Markdown-based output generation

### Product use cases
- Product requirement processing
- HLD / LLD drafting
- API and database design
- UI architecture generation
- Test plan creation
- Documentation generation

---

## 4) Stock Research Crew

Project folder: `stock-research-crew`

### What it does
This project creates a research workflow for analyzing stocks, understanding fundamentals, and generating investment research summaries.

### Product idea
An AI analyst workflow for investment research.

### Technology stack
- Python
- CrewAI or similar agent orchestration
- Financial data context
- LLM-based reasoning
- Structured research outputs

### Product use cases
- Stock company analysis
- Investment thesis generation
- Research summaries
- Equity screening support
- AI-assisted analyst workflows

---

## 5) Sales Email Automation

Project folder: `Project Sales Email Automation`

### What it does
This project automates the creation of sales outreach emails, likely using structured context and content generation.

### Product idea
A sales enablement AI that drafts personalized follow-ups.

### Technology stack
- Python
- LLMs
- Prompt engineering
- Business workflow automation

### Product use cases
- Personalized outbound emails
- Sales follow-up automation
- CRM-ready draft generation
- Marketing sequence support
- B2B outreach acceleration

---

## 6) Resume Conversion Chatbot

Project folder: `resume_conversion_chatbot`

### What it does
This project converts resumes and structured candidate documents into cleaner digital formats or simplified structured outputs for automation.

### Product idea
A document transformation assistant for hiring and recruitment workflows.

### Technology stack
- Python
- OpenAI
- Gradio
- pypdf
- python-docx
- requests
- python-dotenv

### Product use cases
- Resume parsing
- Candidate profile transformation
- Recruiter automation
- PDF/Doc conversion
- Job application assistance

---

## 7) Infra GPTs

Project folder: `Infragpts`

### What it does
This project focuses on AI-assisted infrastructure operations, likely for troubleshooting, runbooks, and technical guidance in DevOps environments.

### Product idea
An infrastructure copilot for platform engineering and cloud operations teams.

### Technology stack
- Python
- LLMs
- Tool / runbook integration
- DevOps content grounding
- Local or cloud-backed workflows

### Product use cases
- Infrastructure troubleshooting
- Kubernetes support
- Runbook retrieval
- DevOps question answering
- Platform engineering knowledge access

---

## 8) LangGraph Flows

Project folder: `4_langgraph`

### What it does
This area focuses on stateful workflow design using LangGraph, a framework for graph-based multi-step agent execution.

### Product idea
Reusable orchestration patterns for AI workflows that need memory, branching, and tool calls.

### Technology stack
- LangGraph
- Python
- LLM orchestration
- State management
- Tool calling

### Product use cases
- Stateful conversational agents
- Decision pipelines
- Multi-step reasoning flows
- Workflow automation with memory

---

## 9) AutoGen Patterns

Project folder: `5_autogen`

### What it does
This area demonstrates AutoGen-based multi-agent collaboration patterns.

### Product idea
A learning and experimentation space for agent-to-agent collaboration and task delegation.

### Technology stack
- AutoGen
- Python
- Agent collaboration frameworks
- LLMs

### Product use cases
- Multi-agent planning
- Delegated task execution
- Collaborative problem-solving
- Research and simulation patterns

---

## 10) MCP Servers and Tool Use

Project folder: `6_mcp`

### What it does
This project likely explores the Model Context Protocol (MCP), which connects AI agents with external tools and services in a structured way.

### Product idea
A tool integration layer for AI agents to interact with external systems.

### Technology stack
- MCP
- Python
- Tool integrations
- LLM agent frameworks

### Product use cases
- Agent tool calling
- External service integration
- AI workflows connected to APIs and local tools
- Production tool adapters for agents

---

## 11) OpenAI and Foundation Labs

Project folder: `2_openai`

### What it does
This area likely contains exercises and demonstrations based on OpenAI models, APIs, and prompt techniques.

### Product idea
Foundational AI sprint work that prepares the rest of the portfolio.

### Technology stack
- OpenAI API
- Python
- Prompt engineering
- LLM experiments

### Product use cases
- Model experimentation
- API integration learning
- Prompt iteration
- Foundation AI experiments

---

## 12) Deep Research

Project folder: `Deep Research`

### What it does
This area appears to house research, design concepts, and strategic AI artifacts related to deep research workflows and reasoning systems.

### Product idea
A design and research engine for advanced investigation tasks.

### Technology stack
- LLMs
- Research design docs
- AI reasoning workflows

### Product use cases
- Deep research automation
- Document synthesis
- Investigative intelligence workflows
- Research assistant design

---

## 13) Foundations and Learning

Project folder: `1_foundations`

### What it does
This is the foundational training layer for the portfolio, likely including notebooks, setup guidance, basic patterns, and first-principles AI learning.

### Product idea
A learning backbone for the broader AI portfolio.

### Technology stack
- Python
- Notebooks
- AI fundamentals
- Prompt, model, and tool basics

### Product use cases
- Beginner AI learning
- Model fundamentals
- Prompt engineering practice
- Agentic AI education

---

## 14) Guides and Setup

Folders:
- `guides`
- `setup`

### What they do
These support the rest of the repo by providing onboarding, environment setup, usage instructions, and project guidance.

### Product idea
A reusable AI engineering enablement layer for local setup and project onboarding.

---

## Related External Repositories in Your Portfolio

### Audio-Video-to-Text
GitHub: https://github.com/kapilgupta86/Audio-Video-to-Text

This is a clear multimodal product prototype for meeting transcription and summarization.

### Log Analysis Agent
GitHub: https://github.com/kapilgupta86/log_analysis_agent

This is a strong enterprise AI operations project focused on Kubernetes log root-cause analysis.

### Claude Trading Skills
GitHub: https://github.com/kapilgupta86/claude-trading-skills

This is your most mature domain-specific AI product in the investment domain.

### AI-Stock-Scanner
GitHub: https://github.com/kapilgupta86/AI-Stock-Scanner

This is an early but promising financial research assistant concept.

---

## Product Themes Across the Portfolio

### 1. Local-first enterprise AI
The largest theme is private AI and local-first deployment.

Examples:
- `knowledge_bot_local22sept`
- `knowledge_bot_v25sept`
- `log_analysis_agent`
- enterprise-focused infrastructure workflows

This is a strong positioning for:
- regulated industries
- telco and infra teams
- private enterprise deployments
- edge AI use cases

### 2. Multi-agent orchestration
The repo heavily demonstrates agent frameworks and composition.

Examples:
- CrewAI (`3_crew`)
- LangGraph (`4_langgraph`)
- AutoGen (`5_autogen`)
- MCP (`6_mcp`)

### 3. Multimodal AI
The portfolio spans:
- video generation
- speech and transcription
- PDF/document processing
- resume conversion
- audio summarization

### 4. AI-powered operations and automation
Examples include:
- infrastructure AI assistants
- sales email automation
- document transformation
- stock research workflows
- incident and RCA reasoning

---

## Recommended Portfolio Framing

When presenting this work, frame it as:

"I build domain-specific AI systems for private enterprise workflows, operations intelligence, and decision-support use cases. My portfolio spans local-first RAG, multi-agent systems, multimodal automation, infrastructure copilots, and investor workflows."

---

## Best Product Storylines

### 1. Private enterprise AI products
- Knowledge bot
- Infra GPTs
- Log analysis agent
- SRE and operations copilots

### 2. Agentic workflow platforms
- CrewAI engineering team
- LangGraph flows
- AutoGen patterns
- MCP tool integration

### 3. Multimodal business automation
- AI video agent
- Audio-video-to-text
- Resume conversion chatbot
- Sales email automation

### 4. Domain-specific decision support
- Stock research agent
- Claude trading skills
- AI stock scanner

---

## Strategic Summary

The real product story in this repository is not "chatbots" but "AI systems that solve operational, knowledge, and workflow problems in a specific domain." That is the strongest and most defensible portfolio narrative.

The portfolio is strongest when grouped into four business lanes:

1. Enterprise operations AI
2. Private knowledge AI
3. Agentic workflow systems
4. Multimodal business automation

---

## Closing Positioning Statement

Kapil's GenAI portfolio reflects a strong capability in building practical AI systems across enterprise, investment, and automation use cases, with a clear emphasis on private-first, local-first, and agentic architectures. The work spans AI agents, knowledge systems, multimodal production flows, and infrastructure intelligence — making the portfolio compelling for AI product, platform engineering, and enterprise AI roles.

---

## Quick Product Stack Summary

- LLM frameworks: LangChain, LangGraph, CrewAI, AutoGen, MCP, OpenAI APIs
- Local models: Ollama, Llama, Mistral
- Data & retrieval: ChromaDB, Elasticsearch
- Interfaces: Gradio, CLI, notebooks
- Data types: PDF, audio, video, text, structured docs
- Domains: DevOps, finance, sales, enterprise knowledge, media automation

This is a strong and realistic AI product portfolio, and it is much broader and deeper than a basic demo repository.
