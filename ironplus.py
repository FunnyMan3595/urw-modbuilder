from modbuilder import *

ironworking = Menu("Ironworking")
weaponsmithing = Menu("Weaponsmithing", "P")
armorsmithing = Menu("Armorsmithing", "A")

fire = Tool("Fire", note="+lit nearby")
torch = Ingredient("Torch", note="+to transfer the flame")
anvil = GTool("Anvil", note="+nearby")
hammer = Tool("Hammer")
stake = Ingredient("Wooden Stake", note="+for a handle")
staff = Ingredient("Staff", note="+for a handle")

charcoal = lambda *args, **kwargs: GIngredient("Charcoal", *args, **kwargs)
bloom = lambda *args, **kwargs: Ingredient("Bloom of Iron", *args, **kwargs)
wrought = lambda *args, **kwargs: Ingredient("Wrought Iron", *args, **kwargs)


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
    r.key = "B"
    r.base = "Stone"
    r.skill = "SURVIVAL"
    r.time = 90

    r.add(Tool("Shovel"))
    r.add(Tool("[TERRAIN:spruce_mire pine_mire open_mire]",
               note="Be in a Mire"))

with BuildRecipe(ironworking, "Charcoal") as r:
    r.key = "C"
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
    r.key = "S"
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
    r.key = "H"
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
    r.key = "M"
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

build_files("ironworking", all_recipes)
