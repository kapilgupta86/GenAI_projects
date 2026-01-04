import os
import json
import gradio as gr
from dotenv import load_dotenv

from knowledge_bot.crew import KnowledgeBotCrew

# Load environment early for CLI and UI runs
load_dotenv()

# -----------------------------
# Google Drive helpers for UI
# -----------------------------
def _drive_connect_and_list_root():
    """
    Opens a local OAuth browser window and lists root folders.
    Returns a dropdown update and a status text.
    """
    try:
        from pydrive2.auth import GoogleAuth
        from pydrive2.drive import GoogleDrive

        gauth = GoogleAuth()
        gauth.LocalWebserverAuth()
        drive = GoogleDrive(gauth)

        file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
        # Only folders for navigation
        choices = []
        for f in file_list:
            mt = f.get('mimeType', '')
            if 'folder' in mt:
                name = f.get('title') or f.get('name')
                fid = f['id']
                if name and fid:
                    choices.append(f"{name}::{fid}")
        if not choices:
            choices = ["<no folders found in root>"]
        return gr.update(choices=choices, value=None), "Drive connected. Select a folder from the dropdown."
    except Exception as e:
        return gr.update(choices=[]), f"Drive error: {e}"

# -----------------------------
# Crew kickoff pipeline
# -----------------------------
def kickoff_pipeline(query, folder_path, github_url, model, save_markdown, embed_model, use_drive, drive_folder_choice, top_k):
    """
    Runs the sequential crew: ingest -> embed -> query with provided UI inputs.
    """
    # Parse selected drive folder id if provided
    drive_folder_id = None
    if use_drive and drive_folder_choice and "::" in drive_folder_choice:
        drive_folder_id = drive_folder_choice.split("::")[-1]

    kb = KnowledgeBotCrew()
    inputs = {
        "query": query or "",
        "folder_path": folder_path or os.path.join(os.path.expanduser("~"), "Desktop"),
        "github_url": github_url or "",
        "model": model or "mistral",
        "embed_model": embed_model or "mistral",
        "save_markdown": save_markdown if save_markdown else None,
        "use_drive": bool(use_drive),
        "drive_folder_id": drive_folder_id,
        "top_k": int(top_k or 5),
    }
    try:
        result = kb.crew().kickoff(inputs=inputs)
        # Prefer final_output if available; otherwise fall back to last task output
        final = getattr(result, "final_output", None)
        if not final:
            outs = getattr(result, "tasks_output", [])
            last_item = outs[-1] if outs else None
            final = getattr(last_item, "raw", last_item)
        answer = final.get("answer", "") if isinstance(final, dict) else str(final)
    except Exception as e:
        answer = f"Error during crew execution: {e}"
    return answer

# -----------------------------
# Gradio UI
# -----------------------------
with gr.Blocks(title="KnowledgeBot") as demo:
    gr.Markdown("## KnowledgeBot")

    query = gr.Textbox(label="Text query", placeholder="Ask a question...")
    folder = gr.Textbox(label="Folder path (default: Desktop)")
    github = gr.Textbox(label="GitHub repo URL (optional)")

    with gr.Row():
        model = gr.Dropdown(
            choices=["mistral", "llama3", "llama2", "gemma"],
            value="mistral",
            label="Ollama model"
        )
        embed_model = gr.Dropdown(
            choices=["mistral", "nomic-embed-text", "mxbai-embed-large"],
            value="mistral",
            label="Embedding model"
        )
        top_k = gr.Slider(1, 10, value=5, step=1, label="Top-k")

    with gr.Row():
        use_drive = gr.Checkbox(label="Use Google Drive", value=False)
        drive_folder = gr.Dropdown(label="Drive Folder (select after connect)", choices=[])

    with gr.Row():
        drive_btn = gr.Button("Connect & List Root Folders")
        drive_status = gr.Textbox(label="Drive status", interactive=False)
        drive_btn.click(fn=_drive_connect_and_list_root, inputs=None, outputs=[drive_folder, drive_status])

    save_md = gr.Textbox(label="Save response to markdown file (path optional)")

    run_btn = gr.Button("Run")
    output = gr.Textbox(label="AI-generated response")

    run_btn.click(
        kickoff_pipeline,
        inputs=[query, folder, github, model, save_md, embed_model, use_drive, drive_folder, top_k],
        outputs=output
    )

# -----------------------------
# CLI entry for `crewai run`
# -----------------------------
def run():
    """
    Entry point for CrewAI CLI via pyproject [project.scripts].
    Reads optional env vars and kicks off the crew in headless mode.
    """
    kb = KnowledgeBotCrew()
    try:
        inputs = {
            "query": os.getenv("KB_QUERY", ""),
            "folder_path": os.getenv("KB_FOLDER_PATH", os.path.join(os.path.expanduser("~"), "Desktop")),
            "github_url": os.getenv("KB_GITHUB_URL", ""),
            "model": os.getenv("KB_MODEL", "mistral"),
            "embed_model": os.getenv("KB_EMBED_MODEL", "mistral"),
            "save_markdown": os.getenv("KB_SAVE_MD") or None,
            "use_drive": os.getenv("KB_USE_DRIVE", "false").lower() == "true",
            "drive_folder_id": os.getenv("KB_DRIVE_FOLDER_ID") or None,
            "top_k": int(os.getenv("KB_TOP_K", "5")),
        }
        result = kb.crew().kickoff(inputs=inputs)
        final = getattr(result, "final_output", None)
        if not final:
            outs = getattr(result, "tasks_output", [])
            last_item = outs[-1] if outs else None
            final = getattr(last_item, "raw", last_item)
        if isinstance(final, dict) and "answer" in final:
            print(final["answer"])
        else:
            print(final)
    except Exception as e:
        # Print a single-line error for CLI ergonomics
        print(f"Error during crew execution: {e}")

if __name__ == "__main__":
    # Launch UI for interactive usage
    demo.launch(server_name="0.0.0.0", server_port=7861)

