clean:
	find . | grep -E "(__pycache__|\.pyc|\.pyo)" | xargs rm -rf

tree:
	tree -I 'docs|bin|lib|venv'

unittest:
	python -m unittest discover

coverage:
	coverage run -m unittest discover
	coverage html --omit="venv/*"
