---
applyTo: "**/*.py,**/pyproject.toml,**/requirements*.txt"
---
# Python Instructions

- Prefer explicit types at public boundaries.
- Separate transport/framework code from domain behavior.
- Do not perform blocking I/O on an async event loop.
- Validate external input at the boundary.
- Keep dependency sets minimal and pinned through the adopting project's approved process.
- Add tests for changed behavior and failure paths.
- Apply the `python-fastapi` skill for FastAPI-specific design and review.
