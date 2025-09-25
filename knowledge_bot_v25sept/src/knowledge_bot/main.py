# src/knowledge_bot/main.py
import os
import socket
import gradio as gr
from dotenv import load_dotenv

# Import both versions - crew for complex queries, direct for simple ones  
from knowledge_bot.crew import KnowledgeBotCrew
from knowledge_bot.crew_simple import process_query_direct, _detect_intent

load_dotenv()

DEFAULT_KNOWLEDGE_DIR = "./knowledge"

def find_free_port(start_port=7861):
    """Find an available port starting from the given port."""
    for port in range(start_port, start_port + 10):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(('0.0.0.0', port))
                return port
            except OSError:
                continue
    return 7870

def _drive_connect_and_list_root():
    """Connect to Google Drive and list root folders."""
    try:
        from pydrive2.auth import GoogleAuth
        from pydrive2.drive import GoogleDrive
        gauth = GoogleAuth()
        gauth.LocalWebserverAuth()
        drive = GoogleDrive(gauth)
        file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
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

def kickoff_pipeline(
    query,
    folder_path,
    github_url,
    model,
    save_markdown,
    embed_model,
    use_drive,
    drive_folder_choice,
    top_k,
    knowledge_dir,
    profile_name,
    answer_sink_path,
    answer_max_tokens,
    continue_segments,
    num_ctx,
):
    """Execute the pipeline - uses direct processor for all queries now."""
    
    if not query or not query.strip():
        return "Please enter a query."
    
    # Set up the knowledge directory
    knowledge_path = (knowledge_dir or DEFAULT_KNOWLEDGE_DIR).strip()
    if knowledge_path:
        os.environ["KNOWLEDGE_DIR"] = os.path.abspath(knowledge_path)
    
    # Use the folder path from UI or default to knowledge directory
    folder_to_use = folder_path or os.path.abspath(knowledge_path)
    
    print(f"[MAIN] Processing query: '{query}'")
    print(f"[MAIN] Using folder: {folder_to_use}")
    
    try:
        # Use our working direct processor for all queries
        result = process_query_direct(query, folder_to_use)
        
        # Extract the answer
        answer = result.get("answer", "No answer generated")
        sources = result.get("sources", [])
        
        # Add source information to the answer if available
        if sources and any(s.get("intent") == "rag_query" for s in sources):
            source_files = [s.get("name", "unknown") for s in sources if s.get("name")]
            if source_files:
                answer += f"\n\n📄 Sources: {', '.join(source_files[:3])}"
        
        # Save to markdown if requested
        if save_markdown and save_markdown.strip():
            try:
                with open(save_markdown.strip(), 'w', encoding='utf-8') as f:
                    f.write(f"# Query: {query}\n\n{answer}\n")
                answer += f"\n\n💾 Saved to: {save_markdown.strip()}"
            except Exception as e:
                answer += f"\n\n❌ Error saving to file: {e}"
        
        return answer
        
    except Exception as e:
        error_msg = f"Error processing query: {str(e)}"
        print(f"[MAIN] Error: {error_msg}")
        return error_msg

