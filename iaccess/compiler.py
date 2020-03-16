from sqlalchemy.sql import compiler


class IAccessCompiler(compiler.SQLCompiler):
    def default_from(self):
        return " from sysibm.sysdummy1"


class IAccessDDLCompiler(compiler.DDLCompiler):
    pass


class IAccessTypeCompiler(compiler.GenericTypeCompiler):
    pass


class IAccessIdentifierPreparer(compiler.IdentifierPreparer):
    pass
