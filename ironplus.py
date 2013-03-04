from modbuilder import *

ironworking = Menu("Ironworking")
blades = Menu("Iron Blades", "S")
armor = Menu("Iron Armor", "A")

fire = Tool("Fire", note="+lit nearby")
torch = Ingredient("Torch", note="+to transfer the flame")
anvil = GTool("Anvil", note="+nearby")
hammer = Tool("Hammer")
stake = Ingredient("Wooden Stake", note="+for a handle")
staff = Ingredient("Staff", note="+for a handle")
knife = Tool("Knife")

charcoal = lambda *args, **kwargs: GIngredient("Charcoal", *args, **kwargs)
bloom = lambda *args, **kwargs: Ingredient("Bloom of Iron", *args, **kwargs)
wrought = lambda *args, **kwargs: Ingredient("Wrought Iron", *args, **kwargs)
cord = lambda *args, **kwargs: Ingredient("Tying equipment", *args, **kwargs)


all_recipes = []

class BuildRecipe(Recipe):
    def __init__(self, menu, name):
        super(BuildRecipe, self).__init__(menu, name)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        all_recipes.append(self)

    def haf(self):
        self.add(hammer)
        self.add(anvil)
        self.add(fire)

with BuildRecipe(ironworking, "Bog Iron") as r:
    r.key = "1"
    r.base = "Stone"
    r.skill = "SURVIVAL"
    r.time = 90

    r.add(Tool("Shovel"))
    r.add(Tool("[TERRAIN:spruce_mire pine_mire open_mire]",
               note="Be in a Mire"))

with BuildRecipe(ironworking, "Charcoal") as r:
    r.key = "2"
    r.amount = 20
    r.base = "Firewood"
    r.skill = "SURVIVAL"
    r.time = 45
    r.waittime = "5d"
    r.skillfreq = -1
    r.patch = 5

    r.add(GIngredient("Slender trunk", 3, note="+for a chimney"))
    r.add(PGIngredient("Firewood", 50, note="+piled around it"))
    r.add(Tool("Shovel", note="+to cover it all in soil"))
    r.add(fire)
    r.add(torch)

with BuildRecipe(ironworking, "Smelt Iron") as r:
    r.key = "3"
    r.amount = 2
    r.base = "Rock"
    r.skill = "SURVIVAL"
    r.time = "1h"
    r.waittime = "1d"
    r.skillfreq = "-1"
    r.patch = 5

    r.add(Tool("Shovel", note="+to dig a pit"))
    r.add(PIngredient("Bog Iron", extra="[name:Bloom of Iron]"))
    r.add(charcoal(10, patchwise=True))
    r.add(fire)
    r.add(torch)

with BuildRecipe(ironworking, "Hammer Bloom") as r:
    r.key = "4"
    r.base = "Rock"
    r.skill = "CLUB"
    r.time = "3h"
    r.patch = 5

    r.add(bloom(patchwise=True, extra="[name:Wrought Iron]"))
    r.add(charcoal(6, patchwise=True))
    r.haf()

with BuildRecipe(ironworking, "Anvil") as r:
    r.key = "A"
    r.base = "Stone"
    r.skill = "CLUB"
    r.time = "4h"

    r.add(bloom(5))
    r.add(charcoal(10))
    r.add(fire)
    r.add(Tool("Rock", note="+to pound it"))
    r.add(Ingredient("Block of wood", note="+for a base"))
    r.add(Tool("Axe", prefer="Carving Axe"))

with BuildRecipe(ironworking, "Hammer") as r:
    r.key = "H"
    r.base = "Mace"
    r.skill = "CLUB"
    r.time = "3h"

    r.add(bloom(2))
    r.add(charcoal(6))
    r.add(fire)
    r.add(Ingredient("Rock", note="+to pound it"))
    r.add(anvil)
    r.add(stake)

with BuildRecipe(ironworking, "Pot") as r:
    r.key = "P"
    r.skill = "CLUB"
    r.time = 90

    r.add(wrought())
    r.add(charcoal(3))
    r.haf()

