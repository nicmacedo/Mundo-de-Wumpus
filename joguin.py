from experta import *
from base_conhecimento import Sensor, Estado, RegrasJogo
import random

class MapaWumpus:
    def __init__(self, tamanho=4):  
        self.tamanho = tamanho
        self.mapa = [[[] for _ in range(self.tamanho)] for _ in range(self.tamanho)]
        self.mapa_revelado = [[False for _ in range(self.tamanho)] for _ in range(self.tamanho)]
        self.memoria = [[[] for _ in range(self.tamanho)] for _ in range(self.tamanho)]
        self.posicao_agente = (0, 0)
        self.direcao = 'direita'
        self.flechas = 1
        self.ouro_coletado = False
        self.criar_mapa()
        
    def criar_mapa(self):
        # Posiciona o ouro
        self.ouro_pos = (random.randint(1, self.tamanho-1), (random.randint(1, self.tamanho-1)))
        self.mapa[self.ouro_pos[0]][self.ouro_pos[1]].append('ouro')
        
        # Posiciona o Wumpus
        self.wumpus_pos = (random.randint(1, self.tamanho-1), (random.randint(0, self.tamanho-1)))
        while self.wumpus_pos == self.ouro_pos:
            self.wumpus_pos = (random.randint(1, self.tamanho-1), (random.randint(0, self.tamanho-1)))
        self.mapa[self.wumpus_pos[0]][self.wumpus_pos[1]].append('wumpus')
        
        # Posiciona os buracos
        for _ in range(2):
            buraco_pos = (random.randint(0, self.tamanho-1), (random.randint(0, self.tamanho-1)))
            while buraco_pos == (0, 0) or buraco_pos == self.ouro_pos or buraco_pos == self.wumpus_pos or 'buraco' in self.mapa[buraco_pos[0]][buraco_pos[1]]:
                buraco_pos = (random.randint(0, self.tamanho-1), (random.randint(0, self.tamanho-1)))
            self.mapa[buraco_pos[0]][buraco_pos[1]].append('buraco')
        
        # Adiciona percepções adjacentes
        self.adicionar_percepcoes()
    
    def adicionar_percepcoes(self):
        direcoes = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for i in range(self.tamanho):
            for j in range(self.tamanho):
                if 'wumpus' in self.mapa[i][j]:
                    for di, dj in direcoes:
                        ni, nj = i + di, j + dj
                        if 0 <= ni < self.tamanho and 0 <= nj < self.tamanho:
                            if 'fedor' not in self.mapa[ni][nj]:
                                self.mapa[ni][nj].append('fedor')
                if 'buraco' in self.mapa[i][j]:
                    for di, dj in direcoes:
                        ni, nj = i + di, j + dj
                        if 0 <= ni < self.tamanho and 0 <= nj < self.tamanho:
                            if 'brisa' not in self.mapa[ni][nj]:
                                self.mapa[ni][nj].append('brisa')
    
    '''Permite a movimentação'''
    def mover_agente(self, direcao):
        x, y = self.posicao_agente
        nova_x, nova_y = x, y

        if direcao == 'direita':
            nova_y += 1
        elif direcao == 'esquerda':
            nova_y -= 1
        elif direcao == 'cima':
            nova_x -= 1
        elif direcao == 'baixo':
            nova_x += 1

        if 0 <= nova_x < self.tamanho and 0 <= nova_y < self.tamanho:
            self.posicao_agente = (nova_x, nova_y)
            print(f"Movendo para {self.posicao_agente}")
            return True
        else:
            print("Movimento inválido - você bateu na parede!")
            return False    
    
    '''Faz com que gire (Acabei nem usando, mas funciona e como pedia no exemplo deixei KKKKK)'''
    def girar_agente(self, direcao):
        direcoes_validas = ['esquerda', 'direita', 'cima', 'baixo']
        if direcao in direcoes_validas:
            self.direcao = direcao
            print(f"Virando para {self.direcao}")
            return True
        else:
            print("Direção inválida!")
            return False
    
    '''Permite que colete o ouro'''
    def pegar_ouro(self):
        x, y = self.posicao_agente
        if 'ouro' in self.mapa[x][y]:
            self.mapa[x][y].remove('ouro')
            self.ouro_coletado = True
            print("Ouro coletado!")
            return True
        else:
            print("Não há ouro aqui para pegar!")
            return False
    
    '''Permite que atire a flecha'''
    def atirar_flecha(self, direcao):
        if self.flechas > 0:
            self.flechas -= 1
            x, y = self.posicao_agente
            wumpus_x, wumpus_y = self.wumpus_pos

            '''Verifica se o wumpus esta na direção que a flecha foi atirada e o mata se for'''
            if (direcao == 'direita' and y < wumpus_y and x == wumpus_x) or \
                (direcao == 'esquerda' and y > wumpus_y and x == wumpus_x) or \
                (direcao == 'cima' and x > wumpus_x and y == wumpus_y) or \
                (direcao == 'baixo' and x < wumpus_x and y == wumpus_y):
                print("Você matou o Wumpus!")
                self.mapa[wumpus_x][wumpus_y].remove('wumpus')
                self.mapa[wumpus_x][wumpus_y].append('grito')
                self.adicionar_percepcoes()
                return True
            else:
                print("Flecha não acertou nada!")
                return False
        else:
            print("Você não tem mais flechas!")
            return False
    
    '''Permite sair da caverna na saída (0,0)'''
    def sair_caverna(self):
        if self.posicao_agente == (0, 0):
            print("Saindo da caverna...")
            return True
        else:
            print("Você só pode sair da caverna a partir da posição (0,0)!")
            return False
    
    '''Verifica se a caverna atual tem algum perigo ou outro efeito'''
    def verificar_perigo(self):
        x, y = self.posicao_agente
        celula = self.mapa[x][y]
        self.mapa_revelado[x][y] = True
    
        # Atualiza memória com as percepções atuais
        self.memoria[x][y] = []
        if 'fedor' in celula:
            self.memoria[x][y].append('fedor')
        if 'brisa' in celula:
            self.memoria[x][y].append('brisa')
        if 'grito' in celula:
            self.memoria[x][y].append('grito')
        
        if 'wumpus' in celula:
            print("Você encontrou o Wumpus!")
            self.jogando = False
            return 'monstro'
        elif 'buraco' in celula:
            print("Você caiu em um buraco!")
            self.jogando = False
            return 'buraco'
        elif 'ouro' in celula:
            print("Você vê um brilho de ouro!")
            return 'ouro'
        else:
            percepcoes = []
            if 'fedor' in celula:
                percepcoes.append("Você sente um fedor horrível.")
            if 'brisa' in celula:
                percepcoes.append("Você sente uma brisa suave.")
            if 'grito' in celula:
                percepcoes.append("Você ouve um grito agonizante.")
            
            if percepcoes:
                print("\n".join(percepcoes))
            else:
                print("Esta caverna parece segura.")
            
            return 'seguro'

