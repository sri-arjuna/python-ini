@echo off

echo Creating package build data...
py -m build

echo Preparing upload...
py -m twine upload --repository pypi dist/*

echo Package and upload completed.
pause
