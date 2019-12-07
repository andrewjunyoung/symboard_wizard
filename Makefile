clean:
	find . | grep -E "(__pycache__|\.pyc|\.pyo)" | xargs rm -rf
	rm -rf htmlcov
	rm actual.*
	rm .coverage

tree:
	tree -I 'docs|bin|lib|venv|htmlcov|.coverage'

unittest:
	python -m unittest discover -v

coverage:
	make clean
	coverage run -m unittest discover
	coverage html --omit="venv/*"
