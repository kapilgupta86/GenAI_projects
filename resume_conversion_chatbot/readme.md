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

The provided Python code (app.py) implements a chatbot application using the Gradio framework, designed to act as a personal representative for an individual (Kapil Gupta). Here's a breakdown of its functionality:

Environment Setup:

Loads environment variables (e.g., GOOGLE_API_KEY, PUSHOVER_TOKEN, PUSHOVER_USER) using dotenv.
Configures an OpenAI-compatible client to interact with a Google Generative AI model (e.g., Gemini) via an API endpoint.


File Reading and Corpus Creation:

Reads files (PDF, DOCX, TXT) from a me/ directory using pypdf and python-docx libraries.
Aggregates content from these files into a profile_corpus (up to 600,000 characters) and optionally includes a summary.txt (up to 80,000 characters).
Handles file reading errors gracefully, returning error messages if files cannot be processed.


Tool Integration:

Defines two tools for interaction:

record_user_details: Logs user contact information (email, name, notes) via a Pushover notification.
record_unknown_question: Logs unanswered questions for later review.


These tools are defined in JSON format for use with the AI model's tool-calling capability.


Chatbot Logic (Me class):

Initializes with a system prompt that instructs the AI to act as Kapil Gupta, using the aggregated profile_corpus and summary to answer questions about his career, skills, and experience.
Supports conversational interaction via a Gradio chat interface.
Handles tool calls (e.g., recording user details or unknown questions) by executing the appropriate function and feeding results back into the conversation.
Implements a retry mechanism with a lighter system prompt if the model fails to respond due to context overflow or other issues.


Gradio Interface:

Launches a web-based chat interface using Gradio, where users can interact with the chatbot.
Maintains conversation history and processes user inputs to generate responses.
