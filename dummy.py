from app import nba_scraper
from app import nba_stattleship

# get nba players' names and ids
nba_players = nba_scraper.get_player_data()
nba_name_to_id = nba_scraper.get_player_name_id_map(nba_players)

# get stattleship players' names and slugs
stattleship_players = nba_stattleship.get_player_data()
stattleship_name_to_slug = nba_stattleship.get_player_name_slug_map(
    stattleship_players)

# set all the nba id to stattleship slug maps in redis
# for nba_name, nba_id in nba_name_to_id.iteritems():
#     if nba_name in stattleship_name_to_slug.iterkeys():
#         stattleship_slug = stattleship_name_to_slug[nba_name]
#         redis_db.set(nba_id, stattleship_slug)

nba_name_set = set(nba_name_to_id.keys())
stattleship_name_set = set(stattleship_name_to_slug.keys())

print stattleship_name_to_slug
