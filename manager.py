import random
import sqlite3
import pandas as pd
import time

class Player:
    def __init__(self, name, position, overall_rating, age):
        self.name = name
        self.position = position
        self.overall_rating = overall_rating
        self.age = age
        self.stamina = 100
        self.form = random.uniform(0.7, 1.3)
        self.skills = {
            'shooting': random.uniform(60, 90),
            'passing': random.uniform(60, 90),
            'dribbling': random.uniform(60, 90),
            'defending': random.uniform(60, 90),
            'speed': random.uniform(60, 90)
        }

    def get_skill_rating(self, skill_type):
        """Get player's rating for a specific skill"""
        return self.skills[skill_type] * self.form * (self.stamina / 100)

class Team:
    def __init__(self, name):
        self.name = name
        self.players = []
        self.formation = '4-4-2'
        self.tactics = 'Balanced'
        
    def add_player(self, player):
        self.players.append(player)
    
    def get_starting_eleven(self):
        """Return the best 11 players based on their overall rating"""
        return sorted(self.players, key=lambda x: x.overall_rating, reverse=True)[:11]

class Match:
    def __init__(self, home_team, away_team, user_team=None):
        self.home_team = home_team
        self.away_team = away_team
        self.user_team = user_team
        self.home_score = 0
        self.away_score = 0
        self.match_events = []
        self.current_minute = 0
        
    def simulate_interactive_match(self):
        """Interactive match simulation"""
        print(f"\n--- Match: {self.home_team.name} vs {self.away_team.name} ---")
        
        # Determine user's team and opponent
        if self.user_team == self.home_team:
            user_side = 'home'
            opponent_side = 'away'
            user_team = self.home_team
            opponent_team = self.away_team
        elif self.user_team == self.away_team:
            user_side = 'away'
            opponent_side = 'home'
            user_team = self.away_team
            opponent_team = self.home_team
        else:
            # If no user team, simulate automatically
            return self._simulate_auto_match()
        
        # Match simulation
        for minute in range(1, 91):
            self.current_minute = minute
            print(f"\n--- Minute {minute} ---")
            print(f"Score: {self.home_team.name} {self.home_score} - {self.away_score} {self.away_team.name}")
            
            # User's turn to make a decision
            action = self._get_user_action(user_team)
            result = self._process_action(action, user_side, opponent_side)
            
            # Opponent's turn
            if result != 'goal':
                opp_action = self._get_opponent_action(opponent_team)
                self._process_action(opp_action, opponent_side, user_side)
            
            # Small delay for readability
            time.sleep(1)
        
        # Match summary
        self._match_summary()
        return self.home_score, self.away_score
    
    def _get_user_action(self, team):
        """Prompt user for match action"""
        print("\nChoose your action:")
        actions = [
            "Pass", 
            "Shoot", 
            "Dribble", 
            "Cross", 
            "Through Ball"
        ]
        
        for i, action in enumerate(actions, 1):
            print(f"{i}. {action}")
        
        while True:
            try:
                choice = int(input("Enter action number: "))
                if 1 <= choice <= len(actions):
                    return actions[choice-1]
                else:
                    print("Invalid choice. Try again.")
            except ValueError:
                print("Please enter a number.")
    
    def _get_opponent_action(self, team):
        """Generate random action for opponent"""
        actions = ["Pass", "Shoot", "Dribble", "Cross", "Through Ball"]
        return random.choice(actions)
    
    def _process_action(self, action, attacking_side, defending_side):
        """Process match action with probability of success"""
        # Skill mapping
        skill_map = {
            'Pass': 'passing',
            'Shoot': 'shooting',
            'Dribble': 'dribbling',
            'Cross': 'passing',
            'Through Ball': 'passing'
        }
        
        # Determine attacking team and skill
        attacking_team = self.home_team if attacking_side == 'home' else self.away_team
        skill_type = skill_map[action]
        
        # Calculate success probability
        best_player = max(attacking_team.players, key=lambda p: p.get_skill_rating(skill_type))
        success_prob = best_player.get_skill_rating(skill_type) / 100
        
        # Determine action outcome
        if random.random() < success_prob:
            print(f"{attacking_team.name} successfully {action.lower()}ed!")
            
            # Chance of scoring
            if action in ['Shoot', 'Through Ball']:
                if random.random() < 0.3:  # 30% chance of goal
                    if attacking_side == 'home':
                        self.home_score += 1
                    else:
                        self.away_score += 1
                    print(f"GOOOAL! {attacking_team.name} scores!")
                    return 'goal'
            
            return 'success'
        else:
            print(f"{attacking_team.name}'s {action.lower()} failed.")
            return 'failure'
    
    def _match_summary(self):
        """Display match summary"""
        print("\n--- Match Summary ---")
        print(f"{self.home_team.name} {self.home_score} - {self.away_score} {self.away_team.name}")
        
        # Determine winner
        if self.home_score > self.away_score:
            print(f"{self.home_team.name} wins!")
        elif self.home_score < self.away_score:
            print(f"{self.away_team.name} wins!")
        else:
            print("It's a draw!")
    
    def _simulate_auto_match(self):
        """Simulate match automatically if no user team"""
        # Team strength calculation
        home_strength = sum(p.overall_rating for p in self.home_team.players) / 11
        away_strength = sum(p.overall_rating for p in self.away_team.players) / 11
        
        # Probabilistic goal scoring
        home_goal_prob = home_strength / (home_strength + away_strength)
        
        for _ in range(90):
            if random.random() < home_goal_prob * 0.1:
                self.home_score += 1
            if random.random() < (1 - home_goal_prob) * 0.1:
                self.away_score += 1
        
        return self.home_score, self.away_score

