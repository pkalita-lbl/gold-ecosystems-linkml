from collections import defaultdict

import pandas as pd
from linkml_runtime.utils.formatutils import camelcase, underscore
from linkml_runtime.utils.schemaview import (ClassDefinition, ClassExpression,
                                             ClassRule, EnumDefinition,
                                             SchemaDefinition, SchemaView,
                                             SlotDefinition, SlotExpression)


def column_to_slot_name(column):
    """Generate a slot name (snake_cake) from a DataFrame column name"""
    return underscore(column.lower())


def column_to_enum_name(column):
    """Generate an enum name (CamelCase) from a DataFrame column name"""
    return camelcase(column.lower())


def generate_schema_from_dataframe(df: pd.DataFrame) -> SchemaDefinition:
    """Generate a LinkML SchemaDefinition object from a DataFrame
    
    The input DataFrame should represent the GOLD Ecosystem Classification 
    specification spreadsheet which enumerates all of the valid 5-part paths,
    one part per column. There is one class generated (Path). The Path class
    will have five slots with name corresponding to the column headers. Five
    enums will also be generated based on the unique values in each column. They
    will serve as the range of each respective slot. Finally, each row of the
    spreadsheet will be used to generate rules on the Path class which constrain
    the valid combinations of slot values.
    """

    # Set up basic schema definition and view
    schema_def = SchemaDefinition(
        id="http://example.com/gold-ecosystem",
        name="gold-ecosystem-classification",
        title="GOLD Ecosystem Classification"
    )
    schema_view = SchemaView(schema=schema_def)
    
    # For each column create a slot and an enum that represents all
    # of the unique values in that column. Not all combinations of 
    # enum values represent valid paths. Valid combinations are 
    # enforced by the rules defined next.
    slots = []
    for column in df:
        slot = SlotDefinition(name=column_to_slot_name(column))
        slots.append(slot.name)
        schema_view.add_slot(slot)

        col_enum = EnumDefinition(
            name=column_to_enum_name(column),
            permissible_values=list(df[column].unique()),
        )
        slot.range = col_enum.name
        schema_view.add_enum(col_enum)

    # Build a dict that maps partial paths to a sets of terms that
    # are valid values for the next part of the path
    partial_path_completions = defaultdict(set)
    for _, row in df.iterrows():
        key = ()
        for _, value in row.iteritems():
            partial_path_completions[key].add(value)
            key = key + (value,)
    
    # From the dict of partial paths and completions build a set of
    # rules where the partial path forms the precondition and the 
    # postcondition is `exactly_one_of` the possible completions
    rules = []
    for partial_path, completions in partial_path_completions.items():
        if len(partial_path) == 0:
            continue

        preconditions = {}
        for idx, value in enumerate(partial_path):
            precondintion_column = column_to_slot_name(df.columns[idx])
            preconditions[precondintion_column] = SlotExpression(equals_string=value)

        postcondition_column = column_to_slot_name(df.columns[len(partial_path)])
        postcondition = {
            postcondition_column: SlotExpression(
                exactly_one_of=[SlotExpression(equals_string=c) for c in sorted(completions)]
            )
        }

        rule = ClassRule(
            preconditions=ClassExpression(slot_conditions=preconditions),
            postconditions=ClassExpression(slot_conditions=postcondition)
        )
        rules.append(rule)

    # Create the Path class
    path = ClassDefinition(name='Path', rules=rules, slots=slots)
    schema_view.add_class(path)

    return schema_def
