import platform

from sqlalchemy.testing import exclusions, fails_if
from sqlalchemy.testing.exclusions import LambdaPredicate, skip_if, skip
from sqlalchemy.testing.requirements import SuiteRequirements


class Requirements(SuiteRequirements):
    @property
    def implicitly_named_constraints(self):
        return exclusions.open()

    @property
    def temp_table_reflection(self):
        return exclusions.closed()

    @property
    def ctes(self):
        return exclusions.open()

    @property
    def autocommit(self):
        return exclusions.open()

    @property
    def reflects_pk_names(self):
        return exclusions.open()

    @property
    def datetime(self):
        return exclusions.closed()

    @property
    def datetime_microseconds(self):
        return exclusions.closed()

    @property
    def empty_inserts(self):
        return exclusions.closed()

    @property
    def implicit_decimal_binds(self):
        return exclusions.closed()

    @property
    def unbounded_varchar(self):
        return exclusions.closed()

    @property
    def time_microseconds(self):
        return exclusions.closed()

    def get_isolation_levels(self, config):
        return {
            "default": "READ COMMITTED",
            "supported": [
                "SERIALIZABLE", "READ UNCOMMITTED",
                "READ COMMITTED", "REPEATABLE READ",
                "NO COMMIT", "AUTOCOMMIT"
            ]
        }
