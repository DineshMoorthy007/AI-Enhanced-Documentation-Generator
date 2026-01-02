import re

# Regex patterns for JS/TS
FUNCTION_PATTERN = re.compile(
    r"""
    function\s+([a-zA-Z0-9_]+)\s*\( |           # function foo(...)
    const\s+([a-zA-Z0-9_]+)\s*=\s*\( |           # const foo = (...)
    let\s+([a-zA-Z0-9_]+)\s*=\s*\( |             # let foo = (...)
    var\s+([a-zA-Z0-9_]+)\s*=\s*\( |             # var foo = (...)
    ([a-zA-Z0-9_]+)\s*=\s*\(.*\)\s*=>             # foo = (...) =>
    """,
    re.VERBOSE,
)

CLASS_PATTERN = re.compile(
    r"class\s+([a-zA-Z0-9_]+)"
)


def extract_functions_and_classes(code: str):
    """
    Extract function and class names from JS/TS code using regex.
    """
    functions = set()
    classes = set()

    for match in FUNCTION_PATTERN.finditer(code):
        for group in match.groups():
            if group:
                functions.add(group)

    for match in CLASS_PATTERN.finditer(code):
        classes.add(match.group(1))

    return {
        "functions": sorted(functions),
        "classes": sorted(classes),
    }
