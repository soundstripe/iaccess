import re
import warnings

import pyodbc
from sqlalchemy.connectors.pyodbc import PyODBCConnector

CLIENT_SOLUTIONS_URL = 'https://www.ibm.com/support/pages/odbc-driver-ibm-i-access-client-solutions'


class IAccessDriverMissingWarning(UserWarning):
    pass


class IAccessConnector(PyODBCConnector):
    pyodbc_driver_name = 'IBM i Access ODBC Driver'

    def create_connect_args(self, url):
        available_drivers = pyodbc.drivers()
        selected_driver = url.query.get('DRIVER', self.pyodbc_driver_name)
        if selected_driver not in available_drivers:
            warnings.warn(f'driver "{selected_driver}" not found by pyodbc\n'
                          f'install from {CLIENT_SOLUTIONS_URL} or specify an alternate driver name\n'
                          f'available drivers: {repr(available_drivers or None)}',
                          IAccessDriverMissingWarning)

        connectors, connect_args = super().create_connect_args(url)

        # force unicode mode (utf-16 instead of ebdic default)
        connect_args.update(unicodesql=1)

        # set true autocommit on (without this, autocommit forces isolation mode *NONE
        connect_args.update(trueautocommit=1)

        # non-standard "system" keyword required instead of "server"
        server = re.search('server=([^;]+)', connectors[0], re.IGNORECASE)
        if server:
            connectors[0] = connectors[0].rstrip(';') + ';system=' + server.group(1)
            connect_args.update(system=server.group(1))

        return [connectors, connect_args]
