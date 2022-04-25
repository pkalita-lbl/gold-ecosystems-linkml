from typing import List
import pandas as pd
import unittest

from linkml_runtime.utils.schemaview import SchemaView, EnumDefinition

from gold_ecosystems_linkml.linkml import generate_schema_from_dataframe


class TestGenerateLinkMLFromDataFrame(unittest.TestCase):
    def setUp(self):
        data = {
            'ECOSYSTEM':          ['a1', 'a1', 'a2', 'a2', 'a3'],
            'ECOSYSTEM CATEGORY': ['b1', 'b2', 'b3', 'b3', 'b4'],
            'ECOSYSTEM TYPE':     ['c1', 'c2', 'c3', 'c3', 'c4'],
            'ECOSYSTEM SUBTYPE':  ['d1', 'd2', 'd3', 'd2', 'd4'],
            'SPECIFIC ECOSYSTEM': ['e1', 'e2', 'e3', 'e4', 'e5']
        }
        df = pd.DataFrame(data=data)
        self.schema = generate_schema_from_dataframe(df)
        self.schema_view = SchemaView(self.schema)


    def test_schema_title(self):
        self.assertEqual(self.schema.title, "GOLD Ecosystem Classification")

    
    def test_path_class_exists(self):
        self.assertIn('Path', self.schema_view.all_classes())


    def test_slots_exist(self):
        slots = self.schema_view.all_slots()
        self.assertIn('ecosystem', slots)
        self.assertIn('ecosystem_category', slots)
        self.assertIn('ecosystem_type', slots)
        self.assertIn('ecosystem_subtype', slots)
        self.assertIn('specific_ecosystem', slots)


    def test_slots_exist_on_path(self):
        path_class = self.schema_view.get_class('Path')
        self.assertIsNotNone(path_class)
        self.assertIn('ecosystem', path_class.slots)
        self.assertIn('ecosystem_category', path_class.slots)
        self.assertIn('ecosystem_type', path_class.slots)
        self.assertIn('ecosystem_subtype', path_class.slots)
        self.assertIn('specific_ecosystem', path_class.slots)


    def test_enums_have_correct_values(self):
        enums = self.schema_view.all_enums()
        self.assertIn('Ecosystem', enums)
        self.assertIn('EcosystemCategory', enums)
        self.assertIn('EcosystemType', enums)
        self.assertIn('EcosystemSubtype', enums)
        self.assertIn('SpecificEcosystem', enums)

        self.assertEnumPermissibleValues(['a1', 'a2', 'a3'], enums['Ecosystem'])
        self.assertEnumPermissibleValues(['b1', 'b2', 'b3', 'b4'], enums['EcosystemCategory'])
        self.assertEnumPermissibleValues(['c1', 'c2', 'c3', 'c4'], enums['EcosystemType'])
        self.assertEnumPermissibleValues(['d1', 'd2', 'd3', 'd4'], enums['EcosystemSubtype'])
        self.assertEnumPermissibleValues(['e1', 'e2', 'e3', 'e4', 'e5'], enums['SpecificEcosystem'])


    def test_slot_ranges(self):
        slots = self.schema_view.all_slots()
        self.assertEqual(slots['ecosystem'].range, 'Ecosystem')
        self.assertEqual(slots['ecosystem_category'].range, 'EcosystemCategory')
        self.assertEqual(slots['ecosystem_type'].range, 'EcosystemType')
        self.assertEqual(slots['ecosystem_subtype'].range, 'EcosystemSubtype')
        self.assertEqual(slots['specific_ecosystem'].range, 'SpecificEcosystem')


    def test_class_has_rules(self):
        self.assertGreater(len(self.schema_view.get_class('Path').rules), 0)


    def assertEnumPermissibleValues(self, values: List[str], enum: EnumDefinition):
        permissible_value_names = [val for val in enum.permissible_values]
        self.assertEqual(values, permissible_value_names)


if __name__ == '__main__':
    unittest.main()
