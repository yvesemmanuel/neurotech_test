

requirements:
	@pip install -r requirements.txt
	@pip install -r ./app/requirements.txt

dev-requirements:
	@pip install -r requirements.dev.txt

lint:
	@pylint app/*.py

testing:
	@cd test & pytest
