init:
	python3 -m venv venv
install:
	pip install -r requirements.txt
venv-start:
	source venv/bin/activate
venv-stop:
	deactivate