with BuildRecipe(ironworking, "Iron Hoop") as r:
    r.key = "O"
    r.skill = "CLUB"
    r.base = "Hunting Horn"
    r.patch = 5

    r.add(wrought(patchwise=True))
    r.add(charcoal(patchwise=True))
    r.haf()

with BuildRecipe(ironworking, "Wooden tub") as r:
    r.key = "T"
    r.skill = "CARPENTRY"
    r.time = 120

    r.add(Ingredient("Iron Hoop"))
    r.add(Ingredient("Board", 8))
    r.add(Tool("Axe", prefer="Handaxe"))
    r.add(Tool("Knife"))

with BuildRecipe(blades, "Hammer ROUGH Blade") as r:
    r.skill = "CLUB"
    r.time = 90
    r.base = "Hunting Horn"

    r.add(Ingredient("Rough *", note="A rough blade",
                     extra="[name:Soft %s] [naming:last word]"))
    r.add(charcoal(3))
    r.haf()

with BuildRecipe(blades, "Temper SOFT Blade") as r:
    r.skill = "COOKERY"
    r.time = "1h"
    r.base = "Hunting Horn"

    r.add(Ingredient("Soft *", note="A soft blade",
                     extra="[name:Dull %s] [naming:last word]"))
    r.add(charcoal(2))
    r.add(Ingredient("Water", -1, note="+for quenching"))
    r.add(fire)

with BuildRecipe(blades, "Sharpen DULL Blade") as r:
    r.skill = "SURVIVAL"
    r.time = "1h"
    r.base = "Hunting Horn"

    r.add(Ingredient("Dull *", note="A dull blade",
                     extra="[name:Sharp %s] [naming:last word]"))
    r.add(Tool("Rock"))

with BuildRecipe(blades, "Spearhead") as r:
    r.skill = "CLUB"
    r.base = "Hunting Horn"
    r.time = "1h"

    r.add(wrought(extra="[name:Rough Spearhead]"))
    r.add(charcoal(2))
    r.haf()

with BuildRecipe(weapons, "Spear") as r:
    r.skill = "SPEAR"
    r.time = 30

    r.add(Ingredient("Sharp Spearhead"))
    r.add(staff)
    r.add(cord())
    r.add(knife)

with BuildRecipe(blades, "Knifeblade") as r:
    r.skill = "CLUB"
    r.base = "Hunting Horn"
    r.time = "1h"

    r.add(wrought(extra="[name:Rough Knifeblade]"))
    r.add(charcoal(2))
    r.haf()

with BuildRecipe(weapons, "Knife") as r:
    r.skill = "DAGGER"
    r.time = 30

    r.add(Ingredient("Sharp Knifeblade"))
    r.add(cord())

with BuildRecipe(blades, "Small-Axehead") as r:
    r.skill = "CLUB"
    r.base = "Hunting Horn"
    r.time = 150

    r.add(wrought(2, extra="[name:Rough Small-Axehead]"))
    r.add(charcoal(5))
    r.haf()

with BuildRecipe(weapons, "Handaxe") as r:
    r.skill = "AXE"
    r.time = 30

    r.add(Ingredient("Sharp Small-Axehead"))
    r.add(stake)
    r.add(cord())
    r.add(knife)

with BuildRecipe(blades, "Axehead") as r:
    r.skill = "CLUB"
    r.base = "Hunting Horn"
    r.time = "3h"

    r.add(wrought(3, extra="[name:Rough Axehead]"))
    r.add(charcoal(6))
    r.haf()

with BuildRecipe(weapons, "Carving Axe") as r:
    r.skill = "AXE"
    r.skillmod = -20
    r.time = 40

    r.add(Ingredient("Sharp Axehead"))
    r.add(stake)
    r.add(cord())
    r.add(knife)

with BuildRecipe(blades, "Large-Axehead") as r:
    r.skill = "CLUB"
    r.base = "Hunting Horn"
    r.time = "4h"

    r.add(wrought(4, extra="[name:Rough Large-Axehead]"))
    r.add(charcoal(8))
    r.haf()

