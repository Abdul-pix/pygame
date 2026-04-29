# 2D spel gemaakt in Python met pygame

Dit is een klein 2D platformspel gemaakt in Python met pygame.  
Je loopt links en rechts met ← → en je springt met ↑ of spatie.  
Je kunt het spel starten met Enter. Het doel van het spel is om zo snel mogelijk de finish te bereiken zonder in een gat te vallen of geraakt te worden door de vijand. Hoe sneller je finisht, hoe meer punten je krijgt.

De vijand gebruikt simpele AI:  
- hij volgt je  
- hij springt als jij ook springt  
- hij wordt sneller naarmate de tijd stijgt  
- hij respawnt als hij valt

Het level wordt willekeurig gegenereerd zodat elke run anders is.

# Bestanden
- main.py: hoofdprogramma
- player.py: speler
- enemy.py: vijand
- platform.py: platformen
- level_generator.py: maakt het level
- finish.py: eindpunt
- score_manager.py: score en tijd

# Groep
Naam: Abdulrahman Kadhim  
WPO-groep: 3
