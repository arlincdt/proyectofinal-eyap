from psycopg2 import pool
# from src.common.database import Database, CursorFromConnectionFromPool
# Database.initialize(minconn=1, maxconn=10, user="edlgg", password="6627982", host="localhost", database="postgres")
# Database.create_tables()
class Database:
    __connection_pool = None

    @classmethod
    def initialize(cls, minconn, maxconn, **kwargs):
        cls.__connection_pool = pool.SimpleConnectionPool(minconn, maxconn, **kwargs)

    @classmethod
    def get_connection(cls):
        return cls.__connection_pool.getconn()

    @classmethod
    def return_connection(cls, connection):
        Database.__connection_pool.putconn(connection)
    
    @classmethod
    def close_all_connections(cls):
        Database.__connection_pool.closeall()

    @classmethod
    def create_tables(cls):
        with CursorFromConnectionFromPool() as cursor:
                cursor.execute("""
                                CREATE TABLE IF NOT EXISTS promotor(
                                nombre text primary key,
                                password text,
                                isAdmin integer
                            );

                            CREATE TABLE IF NOT EXISTS cliente(
                                cId serial primary key,
                                nombre text,
                                saldoVista integer,
                                saldoInvertido integer,
                                nombrePromotor text references promotor(nombre)
                            );

                            CREATE TABLE IF NOT EXISTS tasa(
                                tId text primary key,
                                tipo text,
                                periodoEnMeses integer,
                                interesAnual float,
                                interesDiario float,
                                interesTotal float
                            );

                            CREATE TABLE IF NOT EXISTS inversion(
                                iId serial primary key,
                                cId integer references cliente(cId),
                                fechaInicial DATE,
                                fechaFinal DATE,
                                tId text references tasa(tID),
                                montoInicial integer,
                                montoFinal integer
                            );

                            CREATE TABLE IF NOT EXISTS fecha(
                                fId integer primary key,
                                fechaActual DATE
                            );

                            CREATE TABLE IF NOT EXISTS fondo(
                                fId integer primary key,
                                ganancias integer
                            );

                            INSERT INTO promotor VALUES ('Admin'    , '123', 1) on conflict do nothing;
                            INSERT INTO promotor VALUES ('promotor1', '123', 0) on conflict do nothing;
                            INSERT INTO promotor VALUES ('promotor2', '123', 0) on conflict do nothing;

                            INSERT INTO tasa VALUES ('c1',  'Cetes', 1,  6.99, 0.01915068493150685, 0.5745205479 ) on conflict do nothing;
                            INSERT INTO tasa VALUES ('c3',  'Cetes', 3,  7.08, 0.019397260273972605, 1.7457534243000001 ) on conflict do nothing;
                            INSERT INTO tasa VALUES ('c6',  'Cetes', 6,  7.17, 0.01964383561, 3.5358904098000004 ) on conflict do nothing;
                            INSERT INTO tasa VALUES ('c12', 'Cetes', 12, 7.23, 0.01980821917, 7.23) on conflict do nothing;
                            INSERT INTO tasa VALUES ('b12', 'Bondes D', 12, 7.53, 0.02063013698, 7.53) on conflict do nothing;
                            INSERT INTO tasa VALUES ('b36', 'Bondes D', 36, 7.55, 0.020684931506849316, 15.1 ) on conflict do nothing;
                            INSERT INTO tasa VALUES ('b60', 'Bondes D', 60, 7.57, 0.02073972602739726, 37.85 ) on conflict do nothing;

                            INSERT INTO fecha VALUES (1,'2018-03-17')

                            """)


class CursorFromConnectionFromPool:
    def __init__(self):
        self.connection = None
        self.cursor = None
    
    def __enter__(self):
        self.connection = Database.get_connection()
        self.cursor = self.connection.cursor()
        return self.cursor
    
    def __exit__(self, exception_type, exception_value, exception_traceback):
        if exception_value is not None:
            self.connection.rollback()
        else:
            self.cursor.close()
            self.connection.commit()
        Database.return_connection(self.connection)