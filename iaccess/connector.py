from sqlalchemy.connectors.pyodbc import PyODBCConnector


class IAccessConnector(PyODBCConnector):
    def create_connect_args(self, url):
        connectors, connect_args = super().create_connect_args(url)
        connect_args.update(unicodesql=1)
        return [connectors, connect_args]
