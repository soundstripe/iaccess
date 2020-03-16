from sqlalchemy.sql import compiler


class IAccessCompiler(compiler.SQLCompiler):
    def default_from(self):
        return " from sysibm.sysdummy1"


class IAccessDDLCompiler(compiler.DDLCompiler):
    pass


class IAccessTypeCompiler(compiler.GenericTypeCompiler):
    def visit_boolean(self, type_, **kw):
        return self.visit_SMALLINT(type_, **kw)


class IAccessIdentifierPreparer(compiler.IdentifierPreparer):
    pass
