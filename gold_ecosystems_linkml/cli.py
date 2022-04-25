import click
import pandas as pd
from linkml_runtime.dumpers import yaml_dumper

from gold_ecosystems_linkml.linkml import generate_schema_from_dataframe


@click.command()
@click.argument('filename', type=click.File('rb'))
def generate_linkml(filename):
    """Read FILENAME, an XLSX file defining valid Gold Ecosystem Classification paths, and
    generate a corresponding LinkML model"""

    df = pd.read_excel(filename, index_col=0)
    schema = generate_schema_from_dataframe(df)
    click.echo(yaml_dumper.dumps(schema))


if __name__ == '__main__':
    generate_linkml()
