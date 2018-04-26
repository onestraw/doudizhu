test:
	PYTHONPATH=$PYTHONPATH:./ python2 -m pytest -s tests/ --showlocals
	PYTHONPATH=$PYTHONPATH:./ python3 -m pytest -s tests/ --showlocals

check:
	flake8 doudizhu/*.py

clean:
	find . -name '*.pyc' -exec rm {} \;

install:
	python2 setup.py install
	python3 setup.py install

dry_publish:
	rm -rf dist/
	python setup.py sdist

publish: dry_publish
	twine upload -s dist/*
