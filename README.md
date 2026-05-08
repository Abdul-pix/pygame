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

## Extra mechanics

- Willekeurig gegenereerde levels
- Shield power-ups
- Score gebaseerd op tijd
- Botsingen met platformen en objecten
- Zwaartekracht

## Klassenstructuur

Het project gebruikt objectgeoriënteerd programmeren met een abstracte hoofdklasse:

- `GameObject`
    - `Player`
    - `Enemy`
    - `Platform`
    - `Finish`
    - `PowerUp`

## Bestanden

- `main.py` → hoofdgame en game loop
- `game_object.py` → abstracte hoofdklasse + collision systeem
- `player.py` → speler
- `enemy.py` → vijand + lasers
- `platform.py` → platformen
- `finish.py` → finishlijn
- `powerups.py` → shield power-up
- `level_generator.py` → random level generator
- `score_manager.py` → score en tijd

## Groep

Naam: Abdulrahman Kadhim  
WPO-groep: 3
