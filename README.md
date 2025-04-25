# 🌍 Mundo de Wumpus - Sistema Baseado em Conhecimento (SBC)

[![Python Version](https://img.shields.io/badge/python-3.6%2B-blue)](https://www.python.org/)
[![Experta Version](https://img.shields.io/badge/experta-1.9.0-green)](https://pypi.org/project/experta/)

Bem-vindo ao Mundo de Wumpus, uma implementação do clássico jogo de inteligência artificial utilizando Sistemas Baseados em Conhecimento (SBC) com a biblioteca Experta.

Este projeto foi desenvolvido como parte de um estudo sobre Inteligência Artificial, com foco em SBCs.

Neste jogo, você assume o papel de um explorador em uma caverna 4x4 (podendo alterar o tamanho) cheia de perigos:
- ⚠️ Buracos sem fundo
- 👹 O temido Wumpus
- 💰 O valioso ouro dourado

## 📋 Índice
- [Instalação e Execução](#⚙️-instalação-e-execução)
- [Como Jogar](#🎮-como-jogar)
- [Arquitetura do Sistema](#🏗️-arquitetura-do-sistema)
- [Regras de Conhecimento](#🧠-regras-de-conhecimento)
- [Roadmap](#✨-roadmap)
- [Contribuição](#🤝-contribuição)

## ⚙️ Instalação e Execução

### Pré-requisitos
- Python 3.6 ou superior
- Biblioteca Experta (`pip install experta`)

### Passo a Passo
1. Clone o repositório:
   ```bash
   git clone https://github.com/nicmacedo/Mundo-de-Wumpus.git
   cd Mundo-de-Wumpus
   ```
2. Instale dependências:
   ```bash
   pip install experta
   ```
3. Execute o jogo:
   ```bash
   python joguin.py
   ```

## 🎮 Como Jogar

### 🕹️ Comandos Disponíveis
| Comando  | Descrição                                                                 | Exemplo                     |
|----------|---------------------------------------------------------------------------|-----------------------------|
| `mover`  | Move o agente na direção atual                                            | `mover direita`             |
| `girar`  | Altera a direção do agente                                                | `girar cima`                |
| `pegar`  | Coleta o ouro se estiver na mesma posição                                 | `pegar`                     |
| `atirar` | Dispara uma flecha (você tem apenas 1!)                                   | `atirar esquerda`           |
| `mapa`   | Mostra o mapa revelado até o momento                                      | `mapa`                      |
| `ajuda`  | Mostra esta lista de comandos                                             | `ajuda`                     |
| `sair`   | Encerra o jogo                                                            | `sair`                      |

### 🎯 Objetivo
Encontre o ouro na caverna e volte para a saída (posição [0,0]) sem:
- Cair em um buraco
- Ser pego pelo Wumpus

### 🚨 Percepções
O jogo avisa sobre perigos próximos:
- 🌬️ Brisa - Indica buraco nas adjacências
- 👃 Fedor - Wumpus está próximo
- 💡 Brilho - Ouro está nesta sala
- 😱 Grito - Você matou o Wumpus!

## 🏗️ Arquitetura do Sistema

### 📂 Estrutura de Arquivos
```bash
.
├── base_conhecimento.py    # Regras e fatos do SBC
├── joguin.py              # Lógica principal do jogo
└── README.md              # Este arquivo
```

### 🔧 Componentes Principais
1. MapaWumpus - Gerencia o tabuleiro e posicionamento dos elementos

2. JogoWumpus - Controla o fluxo do jogo e interface com usuário

3. RegrasJogo (SBC) - Motor de inferência com as regras do jogo

## 🧠 Regras de Conhecimento
O sistema utiliza regras de produção para tomar decisões:
```python
# Exemplo: Detectando o ouro
@Rule(Sensor(brilho=True))
def caverna_ouro(self):
    print("Você está na caverna do ouro")
    self.declare(Estado(pegarObj=True))
```
### 📋 Principais regras implementadas:

- Detecção de ouro e coleta automática
- Alerta de perigos próximos (fedor/brisa)
- Mecânica de disparo de flecha
- Verificação de vitória/derrota

📸 Exemplo do Código em Ação

### 🕹️ Início jogo:
![image](https://github.com/user-attachments/assets/94a01569-fd0a-4bb5-9d37-31a6d1b317fb)

#### 📋 Legenda:
| Imagem                                                                                   | Descrição                                            |
|------------------------------------------------------------------------------------------|------------------------------------------------------|
| ![image](https://github.com/user-attachments/assets/b6156e15-8e43-41d0-a86b-2d9a57a1c0f3) | 🗺️ Mostra sua posição atual e direção (🧭)          |
| ![image](https://github.com/user-attachments/assets/6a35b007-e80f-45e8-8f95-35b92cc244b3) | 🏹 Flechas restantes e status do ouro (💰/❌)        |
| ![image](https://github.com/user-attachments/assets/66015f8e-eb42-45a5-8799-3f08faada8ae) | 🔍 Condição da caverna atual (⚠️ Seguro/Perigoso)   |

### ✨ Melhorias Planejadas
- [ ] Interface gráfica

- [ ] Agente autônomo que joga sozinho

- [ ] Sistema de pontuação e ranking