'''Inicia o jogo definindo as coisas'''
class JogoWumpus:
    def __init__(self, tamanho=4):  # Adicione o parâmetro aqui
        self.tamanho = tamanho  # Armazene como atributo
        self.mapa = MapaWumpus(tamanho)  # Passe o tamanho para o mapa
        self.engine = RegrasJogo()
        self.engine.reset()
        self.jogando = True
        self.mapa_revelado = [[False for _ in range(self.tamanho)] for _ in range(self.tamanho)]
        self.memoria = [[[] for _ in range(self.tamanho)] for _ in range(self.tamanho)]
        self.mapa_revelado[0][0] = True  # Posição inicial já revelada
    
    '''Atualiza os sensores de acordo com a posição atual'''
    def atualizar_sensores(self):
        x, y = self.mapa.posicao_agente
        celula = self.mapa.mapa[x][y]
        
        # Limpa fatos anteriores
        for fato in self.engine.facts:
            if isinstance(fato, Sensor):
                self.engine.retract(fato)
        
        # Adiciona novos fatos sensoriais
        sensores = {
            'brilho': 'ouro' in celula,
            'buraco': 'buraco' in celula,
            'monstro': 'wumpus' in celula,
            'grito': 'grito' in celula,
            'fedor': 'fedor' in celula,
            'brisa': 'brisa' in celula
        }
        
        self.engine.declare(Sensor(**sensores))
    
    '''Permite ver um mapa que atualiza com base no aprendizado dos caminhos já percorridos'''
    def mostrar_mapa(self):
        print("\nMapa Conhecido:")
        print("  " + " ".join(str(i) for i in range(self.tamanho)))
        for i in range(self.tamanho):
            linha = str(i) + " "
            for j in range(self.tamanho):
                if (i, j) == self.mapa.posicao_agente:
                    linha += "A "  # Agente
                elif not self.mapa.mapa_revelado[i][j]:
                    linha += "? "  # Desconhecido
                elif 'wumpus' in self.mapa.mapa[i][j] and self.mapa.mapa_revelado[i][j]:
                    linha += "W "  # Wumpus
                elif 'buraco' in self.mapa.mapa[i][j] and self.mapa.mapa_revelado[i][j]:
                    linha += "B "  # Buraco
                elif 'ouro' in self.mapa.mapa[i][j] and self.mapa.mapa_revelado[i][j]:
                    linha += "O "  # Ouro
                else:
                    percepcoes = self.mapa.memoria[i][j]
                    if not percepcoes:
                        linha += ". "  # Seguro
                    else:
                        linha += "P "  # Perigo (fedor/brisa)
            print(linha)
        print("Legenda: A=Você, ?=Desconhecido, W=Wumpus, B=Buraco, O=Ouro, P=Perigo, .=Seguro")
    
    '''Define as ações possíveis de fazer no jogo'''
    def executar_acao(self, acao):
        if acao == 'mover':
            print("Direções disponíveis: esquerda, direita, cima, baixo")
            while True:
                direcao = input("Para qual direção você quer mover? ").lower().strip()
                if direcao in ['esquerda', 'direita', 'cima', 'baixo']:
                    if self.mapa.mover_agente(direcao):
                        return True
                    else:
                        print("Não foi possível mover nessa direção!")
                        return False
                else:
                    print("Direção inválida! Tente novamente.")
        
        elif acao == 'girar':
            print("Direções disponíveis: esquerda, direita, cima, baixo")
            while True:
                direcao = input("Para qual direção? ").lower().strip()
                if direcao in ['esquerda', 'direita', 'cima', 'baixo']:
                    self.mapa.girar_agente(direcao)
                    return True
                print("Direção inválida! Tente novamente.")
        
        elif acao == 'pegar':
            if self.mapa.pegar_ouro():
                return True
            print("Não há ouro aqui para pegar!")
            return False
        
        elif acao == 'atirar':
            print("Direções disponíveis para atirar: esquerda, direita, cima, baixo")
            while True:
                direcao = input("Para qual direção você quer atirar? ").lower().strip()
                if direcao in ['esquerda', 'direita', 'cima', 'baixo']:
                    if self.mapa.atirar_flecha(direcao):
                        return True
                    else:
                        print("Não foi possível atirar!")
                        return False
                else:
                    print("Direção inválida! Tente novamente.")
    
    '''Verifica se esta vivo'''
    def verificar_estado_jogo(self):
        # Verifica se o agente morreu
        for fato in self.engine.facts:
            if isinstance(fato, Estado) and not fato['vida']:
                print("Fim de jogo! Você morreu.")
                self.jogando = False
                return
        
        # Verifica se o agente saiu com o ouro
        for fato in self.engine.facts:
            if isinstance(fato, Estado) and fato['sair'] and fato['ouro']:
                print("Parabéns! Você venceu o jogo!")
                self.jogando = False
                return
    
    '''Auxiliar para ver comandos disponiveis no jogo'''
    def mostrar_ajuda(self):
        print("\n=== COMANDOS DISPONÍVEIS ===")
        print("mover   - Avança uma casa na direção atual")
        print("girar   - Muda sua direção")
        print("pegar   - Coleta o ouro se estiver na mesma casa")
        print("atirar  - Dispara uma flecha na direção atual")
        print("mapa    - Mostra o mapa conhecido")
        print("ajuda   - Mostra esta mensagem")
        print("sair    - Termina o jogo")
        print("\nDireções disponíveis: esquerda, direita, cima, baixo")
    
    '''Jogo rolando'''
    def iniciar(self):
        print("Bem-vindo ao Jogo do Wumpus!")
        print("Você está na posição (0,0), olhando para a direita.")
        print("Digite 'ajuda' para ver os comandos disponíveis.\n")
        
        while self.jogando:
            # Atualiza sensores e motor de inferência
            self.atualizar_sensores()
            self.engine.run()
            
            # Mostra informações atuais
            x, y = self.mapa.posicao_agente
            print(f"\nPosição atual: ({x},{y}) - Direção: {self.mapa.direcao}")
            print(f"Flechas restantes: {self.mapa.flechas}")
            print(f"Ouro coletado: {'Sim' if self.mapa.ouro_coletado else 'Não'}")
            
            # Verifica perigos e mostra percepções
            self.mapa.verificar_perigo()
            
            # Pede ação do jogador - versão simplificada
            while True:
                acao = input("\nO que você quer fazer? ").lower().strip()

                if acao == 'ajuda':
                    self.mostrar_ajuda()
                    continue
                elif acao == 'mapa':
                    self.mostrar_mapa()
                    continue
                elif acao == 'sair':
                    self.jogando = False
                    break
                elif acao in ['mover', 'pegar', 'atirar']:
                    if self.executar_acao(acao):
                        break
                elif acao == 'girar':
                    self.executar_acao(acao)
                    break
                else:
                    print("Comando inválido! Digite 'ajuda' para ver os comandos.")
            
            # Verifica se o jogo terminou
            self.verificar_estado_jogo()

'''Iniciando o jogo'''
if __name__ == "__main__":
    jogo = JogoWumpus()
    jogo.iniciar()