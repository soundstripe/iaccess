from itertools import groupby

from iaccess.compiler import IAccessCompiler, IAccessDDLCompiler, IAccessTypeCompiler, IAccessIdentifierPreparer
from iaccess.connector import IAccessConnector
from iaccess.information_schema import iseries as ischema
from sqlalchemy import sql, util, and_
from sqlalchemy.connectors.pyodbc import PyODBCConnector
from sqlalchemy.engine import default, reflection
from sqlalchemy.sql import sqltypes
from sqlalchemy.types import BLOB, DATE, DATETIME, SMALLINT, BIGINT, INTEGER, CHAR, VARCHAR, CLOB, DECIMAL, NUMERIC, \
    REAL, FLOAT, TIME, TIMESTAMP


class DOUBLE(sqltypes.Numeric):
    __visit_name__ = 'DOUBLE'


class LONGVARCHAR(sqltypes.VARCHAR):
    __visit_name_ = 'LONGVARCHAR'


class DBCLOB(sqltypes.CLOB):
    __visit_name__ = "DBCLOB"


class GRAPHIC(sqltypes.CHAR):
    __visit_name__ = "GRAPHIC"


class VARGRAPHIC(sqltypes.Unicode):
    __visit_name__ = "VARGRAPHIC"


class LONGVARGRAPHIC(sqltypes.UnicodeText):
    __visit_name__ = "LONGVARGRAPHIC"


class XML(sqltypes.Text):
    __visit_name__ = "XML"


ischema_names = {
    'BLOB': BLOB,
    'CHAR': CHAR,
    'CHARACTER': CHAR,
    'CLOB': CLOB,
    'DATE': DATE,
    'DATETIME': TIMESTAMP,
    'INTEGER': INTEGER,
    'SMALLINT': SMALLINT,
    'BIGINT': BIGINT,
    'DECIMAL': DECIMAL,
    'NUMERIC': NUMERIC,
    'REAL': REAL,
    'DOUBLE': DOUBLE,
    'FLOAT': FLOAT,
    'TIME': TIME,
    'TIMESTAMP': TIMESTAMP,
    'VARCHAR': VARCHAR,
    'LONGVARCHAR': LONGVARCHAR,
    'XML': XML,
    'GRAPHIC': GRAPHIC,
    'VARGRAPHIC': VARGRAPHIC,
    'LONGVARGRAPHIC': LONGVARGRAPHIC,
    'DBCLOB': DBCLOB,
    'TIMESTMP': TIMESTAMP,
}


class IAccessExecutionContext(default.DefaultExecutionContext):
    def get_lastrowid(self):
        s = sql.select([sql.literal_column('IDENTITY_VAL_LOCAL()')])
        return self.connection.scalar(s)

    def fire_sequence(self, sequence, type_):
        d: IAccessDialect = self.dialect
        return self._execute_scalar(
            "SELECT NEXT VALUE FOR "
            + d.identifier_preparer.format_sequence(sequence)
            + d.statement_compiler.default_from(),
            type_,
        )


