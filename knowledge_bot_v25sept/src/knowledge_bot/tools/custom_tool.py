# src/knowledge_bot/tools/custom_tool.py
import os
from typing import List, Dict, Any

# Optional imports with graceful fallbacks
try:
    import pdfplumber
    HAS_PDFPLUMBER = True
except Exception:
    HAS_PDFPLUMBER = False

try:
    import PyPDF2
    HAS_PYPDF2 = True
except Exception:
    HAS_PYPDF2 = False

try:
    import docx
    HAS_DOCX = True
except Exception:
    HAS_DOCX = False

try:
    import pandas as pd
    HAS_PANDAS = True
except Exception:
    HAS_PANDAS = False

SUPPORTED_LOCAL = {".pdf", ".docx", ".txt", ".csv", ".xlsx", ".md"}

def _read_pdf_per_page(path: str) -> List[Dict[str, Any]]:
    """
    Return a list of page-level documents: [{"content": str, "metadata": {...}}].
    Prefers pdfplumber; falls back to PyPDF2 if unavailable.
    """
    docs: List[Dict[str, Any]] = []
    name = os.path.basename(path)

    # Preferred: pdfplumber
    if HAS_PDFPLUMBER:
        try:
            with pdfplumber.open(path) as pdf:
                for i, page in enumerate(pdf.pages, start=1):
                    try:
                        text = page.extract_text() or ""
                    except Exception:
                        text = ""
                    if text.strip():
                        st = os.stat(path)
                        docs.append({
                            "content": text,
                            "metadata": {
                                "source": path,
                                "path": path,
                                "name": name,
                                "type": ".pdf",
                                "size": st.st_size,
                                "last_modified": st.st_mtime,
                                "page": i,
                                "page_count": len(pdf.pages),
                            }
                        })
        except Exception:
            pass

    # Fallback: PyPDF2
    if not docs and HAS_PYPDF2:
        try:
            with open(path, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                for i, page in enumerate(reader.pages, start=1):
                    try:
                        text = page.extract_text() or ""
                    except Exception:
                        text = ""
                    if text.strip():
                        st = os.stat(path)
                        docs.append({
                            "content": text,
                            "metadata": {
                                "source": path,
                                "path": path,
                                "name": name,
                                "type": ".pdf",
                                "size": st.st_size,
                                "last_modified": st.st_mtime,
                                "page": i,
                                "page_count": len(reader.pages),
                            }
                        })
        except Exception:
            pass

    return docs

def _read_docx(path: str) -> str:
    if not HAS_DOCX:
        return ""
    try:
        d = docx.Document(path)
        return "\n".join(p.text for p in d.paragraphs)
    except Exception:
        return ""

def _read_txt(path: str) -> str:
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()
    except Exception:
        return ""

def _read_csv(path: str) -> str:
    if not HAS_PANDAS:
        return _read_txt(path)
    try:
        df = pd.read_csv(path)
        return df.head(1000).to_string(index=False)
    except Exception:
        return ""

def _read_xlsx(path: str) -> str:
    if not HAS_PANDAS:
        return ""
    try:
        df = pd.read_excel(path)
        return df.head(1000).to_string(index=False)
    except Exception:
        return ""

def LocalFileReader(folder: str) -> List[Dict[str, Any]]:
    """
    Read and parse supported files from a local folder with per-page PDFs.
    Returns a list of documents with content and metadata.
    """
    docs: List[Dict[str, Any]] = []
    if not folder or not os.path.isdir(folder):
        return docs

    for root, _, files in os.walk(folder):
        for fn in files:
            ext = os.path.splitext(fn)[1].lower()
            if ext not in SUPPORTED_LOCAL:
                continue
            full_path = os.path.join(root, fn)

            try:
                if ext == ".pdf":
                    docs.extend(_read_pdf_per_page(full_path))
                else:
                    if ext == ".docx":
                        content = _read_docx(full_path)
                    elif ext in {".txt", ".md"}:
                        content = _read_txt(full_path)
                    elif ext == ".csv":
                        content = _read_csv(full_path)
                    elif ext == ".xlsx":
                        content = _read_xlsx(full_path)
                    else:
                        content = ""

                    if content and content.strip():
                        st = os.stat(full_path)
                        docs.append({
                            "content": content,
                            "metadata": {
                                "source": full_path,
                                "path": full_path,
                                "name": fn,
                                "type": ext,
                                "size": st.st_size,
                                "last_modified": st.st_mtime,
                            }
                        })
            except Exception:
                # Skip unreadable file but continue others
                continue

    return docs

def GitHubRepoCloner(repo_url: str) -> tuple[str, List[Dict[str, Any]]]:
    """
    Placeholder for GitHub repository cloning and parsing.
    Returns (repo_name, documents_list). Keep empty for now.
    """
    if not repo_url:
        return "", []
    return "", []

def GoogleDriveReader(folder_id: str) -> List[Dict[str, Any]]:
    """
    Placeholder for Google Drive folder reading.
    Returns list of document dicts. Keep empty for now.
    """
    if not folder_id:
        return []
    return []

