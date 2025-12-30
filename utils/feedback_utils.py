import json
from datetime import datetime

FEEDBACK_FILE = "feedback_log.jsonl"

def log_feedback(question, solution, feedback, comment=None):
    """
    Logs user feedback for a math problem solution.
    
    Parameters:
    - question: str, the math problem text
    - solution: any, the solver output (can be dict, list, int, float, etc.)
    - feedback: str, "✅" for correct or "❌" for incorrect
    - comment: str, optional comment or correction if incorrect
    """

    # Create a dictionary for logging
    data = {
        "timestamp": datetime.now().isoformat(),
        "question": question,
        "solution": solution,
        "feedback": feedback,
        "comment": comment
    }

    # Serialize using default=str to handle non-serializable objects
    try:
        with open(FEEDBACK_FILE, "a") as f:
            f.write(json.dumps(data, default=str) + "\n")
    except TypeError as e:
        print("Error logging feedback:", e)
