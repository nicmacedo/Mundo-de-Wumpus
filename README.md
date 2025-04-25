# 🌍 Mundo de Wumpus - Sistema Baseado em Conhecimento (SBC)

Bem-vindo ao Mundo de Wumpus, um jogo clássico reimaginado utilizando Sistemas Baseados em Conhecimento (SBC) com a biblioteca experta.

Aqui, você assume o papel de um explorador em uma caverna cheia de perigos: buracos, o temido Wumpus e... o tão desejado OURO! 🏆

Este projeto foi desenvolvido como parte de um estudo sobre Inteligência Artificial, com foco em SBCs.

## 🚀 Como Jogar

Comandos disponíveis:

| Comando | Descrição |
|---------|-----------|
| `mover` | Move o agente para uma das direções: esquerda, direita, cima ou baixo. |
| `girar` | Altera a direção do agente para: esquerda, direita, cima ou baixo. |
| `pegar` | Coleta o ouro se estiver na mesma posição do agente. |
| `atirar` | Dispara uma flecha na direção escolhida. |
| `mapa`  | Mostra o mapa conhecido até o momento. |
| `ajuda` | Lista todos os comandos disponíveis. |
| `sair`  | Encerra o jogo. |

### 🧠 Sobre a Inteligência
O jogo utiliza regras de produção (SBC) para determinar:

- Quando você encontra ouro 💰

- Quando um monstro ou buraco está próximo (fedor/brisa)

- Quando a flecha acerta ou erra o Wumpus 🏹

- Quando você morre 💀 ou vence o jogo 🏆

Exemplo de regra:

```python
@Rule(Sensor(brilho=True))
def caverna_ouro(self):
    print("Você está na caverna do ouro")
    self.declare(Estado(pegarObj=True))
```

#### ✨ To-Do / Melhorias Futuras
- [ ] Implementar uma interface gráfica (quem sabe um dia? 😂)

- [ ] Agente inteligente que joga sozinho

- [ ] Ranking de pontuação

