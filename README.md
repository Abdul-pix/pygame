# RUN.EXE

2D platformspel gemaakt in Python met pygame.

## Gameplay

De speler beweegt met:
- ← →
- ↑ of spatie om te springen
- ENTER om het spel te starten of opnieuw te starten

Het doel van het spel is om zo snel mogelijk de finish te bereiken zonder:
- in een gat te vallen
- geraakt te worden door de vijand
- geraakt te worden door lasers

Hoe sneller je de finish bereikt, hoe hoger je score.

## Enemy AI

De vijand gebruikt simpele AI:
- volgt de speler automatisch
- springt over gaten
- wordt sneller naarmate de tijd stijgt
- schiet horizontale lasers richting de speler
- respawnt als hij van het level valt
- gebruikt een state machine: patrol-state als de speler ver weg is, 
  chase-state als de speler dichtbij is
  
## Smart Design

Het spel gebruikt verschillende vormen van rule-based Smart Design:

- De bewegende Enemy gebruikt patrol/chase states.
- De Enemy berekent de richting en afstand tot de speler.
- De Enemy detecteert gaten en springt automatisch.
- De Enemy wordt geleidelijk sneller.
- De TurretEnemy gebruikt idle/attack states.
- De TurretEnemy bewaakt een gebied en schiet als de speler binnen bereik komt.
- De levelgenerator bouwt willekeurige levels binnen vaste speelbaarheidsgrenzen.

## Extra mechanics

- Willekeurig gegenereerde levels
- Shield power-ups
- Score gebaseerd op tijd
- Botsingen met platformen en objecten
- Zwaartekracht

## Klassenstructuur

Het project gebruikt objectgeoriënteerd programmeren met een abstracte hoofdklasse:

GameObject
├── Player
├── Enemy
├── TurretEnemy
├── Platform
├── Finish
└── PowerUp

Game
LevelGenerator
ScoreManager

## Bestanden

- `main.py` → hoofdgame en game loop
- `game_object.py` → abstracte hoofdklasse + collision systeem
- `player.py` → speler
- `enemy.py` → vijand + lasers
- `turret_enemy.py` → 2de vijand en lasers
- `platforms.py` → platformen
- `finish.py` → finishlijn
- `powerups.py` → shield power-up
- `level_generator.py` → random level generator
- `score_manager.py` → score en tijd

## Groep

Naam: Abdulrahman Kadhim  
WPO-groep: 3

## GitHub

https://github.com/Abdul-pix/pygame
