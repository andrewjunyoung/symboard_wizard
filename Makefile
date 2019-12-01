clean:
	find . | grep -E "(__pycache__|\.pyc|\.pyo)" | xargs rm -rf
	rm -rf htmlcov
	rm .coverage

tree:
	tree -I 'docs|bin|lib|venv|htmlcov|.coverage'

unittest:
	python -m unittest discover

coverage:
	coverage run -m unittest discover
	coverage html --omit="venv/*"
