

class Namespace(object):
    # gamelogs id postfix
    GAMELOGS = "gamelogs"

    # redis last updated key
    REDIS_LAST_UPDATED_KEY = "last_updated"

    # team name maps
    TEAM_MAP_NF_NBA = {"CHI": 'CHI',
                       "CHA": 'CHA',
                       "UTAH": 'UTA',
                       "IND": 'IND',
                       "NO": 'NOP',
                       "ORL": 'ORL',
                       "MIN": 'MIN',
                       "ATL": 'ATL',
                       "POR": 'POR',
                       "WSH": 'WAS',
                       "PHX": 'PHX',
                       "MEM": 'MEM',
                       "MIA": 'MIA',
                       "CLE": 'CLE',
                       "GS": 'GSW',
                       "DET": 'DET',
                       "LAL": 'LAL',
                       "POR": 'POR',
                       "SAC": 'SAC',
                       "DEN": 'DEN',
                       "TOR": 'TOR',
                       "LAC": 'LAC',
                       "BOS": 'BOS',
                       "BKN": 'BKN',
                       "SA": 'SACN',
                       "NY": 'NYK',
                       "DAL": 'DAL',
                       "OKC": 'OKC',
                       "MIL": 'MIL',
                       "HOU": 'HOU'}

    # csv file names
    PLAYER_INFO_CSV = "player_info.csv"
    NBA_TO_STATTLESHIP_CSV = "nba_to_stattleship_map.csv"
    NUMBERFIRE_TO_NBA_CSV = "numberfire_to_nba_map.csv"
    PLAYER_STATS_CSV = "player_stats.csv"
