import os
import io
import tempfile
from typing import List, Dict, Any, Tuple

import pandas as pd
from PyPDF2 import PdfReader
from docx import Document as DocxDocument
from git import Repo

# Google Drive
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

SUPPORTED_LOCAL = [".pdf", ".docx", ".txt", ".csv", ".xlsx"]
SUPPORTED_GH = [".py", ".md", ".txt"]

def _read_pdf(path: str) -> str:
    text = []
    with open(path, "rb") as f:
        reader = PdfReader(f)
        for page in reader.pages:
            text.append(page.extract_text() or "")
    return "\n".join(text)

def _read_docx(path: str) -> str:
    doc = DocxDocument(path)
    return "\n".join([p.text for p in doc.paragraphs])

def _read_txt(path: str) -> str:
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()

def _read_csv(path: str) -> str:
    df = pd.read_csv(path)
    return df.to_csv(index=False)

def _read_xlsx(path: str) -> str:
    df = pd.read_excel(path)
    return df.to_csv(index=False)

def LocalFileReader(folder: str) -> List[Dict[str, Any]]:
    docs: List[Dict[str, Any]] = []
    if not folder or not os.path.isdir(folder):
        return docs
    for root, _, files in os.walk(folder):
        for fn in files:
            ext = os.path.splitext(fn)[1].lower()
            if ext not in SUPPORTED_LOCAL:
                continue
            full = os.path.join(root, fn)
            try:
                if ext == ".pdf":
                    content = _read_pdf(full)
                elif ext == ".docx":
                    content = _read_docx(full)
                elif ext == ".txt":
                    content = _read_txt(full)
                elif ext == ".csv":
                    content = _read_csv(full)
                elif ext == ".xlsx":
                    content = _read_xlsx(full)
                else:
                    continue
                if content.strip():
                    docs.append({"content": content, "metadata": {"source": "local", "path": full}})
            except Exception as e:
                docs.append({"content": "", "metadata": {"source": "local", "path": full, "error": str(e)}})
    return docs

def GitHubRepoCloner(repo_url: str) -> Tuple[str, List[Dict[str, Any]]]:
    if not repo_url:
        return "", []
    tmpdir = tempfile.mkdtemp(prefix="kb_gh_")
    Repo.clone_from(repo_url, tmpdir)
    docs: List[Dict[str, Any]] = []
    for root, _, files in os.walk(tmpdir):
        for fn in files:
            ext = os.path.splitext(fn)[1].lower()
            if ext not in SUPPORTED_GH:
                continue
            full = os.path.join(root, fn)
            try:
                content = _read_txt(full)
                if content.strip():
                    docs.append({"content": content, "metadata": {"source": "github", "path": full}})
            except Exception as e:
                docs.append({"content": "", "metadata": {"source": "github", "path": full, "error": str(e)}})
    return tmpdir, docs

def GoogleDriveReader(folder_id: str = None) -> List[Dict[str, Any]]:
    # OAuth via browser; credentials cached locally by PyDrive2
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    drive = GoogleDrive(gauth)

    q = "'root' in parents and trashed=false" if not folder_id else f"'{folder_id}' in parents and trashed=false"
    file_list = drive.ListFile({'q': q}).GetList()

    docs: List[Dict[str, Any]] = []
    for f in file_list:
        name = f.get('title') or f.get('name')
        fid = f['id']
        if not name:
            continue
        ext = os.path.splitext(name)[1].lower()
        if ext not in SUPPORTED_LOCAL and ext not in [".md", ".py"]:
            continue
        try:
            # Download to cwd, reuse local readers
            f.GetContentFile(name)
            path = os.path.abspath(name)
            if ext == ".pdf":
                content = _read_pdf(path)
            elif ext == ".docx":
                content = _read_docx(path)
            elif ext in [".txt", ".md", ".py"]:
                content = _read_txt(path)
            elif ext == ".csv":
                content = _read_csv(path)
            elif ext == ".xlsx":
                content = _read_xlsx(path)
            else:
                content = ""
            if content.strip():
                docs.append({"content": content, "metadata": {"source": "gdrive", "name": name, "id": fid}})
        except Exception as e:
            docs.append({"content": "", "metadata": {"source": "gdrive", "id": fid, "error": str(e)}})
        finally:
            if os.path.exists(name):
                try:
                    os.remove(name)
                except Exception:
                    pass
    return docs

