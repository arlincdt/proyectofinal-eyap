from src.common.database import Database, CursorFromConnectionFromPool

class Fecha:
    def __init__(self, fId, fechaActual):
        self.fId = fId
        self.fechaActual = fechaActual

    def __repr__(self):
        return "<Promotor>".format(self.fechaActual)

    @classmethod
    def getFecha(cls):
        with CursorFromConnectionFromPool() as cursor:
                cursor.execute("SELECT * FROM fecha WHERE fId=1")
                fecha = cursor.fetchone()
                if fecha:
                    return cls(fId=fecha[0], fechaActual=fecha[1])

    @classmethod
    def updateFecha(self, fecha):
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute("UPDATE fecha set fechaactual = %s WHERE fId=1", (fecha, ))

    def json(self):
        return{
                'fId': self.fId,
                'fecha': self.fechaActual,
             }