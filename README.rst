============================================================
i Access Db2 SQLAlchemy Driver
============================================================


.. image:: https://img.shields.io/pypi/v/iaccess.svg
        :target: https://pypi.python.org/pypi/iaccess

.. image:: https://img.shields.io/travis/soundstripe/iaccess.svg
        :target: https://travis-ci.com/soundstripe/iaccess

.. image:: https://readthedocs.org/projects/python-iaccess/badge/?version=latest
        :target: https://python-iaccess.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status




Provides support for DB2 for iSeries for remote python clients using IBM i Access Client Solutions ODBC driver. On up-to-date systems (7.2+ with latest PTFs) you can also `use this driver locally`_ on your i Series machine, making local development of server code more feasible.


Other work in this area includes the ibm_db_ and ibm_db_sa_ projects, which also provide access to DB2 and support SQLAlchemy. Those two packages rely on and automatically install a binary driver for DB2, while this package relies on you already having install the `i Access Client Solutions ODBC`_ driver available on IBM's support/download site.


* Free software: MIT license


Installation
------------
Pre-requisites
==============
* UnixODBC (if on Linux or in PASE for i): Windows ships with ODBC installed, but on Linux you'll need unixodbc. On Ubuntu you can install this with :code:`apt-get install unixodbc`. You may also need to :code:`apt-get install unixodbc-dev` if you get errors about a missing `sql.h` file.
* `i Access Client Solutions ODBC`_ driver: You'll need this driver available only from IBM.
* IBM i 7.2+ on your target system: Older versions of the OS may work but I have not tested against them. If you do not happen to have an IBM Power system sitting around your house (although who doesn't?!) you may be able to get an account to play with at Pub400.com_.


Install via pip
===============

Use pip to download and install the latest released version of this tool.::

    pip install iaccess

Install via setup.py
====================
Download or clone this repo and install via setup.py::

    python setup.py install


Quickstart
----------
If you know what you're doing with SQLAlchemy this package should be nearly invisible to you with the exception of the URI used to connect to the database.::

    # connect via hostname / ip address
    >>> from sqlalchemy import create_engine
    >>> engine = create_engine('iaccess+pyodbc://user:password@hostname/dummy?DBQ=DEFAULT_SCHEMA')  # `dummy` can be any string

    # connect via named ODBC DSN
    >>> from sqlalchemy import create_engine
    >>> engine = create_engine('iaccess+pyodbc://user:password@dsn_name')

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

The IBM i Access ODBC Driver is developed and licensed separately by IBM.

Continuous integration testing is performed against the system available from the great guys at Pub400.com_.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
.. _`i Access Client Solutions ODBC`: https://www.ibm.com/support/pages/ibm-i-access-client-solutions
.. _ibm_db: https://github.com/ibmdb/python-ibmdb
.. _ibm_db_sa: https://github.com/ibmdb/python-ibmdb
.. _`use this driver locally`: https://www.ibmsystemsmag.com/Power-Systems/08/2019/ODBC-Driver-for-IBM-i
.. _Pub400.com: https://pub400.com
