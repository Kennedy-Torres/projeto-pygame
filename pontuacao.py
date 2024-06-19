class Pontuacao:
    def __init__(self):
        self.pontos = 0
        self.recorde = 0

    def adicionar_ponto(self):
        self.pontos += 1

    def resetar_pontos(self):
        self.pontos = 0

    def atualizar_recorde(self):
        if self.pontos > self.recorde:
            self.recorde = self.pontos
