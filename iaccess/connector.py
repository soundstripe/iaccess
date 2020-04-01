import re

from sqlalchemy.connectors.pyodbc import PyODBCConnector


class IAccessConnector(PyODBCConnector):
    pyodbc_driver_name = 'IBM i Access ODBC Driver'

    def create_connect_args(self, url):
        connectors, connect_args = super().create_connect_args(url)

        # force unicode mode (utf-16 instead of ebdic default)
        connect_args.update(unicodesql=1)

        # set true autocommit on (without this, autocommit forces isolation mode *NONE
        connect_args.update(trueautocommit=1)

        # non-standard "system" keyword required instead of "server"
        server = re.search('server=([^;]+)', connectors[0], re.IGNORECASE)
        if server:
            connect_args.update(system=server.group(1))

        return [connectors, connect_args]
