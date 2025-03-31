"""
36 Spellstones / 30 Life Tokens / 5 Point Tokens / 1 Die / 1 Gameboard / 5 Reference Sheet / 1 Rules


Players continue to try casting spells until someone is knocked out or someone uses all of his spellstones.
Each player has a hand of 5 spellstones, but players can only see the spells the other players have,
NOT their own. Players shout the name of the spell they want to cast, and if they have the corresponding
spellstone, the effect will be triggered. If they don't have the corresponding stone, they will lose some life.
It is possible to increase the accuracy of spellcasting by deducing the likelihood of having certain spells: the
amount of stones of a given spell is known and players can always see other players' spellstones.
Players continue to try casting spells until someone is knocked out or someone uses all of his spellstones.
When the round ends, players may move up the tower according to their result and the first player to reach
the top of the tower (8 points) wins the game (this will take more than 1 round).


When playing with 3/2 players, remove 6/12 spellstones from the main pile and place them at the
corresponding number area on the gameboard, openly.

Take 4 of the remaining spellstones and put them in the center of the table. Those are
the secret stones of this round. No one can see the secret stones unless they use the secret spell
Night Singer

The oldest player starts the round (this player will move the point markers and clean up the game, so he
gets to start the game as a compensation).


On your turn, say out loud the spell that you want to cast.
A) If you have no matching spellstone, you lose one life and your turn is over.
(Exception: If you try to cast spell 1, you roll the die to see how many life you lose.)
B) If you have at least one matching spellstone, the player to your right takes one (of them) and places
it next to the corresponding number on the gameboard. Then the effect of that spell is resolved
(it might make other players lose life, heal yourself, or let you look at one of the secret stones).

Notes: It is often possible to gain information by looking at what spells other players try to cast: if other
players don't cast spells of a certain number, it is quite likely many of them are in your possession!

If you successfully cast a spell, you may end your turn or cast another spell: simply say another spell's name
out loud and follow the same procedure as the first time. However, there is one restriction: you may only cast
an additional spell whose number is equal or higher than the spell you cast right before.
Note: If you accidentally try to cast a spell that has a lower number than the spell you just cast, another
player may call you out on your mistake. In that case, you lose one life and your turn ends.

Note: You may never have more than 6 life tokens at a time

When you fail to cast a spell, your turn ends immediately. You may also choose to end your turn each time
you successfully cast a spell.
If you have no spellstones left in front of you, you immediately win the round.
Otherwise, refill your hand to 5 spellstones from the center pile of unused spellstones. If there are no
spellstones in the center pile, don't refill your hand (the secret stones and spellstones that were successfully
used cannot be used again).
Now, the player on your left takes their turn.



When all of the spellstones in front of a player have been used or when a player's last life token is taken,
the round ends. Move the point markers of each player according to the following rules:
When you use all the spellstones in front of you, you immediately
win the round and score 3 points. All other players' life tokens are
reduced to 0, and therefore gain no points for this round.
If the round ends because one player causes another player (or
players) to lose their last life token, the player who made the last
attack is the winner. He gains 3 points. All other surviving players
gain 1 point.
If a player causes himself to lose his own last life token, he is the
sole loser in that round, and all surviving players gain 1 point (there
is no winner).
In short, the winner gains 3 points, the loser gains no points, and the
other survivors gain 1 point.
Secret Stone Award: If a player has survived the round—whether or not she is the winner—with 1 or more life
tokens, he also gains 1 point for each secret stone he collected during the round.


Play continues normally, with the player whose turn it would
have been after the last turn of the previous round.


If a player has 8 points at the end of the round, the game ends and that player wins.
If two or more players have 8 points, the player who scored the most points in the last round wins.
If there is still a tie, the tied player with more life tokens wins.
If they have the same number of life tokens, they share the victory.


---------
Rule Variants:

Easy version:
When you choose to cast another spell during the same turn, you can cast any spell, regardless of which
spell(s) you cast previously.

Last standing magician takes all:
The round ends only when all of the spellstones in front of any player have been used or only one
player survives. The winner scores 2 points, plus an additional point for each secret stone. The other
players score no points.
--------------------------------

Detailed Spell Overview

(1) Ancient Dragon
Roll the die: all other players lose life tokens according to the result.
Note: If you fail to summon the dragon, you roll the die to see how many life tokens you
lose. It is very dangerous to summon a dragon!

(2) Dark Wanderer
All other players lose 1 life. You gain 1 life (maximum of 6).

(3) Sweet Dream
Roll the die: you gain life according to the result (maximum of 6).

(4) Night Singer
You may look at one of the secret stones and place it in front of yourself.
If you have any life tokens left at the end of the round, you gain one extra
point for each secret stone acquired this way.
Note: You place the secret stone facedown in front of yourself, but you may look at it
again any time you want. You may not cast the spell on the secret stone.

(5) Lightning Tempest
The players to your left and right lose 1 life each.
Note: When playing with only 2 players, the other player only loses 1 life in total.

(6) Blizzard
The player to your left loses 1 life.

(7) Fireball
The player to your right loses 1 life.

(8) Magic Drink
You gain 1 life (maximum of 6).
Note: Many players try casting another spell to cause loss of life after recovering life with
this spell, but this causes them to lose life instead. Remember that you can only cast spells
of an equal or higher number than the spell you just cast. So, after you have cast this spell,
the only spell you are allowed to cast is this one (it is number 8 - the highest number). If you
wish to recover life before attacking, you will have to try casting spell number 2 or 3 (but
this is much riskier).

"""

