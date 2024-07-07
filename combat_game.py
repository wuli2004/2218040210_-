# filename: combat_game.py
# Description: Implementation of a combat game with various combatants and arenas.
# Author: luyang Chen(陈禄洋)
# StudentID: 2218040210
# This is my own work as defined by the University's Academic Misconduct Policy.

import random

class Combatant:
    def __init__(self, name, max_health, strength, defence, magic=1, ranged=1):
        self.name = name
        self.max_health = max_health
        self.health = max_health
        self.strength = strength
        self.defence = defence
        self.magic = magic
        self.ranged = ranged

    def attack(self, opponent):
        damage = self.calculate_damage()
        opponent.take_damage(damage)
    
    def calculate_damage(self):
        return self.strength

    def take_damage(self, damage):
        damage_taken = max(damage - self.defence, 0)
        self.health -= damage_taken
        print(f"{self.name} took {damage_taken} damage and has {self.health} health remaining")

    def reset(self):
        self.health = self.max_health
    
    def details(self):
        return (f"{self.name} is a {self.__class__.__name__} and has the following stats:\n"
                f"Health: {self.health}/{self.max_health}\n"
                f"Strength: {self.strength}\n"
                f"Defence: {self.defence}\n"
                f"Magic: {self.magic}\n"
                f"Ranged: {self.ranged}\n")

class Ranger(Combatant):
     def __init__(self, name, max_health, strength, defence, magic, ranged):
        super().__init__(name, max_health, strength, defence, magic, ranged)
        self.arrows = 3

     def calculate_damage(self):
        if self.arrows > 0:
            self.arrows -= 1
            damage = self.ranged
            print(f"{self.name} fires an arrow for {damage} damage!")
        else:
            damage = self.strength
            print(f"{self.name} attacks for {damage} damage!")
        return damage

     def reset(self):
        super().reset()
        self.arrows = 3
class Warrior(Combatant):
    def __init__(self, name, max_health, strength, defence, magic, ranged, armour_value):
        super().__init__(name, max_health, strength, defence, magic, ranged)
        self.armour_value = armour_value
        self.original_armour_value = armour_value

    def take_damage(self, damage):
        if self.armour_value > 0:
            damage_blocked = min(damage, 5)
            self.armour_value -= damage_blocked
            if self.armour_value <= 0:
                print(f"{self.name}'s armour shattered!")
        else:
            damage_blocked = 0
        super().take_damage(damage - damage_blocked)

    def reset(self):
        super().reset()
        self.armour_value = self.original_armour_value

class Dharok(Warrior):
    def calculate_damage(self):
        additional_damage = (self.max_health - self.health) // 4
        damage = self.strength + additional_damage
        print(f"The power of Dharok activates adding {additional_damage} damage")
        return damage

