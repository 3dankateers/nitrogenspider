##make all runs main.py

PYTHON_LIBS=""

run_main_py:
	PYTHONPATH=${PYTHON_LIBS} python main.py

run_scrape_py:
	PYTHONPATH=${PYTHON_LIBS} python scrape_all.py

scrape: run_scrape_py

all: run_main_py
