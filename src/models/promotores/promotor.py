from src.common.database import Database, CursorFromConnectionFromPool

class Promotor:
    def __init__(self, nombre, password, isAdmin):
        self.nombre = nombre
        self.password = password
        self.isAdmin = isAdmin


    def __repr__(self):
        return "<Promotor>".format(self.nombre)


    @classmethod
    def getByNombre(cls, nombre):
        with CursorFromConnectionFromPool() as cursor:
                cursor.execute("SELECT * FROM promotor WHERE nombre=%s", (nombre,))
                promotor = cursor.fetchone()
                if promotor:
                    return cls(nombre=promotor[0], password=promotor[1], isAdmin=promotor[2])


    def saveToDb(self):
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute("INSERT INTO promotor (nombre, password, isAdmin) VALUES (%s, %s, %s) on conflict do nothing",(self.nombre, self.password, self.isAdmin))


    def json(self):
        return{
                'nombre': self.nombre,
                'password': self.password,
                'isAdmin':self.isAdmin
             }
     

    def loginValid(nombre, password):
        promotor = Promotor.getByNombre(nombre)
        if promotor:
            if promotor.password == str(password):
                return True
        return False
