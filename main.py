#Imports
import pandas as pd
ingredient_data = pd.read_csv("ingredients.csv"); seasosoning_data = pd.read_csv("seasonings.csv")

#Constants
min_ingredients = 1; max_ingredients = 6; max_seasonings = 4
level2 = 100; level3 = 2000

#Variable Setup
ingredients = []; seasonings = []
num_players = 1
powers = {'egg': 0, 'catching': 0, 'exp': 0, 'item': 0, 'raid': 0, 'title': 0, 'sparkling': 0, 'humungo': 0, 'teensy': 0, 'encounter': 0}
flavors = {'sweet': 0, 'spicy': 0, 'bitter': 0, 'sour': 0, 'salty': 0}
types = {'grass': 0, 'water': 0, 'fire': 0, 'dragon': 0, 'dark': 0, 'steel': 0, 'fairy': 0,
    'electric': 0, 'ice': 0, 'ghost': 0, 'psychic': 0, 'poison': 0, 'normal': 0, 'fighting': 0, 'rock': 0, 'ground': 0, 'bug': 0, 'flying': 0}
#How are types matched to their associated powers?

#Selection

#Check selection validity
if len(ingredients) < num_players * min_ingredients:
    raise ValueError("You must select at least one ingredient per player.")
elif (len(ingredients) > num_players * max_ingredients) or (len(seasonings) > num_players * max_seasonings):
    raise ValueError("Too many ingredients or seasonings were selected. Please submit a bug report at https://github.com/nuclearGoblin/arven/issues.")

#Sum up selection
for x in ingredients + seasonings:
    for y in powers + flavors + types:
        y += x[y]

#once quantifiable, program in reductions caused by the use of too many ingredients.

#apply bonus from flavor
#do bonuses for combinations only apply on a tie?
if max(flavors) == 'sweet':
    powers['egg'] += 100
elif max(flavors) == 'spicy':
    powers['humungo'] += 100
elif max(flavors) == 'bitter':
    powers['item'] += 100
elif max(flavors) == 'sour':
    powers['teensy'] += 100
elif max(flavors) == 'salty':
    powers['encounter'] += 100
elif max(flavors) == ['sweet','sour']:
    powers['catching'] += 100
elif max(flavors) == ['salty','bitter']:
    powers['exp'] += 100
elif max(flavors) == ['spicy','sweet']:
    powers['raid'] += 100

#Check if sparkling power is permitted
if sum([("Herba Mystica" in x) for x in ingredients]) < 2:
    powers['sparkling'] = 0; #reset to 0 to force it not to appear.

#Get powers list