.PHONY: starter test validate
starter:
	python tools/starter_build.py
validate:
	python tools/discovery_index.py examples/discovery.json --output /tmp/discovery-index.json
test:
	python -m unittest discover -s tests -v
