from sqlalchemy import MetaData, Table, Column, String

ischema = MetaData()

schema = Table(
    'SYSSCHEMAS',
    ischema,
    Column('SCHEMA_NAME', String, key='schema_name'),
    schema='QSYS2'
)


tables = Table(
    'SYSTABLES',
    ischema,
    Column('TABLE_NAME', String, key='table_name'),
    Column('TABLE_SCHEMA', String, key='table_schema'),
    Column('TABLE_TYPE', String, key='table_type'),
    schema='QSYS2'
)
