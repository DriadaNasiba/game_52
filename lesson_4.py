from random import randint, choice


class GameEntity:
    def __init__(self, name, health, damage):
        self.__name = name
        self.__health = health
        self.__damage = damage

    @property
    def name(self):
        return self.__name

    @property
    def health(self):
        return self.__health

    @health.setter
    def health(self, value):
        if value < 0:
            self.__health = 0
        else:
            self.__health = value

    @property
    def damage(self):
        return self.__damage

    @damage.setter
    def damage(self, value):
        self.__damage = value

    def __str__(self):
        return f'{self.__name} health: {self.__health}, damage: {self.__damage}'


class Boss(GameEntity):
    def __init__(self, name, health, damage):
        super().__init__(name, health, damage)
        self.__defence = None

    @property
    def defence(self):
        return self.__defence

    def choose_defence(self, heroes: list):
        random_hero: Hero = choice(heroes)
        self.__defence = random_hero.ability

    def attack(self, heroes: list):
        for hero in heroes:
            if hero.health > 0:
                if type(hero) == Berserk and self.defence != hero.ability:
                    hero.blocked_damage = choice([5, 10])
                    hero.health -= self.damage - hero.blocked_damage
                else:
                    hero.health -= self.damage

    def __str__(self):
        return 'BOSS ' + super().__str__() + ' defence: ' + str(self.__defence)


class Hero(GameEntity):
    def __init__(self, name, health, damage, ability):
        super().__init__(name, health, damage)
        self.__ability = ability

    @property
    def ability(self):
        return self.__ability

    def attack(self, boss: Boss):
        boss.health -= self.damage

    def apply_super_power(self, boss: Boss, heroes: list):
        pass


class Warrior(Hero):
    def __init__(self, name, health, damage):
        super().__init__(name, health, damage, 'CRITICAL_DAMAGE')

    def apply_super_power(self, boss: Boss, heroes: list):
        crit = self.damage * randint(2, 5) # 2,3,4
        boss.health -= crit
        print(f'Warrior {self.name} hit critically: {crit}')


class Magic(Hero):
    def __init__(self, name, health, damage):
        super().__init__(name, health, damage, 'BOOSTING')
        self.rounds_boosted = 0
        self.attack_boost = 5

    def apply_super_power(self, boss: Boss, heroes: list):
        # TODO Here will be implementation of boosting
        if self.rounds_boosted < 4:
            self.rounds_boosted += 1
            for hero in heroes:
                if hero.health > 0:
                    hero.damage += self.attack_boost
                    print(f'{self.name} boosts {hero.name} attack by {self.attack_boost} in round {round_number}')
                else:
                    print(f'{self.name} cannot boost attack anymore, 4 rounds passed.')


class Medic(Hero):
    def __init__(self, name, health, damage, heal_points):
        super().__init__(name, health, damage, 'HEAL')
        self.__heal_points = heal_points

    def apply_super_power(self, boss: Boss, heroes: list):
        for hero in heroes:
            if hero.health > 0 and self != hero:
                hero.health += self.__heal_points


class Berserk(Hero):
    def __init__(self, name, health, damage):
        super().__init__(name, health, damage, 'BLOCK_REVERT')
        self.__blocked_damage = 0

    @property
    def blocked_damage(self):
        return self.__blocked_damage

    @blocked_damage.setter
    def blocked_damage(self, value):
        self.__blocked_damage = value

    def apply_super_power(self, boss: Boss, heroes: list):
        boss.health -= self.__blocked_damage
        print(f'Berserk {self.name} reverted: {self.__blocked_damage}')

