test:
	PYTHONPATH=$PYTHONPATH:./ pytest -s tests/

check:
	flake8 doudizhu.py card.py

clean:
	find . -name '*.pyc' -exec rm {} \;
