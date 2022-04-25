.PHONY: test linkml clean

test:
	poetry run python -m unittest -v

linkml: resources/gold_paths.xlsx
	poetry run generate-linkml $<

resources:
	mkdir $@

resources/gold_paths.xlsx: resources
	curl -L -o $@ "https://gold.jgi.doe.gov/download?mode=ecosystempaths"

clean:
	rm -rf resources
