clean:
	find . | grep -E "(__pycache__|\.pyc|\.pyo)" | xargs rm -rf

tree:
	tree -I 'docs|bin|lib|venv'
