import pandas as pd

class Club:
    def __init__(self, name, points=0, position=0, goals_scored=0, goals_conceded=0, goal_difference=0, matches_played=0):
        self.name = name
        self.points = points
        self.position = position
        self.goals_scored = goals_scored  # GF
        self.goals_conceded = goals_conceded  # GA
        self.goal_difference = goal_difference  # GD
        self.matches_played = matches_played  # MP

    def update_points(self, result):
        if result == 'win':
            self.points += 3
        elif result == 'draw':
            self.points += 1
        self.matches_played += 1  # Increment matches played for any result

    def update_goals(self, goals_for, goals_against):
        self.goals_scored += goals_for
        self.goals_conceded += goals_against
        self.goal_difference += (goals_for - goals_against)

    def set_position(self, position):
        self.position = position

    def get_info(self):
        return {
            'Club': self.name,
            'Points': self.points,
            'GF': self.goals_scored,
            'GA': self.goals_conceded,
            'GD': self.goal_difference,
            'MP': self.matches_played,  # Add 'MP' to the dictionary
            'Position': self.position
        }

class League:
    def __init__(self):
        self.clubs = []

    def add_club(self, club):
        self.clubs.append(club)

    def update_league_table(self):
        # Sort clubs by points, then by goal difference if points are tied
        self.clubs.sort(key=lambda x: (x.points, x.goal_difference), reverse=True)
        for index, club in enumerate(self.clubs):
            club.set_position(index + 1)

    def display_league_table(self):
        club_data = [club.get_info() for club in self.clubs]
        df = pd.DataFrame(club_data)
        df.sort_values(by=['Position'], inplace=True)
        df.set_index('Position', inplace=True)  # Set 'Position' as the index
        print("\nLeague Table:")
        print(df)

    def update_league_with_matchday_results(self, match_results):
        """
        Updates the league table with results from a matchday.

        Args:
            match_results: A list of tuples, where each tuple represents a match:
                (home_team_name, away_team_name, home_team_goals, away_team_goals)
        """
        for home_team_name, away_team_name, home_goals, away_goals in match_results:
            home_team = next((club for club in self.clubs if club.name == home_team_name), None)
            away_team = next((club for club in self.clubs if club.name == away_team_name), None)

            if home_team and away_team:
                if home_goals > away_goals:
                    home_team.update_points("win")
                    away_team.update_points("loss")
                elif home_goals < away_goals:
                    home_team.update_points("loss")
                    away_team.update_points("win")
                else:  # Draw
                    home_team.update_points("draw")
                    away_team.update_points("draw")

                home_team.update_goals(home_goals, away_goals)
                away_team.update_goals(away_goals, home_goals)

        self.update_league_table()  # Update the league table after processing all matches

# Create 20 club objects
club1 = Club("Arsenal")
club2 = Club("Man United")
club3 = Club("Man City")
club4 = Club("Liverpool")
club5 = Club("Tottenham")
club6 = Club("Chelsea")
club7 = Club("Newcastle United")
club8 = Club("Aston Villa")
club9 = Club("West Ham United")
club10 = Club("Brighton & Hove Albion")
club11 = Club("Wolverhampton Wanderers")
club12 = Club("Leeds United")
club13 = Club("Leicester City")
club14 = Club("Everton")
club15 = Club("Southampton")
club16 = Club("Crystal Palace")
club17 = Club("Brentford")
club18 = Club("Nottingham Forest")
club19 = Club("Fulham")
club20 = Club("Bournemouth")

# Create a league and add clubs
Premier_League = League()
clubs = [club1, club2, club3, club4, club5, club6, club7, club8, club9, club10, club11, club12, club13, club14, club15, club16, club17, club18, club19, club20]
for club in clubs:
    Premier_League.add_club(club)

# Update and display the league table
Premier_League.update_league_table()
Premier_League.display_league_table()

# Example usage of the new method
matchday_results = [
    ("Arsenal", "Man United", 3, 1),
    ("Man City", "Liverpool", 3, 0),
    ("Tottenham", "Chelsea", 2, 1),
    ("Newcastle United", "Aston Villa", 2, 2),
    ("West Ham United", "Brighton & Hove Albion", 0, 2),
    ("Wolverhampton Wanderers", "Leeds United", 2, 2),
    ("Leicester City", "Everton", 1, 4),
    ("Southampton", "Crystal Palace", 1, 1),
    ("Brentford", "Nottingham Forest", 3, 2),
    ("Fulham", "Bournemouth", 3, 1),
]

Premier_League.update_league_with_matchday_results(matchday_results)
Premier_League.display_league_table() 

#crete a database to store results and table status