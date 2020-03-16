import re

from sqlalchemy.sql import compiler


class IAccessCompiler(compiler.SQLCompiler):
    def default_from(self):
        return " from sysibm.sysdummy1"


class IAccessDDLCompiler(compiler.DDLCompiler):
    def visit_create_table(self, create):
        ddl = super().visit_create_table(create)

        # IBM supports `DECLARE GLOBAL TEMPORARY TABLE` instead of `CREATE GLOBAL TEMPORARY TABLE`
        if re.match('\W*CREATE GLOBAL TEMPORARY', ddl):
            ddl = ddl.replace('CREATE GLOBAL', 'DECLARE GLOBAL', 1)
        return ddl


class IAccessTypeCompiler(compiler.GenericTypeCompiler):
    def visit_boolean(self, type_, **kw):
        return self.visit_SMALLINT(type_, **kw)


class IAccessIdentifierPreparer(compiler.IdentifierPreparer):
    pass
