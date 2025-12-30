import re

def parse_problem(text):
    text = text.strip()

    topic = "algebra"
    if any(k in text.lower() for k in ["derivative", "limit", "maximize", "minimize"]):
        topic = "calculus"
    elif any(k in text.lower() for k in ["probability", "dice", "coin"]):
        topic = "probability"
    elif any(k in text.lower() for k in ["matrix", "determinant"]):
        topic = "linear_algebra"

    return {
        "problem_text": text,
        "topic": topic
    }
