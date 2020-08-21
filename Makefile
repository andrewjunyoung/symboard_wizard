clean:
	find . | grep -E "(dist|__pycache__|\.pyc|\.pyo)" | xargs rm -rf; rm -rf htmlcov; rm actual*; rm .coverage

tree:
	tree -I 'docs|bin|lib|venv|htmlcov|.coverage'

tests:
	nosetests -v

unit:
	nosetests -v test/units

integration:
	nosetests -v test/integration

coverage:
	nosetests -v --with-coverage --cover-package=symboard --cover-erase
	coverage html --omit="venv/*"

show_states:
	python scripts/show_states.py
