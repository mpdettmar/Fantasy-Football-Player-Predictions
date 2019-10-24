import time
from sportsreference.nfl.teams import Teams 
import pandas as pd

defense_list = []

for year in ['2010', '2011', '2012']:
	teams = Teams(year)
	for team in teams:
		i = 1
		for game in team.schedule:
			t0 = time.time()
			if game.location=='Home':
				prefix='away'
			else:
				prefix='home'
			game_df = game.boxscore.dataframe
			row = [
				team.abbreviation,
				game.datetime,
				game_df['{}_fumbles_lost'.format(prefix)].values[0],
				game_df['{}_interceptions'.format(prefix)].values[0],
				game_df['{}_pass_yards'.format(prefix)].values[0],
				game_df['{}_rush_yards'.format(prefix)].values[0],
				game_df['{}_times_sacked'.format(prefix)].values[0],
				game_df['{}_points'.format(prefix)].values[0]
			]
			defense_list.append(row)
			print('{}, {} game {} finished in {:.2f}s'.format(year, team.abbreviation, i, time.time() - t0))
			i += 1

defense_df = pd.DataFrame(
	defense_list,
	columns = [
	'team', 
	'date',
	'fumbles_forced',
	'interceptions',
	'pass_yards_allowed',
	'rush_yards_allowed',
	'sacks',
	'points_allowed'
	])

defense_df.to_csv('../data/opponents/defensive_stats.csv', index=False)