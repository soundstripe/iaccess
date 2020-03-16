from sqlalchemy.sql import compiler


class IAccessCompiler(compiler.SQLCompiler):
    pass


class IAccessDDLCompiler(compiler.DDLCompiler):
    pass


class IAccessTypeCompiler(compiler.TypeCompiler):
    pass


class IAccessIdentifierPreparer(compiler.IdentifierPreparer):
    pass