with BuildRecipe(weapons, "Woodsman's Axe") as r:
    r.skill = "AXE"
    r.time = 60

    r.add(Ingredient("Sharp Large-Axehead"))
    r.add(stake)
    r.add(cord(2))
    r.add(knife)

with BuildRecipe(weapons, "Splitting Axe") as r:
    r.skill = "AXE"
    r.time = 60

    r.add(Ingredient("Sharp Large-Axehead"))
    r.add(stake)
    r.add(cord(2))
    r.add(knife)

with BuildRecipe(weapons, "Battleaxe") as r:
    r.skill = "AXE"
    r.time = 80
    r.skillmod = -20

    r.add(Ingredient("Sharp Large-Axehead"))
    r.add(stake)
    r.add(cord(2))
    r.add(knife)

with BuildRecipe(blades, "Huge-Axehead") as r:
    r.skill = "CLUB"
    r.base = "Hunting Horn"
    r.time = "5h"

    r.add(wrought(6, extra="[name:Rough Huge-Axehead]"))
    r.add(charcoal(10))
    r.haf()

with BuildRecipe(weapons, "Broad Axe") as r:
    r.skill = "AXE"
    r.time = 90

    r.add(Ingredient("Sharp Huge-Axehead"))
    r.add(stake)
    r.add(cord(3))
    r.add(knife)

with BuildRecipe(blades, "Shovelblade") as r:
    r.skill = "CLUB"
    r.base = "Hunting Horn"
    r.time = 90

    r.add(wrought(2, extra="[name:Rough Shovelblade]"))
    r.add(charcoal(3))
    r.haf()

with BuildRecipe(utility, "Shovel") as r:
    r.skill = "BUILDING"
    r.time = 45

    r.add(Ingredient("Sharp Shovelblade"))
    r.add(staff)
    r.add(cord())
    r.add(knife)

with BuildRecipe(ironworking, "Hilt") as r:
    r.key = "I"
    r.skill = "CLUB"
    r.base = "Hunting Horn"
    r.time = "3h"

    r.add(wrought())
    r.haf()
    r.add(Ingredient("Block of Wood"))
    r.add(Tool("Axe", prefer="Carving Axe"))
    r.add(Ingredient("Leather", -0.5))
    r.add(knife)

with BuildRecipe(blades, "Short-Swordblade") as r:
    r.skill = "CLUB"
    r.base = "Hunting Horn"
    r.time = "3h"

    r.add(wrought(2, extra="[name:Rough Short-Swordblade]"))
    r.add(charcoal(6))
    r.haf()

with BuildRecipe(weapons, "Shortsword") as r:
    r.skill = "SWORD"
    r.time = "1h"

    r.add(Ingredient("Sharp Short-Swordblade"))
    r.add(Ingredient("Hilt"))
    r.haf()

with BuildRecipe(blades, "Swordblade") as r:
    r.skill = "CLUB"
    r.base = "Hunting Horn"
    r.time = "3h"

    r.add(wrought(4, extra="[name:Rough Swordblade]"))
    r.add(charcoal(10))
    r.haf()

with BuildRecipe(weapons, "Bastard sword") as r:
    r.skill = "SWORD"
    r.time = "1h"
    r.skillmod = -10

    r.add(Ingredient("Sharp Swordblade"))
    r.add(Ingredient("Hilt"))
    r.add(hammer)
    r.add(anvil)

with BuildRecipe(blades, "Large-Swordblade") as r:
    r.skill = "CLUB"
    r.base = "Hunting Horn"
    r.time = "3h"

    r.add(wrought(6, extra="[name:Rough Large-Swordblade]"))
    r.add(charcoal(15))
    r.haf()

with BuildRecipe(weapons, "Battlesword") as r:
    r.skill = "SWORD"
    r.time = "1h"
    r.skillmod = -20

    r.add(Ingredient("Sharp Large-Swordblade"))
    r.add(Ingredient("Hilt"))
    r.add(hammer)
    r.add(anvil)

build_files("ironworking", all_recipes)
