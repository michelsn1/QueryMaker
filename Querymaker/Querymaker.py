import psycopg2
import pandas as pd

class Querymaker():

    def __init__(self, database, user, password, host, port,sql_file=True):
        self.database = database
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.cursor = None
        self.sql_file=sql_file


    def _open_sql_file(self,file):
        data=open(file, 'r')
        return data.read()

    def _connect(self):
        conn = psycopg2.connect(
            dbname=self.database,
            user=self.user,
            password=self.password,
            host=self.host,
            port =self.port
        )
        print("Connected to %s" %self.database)

        self.cursor=conn.cursor()

        return self


    def _execute(self, query):
        if self.cursor is None:
            self._connect()
        if self.sql_file==True:
            query=self._open_sql_file(query)
        columns = []
        self.cursor.execute(query)
        for i in self.cursor.description:
            columns.append(i[0])

        return self.cursor.fetchall() , columns


    def dataframe_creator(self,query):
        result, columns = self._execute(query)
        return pd.DataFrame(result, columns=columns)
