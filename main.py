#Imports
import pandas as pd
from tkinter import *

#Load Data
ingredient_data = pd.read_csv("ingredients.csv"); seasoning_data = pd.read_csv("seasonings.csv")
recipes = pd.read_csv("recipes.csv")

#Constants
min_ingredients = 1; max_ingredients = 6; max_seasonings = 4
level2 = 100; level3 = 2000

#Variable Setup
ingredients = []; seasonings = []
powers = {'egg': 0, 'catching': 0, 'exp': 0, 'item': 0, 'raid': 0, 'title': 0, 'sparkling': 0, 'humungo': 0, 'teensy': 0, 'encounter': 0}
flavors = {'sweet': 0, 'spicy': 0, 'bitter': 0, 'sour': 0, 'salty': 0}
types = {'grass': 0, 'water': 0, 'fire': 0, 'dragon': 0, 'dark': 0, 'steel': 0, 'fairy': 0,
    'electric': 0, 'ice': 0, 'ghost': 0, 'psychic': 0, 'poison': 0, 'normal': 0, 'fighting': 0, 'rock': 0, 'ground': 0, 'bug': 0, 'flying': 0}
#How are types matched to their associated powers?

#Selection - structured based on https://www.geeksforgeeks.org/dropdown-menus-tkinter/
playerdropdown = Tk()
playerdropdown.geometry("200x200")
playeroptions = [1,2,3,4]
clickedplayers = IntVar()
clickedplayers.set(1)
dropplayers = OptionMenu(playerdropdown,clickedplayers, *playeroptions)
dropplayers.pack()
labelplayers = Label(playerdropdown,text = "Number of Players:")
labelplayers.pack()
playerdropdown.mainloop()
num_players = playerdropdown.get()

for i in num_players*max_ingredients:
    ingredients.append("")
    ingredientdropdown = Tk()
    ingredientdropdown.geometry("200x200")
    ingredientoptions = ingredient_data['Name']
    clickedingredient = IntVar()
    clickedingredient.set(1)
    dropingredients = OptionMenu(ingredientdropdown,clickedingredient, *ingredientoptions)
    dropingredients.pack()
    labelingredient = Label(ingredientdropdown,text = "Ingredient #"+str(i)+":")
    labelingredient.pack()
    ingredientdropdown.mainloop()
    ingredients[i] = ingredientdropdown.get()

def calculate():
    #Remove blank entries
    for i,x in enumerate(ingredients):
        if x == "":
            ingredients[i].delete()
    for i,x in enumerate(seasonings):
        if x == "":
            seasonings[i].delete()

    #Check selection validity
    if (len(ingredients) < num_players * min_ingredients) or (len(seasonings) < num_players * min_ingredients):
        raise ValueError("You must select at least one ingredient and one seasoning per player.")
    elif (len(ingredients) > num_players * max_ingredients) or (len(seasonings) > num_players * max_seasonings):
        raise ValueError("Too many ingredients or seasonings were selected. Please submit a bug report at https://github.com/nuclearGoblin/arven/issues.")

    #Sum up selection
    for x in ingredients + seasonings:
        for y in powers + flavors + types:
            y += (ingredient_data + seasoning_data)[x][y]

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
    if sum([("Herba Mystica" in x) for x in seasonings]) < 2:
        powers['sparkling'] = 0; #reset to 0 to force it not to appear.

    #Get powers list
    powers.sort()
    types.sort()

    #Check if recipe exists as exception
    if [sorted(ingredients), sorted(seasonings)] in recipes:
        recipe = recipes[recipes == [ingredients,seasonings]]
        print("Recipe:",recipe["Name"])
        print(recipes[recipe][powers])
    else: #Print powers list
        typeoffset = 0
        for i in [1,2,3]:
            if powers[-i] >= level3:
                level = 3
            elif powers[-i] >= level2:
                level = 2
            elif powers[-i] >= 0:
                level = 1
            else:
                break
            if (powers[-i] == 'sparkling') or (powers[-i] == 'egg'):
                print(powers[-i],"power Lv.",level)
                typeoffset +=1 
                while types[-i+typeoffset] <= 0:
                    typeoffset += 1
                    if types[-1] == 0:
                        raise ValueError("No type had a value higher than any other type. Please submit a bug report at https://github.com/nuclearGoblin/arven/issues.")
            else:
                print(powers[-i]+":",types[-i+typeoffset],"Lv.",level)

button = Button(playerdropdown, text = "Calculate", command = calculate).pack()