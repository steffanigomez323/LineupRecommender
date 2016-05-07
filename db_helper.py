"""
CS1951A Final Project
Brown University
Spring 2016

Vann, Steffani, JJ, Chaitu

Database
"""
from app import nba_stattleship
from app import nf_scraper
from app import redis_db
from app import nba_scraper
from app import namespace
import csv
import time


class RedisHelper(object):
    # populate the database with all players using
    # stattleship, nba and numberfire
    def populate_db(self):
        # flush the db
        redis_db.flushall()

        # set basic information
        self.set_basic_player_information()

        # get nba players' names and ids
        nba_players = nba_scraper.get_player_data()
        nba_name_to_id = nba_scraper.get_player_name_id_map(nba_players)

        # set nba to stattleship mapping
        self.set_nba_to_stattleship_maps(nba_name_to_id)

        # set numberfire to nba mapping
        self.set_nf_to_nba_maps(nba_name_to_id)

        # set player stats
        self.set_player_stats(nba_name_to_id)

    def set_basic_player_information(self):
        # get player data from stattleship
        stattleship_data = nba_stattleship.get_player_data()
        # get only the required fields
        stattleship_players = nba_stattleship.get_player_fields(
            stattleship_data)

        # set the player basic information in redis
        for player in stattleship_players:
            name = player["name"]
            weight = player["weight"]
            height = player["height"]
            active = player["active"]
            years_of_experience = player["years_of_experience"]

            redis_db.hmset(player["slug"], {'name': name,
                                            'height': height,
                                            'weight': weight,
                                            'active': active,
                                            'years_of_experience':
                                            years_of_experience})

    def set_nba_to_stattleship_maps(self, nba_name_to_id):
        # get stattleship players' names and slugs
        stattleship_players = nba_stattleship.get_player_data()
        stattleship_name_to_slug = nba_stattleship.get_player_name_slug_map(
            stattleship_players)

        # set all the nba id to stattleship slug maps in redis
        for nba_name, nba_id in nba_name_to_id.iteritems():
            if nba_name in stattleship_name_to_slug.iterkeys():
                stattleship_slug = stattleship_name_to_slug[nba_name]
                redis_db.set(nba_id, stattleship_slug)

        # set all the mismatches manually
        redis_db.set('203933', 'nba-t-j-warren')
        redis_db.set('203922', 'nba-glenn-robinson-iii')
        redis_db.set('203798', 'nba-p-j-hairston')
        redis_db.set('2403', 'nba-nene')
        redis_db.set('101236', 'nba-chuck-hayes')
        redis_db.set('203912', 'nba-c-j-wilcox')
        redis_db.set('203468', 'nba-c-j-mccollum')
        redis_db.set('200782', 'nba-p-j-tucker')
        redis_db.set('203909', 'nba-k-j-mcdaniels')
        redis_db.set('101139', 'nba-c-j-miles')
        redis_db.set('201581', 'nba-j-j-hickson')
        redis_db.set('203948', 'nba-johnny-o-bryant-iii')
        redis_db.set('201228', 'nba-c-j-watson')
        redis_db.set('101150', 'nba-louis-williams')
        redis_db.set('200755', 'nba-j-j-redick')
        redis_db.set('1626154', 'nba-r-j-hunter')
        redis_db.set('203960', 'nba-jakarr-sampson')
        redis_db.set('1626202', 'nba-joseph-young')
        redis_db.set('204456', 'nba-t-j-mcconnell')
        redis_db.set('201591', 'nba-d-j-white')
        redis_db.set('203315', 'nba-toure-murry')
        redis_db.set('203548', 'nba-elias-harris')
        redis_db.set('200839', 'nba-mike-harris')
        redis_db.set('2562', 'nba-aleksandar-pavlovic')
        redis_db.set('204021', 'nba-sim-bhullar')
        redis_db.set('204033', 'nba-david-wear')
        redis_db.set('203474', 'nba-d-j-stephens')
        redis_db.set('203816', 'nba-scotty-hopson')
        redis_db.set('203540', 'nba-luigi-datome')
        redis_db.set('204037', 'nba-travis-wear')
        redis_db.set('203580', 'nba-larry-drew-ii')
        redis_db.set('203945', 'nba-alex-kirk')
        redis_db.set('204079', 'nba-drew-gordon')
        redis_db.set('202197', 'nba-shane-edwards')
        redis_db.set('201595', 'nba-joey-dorsey')
        redis_db.set('203106', 'nba-jeffery-taylor')
        redis_db.set('201986', 'nba-nando-de-colo')
        redis_db.set('203139', 'nba-vyacheslav-kravtsov')
        redis_db.set('2052', 'nba-deshawn-stevenson')

    def set_nf_to_nba_maps(self, nba_name_to_id):
        # get numberfire players' names and slugs
        nf_name_to_slug = nf_scraper.get_player_name_slug_map()

        # set all the nf slug to nba id maps in redis
        for nf_name, nf_slug in nf_name_to_slug.iteritems():
            if nf_name in nba_name_to_id.iterkeys():
                nba_id = nba_name_to_id[nf_name]
                redis_db.set(nf_slug, nba_id)

        # set all the mismatches manually
        redis_db.set('patrick-mills', '201988')
        redis_db.set('glenn-robinson-iii', '203922')
        redis_db.set('k-j-mcdaniels', '203909')
        redis_db.set('c-j-wilcox', '203912')
        redis_db.set('louis-amundson', '200811')
        redis_db.set('p-j-hairston', '203798')
        redis_db.set('louis-williams', '101150')
        redis_db.set('c-j-mccollum', '203468')
        redis_db.set('joseph-young', '1626202')
        redis_db.set('r-j-hunter', '1626154')
        redis_db.set('t-j-warren', '203933')
        redis_db.set('cj-watson', '201228')
        redis_db.set('p-j-tucker', '200782')
        redis_db.set('ishmael-smith', '202397')
        redis_db.set('johnny-o-bryant-iii', '203948')
        redis_db.set('jj-hickson', '201581')
        redis_db.set('nene-hilario', '2403')
        redis_db.set('jj-redick', '200755')
        redis_db.set('roy-devyn-marble', '203906')
        redis_db.set('cj-miles', '101139')
        redis_db.set('t-j-mcconnell', '204456')

    def set_player_stats(self, nba_name_to_id):
        player_stats = nba_scraper.get_player_stats()
        gamelog_data = nba_scraper.get(
            player_stats)
        count = 0
        for nba_id in gamelog_data:
            start_time = time.clock()
            gameids = []
            if str(nba_id) not in nba_name_to_id.values():
                print nba_id
                count = count + 1
                continue
            stattleship_slug = redis_db.get(nba_id)
            for game in gamelog_data[nba_id]['allgames']:

                gameids.append(game[0])
                redis_db.hmset(game[0], {'game_time': game[1],
                                         'played_at_home': game[2],
                                         'played_against': game[3],
                                         'plus_minus': game[4],
                                         'time_played_total': game[5],
                                         'rebounds_total': game[6],
                                         'assists': game[7],
                                         'steals': game[8],
                                         'blocks': game[9],
                                         'turnovers': game[10],
                                         'points': game[11]})

            redis_db.lpush(stattleship_slug + namespace.GAMELOGS, *gameids)

            end_time = time.clock()

            print("Time taken: {} seconds.\n".format(end_time - start_time))
        print count

