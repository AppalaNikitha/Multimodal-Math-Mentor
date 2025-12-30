def explain_solution(parsed, solution):
    explanation = []
    explanation.append("We first understand what is being asked.")
    explanation.extend(solution["steps"])
    explanation.append(f"Final Answer: {solution['final_answer']}")
    return explanation
