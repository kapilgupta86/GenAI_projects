#!/usr/bin/env python3
import sys
import os
sys.path.append('./src')

def test_personal_info():
    """Test the exact logic from our crew.py"""
    folder_path = os.path.abspath("./knowledge")
    
    # Try to read from user_preference.txt first
    try:
        pref_file = os.path.join(folder_path, "user_preference.txt")
        print(f"Looking for: {pref_file}")
        print(f"File exists: {os.path.exists(pref_file)}")
        
        if os.path.exists(pref_file):
            with open(pref_file, "r", encoding="utf-8") as f:
                content = f.read()
                print(f"File content:\n{content}")
                for line in content.split("\n"):
                    if line.strip().startswith("name:"):
                        name = line.split(":", 1)[1].strip()
                        print(f"Found name: '{name}'")
                        return {"answer": name, "sources": [{"intent": "personal_info", "file": "user_preference.txt"}]}
    except Exception as e:
        print(f"Error reading user_preference.txt: {e}")
    
    # Fallback to hardcoded
    return {"answer": "Kapil", "sources": [{"intent": "personal_info", "source": "fallback"}]}

if __name__ == "__main__":
    result = test_personal_info()
    print(f"Result: {result}")
