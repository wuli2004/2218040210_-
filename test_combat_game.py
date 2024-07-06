# filename: test_combat_game.py
# Description: Test cases for the combat game implementation
# Author: luyang Chen(陈禄洋)

from combat_game import Mage, Ranger, Karil, Dharok, Guthans, PyroMage, FrostMage, Arena, Combatant, Warrior

# Creating the different combatant objects
tim = Ranger("Tim", 99, 10, 10, 1, 50)
jay = Warrior("Jay", 99, 1, 99, 1, 1, 1)
kevin = Dharok("Kevin", 99, 45, 25, 25, 25, 10)
zac = Guthans("Zac", 99, 45, 30, 1, 1, 10)
jeff = Karil("Jeff", 99, 50, 40, 1, 10, 5)
try:
    durial = Mage("Durial", 99, 99, 99, 99, 99)
except TypeError:
    print("Mages must be specialized!")
jaina = FrostMage("Jaina", 99, 10, 20, 94, 10)
zezima = PyroMage("Zezima", 99, 15, 20, 70, 1)

# setting up the first arena
falador = Arena("Falador")
falador.add_combatant(tim)
falador.add_combatant(jeff)
falador.list_combatants()
# duel between ranger and karil
falador.duel(tim, jeff)
# showcasing incorrect duels
falador.duel(tim, jeff)
falador.duel(jeff, zezima)
# showcasing restoring combatants
falador.list_combatants()
falador.restore_combatants()
falador.list_combatants()
# showcasing removing from arena
falador.remove_combatant(jeff)
falador.remove_combatant(jeff)
# setting up the second arena
varrock = Arena("Varrock")
varrock.add_combatant(kevin)
varrock.add_combatant(zac)
# duel between guthans and dharok.. note guthans does not heal on the final 
# round as Zac was KO'd
varrock.duel(kevin, zac)
# setting up the third arena
wilderness = Arena("Wilderness")
wilderness.add_combatant(jaina)
wilderness.add_combatant(zezima)
# duel between a pyro and frost mage... double ko?!?!?
wilderness.duel(jaina, zezima)
# setting up final arena
lumbridge = Arena("Lumbridge")
lumbridge.add_combatant(jaina)
lumbridge.add_combatant(jay)
lumbridge.add_combatant(tim)
# showcasing health carries over from arenas
lumbridge.duel(jaina, jay)
# showcasing a duel that takes too long...
# tims arrows should also be reset to 3 from the restoing at the falador arena 
# above
lumbridge.duel(jay, tim)