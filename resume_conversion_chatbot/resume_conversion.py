# app.py
from dotenv import load_dotenv
from openai import OpenAI
import json
import os
import requests
import gradio as gr

from pypdf import PdfReader          # pip install pypdf
from docx import Document            # pip install python-docx

# ========== Environment ==========
load_dotenv(override=True)

# ========== Notifications / Tools ==========
def push(text: str):
    try:
        requests.post(
            "https://api.pushover.net/1/messages.json",
            data={
                "token": os.getenv("PUSHOVER_TOKEN"),
                "user": os.getenv("PUSHOVER_USER"),
                "message": text,
            },
            timeout=10,
        )
    except Exception:
        # Non-fatal if Pushover missing
        pass

def record_user_details(email, name="Name not provided", notes="not provided"):
    push(f"Recording {name} with email {email} and notes {notes}")
    return {"recorded": "ok"}

def record_unknown_question(question):
    push(f"Recording {question}")
    return {"recorded": "ok"}

record_user_details_json = {
    "name": "record_user_details",
    "description": "Use this tool to record that a user is interested in being in touch and provided an email address",
    "parameters": {
        "type": "object",
        "properties": {
            "email": {"type": "string", "description": "The email address of this user"},
            "name": {"type": "string", "description": "The user's name, if they provided it"},
            "notes": {"type": "string", "description": "Any additional information about the conversation that's worth recording to give context"},
        },
        "required": ["email"],
        "additionalProperties": False,
    },
}

record_unknown_question_json = {
    "name": "record_unknown_question",
    "description": "Always use this tool to record any question that couldn't be answered as you didn't know the answer",
    "parameters": {
        "type": "object",
        "properties": {
            "question": {"type": "string", "description": "The question that couldn't be answered"},
        },
        "required": ["question"],
        "additionalProperties": False,
    },
}

tools = [
    {"type": "function", "function": record_user_details_json},
    {"type": "function", "function": record_unknown_question_json},
]

# ========== File Readers ==========
def read_txt(path: str) -> str:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except UnicodeDecodeError:
        with open(path, "r", encoding="latin-1", errors="ignore") as f:
            return f.read()
    except Exception as e:
        return f"[TXT read error {os.path.basename(path)}: {e}]"

def read_pdf(path: str) -> str:
    try:
        reader = PdfReader(path)
        out = []
        for page in reader.pages:
            out.append(page.extract_text() or "")
        return "\n".join(out)
    except Exception as e:
        return f"[PDF read error {os.path.basename(path)}: {e}]"

def read_docx(path: str) -> str:
    try:
        doc = Document(path)
        return "\n".join(p.text for p in doc.paragraphs)
    except Exception as e:
        return f"[DOCX read error {os.path.basename(path)}: {e}]"

def read_all_me_files(me_dir: str = "me") -> str:
    if not os.path.isdir(me_dir):
        return ""
    combined = []
    for fname in sorted(os.listdir(me_dir)):
        path = os.path.join(me_dir, fname)
        if not os.path.isfile(path):
            continue
        low = fname.lower()
        if low.endswith(".pdf"):
            content = read_pdf(path)
        elif low.endswith(".docx"):
            content = read_docx(path)
        elif low.endswith(".txt"):
            content = read_txt(path)
        else:
            continue
        combined.append(f"\n\n===== FILE: {fname} =====\n{content}\n")
    return "\n".join(combined)

def truncate(text: str, max_chars: int) -> str:
    if not text:
        return ""
    return text if len(text) <= max_chars else text[:max_chars] + "\n...[truncated]"

