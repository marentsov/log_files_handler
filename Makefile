test:
		uv run pytest
tests coverage:
		uv run pytest --cov=. --cov-report=term-missing
