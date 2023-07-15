include .env

install:
	pip3 install -r requirements.txt

installdev:
	pip3 install -r requirements-dev.txt

postinstall:
	pre-commit run --all-files

test:
	python3 -m unittest discover tests

publish:
	poetry publish --build --username ${POETRY_USERNAME} --password ${POETRY_PASSWORD}

toml:
	actualversion=$(shell python3 -c 'import tomllib; print(tomllib.load(open("pyproject.toml", "rb"))["tool"]["poetry"]["version"])'); \
	if [ $$actualversion == 0.2.3 ]; then  echo success!; fi; \
	echo $$actualversion; \
	pip3 install --use-deprecated=legacy-resolver nsdpy== 2>&1 >/dev/null | grep -c 0.2.3; \