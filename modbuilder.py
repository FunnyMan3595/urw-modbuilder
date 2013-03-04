MAKE, COOK = range(2)

class Menu(object):
    def __init__(self, name, key=None, type=MAKE, default=False):
        self.name = name
        if key is None:
            key = self.name[0]
        self.key = key
        self.type = type
        self.default = False

    def __str__(self):
        if self.type == MAKE:
            type_name = "MAKE"
        else:
            type_name = "COOKERY"

        return ".%s. -%s- *%s*" % (self.name, self.key, type_name)

    def start(self):
        return "[SUBMENU_START:%s]\r\n" % self.name

    def end(self):
        return "[SUBMENU_END:%s]\r\n" % self.name

CookMenu = lambda *args, **kwargs: Menu(*args, type=COOK, **kwargs)

# Default menus
DMenu = lambda *args, **kwargs: Menu(*args, default=True, **kwargs)
clothes = DMenu("Clothes")
lumber = DMenu("Lumber")
trapping = DMenu("Trapping")
transport = DMenu("Transport", "R")
weapons = DMenu("Weapons")

# Default cooking menus
DCookMenu = lambda *args, **kwargs: CookMenu(*args, default=True, **kwargs)
baking = DCookMenu("Baking", "A")
porridge = DCookMenu("Porridge")
meat = DCookMenu("Meat")
fish = DCookMenu("Fish")
Vegetable = DCookMenu("Vegetable")

class Ingredient(object):
    def __init__(self, name, amount=1, note=None, use=True, patchwise=False,
                       ground=False, prefer=None, extra=None):
        self.name = name
        self.note = note
        self.amount = amount
        self.use = use
        self.patchwise = patchwise
        self.ground = ground
        self.prefer = prefer
        self.extra = extra

    def __str__(self):
        s = "{%s}" % (self.name)

        if self.prefer is not None:
            s += " <%s>" % self.prefer

        if self.amount > 1:
            s += " (%d)" % self.amount
        elif self.amount < 0:
            s += " #%d#" % (-self.amount)

        if self.note is not None:
            s += " '%s'" % self.note

        if self.use:
            s += " [remove]"

        if self.patchwise:
            s += " [patchwise]"

        if self.ground:
            s += " [ground]"

        if self.extra is not None:
            s += " %s" % self.extra

        return s + "\r\n"

PIngredient = lambda *args, **kwargs: Ingredient(*args, patchwise=True, **kwargs)
GIngredient = lambda *args, **kwargs: Ingredient(*args, ground=True, **kwargs)
PGIngredient = lambda *args, **kwargs: Ingredient(*args, patchwise=True, ground=True, **kwargs)
Tool = lambda *args, **kwargs: Ingredient(*args, use=False, **kwargs)
GTool = lambda *args, **kwargs: Ingredient(*args, use=False, ground=True, **kwargs)

class Recipe(object):
    def __init__(self, menu, name, amount=1, key=None, skill=None, base=None,
                       time=None, waittime=None, skillmod=0, skillfreq=0,
                       patch=1):
        self.menu = menu
        self.name = name
        self.amount = amount
        self.key = key
        self.skill = skill
        self.base = base
        self.time = time
        self.waittime = waittime
        self.skillmod = skillmod
        self.skillfreq = skillfreq
        self.patch = patch

        self.ingredients = []

    def __str__(self):
        s = ".%s." % self.name

        if self.amount != 1:
            s += " (%d)" % self.amount

        if self.key is not None:
            s += " -%s-" % self.key

        if self.base is not None:
            s += ' "%s"' % self.base

        if self.skill is not None:
            s += " *%s*" % self.skill

        if self.time is not None:
            s += " /%s/" % self.time

        if self.waittime is not None:
            s += " \\%s\\" % self.waittime

        if self.skillmod != 0:
            s += " %" + str(self.skillmod) + "%"

        if self.skillfreq != 0:
            s += " |%s|" % self.skillfreq

        if self.patch != 1:
            s += " [patch:%d]" % self.patch

        return s + "\r\n"

    def add(self, ingredient):
        self.ingredients.append(ingredient)

    def full_string(self):
        s = str(self)
        for ingredient in self.ingredients:
            s += str(ingredient)

        s += "\r\n"

        return s

def build_files(id, all_recipes):
    additional_menus = []
    menu_recipes = {}
    for recipe in all_recipes:
        if recipe.menu not in menu_recipes:
            menu_recipes[recipe.menu] = []
            if not recipe.menu.default:
                additional_menus.append(recipe.menu)

        menu_recipes[recipe.menu].append(recipe)

    with open("menudef_%s.txt" % id, "w") as menudef:
        for menu in additional_menus:
            menudef.write(str(menu))

    with open("diy_%s.txt" % id, "w") as diy:
        for menu, recipes in menu_recipes.items():
            diy.write(menu.start())
            diy.write("\r\n")

            for recipe in recipes:
                diy.write(recipe.full_string())

            diy.write(menu.end())
            diy.write("\r\n")
