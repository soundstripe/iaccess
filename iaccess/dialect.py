from sqlalchemy import sql
from sqlalchemy.connectors.pyodbc import PyODBCConnector
from sqlalchemy.engine import default

from iaccess.compiler import IAccessCompiler, IAccessDDLCompiler, IAccessTypeCompiler, IAccessIdentifierPreparer
from iaccess.information_schema import iseries as ischema


class IAccessExecutionContext(default.DefaultExecutionContext):
    pass


class IAccessDialect(PyODBCConnector, default.DefaultDialect):
    name = 'iaccess'
    driver = 'pyodbc'
    encoding = 'utf-8'
    default_param_style = 'qmark'

    max_identifier_length = 128  # https://www.ibm.com/support/knowledgecenter/en/ssw_ibm_i_74/IAccess/rbafzlimtabs.htm
    supports_alter = True

    supports_sane_rowcount = False
    supports_sane_rowcount_returning = False
    supports_native_boolean = False
    supports_sequences = True
    sequences_optional = True

    supports_default_values = False

    requires_name_normalize = True

    two_phase_transactions = False

    statement_compiler = IAccessCompiler
    ddl_compiler = IAccessDDLCompiler
    type_compiler = IAccessTypeCompiler
    preparer = IAccessIdentifierPreparer
    execution_ctx_cls = IAccessExecutionContext

    @classmethod
    def dbapi(cls):
        import pyodbc
        return pyodbc

    def has_table(self, connection, table_name, schema=None):
        tables = ischema.tables

        whereclause = sql.and_(
            tables.c.table_name == table_name,
            tables.c.table_type == 'T',
        )

        if schema is not None:
            whereclause = sql.and_(tables.c.table_schema == schema)

        s = sql.select([tables], whereclause)
        c = connection.execute(s)
        return c.first() is not None
