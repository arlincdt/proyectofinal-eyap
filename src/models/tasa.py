from src.common.database import Database, CursorFromConnectionFromPool

class Tasa:
    def __init__(self, tId, tipo, periodoEnMeses, interesAnual, interesDiario, interesTotal):
        self.tId = tId
        self.tipo = tipo
        self.periodoEnMeses = periodoEnMeses
        self.interesAnual = interesAnual
        self.interesDiario = interesDiario
        self.interesTotal = interesTotal


    def __repr__(self):
        return "<Tasa>".format(self.tId)


    @classmethod
    def getByTId(cls, tId):
        with CursorFromConnectionFromPool() as cursor:
                cursor.execute("SELECT * FROM tasa WHERE tId=%s", (tId,))
                tasa = cursor.fetchone()
                if tasa:
                    return cls(tId=tasa[0], tipo=tasa[1], periodoEnMeses=tasa[2], interesAnual=tasa[3], interesDiario=tasa[4], interesTotal=tasa[5])

    @classmethod
    def getAll(cls):
        with CursorFromConnectionFromPool() as cursor:
                cursor.execute("SELECT * FROM tasa ")
                tasas_data = cursor.fetchall()
                if tasas_data:
                    tasas = []
                    for tasa in tasas_data:
                        nueva_tasa = Tasa(tasa[0],tasa[1],tasa[2],tasa[3],tasa[4],tasa[5])
                        tasas.append(nueva_tasa)
                    return tasas


    def json(self):
        return{
                'tId':self.tId,
                'tipo':self.tipo,
                'periodoEnMeses':self.periodoEnMeses,
                'interesAnual':self.interesAnual,
                'interesDiario':self.interesDiario,
                'interesTotal':self.interesTotal
             }

