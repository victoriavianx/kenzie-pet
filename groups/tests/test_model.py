from django.test import TestCase
from groups.models import Group
from animals.models import Animal

class GroupTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.group_1_data = {
            "name": "cão", "scientific_name": "canis familiaris"
        }

        cls.group_1 = Group.objects.create(**cls.group_1_data)

    def test_group_fields(self):
        print("Execute test_group_fields")
        
        self.assertEqual(self.group_1.name, self.group_1_data["name"])
        self.assertEqual(self.group_1.scientific_name, self.group_1_data["scientific_name"])

    def test_scientific_name_max_length(self):
        print("Execute test_scientific_name_max_length")

        expected_max_length = 50
        result_max_length = self.group_1._meta.get_field("scientific_name").max_length
        message = "Verifique o max_length do campo 'scientific_name'"

        self.assertEqual(result_max_length, expected_max_length, message)