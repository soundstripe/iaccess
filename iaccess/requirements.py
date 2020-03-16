from sqlalchemy.testing import exclusions
from sqlalchemy.testing.requirements import SuiteRequirements


class Requirements(SuiteRequirements):
    @property
    def order_by_col_from_union(self):
        """target database supports ordering by a column from a SELECT
        inside of a UNION

        E.g.  (SELECT id, ...) UNION (SELECT id, ...) ORDER BY id

        """
        return exclusions.open()

    @property
    def cross_schema_fk_reflection(self):
        return exclusions.closed()