class IAccessDialect(IAccessConnector, default.DefaultDialect):
    name = 'iaccess'
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

    supports_statement_cache = True

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
        query = sql.text("select CURRENT_SCHEMA from sysibm.sysdummy1")
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
        schema = self.denormalize_name(schema or self.default_schema_name)
        s = sql.select(
            [tables.c.table_name],
            sql.and_(
                tables.c.table_schema == schema,
                tables.c.table_type == 'T',
            ),
            order_by=[tables.c.table_name],
        )
        table_names = [self.normalize_name(r.table_name) for r in connection.execute(s)]
        return table_names

    @reflection.cache
    def get_foreign_keys(self, connection, table_name, schema=None, **kw):
        requested_schema = schema
        table_name = self.denormalize_name(table_name)
        schema = self.denormalize_name(schema or self.default_schema_name)
        s = """
        select fk.table_name, cst.constraint_name, fk.column_name as constrained_column,
               tgt.column_name as referred_column, tgt.table_name as referred_table,
               tgt.table_schema as referred_schema
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
                              and pk.column_position = tgt.ordinal_position
            where cst.constraint_type = 'FOREIGN KEY'
              and fk.ordinal_position = pk.ordinal_position
              and fk.table_schema = COALESCE(?, CURRENT_SCHEMA)
              and fk.table_name = ?
              and enabled = 'YES'"""
        r = connection.execute(s, [schema, table_name])
        results = []
        for fk in r:
            referred_schema = requested_schema
            if requested_schema is not None:
                referred_schema = self.normalize_name(fk.referred_schema)
            results.append({
                'name': self.normalize_name(fk.constraint_name),
                'constrained_columns': [self.normalize_name(fk.constrained_column)],
                'referred_schema': referred_schema,
                'referred_table': self.normalize_name(fk.referred_table),
                'referred_columns': [self.normalize_name(fk.referred_column)],
            })
        return results

    @reflection.cache
    def get_columns(self, connection, table_name, schema=None, **kw):
        current_schema = self.denormalize_name(schema or self.default_schema_name)
        table_name = self.denormalize_name(table_name)
        columns = ischema.columns
        s = sql.select([
            columns.c.column_name,
            columns.c.data_type,
            columns.c.length,
            columns.c.numeric_precision,
            columns.c.numeric_scale,
            columns.c.is_nullable,
            columns.c.column_default,
            columns.c.is_identity,
            columns.c.identity_generation,
            columns.c.identity_start,
            columns.c.identity_increment,
            columns.c.identity_minimum,
            columns.c.identity_maximum,
            columns.c.identity_cycle,
            columns.c.identity_cache,
            columns.c.identity_order,
        ], sql.and_(
            columns.c.table_name == table_name,
            columns.c.table_schema == current_schema,
        ))
        r = connection.execute(s)

        results = []
        for col in r:
            data_type = ischema_names.get(col.data_type, None)
            if data_type is None:
                util.warn(
                    "Did not recognize type '%s' of column '%s'"
                    % (col.data_type, col.column_name)
                )
                data_type = sqltypes.NULLTYPE

            if issubclass(data_type, sqltypes.Numeric) and not issubclass(data_type, sqltypes.Float):
                data_type = data_type(precision=col.numeric_precision,
                                      scale=col.numeric_scale)
            elif issubclass(data_type, sqltypes.String) and col.length:
                data_type = data_type(col.length)

            additional = {}

            auto_increment = col.is_identity and col.identity_generation is not None
            if auto_increment:
                additional['sequence'] = {
                    'name': '',
                    'start': col.identity_start,
                    'increment': col.identity_increment,
                    'minvalue': col.identity_minimum,
                    'maxvalue': col.identity_maximum,
                    'nominvalue': False,
                    'nomaxvalue': False,
                    'cycle': col.identity_cycle,
                    'cache': col.identity_cache,
                    'order': col.identity_order
                }

            col_dict = {
                'name': self.normalize_name(col.column_name),
                'type': data_type,
                'nullable': col.is_nullable == 'Y',
                'default': col.column_default,
                'autoincrement': auto_increment,
            }
            col_dict.update(additional)
            results.append(col_dict)
        return results

    @reflection.cache
    def get_indexes(self, connection, table_name, schema=None, **kw):
        table_name = self.denormalize_name(table_name)
        schema = self.denormalize_name(schema or self.default_schema_name)
        indexes = ischema.indexes
        keys = ischema.keys
        j = indexes.join(keys, indexes.c.index_name == keys.c.index_name)
        s = sql.select([
            indexes.c.index_name,
            indexes.c.is_unique,
            keys.c.column_name,
        ], and_(
            indexes.c.table_schema == schema,
            indexes.c.table_name == table_name,
        )).select_from(j).order_by(indexes.c.index_name, keys.c.ordinal_position)
        r = connection.execute(s)
        grouped = groupby(r, lambda x: (x.index_name, x.is_unique in 'VU'))
        results = [dict(name=self.normalize_name(index_name),
                        column_names=[self.normalize_name(c.column_name) for c in columns],
                        unique=is_unique,
                        ) for (index_name, is_unique), columns in grouped]
        return results

    @reflection.cache
    def get_pk_constraint(self, connection, table_name, schema=None, **kw):
        table_name = self.denormalize_name(table_name)
        schema = self.denormalize_name(schema or self.default_schema_name)
        constraints = ischema.constraints
        constraint_columns = ischema.constraint_columns
        j = constraints.join(constraint_columns, and_(
            constraints.c.table_schema == constraint_columns.c.table_schema,
            constraints.c.table_name == constraint_columns.c.table_name,
            constraints.c.constraint_name == constraint_columns.c.constraint_name,
        ))
        s = sql.select([
            constraint_columns.c.constraint_name,
            constraint_columns.c.column_name,
        ], and_(
            constraints.c.constraint_type == 'PRIMARY KEY',
            constraints.c.table_name == table_name,
            constraints.c.table_schema == schema,
        )).select_from(j)
        r = connection.execute(s)
        grouped = groupby(r, lambda x: self.normalize_name(x.constraint_name))
        results = [{
            'constrained_columns': [self.normalize_name(col.column_name) for col in columns],
            'name': cst_name,
        } for (cst_name, columns) in grouped]
        result = results[0] if results else None
        return result

    def get_unique_constraints(
        self, connection, table_name, schema=None, **kw
    ):
        table_name = self.denormalize_name(table_name)
        schema = self.denormalize_name(schema or self.default_schema_name)
        constraints = ischema.constraints
        constraint_columns = ischema.constraint_columns
        j = constraints.join(constraint_columns, and_(
            constraints.c.table_schema == constraint_columns.c.table_schema,
            constraints.c.table_name == constraint_columns.c.table_name,
            constraints.c.constraint_name == constraint_columns.c.constraint_name,
        ))
        s = sql.select([
            constraint_columns.c.constraint_name,
            constraint_columns.c.column_name,
        ], and_(
            constraints.c.constraint_type == 'UNIQUE',
            constraints.c.table_name == table_name,
            constraints.c.table_schema == schema,
        )).select_from(j)
        r = connection.execute(s)
        grouped = groupby(r, lambda x: self.normalize_name(x.constraint_name))
        results = [{
            'column_names': [self.normalize_name(col.column_name) for col in columns],
            'name': cst_name,
        } for (cst_name, columns) in grouped]
        return results

    def has_sequence(self, connection, sequence_name, schema=None):
        schema = self.denormalize_name(schema or self.default_schema_name)
        sequence_name = self.denormalize_name(sequence_name)
        sequences = ischema.sequences
        s = sql.select(
            [sequences.c.sequence_name],
            and_(
                sequences.c.sequence_name == sequence_name,
                sequences.c.sequence_schema == schema,
            ))
        r = connection.execute(s)
        return r.first() is not None

    def get_default_isolation_level(self, dbapi_conn):
        return "READ COMMITTED"

    def set_isolation_level(self, connection, level):
        if hasattr(connection, "connection"):
            dbapi_connection = connection.connection
        else:
            dbapi_connection = connection
        if level == "AUTOCOMMIT":
            dbapi_connection.autocommit = True
        else:
            dbapi_connection.autocommit = False
            connection.rollback()
            with connection.cursor() as cursor:
                cursor.execute("SET TRANSACTION ISOLATION LEVEL %s" % level)
