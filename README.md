pipenv lock -r > requirements.txt
pipenv run pip install -r <(pipenv lock -r) --target dist/
