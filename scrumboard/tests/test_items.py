from django.test import TestCase

from scrumboard.models import Item


class ItemTestCase(TestCase):
    def test_item_name(self):
        Item.objects.create()