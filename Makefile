clean:
	find . | grep -E "(__pycache__|\.pyc|\.pyo)" | xargs rm -rf; rm -rf htmlcov; rm actual.*; rm .coverage

tree:
	tree -I 'docs|bin|lib|venv|htmlcov|.coverage'

tests:
	python -m unittest discover -v

unit:
	python -m unittest discover -v test/unit

integration:
	python -m unittest discover -v test/integration

coverage:
	coverage run -m unittest discover
	coverage html --omit="venv/*"
