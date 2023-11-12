import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
import os


# Function to scrape individual team data
def scrape_team_data(team_name, season):
    team_url = f'https://understat.com/team/{team_name}/{season}'
    response = requests.get(team_url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "lxml")
        scripts = soup.find_all('script')

        for el in scripts:
            if 'teamsData' in str(el):
                json_data = str(el).split('JSON.parse(\'')[1].split('\')')[0].encode().decode('unicode_escape')
                team_data = json.loads(json_data)
                return team_data

    return None


# Directory setup
if not os.path.exists('football_data_csv'):
    os.makedirs('football_data_csv')


# League and season setup
base_url = 'https://understat.com/league'
leagues = ['La_liga', 'EPL', 'Bundesliga', 'Serie_A', 'Ligue_1', 'RFPL']
seasons = [str(year) for year in range(2014, 2024)]


# Scraping team data
print("Starting to scrape team data...")
for league in leagues:
    league_data = {}

    for season in seasons:

        season_data = {}
        url = f'{base_url}/{league}/{season}'
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "lxml")
        scripts = soup.find_all('script')

        for script in scripts:

            if script.string and 'teamsData' in script.string:  # Check if script.string is not None
                json_data = script.string.split("('")[1].split("')")[0].encode().decode('unicode_escape')
                data = json.loads(json_data)

                for team_id, team_info in data.items():

                    team_name = team_info['title']
                    team_stats = team_info['history']
                    team_df = pd.DataFrame(team_stats)
                    season_data[team_name] = team_df

                    # Save each team's data as a CSV file
                    csv_filename = f'football_data_csv/{league}_{season}_{team_name}.csv'
                    team_df.to_csv(csv_filename, index=False)
                    print(f"Saved {team_name} data for {season} season.")

        league_data[season] = season_data

    print(f"Finished scraping {league} league data.")






