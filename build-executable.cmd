rem This script creates a single-file executable for the Python Qt application.
pipenv run pyinstaller --noconsole --distpath . --onefile -n "Rotating Stars" --icon icon.ico main_qt.py

