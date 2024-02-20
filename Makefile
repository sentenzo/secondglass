PACKAGE_NAME = secondglass
PROJECT_DIR = secondglass

CODE = ${PROJECT_DIR} tests

# https://stackoverflow.com/a/4511164/2493536
ifdef OS # Windows
   PATH_ARG_SEP=;
else
   ifeq ($(shell uname), Linux) # Linux
	  PATH_ARG_SEP=:
   endif
endif

run:
	poetry run python -m ${PROJECT_DIR}

init:
	poetry install

lint:
	poetry run isort ${CODE}
	poetry run black ${CODE}
	poetry run flake8 ${CODE} --count --show-source --statistics
	poetry run mypy ${CODE}

test:
	poetry run pytest -vsx -m "not slow"

test-all:
	poetry run pytest -vsx

.PHONY: build
build: lint test
	poetry run pyinstaller \
	    --workpath ./build/.pyinstaller/build \
	    --distpath ./build \
	    --specpath ./build/.pyinstaller \
	    --noconsole \
	    --onefile \
	    --name $(PACKAGE_NAME) \
	    --icon ../../$(PACKAGE_NAME)/resources/icons/clock.ico \
		--add-data ../../$(PACKAGE_NAME)/resources/$(PATH_ARG_SEP)./$(PACKAGE_NAME)/resources \
	    --add-data ../../$(PACKAGE_NAME)/progress/TaskbarLib.tlb$(PATH_ARG_SEP)./$(PACKAGE_NAME)/progress \
		$(PACKAGE_NAME)/__main__.py