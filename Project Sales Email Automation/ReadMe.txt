## Project Overview: Agentic Sales Email Automation

This project demonstrates an agentic framework for automating the generation and sending of cold sales emails using multiple AI models and tools. The workflow leverages OpenAI-compatible models, structured outputs, and guardrails to ensure safe and effective automation.

### Key Components

- **Multiple AI Models:**  
  The system uses DeepSeek, Gemini, and Llama3.3 models to generate diverse sales email drafts.

- **Agentic Design:**  
  Each model is wrapped as an agent, and agents are converted into callable tools for collaboration.

- **Tool Integration:**  
  Functions such as `send_html_email` are decorated with `@function_tool`, making them available for agent workflows.

- **Email Formatting Pipeline:**  
  The process includes generating an email subject, converting the body to HTML, and sending the email via SendGrid.

- **Guardrails:**  
  Input guardrails (using Pydantic models and custom functions) check for sensitive information, such as personal names, before proceeding.

- **Traceability:**  
  All agent actions and tool calls are traced for debugging and review via the OpenAI platform.

### Workflow

1. **Generate Email Drafts:**  
   Three agents, each with a different style, generate cold sales email drafts.

2. **Select the Best Draft:**  
   A sales manager agent reviews the drafts and selects the most effective one.

3. **Format and Send Email:**  
   The selected draft is handed off to an email manager agent, which formats the email and sends it using SendGrid.

4. **Guardrail Protection:**  
   Input guardrails ensure compliance and safety by checking for personal names in the message.

### Technologies Used

- OpenAI API (and compatible endpoints)
- SendGrid for email delivery
- Python agentic framework (`agents` module)
- Pydantic for structured outputs
- Guardrails for input validation

### How to Use

- Set up API keys for OpenAI, Google, DeepSeek, Groq, and SendGrid in your .env file.
- Verify your sender email in SendGrid.
- Run the notebook to generate, select, format, and send sales emails automatically.
- Review traces at [OpenAI Traces](https://platform.openai.com/traces).

---

Let me know if you want a more detailed or technical breakdown for your markdown file!