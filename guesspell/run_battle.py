import random

class Player:
    def __init__(self, name, max_health=100):
        self.name = name
        self.health = max_health
        self.max_health = max_health
        self.is_alive = True

    def attack(self, target):
        """Attack another player."""
        damage = random.randint(10, 25)
        target.health -= damage
        print(f"{self.name} attacks {target.name} for {damage} damage!")
        target.check_health()
        return damage

    def heal(self):
        """Heal the player."""
        heal_amount = random.randint(15, 30)
        self.health = min(self.max_health, self.health + heal_amount)
        print(f"{self.name} heals for {heal_amount} health!")
        return heal_amount

    def check_health(self):
        """Check and update player's alive status."""
        if self.health <= 0:
            self.health = 0
            self.is_alive = False
            print(f"{self.name} has been defeated!")

class MultiplayerBattleGame:
    def __init__(self, player_names):
        if len(player_names) < 2 or len(player_names) > 7:
            raise ValueError("Game requires 2-7 players")
        
        self.players = [Player(name) for name in player_names]
        self.current_player_index = 0

    def display_game_status(self):
        """Show current status of all players."""
        print("\n--- Current Game Status ---")
        for player in self.players:
            status = "ALIVE" if player.is_alive else "DEFEATED"
            print(f"{player.name}: {player.health}/{player.max_health} HP - {status}")
        print("-------------------------\n")

    def next_turn(self):
        """Move to the next living player's turn."""
        while True:
            self.current_player_index = (self.current_player_index + 1) % len(self.players)
            if self.players[self.current_player_index].is_alive:
                break

    def player_turn(self):
        """Manage a single player's turn."""
        current_player = self.players[self.current_player_index]
        
        print(f"\n{current_player.name}'s turn!")
        print("Choose an action:")
        print("1. Attack")
        print("2. Heal")
        
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

    def check_game_over(self):
        """Check if the game has ended."""
        alive_players = [p for p in self.players if p.is_alive]
        
        if len(alive_players) == 1:
            print(f"\n🏆 {alive_players[0].name} WINS THE GAME! 🏆")
            return True
        
        return False

    def play(self):
        """Main game loop."""
        print("🎮 Multiplayer Battle Game Started! 🎮")
        
        while True:
            self.display_game_status()
            
            self.player_turn()
            
            if self.check_game_over():
                break
            
            self.next_turn()

def main():
    print("Welcome to the Multiplayer Battle Game!")
    
    # Get player names
    while True:
        try:
            num_players = int(input("How many players? (2-7): "))
            if 2 <= num_players <= 7:
                break
            else:
                print("Please enter a number between 2 and 7.")
        except ValueError:
            print("Invalid input. Please enter a number.")
    
    players = []
    for i in range(num_players):
        name = input(f"Enter name for Player {i+1}: ")
        players.append(name)
    
    game = MultiplayerBattleGame(players)
    game.play()

if __name__ == "__main__":
    main()