class Guthans(Warrior):
    def attack(self, opponent):
        damage = self.calculate_damage()
        opponent.take_damage(damage)
        healing = min(10, damage // 5)
        self.health = min(self.max_health, self.health + healing)
        print(f"The power of Guthans activates healing {self.name} for {healing} health")

    def calculate_damage(self):
        return self.strength

class Karil(Warrior):
    def calculate_damage(self):
        damage = self.strength + self.ranged
        print(f"The power of Karil activates adding {self.ranged} damage!")
        return damage

class Mage(Combatant):
    def __init__(self, name, max_health, strength, defence, magic, ranged):
        super().__init__(name, max_health, strength, defence, magic, ranged)
        self.mana = magic
        self.regen_rate = magic // 4

    def cast_spell(self, opponent):
        raise NotImplementedError("Must be implemented in subclass")

    def attack(self, opponent):
        self.cast_spell(opponent)

    def reset(self):
        super().reset()
        self.mana = self.magic

class PyroMage(Mage):
    def __init__(self, name, max_health, strength, defence, magic, ranged):
        super().__init__(name, max_health, strength, defence, magic, ranged)
        self.flame_boost = 1

    def cast_spell(self, opponent):
        if self.mana >= 40:
            print(f"{self.name} casts SuperHeat!")
            self.flame_boost += 1
            self.mana -= 40
        elif self.mana >= 10:
            print(f"{self.name} casts FireBlast!")
            damage = (self.strength * self.flame_boost) + 10
            opponent.take_damage(damage)
            self.mana -= 10
        else:
            print(f"{self.name} has insufficient mana!")
        self.mana += self.regen_rate
        print(f"{self.name} regenerates {self.regen_rate} mana!")

class FrostMage(Mage):
    def __init__(self, name, max_health, strength, defence, magic, ranged):
        super().__init__(name, max_health, strength, defence, magic, ranged)
        self.ice_block = False

    def cast_spell(self, opponent):
        if self.mana >= 50:
            print(f"{self.name} sets up an IceBlock!")
            self.ice_block = True
            self.mana -= 50
        elif self.mana >= 10:
            print(f"{self.name} casts IceBarrage!")
            damage = (self.magic // 4) + 30
            opponent.take_damage(damage)
            self.mana -= 10
        else:
            print(f"{self.name} has insufficient mana!")
        self.mana += self.regen_rate
        print(f"{self.name} regenerates {self.regen_rate} mana!")

    def take_damage(self, damage):
        if self.ice_block:
            print(f"{self.name}'s IceBlock absorbs the damage!")
            self.ice_block = False
            damage_taken = 0
        else:
            damage_taken = max(damage - self.defence, 0)
        self.health -= damage_taken
        print(f"{self.name} took {damage_taken} damage and has {self.health} health remaining")
        self.mana += self.regen_rate
        print(f"{self.name} regenerates {self.regen_rate} mana!")



class Field:
    def __init__(self, name="Castle Walls"):
        self.name = name

    def change_field(self):
        fields = ["Toxic Wasteland", "Healing Meadows", "Castle Walls"]
        self.name = random.choice(fields)

    def apply_effect(self, combatant1, combatant2):
        if self.name == "Toxic Wasteland":
            combatant1.take_damage(5)
            combatant2.take_damage(5)
        elif self.name == "Healing Meadows":
            combatant1.health += 5
            combatant2.health += 5
        print(f"Field effect: {self.name}")

class Arena:
    def __init__(self, name):
        self.name = name
        self.combatants = []
        self.field = Field()

    def add_combatant(self, combatant):
        if combatant not in self.combatants:
            self.combatants.append(combatant)
            print(f"{combatant.name} was added to {self.name}")

    def remove_combatant(self, combatant):
        if combatant in self.combatants:
            self.combatants.remove(combatant)
            print(f"{combatant.name} was removed from {self.name}")
        else:
            print(f"{combatant.name} cannot be removed as they were not found in the arena")

    def list_combatants(self):
        for combatant in self.combatants:
            print(combatant.details())

    def restore_combatants(self):
        for combatant in self.combatants:
            combatant.reset()
        print("----- RESTING -----")
        self.list_combatants()

    def duel(self, combatant1, combatant2):
        if combatant1 not in self.combatants or combatant2 not in self.combatants:
            print("Both combatants must be in the arena to duel.")
            return
        if combatant1.health <= 0 or combatant2.health <= 0:
            print("Both combatants must have health to duel.")
            return
        print(f"----- Battle has taken place in {self.name} on the {self.field.name} between {combatant1.name} and {combatant2.name} -----")
        rounds = 0
        while combatant1.health > 0 and combatant2.health > 0 and rounds < 10:
            rounds += 1
            print(f"\nRound {rounds}\n")
            self.field.apply_effect(combatant1, combatant2)
            combatant1.attack(combatant2)
            if combatant2.health > 0:
                combatant2.attack(combatant1)
            if combatant1.health <= 0 or combatant2.health <= 0:
                print("---------- END BATTLE ----------") 
                break
        if combatant1.health <= 0:
            print(f"{combatant1.name} has been defeated!")
        if combatant2.health <= 0:
            print(f"{combatant2.name} has been defeated!")
        if rounds >= 10:
            print("The duel ended in a draw after 10 rounds!")

