=====
Usage
=====


With a hostname
---------------
(requires a dummy database name to be in the URL):python:

    >>> url = 'iaccess+pyodbc://user:password@host/dummy?DBQ=SCHEMA_NAME'
    >>> engine = create_engine(url, echo=True)  # echo to log all generated SQL

With a named DSN
----------------
Must define DSN in ODBC Sources (Windows) or in :code:/etc/odbcinst.ini (UnixODBC).:python:

    >>> url = 'iaccess+pyodbc://dsn_name/?DBQ=SCHEMA_NAME'
    >>> engine = create_engine(url, echo=True)  # echo to log all generated SQL


Using your connection string
----------------------------
For more details, consult `sqlalchemy documention`_. This example is taken from the SQLAlchemy Core tutorial, modified to specify a length on the String columns since Db2 for i does not allow VARCHAR columns without a length specified.

:python:

    >>> from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
    >>> metadata = MetaData()
    >>> users = Table('users', metadata,
    ...     Column('id', Integer, primary_key=True),
    ...     Column('name', String(50)),
    ...     Column('fullname', String(50)),
    ... )

    >>> addresses = Table('addresses', metadata,
    ...   Column('id', Integer, primary_key=True),
    ...   Column('user_id', None, ForeignKey('users.id')),
    ...   Column('email_address', String(50), nullable=False)
    ...  )

    >>> metadata.create_all(engine)

    >>> conn = engine.connect()

    >>> ins = users.insert().values(name='jack', fullname='Jack Jones')
    >>> result = conn.execute(ins)

    >>> result.inserted_primary_key
    [1]

    >>> s = select([users])
    >>> result = conn.execute(s)
    >>> list(result)
    [(1, 'jack', 'Jack Jones')]


.. _sqlalchemy documention: https://docs.sqlalchemy.org/en/13/core/tutorial.html
