import os

os.system("rm -rf dist")
os.system("rm -rf bundle.zip")
os.system("pipenv run pip install -r <(pipenv lock -r) --target dist/")
# os.system("cp -r .venv/lib/python*/site-packages/ dist/")
os.system("rm -rf ./dist/__pycache__")
# os.system("find ./dist -maxdepth 1 -type f -delete")
os.system("cp -r src/*.py dist/")
os.system("cd dist && zip -r ../bundle.zip .")
