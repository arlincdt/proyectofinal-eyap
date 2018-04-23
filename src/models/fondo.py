from src.common.database import Database, CursorFromConnectionFromPool

class Fondo:
    def __init__(self, fId, ganancias):
        self.fId = fId
        self.ganancias = ganancias

    def __repr__(self):
        return "<Fondo>"

    @classmethod
    def getFondo(cls):
        with CursorFromConnectionFromPool() as cursor:
                cursor.execute("SELECT * FROM fondo WHERE fId=1")
                fecha = cursor.fetchone()
                if fecha:
                    return cls(fId=fecha[0], ganancias=fecha[1])

    @classmethod
    def updateGanancias(self, ganancias):
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute("UPDATE fondo set ganancias = %s WHERE fId=1", (ganancias, ))
