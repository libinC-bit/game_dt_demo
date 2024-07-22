# -*- coding: utf-8 -*-
# @Author  : Bin
# @Time    : 2024/7/22 10:58


import math


class Skill:
    def __init__(self, name, damage, max_uses, range):
        self.name = name
        self.damage = damage
        self.max_uses = max_uses  # Maximum number of uses
        self.remaining_uses = max_uses  # Remaining uses
        self.range = range  # Skill's range

    def use(self, enemy, distance):
        if self.remaining_uses > 0 and distance <= self.range:
            print(f"{self.name} used against {enemy.name} for {self.damage} damage!")
            self.remaining_uses -= 1
        else:
            print(f"{self.name} cannot be used at this distance or is out of uses.")

    def can_use(self, distance):
        return self.remaining_uses > 0 and distance <= self.range

class Hero:
    def __init__(self, name, position, attack_range, skills):
        self.name = name
        self.position = position
        self.attack_range = attack_range
        self.skills = skills  # skills is a list of Skill objects

    def attack(self, enemy):
        distance = self.distance_to(enemy)

        # Check if enemy is within attack range
        if distance <= self.attack_range:
            # Select the best skill to use, if available
            best_skill, skill_distance = self.choose_best_skill(enemy, distance)
            if best_skill:
                best_skill.use(enemy, skill_distance)
            else:
                self.normal_attack(enemy)
        else:
            # Move towards the closest enemy
            self.move_towards(enemy)

    def move_towards(self, enemy):
        direction, steps = self.calculate_move_direction(enemy)
        print(f"{self.name} moves {direction} for {steps} steps.")

    def calculate_move_direction(self, enemy):
        current_x, current_y = self.position
        enemy_x, enemy_y = enemy.position

        dx = enemy_x - current_x
        dy = enemy_y - current_y

        if abs(dx) > abs(dy):
            if dx > 0:
                direction = "right"
            else:
                direction = "left"
            steps = abs(dx)
        else:
            if dy > 0:
                direction = "down"
            else:
                direction = "up"
            steps = abs(dy)

        return direction, steps

    def normal_attack(self, enemy):
        print(f"{self.name} attacks {enemy.name} with normal attack.")

    def choose_best_skill(self, enemy, distance):
        best_skill = None
        best_skill_distance = float('inf')

        for skill in self.skills:
            if skill.can_use(distance):
                if skill.range < best_skill_distance:
                    best_skill = skill
                    best_skill_distance = skill.range

        return best_skill, best_skill_distance

    def distance_to(self, enemy):
        return abs(self.position[0] - enemy.position[0]) + abs(self.position[1] - enemy.position[1])

class Enemy:
    def __init__(self, name, position, aggro_level):
        self.name = name
        self.position = position
        self.aggro_level = aggro_level

# Example usage:
hero_position = (3, 3)
hero_attack_range = 2
hero_skills = [
    Skill("Fireball", 30, 3, 3),
    Skill("Lightning", 40, 2, 4),
    Skill("Bash", 20, 1, 1)
]
hero = Hero("Hero1", hero_position, hero_attack_range, hero_skills)

enemies = [
    Enemy("Enemy1", (5, 5), 3),
    Enemy("Enemy2", (2, 4), 2),
    Enemy("Enemy3", (3, 5), 4)
]

# Example of using the hero's attack method
target_enemy = enemies[0]  # Selecting an enemy to attack
hero.attack(target_enemy)
