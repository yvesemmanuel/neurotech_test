PYTHON_PREFIX="python/lib/python3.8/site-packages"
AWS_REGION="us-west-2"

requirements:
	@pip install -r requirements.txt
	@pip install -r ./app/requirements.txt

dev-requirements:
	@pip install -r requirements.dev.txt

update-requirements:
	@pip freeze > requirements.txt
	@pip install -r requirements.txt

lint:
	@pylint app/*.py

testing:
	@cd test & pytest
