from experta import *

class Sensor(Fact):
    """Fatos sensoriais do ambiente"""
    brilho = Field(bool, default=False)
    buraco = Field(bool, default=False)
    monstro = Field(bool, default=False)
    grito = Field(bool, default=False)
    fedor = Field(bool, default=False)
    brisa = Field(bool, default=False)

class Estado(Fact):
    """Estado atual do agente"""
    pegarObj = Field(bool, default=False)
    sair = Field(bool, default=False)
    ouro = Field(bool, default=False)
    atirar = Field(bool, default=False)
    vida = Field(bool, default=True)

class RegrasJogo(KnowledgeEngine):
    """Detectar se esta na caverna do ouro"""
    @Rule(Sensor(brilho=True))
    def cavernaOuro(self):
        print("Você está na caverna do ouro")
        self.declare(Estado(pegarObj=True))
    """Se estiver na caverna do ouro"""
    @Rule(
        AS.sensor << Sensor(brilho=True),  
        Estado(pegarObj=True)
    )
    def pegarOuro(self, sensor):  
        print("Ouro coletado")
        self.declare(Estado(ouro=True))
        self.retract(sensor) 

    '''Detectar se esta na saida com o ouro'''
    @Rule(Estado(sair=True), Estado(ouro=True), salience=-1)
    def saida(self):
        print("Você saiu com o ouro! Vitória!")

    '''Detectar se é possível atirarm e atira'''
    @Rule(Estado(atirar=True), salience=-10)
    def atirarFlecha(self): 
        print("Flecha lançada!")
        self.modify(Estado(atirar=False)) 

    '''Detectar se a flecha acertou o monstro'''
    @Rule(Sensor(grito=True), salience=-10)
    def monstroMorto(self):
        print("Wumpus morto!")
        self.retract(Sensor(monstro=True))

    '''Detectar se existe fedor na sala (monstro próximo)'''
    @Rule(Sensor(fedor=True), salience=-1)
    def alertaMonstro(self):
        print("Monstro próximo!")

    '''Detectar se existe brisa na sala (buraco próximo)'''
    @Rule(Sensor(brisa=True), salience=-1)
    def alertaBuraco(self):
        print("Buraco próximo!")

    '''Detectar se entrou em uma caverna com monstro ou buraco'''
    @Rule(OR(Sensor(buraco=True), Sensor(monstro=True)), salience=-1000)
    def cavernaPerigosa(self): 
        print("Você morreu!")
        self.declare(Estado(vida=False, sair=False, pegarObj=False))

# Teste:
'''
engine = RegrasJogo()
engine.reset()
engine.declare(Sensor(brilho=True))  # Exemplo: agente entrou na caverna do ouro
engine.run()
'''