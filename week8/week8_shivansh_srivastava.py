"""
agent.py — Simple Query Router Agent
=====================================

A single-function agent(query) that:
  - Routes "calculate ..." queries to a calculator tool
  - Routes "keywords ..." queries to a keyword extraction tool
  - Falls back to a general text handler for everything else
  - Returns a clean JSON-shaped dict: {"type": ..., "result": ...}
  - Handles malformed input safely (never raises out to the caller)

Run directly for automated tests + an interactive prompt:
    python agent.py
"""

import re
import json


# ---------------------------------------------------------------------------
# Tool 1: Calculator
# ---------------------------------------------------------------------------
def calculator(expression: str):
    """Safely evaluate a basic arithmetic expression."""
    expression = expression.strip()
    if not expression:
        raise ValueError("No expression found to calculate")
    if not re.fullmatch(r"[0-9+\-*/(). ]+", expression):
        raise ValueError(f"Unsafe or invalid characters in expression: '{expression}'")
    try:
        return eval(expression)  # safe: input restricted to digits/operators above
    except ZeroDivisionError:
        raise ValueError("Division by zero")
    except SyntaxError:
        raise ValueError(f"Malformed expression: '{expression}'")


# ---------------------------------------------------------------------------
# Tool 2: Keyword extractor
# ---------------------------------------------------------------------------
def extract_keywords(text: str):
    """Naive keyword extraction: unique words longer than 4 characters."""
    text = text.strip()
    if not text:
        raise ValueError("No text found to extract keywords from")
    words = re.findall(r"[a-zA-Z]+", text)
    keywords = sorted(set(w.lower() for w in words if len(w) > 4))
    return keywords


# ---------------------------------------------------------------------------
# Fallback: general response handler
# ---------------------------------------------------------------------------
def general_response(query: str):
    return f"Here is a general answer regarding: '{query.strip()}'"


# ---------------------------------------------------------------------------
# The agent: conditional routing on lowercase query text
# ---------------------------------------------------------------------------
def agent(query) -> dict:
    """
    Route a query to the correct tool and return a JSON-shaped dict:
        {"type": "calculation" | "keywords" | "general" | "error", "result": ...}
    Never raises — all failures are caught and returned as an "error" type.
    """
    try:
        if not isinstance(query, str) or not query.strip():
            return {"type": "error", "result": "Query must be a non-empty string"}

        lowered = query.lower()

        # --- Route 1: calculation ---
        if "calculate" in lowered:
            match = re.search(r"[0-9][0-9+\-*/(). ]*[0-9)]", query)
            if not match:
                return {"type": "error", "result": "No valid math expression found in query"}
            try:
                value = calculator(match.group())
            except ValueError as e:
                return {"type": "error", "result": str(e)}
            return {"type": "calculation", "result": value}

        # --- Route 2: keywords ---
        if "keywords" in lowered:
            try:
                kws = extract_keywords(query)
            except ValueError as e:
                return {"type": "error", "result": str(e)}
            return {"type": "keywords", "result": kws}

        # --- Route 3: fallback ---
        return {"type": "general", "result": general_response(query)}

    except Exception as e:
        # Catch-all safety net for anything unexpected
        return {"type": "error", "result": f"Unhandled exception: {e}"}


# ---------------------------------------------------------------------------
# Automated validation checks
# ---------------------------------------------------------------------------
TEST_QUERIES = [
    "Please calculate 12 * (3 + 4)",
    "calculate 10 / 0",                     # division by zero -> error
    "calculate abc + def",                  # no valid expression -> error
    "Extract keywords from this sentence about artificial intelligence",
    "keywords",                              # empty text -> error
    "Tell me a joke",                        # general fallback
    "",                                      # empty query -> error
    123,                                      # bad type -> error
]


def run_validation_tests():
    print("=" * 60)
    print("AUTOMATED VALIDATION CHECKS")
    print("=" * 60)
    passed, failed = 0, 0
    for q in TEST_QUERIES:
        result = agent(q)
        ok = isinstance(result, dict) and "type" in result and "result" in result
        status = "PASS" if ok else "FAIL"
        passed += ok
        failed += not ok
        print(f"[{status}] query={q!r}")
        print(f"       -> {json.dumps(result, default=str)}")
    print("-" * 60)
    print(f"Validation summary: {passed} passed, {failed} failed out of {len(TEST_QUERIES)}")
    print()


# ---------------------------------------------------------------------------
# Interactive loop
# ---------------------------------------------------------------------------
def interactive_loop():
    print("=" * 60)
    print("INTERACTIVE AGENT (type 'exit' or 'quit' to stop)")
    print("=" * 60)
    while True:
        try:
            user_input = input("Query> ")
        except (EOFError, KeyboardInterrupt):
            print("\nExiting.")
            break
        if user_input.strip().lower() in ("exit", "quit"):
            print("Exiting.")
            break
        result = agent(user_input)
        print(json.dumps(result, default=str))


if __name__ == "__main__":
    run_validation_tests()
    interactive_loop()
