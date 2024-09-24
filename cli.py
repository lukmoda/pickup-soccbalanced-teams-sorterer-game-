import argparse
from service import TeamGeneratorService


def main():
    parser = argparse.ArgumentParser(description='Generate balanced soccer teams from a CSV file.')
    parser.add_argument('csv_path', type=str, help='Path to the CSV file containing player data')
    parser.add_argument('--teams', type=int, default=4, help='Number of teams to generate (default: 4)')

    args = parser.parse_args()

    teams = TeamGeneratorService.load_players_from_csv(args.csv_path, args.teams)

    print_teams(teams)


def print_teams(teams):
    for i, team in enumerate(teams, start=1):
        print(f'Team {i}:')
        for player in team:
            print(f'  {player["player"]} ({player["rating"]})')
        print()


if __name__ == '__main__':
    main()
