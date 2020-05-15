from unittest import TestCase
from versy import versy
import impall


class TestImpAll(impall.ImpAllTest):
    pass


class TestVersy(TestCase):
    def test_simple(self):
        assert versy
