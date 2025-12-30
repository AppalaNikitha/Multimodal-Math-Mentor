def verify_solution(solution):
    if solution["final_answer"] in ["N/A", None]:
        return {"valid": False}
    return {"valid": True}
