install:
	chmod +x ./scripts/install.sh
	./scripts/install.sh

lint:
	. .venv/bin/activate; python -m mypy --strict stock_picks_optimizer/
	. .venv/bin/activate; python -m ruff check stock_picks_optimizer/
	. .venv/bin/activate; python -m djlint --lint --quiet .

format:
	. .venv/bin/activate; python -m ruff format stock_picks_optimizer/
	. .venv/bin/activate; python -m djlint --reformat --quiet .

test:
	. .venv/bin/activate; python -m pytest stock_picks_optimizer \
		--doctest-modules \
		--junitxml=reports/test-results-$(shell cat .python-version).xml

.PHONY: build
build: clean lint test
	python -m build

smoke_test: build
	python -m pip install dist/*.whl --force-reinstall
	stock-picks-optimizer latest
	stock-picks-optimizer web --port 8000 --reload

deploy: install build

ship_it: build
	git push

start:
	python -m stock_picks_optimizer.main web --port 8000 --reload

clean:
	rm -rf dist/ build/ reports/ *.egg-info/ *cache