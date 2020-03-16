import pyodbc
from sqlalchemy import sql
from sqlalchemy.connectors.pyodbc import PyODBCConnector
from sqlalchemy.engine import default, reflection

from iaccess.compiler import IAccessCompiler, IAccessDDLCompiler, IAccessTypeCompiler, IAccessIdentifierPreparer
from iaccess.information_schema import iseries as ischema


class IAccessExecutionContext(default.DefaultExecutionContext):
    def get_lastrowid(self):
        s = sql.select([sql.literal_column('IDENTITY_VAL_LOCAL()')])
        return self.connection.scalar(s)


class IAccessDialect(PyODBCConnector, default.DefaultDialect):
    name = 'iaccess'
    driver = 'pyodbc'
    encoding = 'utf-8'
    default_param_style = 'qmark'
    schema_name = 'QGPL'

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
        table_name = self.denormalize_name(table_name)
        schema = self.denormalize_name(schema)

        whereclause = sql.and_(
            tables.c.table_name == table_name,
            tables.c.table_type == 'T',
            tables.c.table_schema == sql.func.coalesce(schema, sql.literal_column('CURRENT_SCHEMA'))
        )

        s = sql.select([tables], whereclause)
        c = connection.execute(s)
        return c.first() is not None

    def _get_default_schema_name(self, connection):
        query = sql.text("SELECT CURRENT_SCHEMA FROM SYSIBM.SYSDUMMY1")
        default_schema_name = connection.scalar(query)
        if default_schema_name is not None:
            # guard against the case where the default_schema_name is being
            # fed back into a table reflection function.
            return sql.quoted_name(default_schema_name, quote=True)
        else:
            return self.schema_name

    @reflection.cache
    def get_table_names(self, connection, schema=None, **kw):
        tables = ischema.tables
        schema = schema or self.default_schema_name
        s = sql.select(
            [tables.c.table_name],
            sql.and_(
                tables.c.table_schema == schema,
                tables.c.table_type == 'T',
            ),
            order_by=[tables.c.table_name],
        )
        table_names = [r[0] for r in connection.execute(s)]
        return table_names

    @reflection.cache
    def get_foreign_keys(self, connection, table_name, schema=None, **kw):
        s = """
        select fk.table_name, cst.constraint_name, fk.column_name as constrained_column,
               tgt.column_name as referred_column, tgt.TABLE_NAME as referred_table, tgt.table_schema as referred_schema
            from qsys2.syscst cst
                     join qsys2.syskeycst fk
                          on cst.constraint_schema = fk.constraint_schema
                              and cst.constraint_name = fk.constraint_name
                     join qsys2.sysrefcst ref
                          on cst.constraint_schema = ref.constraint_schema
                              and cst.constraint_name = ref.constraint_name
                     join qsys2.syskeycst pk
                          on ref.unique_constraint_schema = pk.constraint_schema
                              and ref.unique_constraint_name = pk.constraint_name
                     join qsys2.syscolumns tgt
                          on pk.table_schema = tgt.table_schema
                              and pk.table_name = tgt.table_name
                              and tgt.ordinal_position = fk.column_position
            where cst.constraint_type = 'FOREIGN KEY'
              and fk.ordinal_position = pk.ordinal_position
              and pk.table_schema = COALESCE(?, CURRENT_SCHEMA)
              and pk.table_name = ?
              and enabled = 'YES'"""
        r = connection.execute(s, [schema, table_name])
        results = []
        for fk in r:
            results.append({
                'name': fk.table_name,
                'constrained_columns': [fk.constrained_column],
                'referred_schema': fk.referred_schema,
                'referred_table': fk.referred_table,
                'referred_columns': [fk.referred_column],
            })
        return results
