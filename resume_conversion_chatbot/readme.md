This app is a Gradio chatbot that impersonates “Kapil Gupta,” loads profile documents from a local me/ folder (PDF/DOCX/TXT), and uses Google Gemini via the OpenAI-compatible endpoint to answer queries with tool-calling support for capturing user emails and unknown questions; it includes defensive logic for tool_calls, empty content, and oversized prompts, and notifies via Pushover when tools are used.

How the code works
Environment and setup
Loads environment variables with load_dotenv(override=True) so local .env values populate os.getenv() at runtime; in hosted environments, these are typically injected as secrets/variables.

Expects GOOGLE_API_KEY for Gemini access, optionally PUSHOVER_TOKEN and PUSHOVER_USER for lightweight push notifications.

Tools and notifications
push(text): Sends a minimal notification via the Pushover API; exceptions are swallowed so missing Pushover config doesn’t break the app.

record_user_details(email, name, notes): Uses push() and returns a JSON-serializable result; exposed to the model as a callable tool so it can capture a visitor’s email/notes.

record_unknown_question(question): Uses push() to log any question the model cannot answer, enabling follow-up or dataset improvements.

tools: Defines the JSON schemas for the two functions, enabling function/tool-calling in the chat loop.

