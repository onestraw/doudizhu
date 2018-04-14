test:
	PYTHONPATH=$PYTHONPATH:./ pytest -s tests/

check:
	flake8 engine/*.py

clean:
	find . -name '*.pyc' -exec rm {} \;
