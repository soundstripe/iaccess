from sqlalchemy.testing import exclusions
from sqlalchemy.testing.requirements import SuiteRequirements


class Requirements(SuiteRequirements):
    @property
    def temp_table_reflection(self):
        return exclusions.closed()

    @property
    def ctes(self):
        return exclusions.open()
