from sqlalchemy import MetaData, Table, Column, String, Integer

ischema = MetaData()

schema = Table(
    'SYSSCHEMAS',
    ischema,
    Column('SCHEMA_NAME', String, key='schema_name'),
    schema='QSYS2',
)

tables = Table(
    'SYSTABLES',
    ischema,
    Column('TABLE_NAME', String, key='table_name'),
    Column('TABLE_SCHEMA', String, key='table_schema'),
    Column('TABLE_TYPE', String, key='table_type'),
    schema='QSYS2',
)

columns = Table(
    'SYSCOLUMNS',
    ischema,
    Column('COLUMN_NAME', String, key='column_name'),
    Column('DATA_TYPE', String, key='data_type'),
    Column('LENGTH', String, key='length'),
    Column('NUMERIC_SCALE', String, key='numeric_scale'),
    Column('NUMERIC_PRECISION', String, key='numeric_precision'),
    Column('TABLE_NAME', String, key='table_name'),
    Column('TABLE_SCHEMA', String, key='table_schema'),
    Column('COLUMN_DEFAULT', String, key='column_default'),
    Column('IS_NULLABLE', String, key='is_nullable'),
    Column('IS_IDENTITY', String, key='is_identity'),
    Column('IDENTITY_GENERATION', String, key='identity_generation'),
    Column('IDENTITY_START', String, key='identity_start'),
    Column('IDENTITY_INCREMENT', String, key='identity_increment'),
    Column('IDENTITY_MINIMUM', String, key='identity_minimum'),
    Column('IDENTITY_MAXIMUM', String, key='identity_maximum'),
    Column('IDENTITY_CYCLE', String, key='identity_cycle'),
    Column('IDENTITY_CACHE', String, key='identity_cache'),
    Column('IDENTITY_ORDER', String, key='identity_order'),
    schema='QSYS2',
)

indexes = Table(
    'SYSINDEXES',
    ischema,
    Column('INDEX_NAME', String, key='index_name'),
    Column('TABLE_NAME', String, key='table_name'),
    Column('TABLE_SCHEMA', String, key='table_schema'),
    Column('COLUMN_COUNT', String, key='column_count'),
    Column('IS_UNIQUE', String, key='is_unique'),
    Column('INDEX_SCHEMA', String, key='index_schema'),
    schema='QSYS2',
)

keys = Table(
    'SYSKEYS',
    ischema,
    Column('INDEX_NAME', String, key='index_name'),
    Column('COLUMN_NAME', String, key='column_name'),
    Column('ORDINAL_POSITION', Integer, key='ordinal_position'),
    schema='QSYS2',
)

constraints = Table(
    'SYSCST',
    ischema,
    Column('CONSTRAINT_NAME', String, key='constraint_name'),
    Column('TABLE_NAME', String, key='table_name'),
    Column('TABLE_SCHEMA', String, key='table_schema'),
    Column('CONSTRAINT_TYPE', String, key='constraint_type'),
)


constraint_columns = Table(
    'SYSCSTCOL',
    ischema,
    Column('CONSTRAINT_NAME', String, key='constraint_name'),
    Column('TABLE_NAME', String, key='table_name'),
    Column('TABLE_SCHEMA', String, key='table_schema'),
    Column('COLUMN_NAME', String, key='column_name'),
)


sequences = Table(
    'SYSSEQUENCES',
    ischema,
    Column('SEQUENCE_SCHEMA', String, key='sequence_schema'),
    Column('SEQUENCE_NAME', String, key='sequence_name'),
    schema='QSYS2'
)
