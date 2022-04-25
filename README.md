# gold-ecosystems-linkml

A script to generate a LinkML model describing valid [GOLD Ecosystem Classification](https://gold.jgi.doe.gov/ecosystem_classification) paths.

## Setup

Install project dependencies through [Poetry](https://python-poetry.org/):

```shell
poetry install
```

## Running

The pipeline of downloading the GOLD Ecosystem Classification specification spreadsheet and transforming it into a LinkML model is automated through the `Makefile` target `linkml`. By default, this sends the results to `stdout`; redirect it as necessary.

```shell
make linkml > gold.yaml
```

## Testing

To run unit tests:

```shell
make test
```