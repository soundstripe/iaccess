# test/test_suite.py

# noinspection PyUnresolvedReferences
import pytest
from sqlalchemy.testing.suite import *


class CTETest(CTETest):
    @pytest.mark.xfail(reason="ctes not allowed in insert statements on db2 for iseries")
    def test_insert_from_select_round_trip(self):
        super().test_insert_from_select_round_trip()


class ComponentReflectionTest(ComponentReflectionTest):
    @pytest.mark.xfail(reason="unique constraints with duplicate column sets unsupported on db2 for iseries")
    def test_get_unique_constraints(self):
        return super().test_get_unique_constraints()

    @pytest.mark.xfail(reason="unknown problem with test -- deprecation error not raised")
    def test_deprecated_get_primary_keys(self):
        return super().test_deprecated_get_primary_keys


class ExpandingBoundInTest(ExpandingBoundInTest):
    @pytest.mark.xfail(reason="search condition where null in set not unsupported on db2 for iseries")
    def test_null_in_empty_set_is_false(self):
        return super().test_null_in_empty_set_is_false()


class InsertBehaviorTest(InsertBehaviorTest):
    @pytest.mark.xfail(reason="iaccess odbc driver is not able to infer some data types")
    def test_insert_from_select_with_defaults(self):
        return super().test_insert_from_select_with_defaults()


class NumericTest(NumericTest):
    @pytest.mark.xfail(reason="iaccess odbc driver is not able to infer some data types")
    def test_float_coerce_round_trip(self):
        return super().test_float_coerce_round_trip()


class TableDDLTest(TableDDLTest):
    @pytest.mark.xfail(reason="need to specify test schema")
    def test_create_table_schema(self):
        return super().test_create_table_schema()


class StringTest(StringTest):
    @pytest.mark.skip(reason="high unicode literals cannot fit in UCS-2 encoding used by iaccess driver")
    def test_literal_non_ascii(self):
        super().test_literal_non_ascii()


class TextTest(TextTest):
    @pytest.mark.skip(reason="high unicode literals cannot fit in UCS-2 encoding used by iaccess driver")
    def test_literal_non_ascii(self):
        super().test_literal_non_ascii()


class UnicodeVarcharTest(UnicodeVarcharTest):
    @pytest.mark.skip(reason="high unicode literals cannot fit in UCS-2 encoding used by iaccess driver")
    def test_literal_non_ascii(self):
        super().test_literal_non_ascii()

    @pytest.mark.skip(reason="high unicode literals cannot fit in UCS-2 encoding used by iaccess driver")
    def test_literal(self):
        super().test_literal()


class UnicodeTextTest(UnicodeTextTest):
    @pytest.mark.skip(reason="high unicode literals cannot fit in UCS-2 encoding used by iaccess driver")
    def test_literal_non_ascii(self):
        super().test_literal_non_ascii()

    @pytest.mark.skip(reason="high unicode literals cannot fit in UCS-2 encoding used by iaccess driver")
    def test_literal(self):
        super().test_literal()


class ExistsTest(ExistsTest):
    def test_select_exists(self, connection):
        """overridden because iseries does not support naked literal bound parameters in select clauses"""
        stuff = self.tables.stuff
        eq_(
            connection.execute(
                select([text('1')]).where(
                    exists().where(stuff.c.data == "some data")
                )
            ).fetchall(),
            [(1,)],
        )

    def test_select_exists_false(self, connection):
        stuff = self.tables.stuff
        eq_(
            connection.execute(
                select([text('1')]).where(
                    exists().where(stuff.c.data == "no data")
                )
            ).fetchall(),
            [],
        )


class CompositeKeyReflectionTest(CompositeKeyReflectionTest):
    @pytest.mark.skip(reason="composite keys unsupported by db2 for i ")
    def test_fk_column_order(self):
        super().test_fk_column_order()

    @pytest.mark.skip(reason="composite keys unsupported by db2 for i ")
    def test_pk_column_order(self):
        super().test_pk_column_order()
