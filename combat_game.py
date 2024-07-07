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

