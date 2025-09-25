#!/usr/bin/env python3
import sys
sys.path.append('./src')

from knowledge_bot.crew import KnowledgeBotCrew, _detect_intent

def test_intent():
    queries = [
        "who am i?",
        "what is my name?", 
        "list .py and .md files",
        "show me projects in folder"
    ]
    
    for q in queries:
        intent = _detect_intent(q)
        print(f"Query: '{q}' -> Intent: {intent}")

def test_crew_task():
    crew = KnowledgeBotCrew()
    task = crew.query_task()
    
    # Test the personal_info directly
    result = task.function({"query": "who am i?"})
    print(f"Direct task result: {result}")

if __name__ == "__main__":
    print("Testing intent detection:")
    test_intent()
    print("\nTesting crew task directly:")
    test_crew_task()