# Gradio UI
with gr.Blocks(title="KnowledgeBot - Enhanced AI Assistant", theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🤖 KnowledgeBot - Enhanced AI Assistant")
    gr.Markdown("Ask questions about your documents, get personal info, or list files/projects.")
    
    # Example queries
    gr.Markdown("""
    ### 💡 Try these example queries:
    - **Personal Info**: `who am i?`, `what are my interests?`, `what is my role?`
    - **File Operations**: `list .py and .md files`, `show me projects in folder`
    - **Document Search**: `what experience do I have?`, `tell me about my skills`
    - **Custom Path**: `list files in {/path/to/folder}`
    """)
    
    # Main query input
    query = gr.Textbox(
        label="🔍 Your Question", 
        placeholder="Ask anything about your documents or use commands like 'who am i?'",
        lines=2
    )
    
    # Configuration sections
    with gr.Accordion("📁 File Sources", open=False):
        with gr.Row():
            folder = gr.Textbox(
                label="Folder path", 
                value="",
                placeholder="Leave empty to use Knowledge directory below"
            )
            github = gr.Textbox(
                label="GitHub repo URL (optional)", 
                placeholder="https://github.com/user/repo"
            )
        
        knowledge_dir = gr.Textbox(
            label="Knowledge directory", 
            value=DEFAULT_KNOWLEDGE_DIR,
            placeholder="Path to your knowledge base folder"
        )
    
    with gr.Accordion("🔧 Model Configuration", open=False):
        with gr.Row():
            model = gr.Dropdown(
                choices=["mistral", "llama3.2", "llama3.2:1b", "llama2", "gemma"], 
                value="mistral", 
                label="Chat model"
            )
            embed_model = gr.Dropdown(
                choices=["mistral", "nomic-embed-text", "mxbai-embed-large"], 
                value="mistral", 
                label="Embedding model"
            )
            top_k = gr.Slider(1, 20, value=5, step=1, label="Retrieval count (top-k)")
        
        profile_name = gr.Textbox(
            label="Your name (optional)", 
            placeholder="Used for personalized responses"
        )
    
    with gr.Accordion("☁️ Google Drive Integration", open=False):
        with gr.Row():
            use_drive = gr.Checkbox(label="Use Google Drive", value=False)
            drive_folder = gr.Dropdown(
                label="Drive Folder (select after connect)", 
                choices=[],
                interactive=True
            )
        
        with gr.Row():
            drive_btn = gr.Button("🔗 Connect & List Root Folders")
            drive_status = gr.Textbox(label="Drive status", interactive=False)
            drive_btn.click(
                fn=_drive_connect_and_list_root, 
                inputs=None, 
                outputs=[drive_folder, drive_status]
            )
    
    with gr.Accordion("⚙️ Advanced Output Controls", open=False):
        save_md = gr.Textbox(
            label="Save response to markdown file (optional)", 
            placeholder="./response.md"
        )
        
        answer_sink_path = gr.Textbox(
            label="Save extended answers to file (optional)", 
            placeholder="./long_answer.md"
        )
        
        with gr.Row():
            answer_max_tokens = gr.Slider(
                256, 4096, value=2048, step=256, 
                label="Max tokens per response chunk"
            )
            continue_segments = gr.Slider(
                0, 20, value=0, step=1, 
                label="Continuation segments for very long answers"
            )
            num_ctx = gr.Slider(
                2048, 32768, value=8192, step=1024, 
                label="Model context window (num_ctx)"
            )
    
    # Execute button and output
    run_btn = gr.Button("🚀 Run Query", variant="primary", size="lg")
    
    # Output with better formatting
    output = gr.Textbox(
        label="🤖 AI Response", 
        lines=20, 
        max_lines=50,
        show_copy_button=True,
        placeholder="Your response will appear here..."
    )
    
    # Wire up the interface
    run_btn.click(
        kickoff_pipeline,
        inputs=[
            query, folder, github, model, save_md, embed_model, 
            use_drive, drive_folder, top_k, knowledge_dir, profile_name, 
            answer_sink_path, answer_max_tokens, continue_segments, num_ctx
        ],
        outputs=output
    )
    
    # Allow Enter key to submit
    query.submit(
        kickoff_pipeline,
        inputs=[
            query, folder, github, model, save_md, embed_model, 
            use_drive, drive_folder, top_k, knowledge_dir, profile_name, 
            answer_sink_path, answer_max_tokens, continue_segments, num_ctx
        ],
        outputs=output
    )

def run():
    """CLI entry point for crew execution."""
    knowledge_path = os.getenv("KNOWLEDGE_DIR", DEFAULT_KNOWLEDGE_DIR)
    os.environ["KNOWLEDGE_DIR"] = os.path.abspath(knowledge_path)
    
    # Simple CLI test
    query = os.getenv("KB_QUERY", "who am i?")
    result = process_query_direct(query, knowledge_path)
    print(result.get("answer", "No answer"))

if __name__ == "__main__":
    port = find_free_port()
    print(f"🚀 Starting KnowledgeBot on port {port}")
    print(f"🌐 Access at: http://0.0.0.0:{port}")
    demo.launch(server_name="0.0.0.0", server_port=port, show_error=True)
