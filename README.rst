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


Features
--------

* TODO

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

The IBM i Access ODBC Driver is developed and licensed separately by IBM.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
.. _`i Access Client Solutions ODBC`: https://www.ibm.com/support/pages/ibm-i-access-client-solutions
.. _ibm_db: https://github.com/ibmdb/python-ibmdb
.. _ibm_db_sa: https://github.com/ibmdb/python-ibmdb
.. _`use this driver locally`: https://www.ibmsystemsmag.com/Power-Systems/08/2019/ODBC-Driver-for-IBM-i
