export PYTHONPATH=$PYTHONPATH:.

TEST_CMD=python -m pytest .
TEST_DEBUG_CMD=python -m pytest --cov=$(PROJECT_HOME) -x -vv --lf $(filter-out $@,$(MAKECMDGOALS))
CHECK_CMD=sh -c "pre-commit run isort -a && \
			pre-commit run autopep8 -a && \
			pre-commit run flake8 -a && \
			pre-commit run mypy -a && \
			pre-commit run bandit -a && \
			pre-commit run xenon -a && \
			pre-commit run bandit && \
			pre-commit run yamllint -a"

run:
	celery -A src.main.app worker -B -l info -Q common

test:
	$(TEST_CMD)

check:
	$(CHECK_CMD)

pip_upgrade:
	pip install --upgrade pip setuptools pip-tools

pip_install: pip_upgrade
	pip install -r requirements.txt

install: pip_install
	pre-commit install

docker-run:
	docker-compose up web

docker-image:
	docker-compose build web
