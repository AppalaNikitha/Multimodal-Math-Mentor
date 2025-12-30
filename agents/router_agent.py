def route_problem(parsed):
    topic = parsed["topic"]

    strategy_map = {
        "algebra": "symbolic_solve",
        "calculus": "differentiate_or_limit",
        "probability": "counting_probability",
        "linear_algebra": "matrix_operations"
    }

    return {
        "topic": topic,
        "strategy": strategy_map.get(topic, "general")
    }