# ========== Chat App ==========
class Me:
    def __init__(self):
        # Configure Gemini via OpenAI-compatible endpoint
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise RuntimeError("GOOGLE_API_KEY not set. Create a .env with GOOGLE_API_KEY=your_key")

        self.openai = OpenAI(
            api_key=api_key,
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
        )
        self.model_name = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")

        self.name = "Kapil Gupta"

        # Aggregate all documents from me/ (trim to avoid context overflow)
        corpus = read_all_me_files("me")
        self.profile_corpus = truncate(corpus, max_chars=600000)

        # Optional short summary
        self.summary = ""
        summary_path = os.path.join("me", "summary.txt")
        if os.path.exists(summary_path):
            try:
                with open(summary_path, "r", encoding="utf-8") as f:
                    self.summary = truncate(f.read(), max_chars=80000)
            except Exception:
                self.summary = ""

        self._retried_once = False  # simple retry flag for null-content fallback

    def handle_tool_call(self, tool_calls):
        results = []
        for tool_call in tool_calls:
            tool_name = tool_call.function.name
            try:
                arguments = json.loads(tool_call.function.arguments or "{}")
            except Exception:
                arguments = {}
            tool_fn = globals().get(tool_name)
            result = tool_fn(**arguments) if callable(tool_fn) else {}
            results.append({
                "role": "tool",
                "content": json.dumps(result),
                "tool_call_id": tool_call.id
            })
        return results

    def system_prompt(self):
        system_prompt = (
            f"You are acting as {self.name}. You are answering questions on {self.name}'s website, "
            f"particularly questions related to {self.name}'s career, background, skills and experience. "
            f"Your responsibility is to represent {self.name} for interactions on the website as faithfully as possible. "
            f"You are given a combined corpus from the 'me/' folder which may include summary, LinkedIn, resume, and other documents to answer questions. "
            f"Be professional and engaging for potential clients or future employers. "
            f"If you don't know the answer to any question, use your record_unknown_question tool to record it. "
            f"If the user is engaging in discussion, steer them towards getting in touch via email; ask for their email and record it using your record_user_details tool.\n\n"
        )
        system_prompt += f"## Summary (if available):\n{self.summary}\n\n"
        system_prompt += f"## Profile Corpus (auto-aggregated from 'me/'):\n{self.profile_corpus}\n\n"
        system_prompt += f"With this context, please chat with the user, always staying in character as {self.name}."
        return system_prompt

    def _chat_once(self, messages):
        return self.openai.chat.completions.create(
            model=self.model_name,
            messages=messages,
            tools=tools,
        )

    def chat(self, message, history):
        messages = [{"role": "system", "content": self.system_prompt()}]
        messages += history
        messages.append({"role": "user", "content": message})

        while True:
            resp = self._chat_once(messages)
            if not getattr(resp, "choices", None):
                # Retry with lighter prompt once
                if not self._retried_once:
                    self._retried_once = True
                    base = [{"role": "system", "content": f"You are {self.name}. Be concise and helpful."}]
                    base += [m for m in messages if m["role"] != "system"]
                    messages = base
                    continue
                return "The model returned no choices. Please try again."

            ch = resp.choices[0]
            fr = getattr(ch, "finish_reason", None)
            msg = getattr(ch, "message", None)
            tool_calls = getattr(msg, "tool_calls", []) if msg else []

            # If tool calls requested, execute and loop
            if fr == "tool_calls" or tool_calls:
                messages.append({
                    "role": "assistant",
                    "content": None,
                    "tool_calls": [
                        {
                            "id": tc.id,
                            "type": "function",
                            "function": {
                                "name": tc.function.name,
                                "arguments": tc.function.arguments
                            }
                        } for tc in (tool_calls or [])
                    ],
                })
                results = self.handle_tool_call(tool_calls or [])
                messages.extend(results)
                continue

            # Normal answer
            content = getattr(msg, "content", None) if msg else None
            if content:
                return content

            # If no content and no tool calls -> try once with a lighter system prompt
            if not self._retried_once:
                self._retried_once = True
                base = [{"role": "system", "content": f"You are {self.name}. Be concise and helpful."}]
                base += [m for m in messages if m["role"] != "system"]
                messages = base
                continue
            return "The model returned no text. Try a shorter question or simplify files in 'me/'."

# ========== Main ==========
if __name__ == "__main__":
    me = Me()
    gr.ChatInterface(me.chat, type="messages").launch()python -m pip install -U gradio
