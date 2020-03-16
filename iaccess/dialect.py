from sqlalchemy.engine import default

from iaccess.compiler import IAccessCompiler, IAccessDDLCompiler, IAccessTypeCompiler, IAccessIdentifierPreparer


class IAccessExecutionContext(default.DefaultExecutionContext):
    pass


class IAccessDialect(default.DefaultDialect):
    name = 'iaccess'
    driver = 'pyodbc'
    encoding = 'utf-8'
    default_param_style = 'qmark'

    max_identifier_length = 128  # https://www.ibm.com/support/knowledgecenter/en/ssw_ibm_i_74/IAccess/rbafzlimtabs.htm
    supports_alter = True

    supports_unicode_statements = True
    supports_sane_rowcount = False
    supports_sane_multi_rowcount = False
    supports_native_decimal = True
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

    def create_connect_args(self, url):
        _, opts = super().create_connect_args(url)
        dsn_opts = {}
        hostname = opts.pop('host')
        if '.' in hostname:
            dsn_opts['SYSTEM'] = hostname
        else:
            dsn_opts['DSN'] = hostname
        if 'username' in opts:
            dsn_opts['UID'] = opts.pop('username')
        if 'password' in opts:
            dsn_opts['PWD'] = opts.pop('password')
        dsn = ';'.join(f'{k}={v}' for (k, v) in dsn_opts.items())
        return [[dsn], {}]