class CSVHelper(object):
    # populate the database with all players using
    # stattleship, nba and numberfire
    def create_csvs(self):
        # set basic information
        self.create_basic_player_information_csv()

        # get nba players' names and ids
        nba_players = nba_scraper.get_player_data()
        nba_name_to_id = nba_scraper.get_player_name_id_map(nba_players)

        # set nba to stattleship mapping
        self.create_nba_to_stattleship_csv(nba_name_to_id)

        # set numberfire to nba mapping
        self.create_numberfire_to_nba_csv(nba_name_to_id)

        # set player stats
        self.create_player_stats_csv(nba_name_to_id)

    def create_basic_player_information_csv(self):
        # get player data from stattleship
        stattleship_data = nba_stattleship.get_player_data()
        # get only the required fields
        stattleship_players = nba_stattleship.get_player_fields(
            stattleship_data)

        # set the player basic information in redis
        for player in stattleship_players:
            name = player["name"]
            weight = player["weight"]
            height = player["height"]
            active = player["active"]
            years_of_experience = player["years_of_experience"]

            redis_db.hmset(player["slug"], {'name': name,
                                            'height': height,
                                            'weight': weight,
                                            'active': active,
                                            'years_of_experience':
                                            years_of_experience})

    def create_nba_to_stattleship_csv(self, nba_name_to_id):
        # get stattleship players' names and slugs
        stattleship_players = nba_stattleship.get_player_data()
        stattleship_name_to_slug = nba_stattleship.get_player_name_slug_map(
            stattleship_players)

        # set all the nba id to stattleship slug maps in redis
        for nba_name, nba_id in nba_name_to_id.iteritems():
            if nba_name in stattleship_name_to_slug.iterkeys():
                with open(namespace.NBA_TO_STATTLESHIP_CSV, 'wb') as f:
                    writer = csv.writer(f)
                    writer.writerows(someiterable)
                stattleship_slug = stattleship_name_to_slug[nba_name]
                redis_db.set(nba_id, stattleship_slug)

        # set all the mismatches manually
        redis_db.set('203933', 'nba-t-j-warren')
        redis_db.set('203922', 'nba-glenn-robinson-iii')
        redis_db.set('203798', 'nba-p-j-hairston')
        redis_db.set('2403', 'nba-nene')
        redis_db.set('101236', 'nba-chuck-hayes')
        redis_db.set('203912', 'nba-c-j-wilcox')
        redis_db.set('203468', 'nba-c-j-mccollum')
        redis_db.set('200782', 'nba-p-j-tucker')
        redis_db.set('203909', 'nba-k-j-mcdaniels')
        redis_db.set('101139', 'nba-c-j-miles')
        redis_db.set('201581', 'nba-j-j-hickson')
        redis_db.set('203948', 'nba-johnny-o-bryant-iii')
        redis_db.set('201228', 'nba-c-j-watson')
        redis_db.set('101150', 'nba-louis-williams')
        redis_db.set('200755', 'nba-j-j-redick')
        redis_db.set('1626154', 'nba-r-j-hunter')
        redis_db.set('203960', 'nba-jakarr-sampson')
        redis_db.set('1626202', 'nba-joseph-young')
        redis_db.set('204456', 'nba-t-j-mcconnell')
        redis_db.set('201591', 'nba-d-j-white')
        redis_db.set('203315', 'nba-toure-murry')
        redis_db.set('203548', 'nba-elias-harris')
        redis_db.set('200839', 'nba-mike-harris')
        redis_db.set('2562', 'nba-aleksandar-pavlovic')
        redis_db.set('204021', 'nba-sim-bhullar')
        redis_db.set('204033', 'nba-david-wear')
        redis_db.set('203474', 'nba-d-j-stephens')
        redis_db.set('203816', 'nba-scotty-hopson')
        redis_db.set('203540', 'nba-luigi-datome')
        redis_db.set('204037', 'nba-travis-wear')
        redis_db.set('203580', 'nba-larry-drew-ii')
        redis_db.set('203945', 'nba-alex-kirk')
        redis_db.set('204079', 'nba-drew-gordon')
        redis_db.set('202197', 'nba-shane-edwards')
        redis_db.set('201595', 'nba-joey-dorsey')
        redis_db.set('203106', 'nba-jeffery-taylor')
        redis_db.set('201986', 'nba-nando-de-colo')
        redis_db.set('203139', 'nba-vyacheslav-kravtsov')
        redis_db.set('2052', 'nba-deshawn-stevenson')

    def create_numberfire_to_nba_csv(self, nba_name_to_id):
        # get numberfire players' names and slugs
        nf_name_to_slug = nf_scraper.get_player_name_slug_map()

        # set all the nf slug to nba id maps in redis
        for nf_name, nf_slug in nf_name_to_slug.iteritems():
            if nf_name in nba_name_to_id.iterkeys():
                nba_id = nba_name_to_id[nf_name]
                redis_db.set(nf_slug, nba_id)

        # set all the mismatches manually
        redis_db.set('patrick-mills', '201988')
        redis_db.set('glenn-robinson-iii', '203922')
        redis_db.set('k-j-mcdaniels', '203909')
        redis_db.set('c-j-wilcox', '203912')
        redis_db.set('louis-amundson', '200811')
        redis_db.set('p-j-hairston', '203798')
        redis_db.set('louis-williams', '101150')
        redis_db.set('c-j-mccollum', '203468')
        redis_db.set('joseph-young', '1626202')
        redis_db.set('r-j-hunter', '1626154')
        redis_db.set('t-j-warren', '203933')
        redis_db.set('cj-watson', '201228')
        redis_db.set('p-j-tucker', '200782')
        redis_db.set('ishmael-smith', '202397')
        redis_db.set('johnny-o-bryant-iii', '203948')
        redis_db.set('jj-hickson', '201581')
        redis_db.set('nene-hilario', '2403')
        redis_db.set('jj-redick', '200755')
        redis_db.set('roy-devyn-marble', '203906')
        redis_db.set('cj-miles', '101139')
        redis_db.set('t-j-mcconnell', '204456')

    def create_player_stats_csv(self, nba_name_to_id):
        player_stats = nba_scraper.get_player_stats()
        gamelog_data = nba_scraper.get(
            player_stats)
        count = 0
        for nba_id in gamelog_data:
            start_time = time.clock()
            gameids = []
            if str(nba_id) not in nba_name_to_id.values():
                print nba_id
                count = count + 1
                continue
            stattleship_slug = redis_db.get(nba_id)
            for game in gamelog_data[nba_id]['allgames']:

                gameids.append(game[0])
                redis_db.hmset(game[0], {'game_time': game[1],
                                         'played_at_home': game[2],
                                         'played_against': game[3],
                                         'plus_minus': game[4],
                                         'time_played_total': game[5],
                                         'rebounds_total': game[6],
                                         'assists': game[7],
                                         'steals': game[8],
                                         'blocks': game[9],
                                         'turnovers': game[10],
                                         'points': game[11]})

            redis_db.lpush(stattleship_slug + namespace.GAMELOGS, *gameids)

            end_time = time.clock()

            print("Time taken: {} seconds.\n".format(end_time - start_time))
        print count

    def prepare_data_from_csvs(self):
        pass
