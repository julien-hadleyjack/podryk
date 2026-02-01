"""
Generates README examples from test functions, keeping docs in sync with tests.
Used by cog (invoked via `cog -r README.md`) or run directly (`python scripts/cog_readme.py`).
"""

import inspect
import sys
import textwrap

# Fall back to print when running outside of cog.
try:
    import cog
except ImportError:
    cog = None

sys.path.insert(0, "src")
sys.path.insert(0, "tests")


def print_example(func):
    """Extract the body of a test function (up to the first assertion) and print it as a fenced code block."""
    # noinspection PyUnresolvedReferences
    output = cog.outl if cog else print

    source = inspect.getsource(func)
    lines = source.splitlines()

    # Skip the function signature, stop before assertions — the rest is the example code.
    start = next(index for index, line in enumerate(lines) if line.strip().startswith("def ")) + 1
    body = []
    for line in lines[start:]:
        if line.strip().startswith("assert "):
            break
        body.append(line)

    output("```python")
    output(textwrap.dedent("\n".join(body)).strip())
    output("```")


if __name__ == "__main__":
    from test_readme import test_full_feed, test_minimal_feed

    print_example(test_minimal_feed)
    print()
    print_example(test_full_feed)
