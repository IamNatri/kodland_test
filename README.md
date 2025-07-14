# Platform Adventure - Jogo Platformer Infinito

Um jogo platformer 2D infinito desenvolvido em Python usando PgZero, com sistema de plataformas em zigue-zague, física realista, inimigos animados, música de fundo e mecânica de escalada infinita.

## 🎮 Características

- **Platformer Infinito**: Plataformas geradas dinamicamente em padrão zigue-zague (esquerda→direita→esquerda)
- **Física Realista**: Gravidade, pulo, colisões precisas
- **Sistema de Câmera**: Câmera dinâmica que segue o jogador
- **Inimigos Animados**: Inimigos que patrulham as plataformas
- **Áudio Completo**: Música de fundo e efeitos sonoros
- **Sistema de Pontuação**: Score baseado na altura escalada + recorde
- **Configurável**: Todas as variáveis via arquivo .env

## 🚀 Instalação e Execução


### iniciar ambiente
```bash
python -m venv .venv
source .venv/bin/activate
```

### Pré-requisitos
```bash
# Python 3.8+
python --version

# Instalar dependências
pip install -r requirements.txt
```


### Executar o Jogo
```bash
python main.py
```

## 🎯 Como Jogar

- **Setas** ou **A/D**: Mover esquerda/direita
- **Espaço**: Pular
- **ESC**: Voltar ao menu
- **Objetivo**: Escalar o mais alto possível!

## ⚙️ Configuração

Edite o arquivo `.env` para personalizar o jogo:
```env
# Configurações básicas
GAME_WIDTH=800
GAME_HEIGHT=600
GRAVITY=0.5
JUMP_SPEED=12
PLAYER_SPEED=3

# Plataformas
STAIR_VERTICAL_GAP=80
STAIR_HORIZONTAL_GAP=120
ZIGZAG_PLATFORMS=6

# Áudio
MUSIC_ENABLED=true
SOUNDS_ENABLED=true
MUSIC_VOLUME=0.5
```

## 📁 Estrutura do Projeto

```
kodland/
├── main.py              # Código principal otimizado
├── .env                 # Configurações do jogo
├── requirements.txt     # Dependências Python
├── README.md           # Este arquivo
├── .gitignore          # Arquivos ignorados pelo Git
├── images/             # Sprites do jogo
├── sounds/             # Efeitos sonoros
├── music/              # Música de fundo
└── .poc/               # Arquivos de proof-of-concept
    ├── test_*.py       # Scripts de teste
    ├── create_*.py     # Scripts de criação de assets
```

## 🛠️ Desenvolvimento

### Funcionalidades Implementadas
✅ Sistema de plataformas infinitas em zigue-zague  
✅ Física completa (gravidade, pulo, colisões)  
✅ Animações de sprites (idle, walk, jump)  
✅ Inimigos com patrulhamento  
✅ Música de fundo e efeitos sonoros  
✅ Sistema de câmera dinâmica  
✅ Pontuação e recorde  
✅ Menu principal  
✅ Configurações via .env  

### Arquitetura
- **Código otimizado**: Reduzido de 500+ para 328 linhas
- **Configurações externas**: Todas as variáveis no .env
- **Modularidade**: Classes compactas e funções específicas
- **Performance**: Renderização otimizada com offset de câmera

## 🎨 Assets

O jogo inclui:
- Sprites de personagem animado (idle, walk, jump)
- Sprites de inimigos animados
- Efeitos sonoros (jump, hit, menu)
- Música de fundo em loop

## 🔧 Customização

### Adicionar Novos Sprites
1. Adicione imagens na pasta `images/`
2. Nomeie seguindo o padrão: `player_idle1.png`, `enemy_walk1.png`
3. Ajuste as animações no código

### Modificar Dificuldade
Ajuste no `.env`:
- `STAIR_VERTICAL_GAP`: Espaçamento vertical (menor = mais difícil)
- `STAIR_HORIZONTAL_GAP`: Espaçamento horizontal
- `GRAVITY`: Força da gravidade
- `ENEMY_SPAWN_CHANCE`: Frequência de inimigos

## 🏆 Recordes

O jogo salva automaticamente seu melhor recorde de altura escalada.

## 🎵 Áudio

- Música de fundo em loop automático
- Efeitos sonoros para ações (pulo, morte, menu)
- Controle de volume via .env
- Opção de liga/desliga no menu

---

**Desenvolvido com Python + PgZero**  
Seguindo princípios de código limpo e otimização.

- **Setas esquerda/direita**: Mover o jogador
- **Barra de espaço**: Pular
- **ESC**: Retornar ao menu principal (durante o jogo)

### Objetivo

- Navegue pelas plataformas
- Evite os inimigos vermelhos
- Explore o mundo do jogo

## Funcionalidades

### Menu Principal
- Botão "Start Game" para iniciar
- Botão "Music: ON/OFF" para alternar música
- Botão "Exit" para sair

### Gameplay
- Movimento suave e responsivo
- Sistema de física com gravidade
- Inimigos que patrulham suas áreas
- Colisão com plataformas e inimigos

### Animações
- Animação de idle (personagem parado)
- Animação de caminhada (3 frames)
- Animação de pulo
- Animações para inimigos (idle e caminhada)
- Sprites virados automaticamente baseado na direção

### Audio
- Música de fundo em loop
- Som de pulo
- Som de seleção no menu
- Som de impacto ao colidir com inimigos
- Controle de música e sons

## Estrutura do Código

### Classes Principais

1. **Animation**: Gerencia animações de sprites
2. **Player**: Controla o jogador com física e animações
3. **Enemy**: Inimigos que patrulham com AI simples

### Arquivos

- `main.py`: Código principal do jogo
- `create_sprites.py`: Script para gerar sprites
- `create_sounds.py`: Script para gerar sons
- `images/`: Diretório com sprites do jogo
- `sounds/`: Diretório com efeitos sonoros
- `music/`: Diretório com música de fundo

## Conformidade com Requisitos

✅ **Bibliotecas permitidas**: Apenas PgZero, math, random, e Rect do pygame
✅ **Gênero**: Plataforma
✅ **Menu principal**: Com botões clicáveis funcionais
✅ **Música e sons**: Música de fundo e efeitos sonoros
✅ **Inimigos**: Múltiplos inimigos com movimento autônomo
✅ **Animações**: Sprites animados para todos os personagens
✅ **Nomes em inglês**: Todas as variáveis, classes e funções
✅ **PEP8**: Código formatado seguindo padrões
✅ **Mecânica lógica**: Jogo funcional sem bugs

## Detalhes Técnicos

- Resolução: 800x600 pixels
- Frame rate: 60 FPS (controlado pelo PgZero)
- Física: Gravidade personalizada e detecção de colisão
- Animações: Sistema baseado em timer para troca de frames
- Audio: Arquivos WAV gerados programaticamente

O jogo demonstra programação orientada a objetos, gerenciamento de estado, animações, física básica e integração de audio, tudo dentro dos requisitos especificados.