class  Witcher(Hero):
    def __init__(self, name, healh, damage):
        super().__init__(name, healh, damage, 'REVIVE')
        self.__revive_chance = 0.1

    def receive_damage(self, damage):
        self.health -= damage
        print(f'{self.name} receives {damage} damage from the boss.')

    def revive(self, dead_hero: Hero):
        if randint(1, 10) / 10 < self.__revive_chance:
            if not dead_hero.health:
                dead_hero.health = 50
                print(f"{self.name} revives {dead_hero.name} with 50.")
                self.health = 0
                print(f"{self.name} dies after reviving {dead_hero.name}.")
            else:
                print(f"{dead_hero.name} is already alive!")
        else:
            print(f"{self.name} failed to revive {dead_hero.name}.")

    def apply_super_power(self, boss, heroes):
        for hero in heroes:
            if hero.health == 0 and hero != self:
                self.revive(hero, heroes)
                break

class Hacker(Hero):
    def __init__(self, name, health, damage, steal_amount):
        super().__init__(name, health, damage, 'STEAL_HEALTH')
        self.__steal_amount = steal_amount

    def apply_super_power(self, boss: Boss, heroes: list):
        if boss.health >0:
            steal = min(self.__steal_amount, boss.health)
            boss.health -= steal
            target_hero = choice(heroes)
            target_hero.health += steal
            print(f"{self.name} steals {steal} health from boss and gives it to {target_hero.name}.")
            print(f"Boss health: {boss.health}, {target_hero.name}'s health: {target_hero.health}")

class Thor(Hero):
    def __init__(self, name, health, damage, stun_chance):
        super().__init__(name, health, damage, 'STUN')
        self.stun_chance = stun_chance

    def apply_super_power(self, boss: Boss, heroes: list):
        if randint(1, 100) / 100 < self.stun_chance:
            boss.health = max(0, boss.health - self.damage)
            print(f"{self.name} stuns the boss!")


class Avenger(Hero):
    def __init__(self, name, health, damage, shield_chance):
        super().__init__(name, health, damage, 'SHIELD')
        self.shield_chance = shield_chance

    def apply_super_power(self, boss: Boss, heroes: list):
        if randint (1, 100) / 100 < self.shield_chance:
            for hero in heroes:
                hero.is_immune = True
                print(f"{self.name} activates a shield! All heroes are immune to damage for 1 round.")
            else:
                print(f"{self.name} failed to activate shield.")


round_number = 0


def show_statistics(boss: Boss, heroes: list):
    print(f'ROUND {round_number} ----------------')
    print(boss)
    for hero in heroes:
        print(hero)


def is_game_over(boss: Boss, heroes: list):
    if boss.health <= 0:
        print('Heroes won!!!')
        return True
    all_heroes_dead = True
    for hero in heroes:
        if hero.health > 0:
            all_heroes_dead = False
            break
    if all_heroes_dead:
        print('Boss won!!!')
        return True
    return False


def play_round(boss: Boss, heroes: list):
    global round_number
    round_number += 1
    boss.choose_defence(heroes)
    boss.attack(heroes)
    for hero in heroes:
        if hero.health > 0 and boss.health > 0 and boss.defence != hero.ability:
            hero.attack(boss)
            hero.apply_super_power(boss, heroes)
    show_statistics(boss, heroes)


def start_game():
    boss = Boss('Splinter', 1000, 50)

    warrior_1 = Warrior('Django', 280, 10)
    warrior_2 = Warrior('Billy', 270, 15)
    magic = Magic('Dulittle', 290, 10)
    doc = Medic('James', 250, 5, 15)
    assistant = Medic('Marty', 300, 5, 5)
    berserk = Berserk('William', 260, 10)
    witcher = Witcher('Vedmak', 290, 10)
    hacker = Hacker('Tim', 230, 10,40)
    thor = Thor( 'Torry', 300, 20, 0.3)
    avenger =  Avenger ('Luca', 270, 30, 0.2)




    heroes_list = [warrior_1, doc, warrior_2, magic, berserk, assistant, witcher, hacker, thor, avenger]

    show_statistics(boss, heroes_list)
    while not is_game_over(boss, heroes_list):
        play_round(boss, heroes_list)

start_game()
