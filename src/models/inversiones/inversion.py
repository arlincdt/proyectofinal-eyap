from src.common.database import Database, CursorFromConnectionFromPool
from src.models.fechas.fecha import Fecha
from src.models.tasa import Tasa
from datetime import timedelta
import time

class Inversion:
    def __init__(self, iId, cId, fechaInicial, fechaFinal, tId, montoInicial, montoFinal):
        self.iId = iId
        self.cId = cId
        self.fechaInicial = fechaInicial
        self.fechaFinal = fechaFinal
        self.tId = tId
        self.montoInicial = montoInicial
        self.montoFinal = montoFinal


    def __repr__(self):
        return "<Inversion {}>".format(self.iId)


    def saveToDb(self):
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute("INSERT INTO inversion (cId, fechaInicial, fechaFinal, tId, montoInicial, montoFinal) VALUES (%s, %s, %s, %s, %s, %s) on conflict do nothing",(self.cId, self.fechaInicial, self.fechaFinal, self.tId, self.montoInicial, self.montoFinal))


    def deleteFromDb(self):
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute("DELETE FROM inversion WHERE iId = %s",(self.iId,))
        pass


    @classmethod
    def getByIId(cls, iId):
        with CursorFromConnectionFromPool() as cursor:
                cursor.execute("SELECT * FROM inversion WHERE iid=%s", (iId,))
                inversion_data = cursor.fetchone()
                if inversion_data:
                    return cls(iId=inversion_data[0], cId=inversion_data[1], fechaInicial=inversion_data[2], fechaFinal=inversion_data[3], tId=inversion_data[4], montoInicial=inversion_data[5], montoFinal=inversion_data[6])
    

    @classmethod
    def getByCId(cls, cId):
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute("SELECT * FROM inversion WHERE cid = %s",(cId,))
            invData = cursor.fetchall()
            if invData:
                inversiones = []
                for inversion in invData:
                    nueva_inversion = Inversion(inversion[0],inversion[1],inversion[2],inversion[3],inversion[4], inversion[5], inversion[6])
                    inversiones.append(nueva_inversion)
                return inversiones


    @classmethod
    def getAll(cls):
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute("SELECT * FROM inversion")
            invData = cursor.fetchall()
            if invData:
                inversiones = []
                for inversion in invData:
                    nueva_inversion = Inversion(inversion[0],inversion[1],inversion[2],inversion[3],inversion[4], inversion[5], inversion[6])
                    inversiones.append(nueva_inversion)
                return inversiones 


    def getMontoActual(self):
        
        fechaActual = Fecha.getFecha()
        fechaActual = fechaActual.fechaActual
        if fechaActual >= self.fechaFinal:
            return self.montoFinal
        tasa = Tasa.getByTId(str(self.tId))
        interesDiario = tasa.interesDiario
        fechaInicial = self.fechaInicial
        f = fechaActual-fechaInicial
        dias = f.days

        montoActual = self.montoInicial * (dias*(interesDiario/100)+1)
        return montoActual
        
    

    def finalizarInversion(self):
        pass
    

    def json(self):
        return{
                'iId' : self.iId,
                'cId' : self.cId,
                'fechaInicial' : self.fechaInicial,
                'fechaFinal' : self.fechaFinal,
                'tId' : self.tId,
                'montoInicial' : self.montoInicial,
                'montoFinal' : self.montoFinal
             }