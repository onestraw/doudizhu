test:
	PYTHONPATH=$PYTHONPATH:./ python -m pytest -s tests/ --showlocals

check:
	flake8 --ignore=E501,F401,E128,E402,E731,F821 doudizhu tests

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
