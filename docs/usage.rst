=====
Usage
=====

To use i Access Db2 SQLAlchemy Driver in a project::

    # With a hostname (requires a dummy database name to be in the URL)
    url = 'iaccess+pyodbc://user:password@host/dummy?DBQ=SCHEMA_NAME'

    # or with a named DSN
    url = 'iaccess+pyodbc://dsn_name/?DBQ=SCHEMA_NAME'

    # now use as normal for sqlalchemy
    from sqlalchemy import create_engine

    e = create_engine(url)
    conn = e.connect()
    results = conn.execute("SELECT 'hello world' FROM SYSIBM.SYSDUMMY1")
    print(list(results))


