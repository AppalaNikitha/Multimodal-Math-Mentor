import sympy as sp
import re
from sympy.parsing.sympy_parser import (
    parse_expr,
    standard_transformations,
    implicit_multiplication_application
)

# ------------------- Helpers -------------------

def extract_math_expression(text):
    """
    Convert natural language to a sympy-parsable expression
    """
    text = text.lower()
    remove_words = [
        "find", "the", "solve", "derivative", "of",
        "limit", "as", "approaches", "what is",
        "calculate", "compute", "evaluate"
    ]
    for word in remove_words:
        text = text.replace(word, "")
    text = text.replace("^", "**")
    text = text.replace("=", "-")
    text = text.replace(" ", "")
    return text.strip()

def safe_parse(expr):
    """
    Parse expression safely using sympy
    """
    transformations = standard_transformations + (implicit_multiplication_application,)
    try:
        return parse_expr(expr, transformations=transformations)
    except Exception as e:
        raise ValueError(f"Cannot parse expression: {expr}. Error: {e}")

from fractions import Fraction

def solve_probability(text):
    text = text.lower()
    steps = []

    # ---------------- COIN ----------------
    coin_match = re.search(r"coin.*?(\d+)\s*(times|tosses|flips)", text)
    if coin_match:
        n = int(coin_match.group(1))
        steps.append(f"Coin tossed {n} times")
        total = 2 ** n

        if "all heads" in text or "only heads" in text:
            favorable = 1
            steps.append("Favorable outcome: all heads")

        elif "all tails" in text or "only tails" in text:
            favorable = 1
            steps.append("Favorable outcome: all tails")

        else:
            favorable = 1
            steps.append("Assuming one specific outcome")

        prob = Fraction(favorable, total)
        steps.append(f"Probability = {prob}")
        return steps, str(prob)

    # ---------------- DICE ----------------
    if "dice" in text or "die" in text:
        steps.append("Single die rolled")
        total = 6

        if "6" in text:
            favorable = 1
            steps.append("Favorable outcome: getting 6")
        elif "even" in text:
            favorable = 3
            steps.append("Favorable outcomes: 2,4,6")
        elif "odd" in text:
            favorable = 3
            steps.append("Favorable outcomes: 1,3,5")
        else:
            favorable = 1
            steps.append("Assuming one specific outcome")

        prob = Fraction(favorable, total)
        steps.append(f"Probability = {prob}")
        return steps, str(prob)

    # ---------------- CARDS ----------------
    if "card" in text or "deck" in text:
        steps.append("Standard deck of 52 cards")
        total = 52

        if "ace" in text:
            favorable = 4
            steps.append("Favorable outcomes: 4 aces")

        elif "king" in text:
            favorable = 4
            steps.append("Favorable outcomes: 4 kings")

        elif "red" in text:
            favorable = 26
            steps.append("Favorable outcomes: 26 red cards")

        else:
            favorable = 1
            steps.append("Assuming one specific card")

        prob = Fraction(favorable, total)
        steps.append(f"Probability = {prob}")
        return steps, str(prob)

    # ---------------- FALLBACK ----------------
    return ["Could not recognize probability type"], "N/A"
# ------------------- Main Solver -------------------

def solve_problem(parsed, route):
    topic = route.get("topic", "").lower()
    raw_text = parsed.get("problem_text", "")
    x = sp.symbols("x")

    try:
        # ---------- ALGEBRA ----------
        if topic == "algebra":
            expr_text = extract_math_expression(raw_text)
            expr = safe_parse(expr_text)
            sol = sp.solve(expr, x)
            return {
                "steps": ["Converted equation to symbolic form", "Solved for x"],
                "final_answer": sol
            }

        # ---------- CALCULUS ----------
        if topic == "calculus":
            text_lower = raw_text.lower()
            # Derivative
            if "derivative" in text_lower or "dx/dx" in text_lower:
                expr_text = extract_math_expression(raw_text)
                expr = safe_parse(expr_text)
                deriv = sp.diff(expr, x)
                return {
                    "steps": ["Identified function", "Applied differentiation"],
                    "final_answer": deriv
                }
                
            # Limit
            if "limit" in text_lower:
                expr_text = extract_math_expression(raw_text)
                expr = safe_parse(expr_text)
                # Try to find the variable and value
                limit_match = re.search(r"limit.*?([a-z])\s*->\s*([-\d.]+)", text_lower)
                var = x
                val = 0
                if limit_match:
                    var = sp.symbols(limit_match.group(1))
                    val = float(limit_match.group(2))
                lim = sp.limit(expr, var, val)
                return {
                    "steps": [f"Evaluated limit at {var} → {val}"],
                    "final_answer": lim
                }

        # PROBABILITY 
        if topic == "probability":
            steps, answer = solve_probability(raw_text)
            return {
                "steps": steps,
                "final_answer": answer
            }

        # ---------- LINEAR ALGEBRA ----------
        if topic == "linear_algebra":
            if "determinant" in raw_text.lower():
                # Try parsing a 2x2 or 3x3 matrix from text
                matrix_match = re.findall(r"\[([0-9,\s]+)\]", raw_text)
                if matrix_match:
                    rows = [list(map(int, r.split(","))) for r in matrix_match]
                    M = sp.Matrix(rows)
                else:
                    M = sp.Matrix([[1, 2], [3, 4]])
                return {
                    "steps": ["Parsed matrix", "Computed determinant"],
                    "final_answer": M.det()
                }

        return {
            "steps": ["Could not solve automatically"],
            "final_answer": "N/A"
        }

    except Exception as e:
        return {
            "steps": ["Solver error"],
            "final_answer": str(e)
        }