import random


class Player:
    def __init__(self, game, name):
        self.game = game
        self.name = name
        self.points = 0
        self.lives = 6
        self.spellstones = []
        self.secret_stones = []

    @property
    def is_alive(self):
        return self.lives > 0

    def cast_spell(self, spell):
        # if spell in self.spellstones:

        # damage = random.randint(10, 25)
        # target.health -= damage
        # print(f"{self.name} attacks {target.name} for {damage} damage!")
        # target.check_health()
        return damage

    def check_status(self):
        """Check and update player's alive status."""
        if self.health <= 0:
            self.health = 0
            self.is_alive = False
            print(f"{self.name} has been defeated!")


class Game:

    def __init__(self, player_names):

        number_of_players = len(player_names)
        if number_of_players < 2 or number_of_players > 5:
            raise ValueError("Game requires 2-5 players")

        self.spellstones = [str(i) for i in range(1, 9) for _ in range(i)]
        random.shuffle(self.spellstones)
        if number_of_players == 3:
            self.spellstones = self.spellstones[:-6]
        elif number_of_players == 2:
            self.spellstones = self.spellstones[:-12]

        self.secret_stones = draw(self.spellstones, 4)

        self.players = [Player(self, name) for name in player_names]
        for p in self.players:
            draw(self.spellstones, 5, p.spellstones)

        self.current_player_index = 0

    def play(self):
        """Main game loop."""
        print("🎮 Guess Spell Game Started! 🎮")

        while True:
            self.display_point_status()

            self.play_round()

            if self.check_game_over():
                break

            self.next_round()

    def display_point_status(self):
        """Show current point status of all players."""
        print("\n--- Current Game Status ---")
        for player in self.players:
            print(f"{player.name}: {player.points}")
        print("-------------------------\n")

    def play_round(self):
        """A round loop."""
        print("🎮 New Round Started! 🎮")

        while True:
            self.display_round_status()

            self.player_turn()

            if self.check_round_over():
                break

            self.next_turn()

    def display_round_status(self):
        """Show current status of all players."""
        print("\n--- Current Game Status ---")
        for player in self.players:
            print(
                f"{player.name}: {player.lives}/{6} HP - Spellstones:{player.spellstones}"
            )
        print("-------------------------\n")

    def next_turn(self):
        """Move to the next living player's turn."""
        while True:
            self.current_player_index = (self.current_player_index + 1) % len(
                self.players
            )
            if self.players[self.current_player_index].is_alive:
                break

    def player_turn(self):
        """Manage a single player's turn."""
        current_player = self.players[self.current_player_index]

        print(f"\n{current_player.name}'s turn!")
        print("Cast your spell!")

        # Get valid action
        while True:
            try:
                action = int(input("Enter 1 or 2: "))
                if action not in [1, 2]:
                    raise ValueError
                break
            except ValueError:
                print("Invalid input. Please enter 1 or 2.")

        # Get target for attack
        if action == 1:
            # List available targets
            targets = [p for p in self.players if p != current_player and p.is_alive]

            print("Choose a target:")
            for i, target in enumerate(targets, 1):
                print(f"{i}. {target.name}")

            while True:
                try:
                    target_choice = int(input("Enter target number: "))
                    if 1 <= target_choice <= len(targets):
                        target = targets[target_choice - 1]
                        current_player.attack(target)
                        break
                    else:
                        raise ValueError
                except ValueError:
                    print("Invalid target. Please choose a valid target.")

        # Heal action
        else:
            current_player.heal()

    def next_turn(self):
        """Move to the next living player's turn."""
        while True:
            self.current_player_index = (self.current_player_index + 1) % len(
                self.players
            )
            if self.players[self.current_player_index].is_alive:
                break

    def check_round_over(self):
        """Check if the round has ended."""
        alive_players = [p for p in self.players if p.is_alive]

        if len(alive_players) == 1:
            print(f"\n🏆 {alive_players[0].name} WINS THE GAME! 🏆")
            return True

        return False

    def check_game_over(self):
        """Check if the game has ended."""
        alive_players = [p for p in self.players if p.is_alive]

        if len(alive_players) == 1:
            print(f"\n🏆 {alive_players[0].name} WINS THE GAME! 🏆")
            return True

        return False


def draw(source, count, destination=None):
    if destination is None:
        destination = []
    for _ in range(count):
        if not source:
            break
        destination.append(source.pop(0))
    return destination


def main():
    print("Welcome to the Guess Spell Game!")

    # Get player names
    while True:
        try:
            num_players = int(input("How many players? (2-5): "))
            if 2 <= num_players <= 5:
                break
            else:
                print("Please enter a number between 2 and 5.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    players = []
    for i in range(num_players):
        name = input(f"Enter name for Player {i+1}: ")
        players.append(name)

    game = Game(players)
    game.play()


if __name__ == "__main__":
    main()
