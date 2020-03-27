# test/test_suite.py

# noinspection PyUnresolvedReferences
import pytest
from sqlalchemy.testing.suite import *


class CTETest(CTETest):
    @pytest.mark.skip(reason="ctes not allowed in insert statements on db2 for iseries")
    def test_insert_from_select_round_trip(self):
        super().test_insert_from_select_round_trip()


class ComponentReflectionTest(ComponentReflectionTest):
    @pytest.mark.skip(reason="unique constraints with duplicate column sets unsupported on db2 for iseries")
    def test_get_unique_constraints(self):
        return super().test_get_unique_constraints()


class ExpandingBoundInTest(ExpandingBoundInTest):
    @pytest.mark.skip(reason="search condition where null in set not unsupported on db2 for iseries")
    def test_null_in_empty_set_is_false(self):
        return super().test_null_in_empty_set_is_false()
