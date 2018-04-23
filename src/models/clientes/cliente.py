from src.common.database import Database, CursorFromConnectionFromPool

class Cliente:
    def __init__(self, cId, nombre, saldoVista, saldoInvertido, nombrePromotor):
        self.cId = cId
        self.nombre = nombre
        self.saldoVista = saldoVista
        self.saldoInvertido = saldoInvertido
        self.nombrePromotor = nombrePromotor


    def __repr__(self):
        return "<Cliente>".format(self.nombre)


    @classmethod
    def getByCId(cls, cId):
        with CursorFromConnectionFromPool() as cursor:
                cursor.execute("SELECT * FROM cliente WHERE cId=%s", (cId,))
                cliente = cursor.fetchone()
                if cliente:
                    return cls(cId=cliente[0], nombre=cliente[1], saldoVista=cliente[2], saldoInvertido=cliente[3], nombrePromotor=cliente[4])


    def saveToDb(self):
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute("INSERT INTO cliente (nombre, saldoVista, saldoInvertido, nombrePromotor) VALUES (%s, %s, %s, %s) on conflict do nothing",(self.nombre, self.saldoVista, self.saldoInvertido, self.nombrePromotor))


    def updateSaldoVista(self, saldo):
        self.saldoVista = self.saldoVista + saldo
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute("UPDATE cliente set saldoVista = %s WHERE cId=%s", (self.saldoVista, self.cId))

    
    def json(self):
        return{
                'cId' : self.cId,
                'nombre' : self.nombre,
                'saldoVista' : self.saldoVista,
                'saldoInvertido' : self.saldoInvertido,
                'nombrePromotor' : self.nombrePromotor,
             }


    @classmethod
    def getClientesByPromotor(cls, nombrePromotor):
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute("SELECT * FROM cliente WHERE nombrePromotor = %s",(nombrePromotor,))
            clientsData = cursor.fetchall()
            if clientsData:
                clientes = []
                for cliente in clientsData:
                    nuevo_cliente = cls(cliente[0],cliente[1],cliente[2],cliente[3],cliente[4])
                    clientes.append(nuevo_cliente)
                return clientes 
    
    @classmethod
    def getAllClientes(cls):
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute("SELECT * FROM cliente")
            clientsData = cursor.fetchall()
            if clientsData:
                clientes = []
                for cliente in clientsData:
                    nuevo_cliente = cls(cliente[0],cliente[1],cliente[2],cliente[3],cliente[4])
                    clientes.append(nuevo_cliente)
                return clientes   