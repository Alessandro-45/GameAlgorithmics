class Pokemon:
    pass

class Pikachu(Pokemon):
    color = 'Amarillo' #No cambiar valor, por fis
    tipo = 'Electrico'

    def __init__(self, ataque:int, defensa:int, salud:int, velocidad:int, alias:str):

        self.alias = alias
        self.ataque = ataque
        self.defensa = defensa
        self.salud = salud
        self.velocidad = velocidad

    def MostrarInfo(self):
        print(f'Bienvenido, {self.alias} tiene las siguientes estadisticas:')
        print(f'Su ataque es: {self.ataque}')
        print(f'Su defensa es: {self.defensa}')
        print(f'Su salud es: {self.salud}')
        print(f'Su velocidad es: {self.velocidad}')

    def ImpacTrueno(self):
        print('Pikachiiii')



Pikachu1 = Pikachu(25, 12, 20, 22, 'Roberto')
Pikachu2 = Pikachu(7, 6, 8, 12, 'Juan')

Pikachu1.MostrarInfo()
Pikachu2.MostrarInfo()


