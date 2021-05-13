import os
import subprocess

os.system("rm -rf dist")
os.system("rm -rf bundle.zip")
os.system("pip install -r requirements.txt --target dist/")
os.system("rm -rf ./dist/__pycache__")
os.system("cp -r src/*.py dist/")
os.system("cd dist && zip -r ../bundle.zip .")
