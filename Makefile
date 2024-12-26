install:
	npm ci
	npx playwright install --with-deps

dev:
	npm run dev

test:
	npm test

build: clean
	npm run build

lint:
	npm run lint

format:
	npm run format

start: clean
	npm run start

ship_it: lint build test
	git push

deploy: install lint build test

clean:
	rm -rf dist/