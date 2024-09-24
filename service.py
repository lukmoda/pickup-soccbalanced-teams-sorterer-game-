import pandas as pd
import random
import io


class TeamGeneratorService:
    def __init__(self, players_df):
        """
        players_df: DataFrame containing columns 'player', 'rating', and 'is_going'
        """
        self.df = players_df

    def find_teams(self, guess, num_teams):
        teams = {i: [] for i in range(1, num_teams + 1)}
        for i, e in enumerate(guess):
            teams[e].append(i)

        team_dfs = {i: self.df.loc[teams[i]] for i in range(1, num_teams + 1)}
        avgs = [team_dfs[i]["rating"].mean() for i in range(1, num_teams + 1)]
        max_diff = max(avgs) - min(avgs)
        return team_dfs, max_diff

    def generate_optimized_teams(self, initial_guess, num_teams):
        new_guess = initial_guess.copy()
        best_guess = initial_guess.copy()
        max_diff_best = None
        max_trials = 10000
        count = 0

        while count < max_trials and (max_diff_best is None or max_diff_best > 0):
            random.shuffle(new_guess)
            _, max_diff = self.find_teams(new_guess, num_teams)

            if max_diff_best is None or max_diff < max_diff_best:
                max_diff_best = max_diff
                best_guess = new_guess.copy()

            count += 1

        return best_guess, max_diff_best

    def generate_teams(self, team_count):
        initial_guess = [i % team_count + 1 for i in range(len(self.df))]
        best_guess, max_diff_best = self.generate_optimized_teams(initial_guess, team_count)
        team_dfs, max_diff = self.find_teams(best_guess, team_count)

        teams = []
        for i in range(1, team_count + 1):
            team = team_dfs[i].to_dict(orient='records')
            teams.append(team)

        return teams

    @staticmethod
    def process_players_dataframe(df):
        df = df[df['is_going'] == 1]
        groups = [df for _, df in df.groupby('rating')]
        random.shuffle(groups)
        df = pd.concat(groups).reset_index(drop=True)
        return df

    @staticmethod
    def load_players_from_csv(csv_path, team_count):
        df = pd.read_csv(csv_path)
        df = TeamGeneratorService.process_players_dataframe(df)
        service = TeamGeneratorService(df)
        return service.generate_teams(team_count)

    @staticmethod
    def process_uploaded_csv(file_content, team_count):
        df = pd.read_csv(io.StringIO(file_content.decode('utf-8')))
        df = TeamGeneratorService.process_players_dataframe(df)
        service = TeamGeneratorService(df)
        return service.generate_teams(team_count)

    @staticmethod
    def load_players_from_list(players, team_count):
        df = pd.DataFrame(players)
        df = TeamGeneratorService.process_players_dataframe(df)
        service = TeamGeneratorService(df)
        return service.generate_teams(team_count)

