import re

from sqlalchemy.sql import compiler

ILLEGAL_INITIAL_CHARACTERS = {str(x) for x in range(0, 10)}.union(["$", "_"])

_MAX_BIGINT = 2**63 - 1  # 9223372036854775807


class IAccessCompiler(compiler.SQLCompiler):
    def default_from(self):
        return " FROM SYSIBM.SYSDUMMY1"

    def visit_empty_set_op_expr(self, type_, expand_op):
        # Db2 for i don't seem to be able to handle
        # the empty set impl
        return self.visit_empty_set_expr(type_)

    def visit_empty_set_expr(self, element_types):
        # noinspection SqlConstantCondition
        return ' '.join(['SELECT 1', self.default_from(), 'WHERE 1!=1'])

    # noinspection PyProtectedMember
    def limit_clause(self, select, **kw):
        text = ""
        if select._limit_clause is not None:
            text += "\n LIMIT " + self.process(select._limit_clause, **kw)
        if select._offset_clause is not None:
            if select._limit_clause is None:
                text += "\n LIMIT " + str(_MAX_BIGINT)
            text += " OFFSET " + self.process(select._offset_clause, **kw)
        return text

    def visit_sequence(self, sequence, **kw):
        seq = self.dialect.identifier_preparer.format_sequence(sequence)
        return f"NEXT VALUE FOR {seq}"

    def visit_mod_binary(self, binary, operator, **kw):
        return "mod(cast(%s as bigint), cast(%s as bigint))" % (
            self.process(binary.left, **kw),
            self.process(binary.right, **kw),
        )

    def visit_savepoint(self, savepoint_stmt):
        return "SAVEPOINT %s ON ROLLBACK RETAIN CURSORS" % self.preparer.format_savepoint(savepoint_stmt)


class IAccessDDLCompiler(compiler.DDLCompiler):
    def visit_create_table(self, create):
        ddl = super().visit_create_table(create)

        # IBM supports `DECLARE GLOBAL TEMPORARY TABLE` instead of `CREATE GLOBAL TEMPORARY TABLE`
        if re.match(r'\W*CREATE GLOBAL TEMPORARY', ddl):
            ddl = ddl.replace('CREATE GLOBAL', 'DECLARE GLOBAL', 1)
        return ddl

    def get_column_specification(self, column, **kwargs):
        colspec = (
            self.preparer.format_column(column)
            + " "
            + self.dialect.type_compiler.process(
                column.type, type_expression=column
            )
        )

        system_name = kwargs.get('system_name', None)
        if system_name is not None:
            colspec += " FOR COLUMN " + system_name

        default = self.get_column_default_string(column)
        if default is not None:
            colspec += " DEFAULT " + default

        if column.computed is not None:
            colspec += " " + self.process(column.computed)

        if (
            column.table is not None
            and column is column.table._autoincrement_column
            and column.server_default is None
        ):
            colspec += " GENERATED BY DEFAULT AS IDENTITY "

        implicitly_hidden = kwargs.get('implicitly_hidden', None)
        if implicitly_hidden is not None:
            colspec += " IMPLICITLY HIDDEN"

        if not column.nullable:
            colspec += " NOT NULL"
        return colspec


class IAccessTypeCompiler(compiler.GenericTypeCompiler):
    def visit_BOOLEAN(self, type_, **kw):
        return self.visit_SMALLINT(type_, **kw)

    def visit_DATETIME(self, type_, **kw):
        return self.visit_TIMESTAMP(type_, **kw)

    def visit_TEXT(self, type_, **kw):
        return self.visit_CLOB(type_, **kw)

    def visit_unicode(self, type_, **kw):
        return self.visit_NVARCHAR(type_, **kw)

    def visit_unicode_text(self, type_, **kw):
        return self.visit_NCLOB(type_, **kw)


class IAccessIdentifierPreparer(compiler.IdentifierPreparer):
    illegal_initial_characters = ILLEGAL_INITIAL_CHARACTERS