class League:
    def __init__(self):
        self.teams = []
        
    def add_team(self, team):
        self.teams.append(team)
    
    def create_fixtures(self):
        """Create round-robin fixtures"""
        fixtures = []
        for i in range(len(self.teams)):
            for j in range(i+1, len(self.teams)):
                fixtures.append((self.teams[i], self.teams[j]))
        return fixtures

def create_team(name):
    """Create a team with generated players"""
    team = Team(name)
    positions = {
        'Goalkeeper': 1,
        'Defender': 4,
        'Midfielder': 4,
        'Striker': 2
    }
    
    for pos, count in positions.items():
        for _ in range(count):
            player_name = f"{name} {pos} {random.randint(1, 99)}"
            overall_rating = random.uniform(60, 90)
            age = random.randint(18, 35)
            
            player = Player(player_name, pos, overall_rating, age)
            team.add_player(player)
    
    return team

def main_menu():
    """Main game interface"""
    print("--- Football Manager Game ---")
    
    # Create league and teams
    league = League()
    team_names = [
        "Manchester City", "Liverpool", "Arsenal", "Manchester United", 
        "Chelsea", "Tottenham", "Newcastle", "Aston Villa", "Brighton"
    ]
    
    teams = {}
    for name in team_names:
        team = create_team(name)
        league.add_team(team)
        teams[name] = team
    
    while True:
        print("\nMenu:")
        print("1. Choose Your Team")
        print("2. View Teams")
        print("3. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            # Team selection
            print("\nAvailable Teams:")
            for i, name in enumerate(team_names, 1):
                print(f"{i}. {name}")
            
            try:
                team_index = int(input("Select your team: ")) - 1
                user_team_name = team_names[team_index]
                user_team = teams[user_team_name]
                
                # Match simulation menu
                while True:
                    print(f"\n--- {user_team_name} Management ---")
                    print("1. Play Match")
                    print("2. View Squad")
                    print("3. Back to Main Menu")
                    
                    match_choice = input("Enter your choice: ")
                    
                    if match_choice == '1':
                        # Choose opponent
                        print("\nChoose Opponent:")
                        opponents = [t for t in team_names if t != user_team_name]
                        for i, name in enumerate(opponents, 1):
                            print(f"{i}. {name}")
                        
                        try:
                            opp_index = int(input("Select opponent: ")) - 1
                            opponent_name = opponents[opp_index]
                            opponent_team = teams[opponent_name]
                            
                            # Create and simulate match
                            match = Match(user_team, opponent_team, user_team)
                            match.simulate_interactive_match()
                        
                        except (ValueError, IndexError):
                            print("Invalid selection!")
                    
                    elif match_choice == '2':
                        # View squad details
                        print(f"\n--- {user_team_name} Squad ---")
                        for player in user_team.players:
                            print(f"{player.name} - {player.position}")
                            print(f"  Overall: {player.overall_rating:.2f}")
                            print("  Skills:")
                            for skill, rating in player.skills.items():
                                print(f"    {skill.capitalize()}: {rating:.2f}")
                            print()
                    
                    elif match_choice == '3':
                        break
                    
                    else:
                        print("Invalid choice!")
            
            except (ValueError, IndexError):
                print("Invalid selection!")
        
        elif choice == '2':
            # View team details
            print("\n--- Team Overview ---")
            for team in league.teams:
                print(f"\n{team.name}:")
                print(f"  Players: {len(team.players)}")
                best_player = max(team.players, key=lambda p: p.overall_rating)
                print(f"  Best Player: {best_player.name} (Rating: {best_player.overall_rating:.2f})")
        
        elif choice == '3':
            print("Thanks for playing!")
            break
        
        else:
            print("Invalid choice!")

# Run the game
if __name__ == "__main__":
    main_menu()