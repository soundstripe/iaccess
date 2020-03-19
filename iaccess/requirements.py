from sqlalchemy.testing import exclusions
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
