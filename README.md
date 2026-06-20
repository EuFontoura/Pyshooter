# Pyshooter

Uma recriação do clássico Endless War 3, originalmente desenvolvido em Flash para navegadores. Este projeto surgiu como parte de um trabalho acadêmico, cujo objetivo era desenvolver um jogo 2D Top-Down utilizando Python.

A escolha do Endless War 3 foi motivada pela variedade de mecânicas e conceitos presentes no jogo, proporcionando uma excelente oportunidade de estudo e prática em áreas como inteligência artificial, movimentação de personagens, detecção de colisões complexas, efeitos sonoros e gestão de estados de jogo.

Além de reproduzir a experiência do jogo original, o projeto serviu como uma forma de explorar o desenvolvimento de jogos com Python, utilizando a biblioteca Pygame, e aprofundar conhecimentos em programação orientada a objetos (POO) e arquitetura de software.

Foram usadas diversas tecnologias novas das quais não conhecia antes, como Pathfinding. Portanto, comentei fortemente e talvez exageradamente em alguns trechos do código, tanto para compartilhar o que aprendi quanto fixar o conhecimento e para revisar conteúdo posteriormente.

## 🛠️ Tech Stack

- **Linguagem:** Python 3
- **Biblioteca Gráfica:** Pygame
- **Algoritmos Aplicados:** Pathfinding (A-Star / A*) e Raycasting (Line of Sight)

## 🌟 Mecânicas Avançadas Implementadas

- **Máquina de Estados (State Machine):** Fluxo profissional de telas controlando o Loop Principal (Menu Principal > Tutorial > Gameplay > Telas de Vitória/Derrota).
- **Inteligência Artificial (A* Pathfinding):** Inimigos utilizam mapeamento de grade (Grid) e o algoritmo A* para desviar ativamente de paredes e obstáculos para encontrar o jogador.
- **Campo de Visão (Raycasting):** Inimigos respeitam a física do cenário, com visão periférica que é logicamente obstruída por paredes.
- **Level Design Modular:** Separação entre o mapa visual (Arte) e o mapa de dados (Colisão e Spawns baseados em código de cores RGB).
- **Trigonometria Balística:** Projéteis calculam dinamicamente a distância vetorial e o offset (deslocamento) da ponta da arma (muzzle) em direção à mira do mouse.

## 📌 Roadmap

- [x] Movimentação e animação do player
- [x] Movimentação e animação dos NPCs (Inimigos)
- [x] Animação e efeitos das armas (Muzzle flash)
- [x] Interface do usuário (HUD - Vida, Escudo, Munição)
- [x] Inteligência artificial avançada dos inimigos (A* e Visão Obstruível)
- [x] Criação do mapa, texturas separadas e colisões
- [x] Mecânica de disparo interativa (offset) e aplicação de dano
- [x] Sistema de munição, cadência (Fire Rate) e recarga (Reload)
- [x] Sistema de Extração Dinâmico (Ponto de fuga condicional)
- [x] Menu principal com gerenciador de estados e instruções

## 🚀 Status

✔️ **Fase 1 Concluída** (Versão base do trabalho acadêmico finalizada e funcional).

## ✒️ Autores

- [@EuFontoura](https://github.com/EuFontoura)