clean:
	find . | grep -E "(dist|__pycache__|\.pyc|\.pyo)" | xargs rm -rf; rm -rf htmlcov; rm actual*; rm .coverage

tree:
	tree -I 'docs|bin|lib|venv|htmlcov|.coverage'

tests:
	python -m unittest discover -v

unit:
	python -m unittest discover -v test/test_units

integration:
	python -m unittest discover -v test/test_integration

coverage:
	coverage run -m unittest discover
	coverage html --omit="venv/*"

show_states:
	python scripts/show_states.py
