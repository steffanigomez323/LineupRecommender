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
import time
import csv


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
        n = namespace.Namespace()
        with open(n.PLAYER_INFO_CSV, 'wb') as f:
            writer = csv.writer(f)
            writer.writerow(['player_slug', 'name', 'height', 'weight', 'active', 'years_of_experience'])
            for player in stattleship_players:
                name = player["name"]
                weight = player["weight"]
                height = player["height"]
                active = player["active"]
                years_of_experience = player["years_of_experience"]
                writer.writerow([player["slug"], name, height, weight, active, years_of_experience])

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

            redis_db.lpush(stattleship_slug + Namespace.GAMELOGS, *gameids)

            end_time = time.clock()

            print("Time taken: {} seconds.\n".format(end_time - start_time))
        print count


class CSVHelper(object):
    # populate the database with all players using
    # stattleship, nba and numberfire
    def create_csvs(self):
        # set basic information
        #self.create_basic_player_information_csv()

        # get nba players' names and ids
        nba_players = nba_scraper.get_player_data()
        nba_name_to_id = nba_scraper.get_player_name_id_map(nba_players)

        self.create_basic_player_information_csv(nba_name_to_id)

        # set nba to stattleship mapping
        self.create_nba_to_stattleship_csv(nba_name_to_id)

        # set numberfire to nba mapping
        self.create_numberfire_to_nba_csv(nba_name_to_id)

        # set player stats
        self.create_player_stats_csv(nba_name_to_id)

    def create_basic_player_information_csv(self, nba_name_to_id):
        # data to write
        data = [['player_slug', 'name', 'height',
                 'weight', 'active', 'years_of_experience']]

        # get player data from stattleship
        stattleship_data = nba_stattleship.get_player_data()
        # get only the required fields
        stattleship_players = nba_stattleship.get_player_fields(
            stattleship_data)

        count = 0
        # set the player basic information
        for player in stattleship_players:
            #print player
            slug = player["slug"]
            name = player["name"]

            if name not in nba_name_to_id.keys():
                print name
                print ""
                count += 1
                continue

            playerid = nba_name_to_id[name]
            position = nba_scraper.get_player_position(playerid)
            #print name
            #print position
            #print ""
            height = player["height"]
            weight = player["weight"]
            active = player["active"]
            years_of_experience = player["years_of_experience"]
            data.append([slug, name, height, weight, active,
                         years_of_experience])

        # write to csv
        print count
        with open(namespace.PLAYER_INFO_CSV, 'wb') as f:
            writer = csv.writer(f)
            writer.writerows(data)

    def create_nba_to_stattleship_csv(self, nba_name_to_id):
        # data to write
        data = [['nba_id', 'stattleship_slug']]

        # get stattleship players' names and slugs
        stattleship_players = nba_stattleship.get_player_data()
        stattleship_name_to_slug = nba_stattleship.get_player_name_slug_map(
            stattleship_players)

        # set all the nba id to stattleship slug maps
        for nba_name, nba_id in nba_name_to_id.iteritems():
            if nba_name in stattleship_name_to_slug.iterkeys():
                stattleship_slug = stattleship_name_to_slug[nba_name]
                data.append([nba_id, stattleship_slug])

        # set all the mismatches manually
        data.append(['203933', 'nba-t-j-warren'])
        data.append(['203922', 'nba-glenn-robinson-iii'])
        data.append(['203798', 'nba-p-j-hairston'])
        data.append(['2403', 'nba-nene'])
        data.append(['101236', 'nba-chuck-hayes'])
        data.append(['203912', 'nba-c-j-wilcox'])
        data.append(['203468', 'nba-c-j-mccollum'])
        data.append(['200782', 'nba-p-j-tucker'])
        data.append(['203909', 'nba-k-j-mcdaniels'])
        data.append(['101139', 'nba-c-j-miles'])
        data.append(['201581', 'nba-j-j-hickson'])
        data.append(['203948', 'nba-johnny-o-bryant-iii'])
        data.append(['201228', 'nba-c-j-watson'])
        data.append(['101150', 'nba-louis-williams'])
        data.append(['200755', 'nba-j-j-redick'])
        data.append(['1626154', 'nba-r-j-hunter'])
        data.append(['203960', 'nba-jakarr-sampson'])
        data.append(['1626202', 'nba-joseph-young'])
        data.append(['204456', 'nba-t-j-mcconnell'])
        data.append(['201591', 'nba-d-j-white'])
        data.append(['203315', 'nba-toure-murry'])
        data.append(['203548', 'nba-elias-harris'])
        data.append(['200839', 'nba-mike-harris'])
        data.append(['2562', 'nba-aleksandar-pavlovic'])
        data.append(['204021', 'nba-sim-bhullar'])
        data.append(['204033', 'nba-david-wear'])
        data.append(['203474', 'nba-d-j-stephens'])
        data.append(['203816', 'nba-scotty-hopson'])
        data.append(['203540', 'nba-luigi-datome'])
        data.append(['204037', 'nba-travis-wear'])
        data.append(['203580', 'nba-larry-drew-ii'])
        data.append(['203945', 'nba-alex-kirk'])
        data.append(['204079', 'nba-drew-gordon'])
        data.append(['202197', 'nba-shane-edwards'])
        data.append(['201595', 'nba-joey-dorsey'])
        data.append(['203106', 'nba-jeffery-taylor'])
        data.append(['201986', 'nba-nando-de-colo'])
        data.append(['203139', 'nba-vyacheslav-kravtsov'])
        data.append(['2052', 'nba-deshawn-stevenson'])

        # write to csv
        with open(namespace.NBA_TO_STATTLESHIP_CSV, 'wb') as f:
            writer = csv.writer(f)
            writer.writerows(data)

    def create_numberfire_to_nba_csv(self, nba_name_to_id):
        # data to write
        data = [['numberfire_slug', 'nba_id']]

        # get numberfire players' names and slugs
        nf_name_to_slug = nf_scraper.get_player_name_slug_map()

        # set all the nf slug to nba id maps
        for nf_name, nf_slug in nf_name_to_slug.iteritems():
            if nf_name in nba_name_to_id.iterkeys():
                nba_id = nba_name_to_id[nf_name]
                data.append([nf_slug, nba_id])

        # set all the mismatches manually
        data.append(['patrick-mills', '201988'])
        data.append(['glenn-robinson-iii', '203922'])
        data.append(['k-j-mcdaniels', '203909'])
        data.append(['c-j-wilcox', '203912'])
        data.append(['louis-amundson', '200811'])
        data.append(['p-j-hairston', '203798'])
        data.append(['louis-williams', '101150'])
        data.append(['c-j-mccollum', '203468'])
        data.append(['joseph-young', '1626202'])
        data.append(['r-j-hunter', '1626154'])
        data.append(['t-j-warren', '203933'])
        data.append(['cj-watson', '201228'])
        data.append(['p-j-tucker', '200782'])
        data.append(['ishmael-smith', '202397'])
        data.append(['johnny-o-bryant-iii', '203948'])
        data.append(['jj-hickson', '201581'])
        data.append(['nene-hilario', '2403'])
        data.append(['jj-redick', '200755'])
        data.append(['roy-devyn-marble', '203906'])
        data.append(['cj-miles', '101139'])
        data.append(['t-j-mcconnell', '204456'])

        # write to csv
        with open(namespace.NUMBERFIRE_TO_NBA_CSV, 'wb') as f:
            writer = csv.writer(f)
            writer.writerows(data)

    def create_player_stats_csv(self, nba_name_to_id):
        # data to write
        data = [['nba_id', 'game_time', 'played_at_home',
                 'played_against', 'plus_minus',
                 'time_played_total', 'rebounds_total',
                 'assists', 'steals', 'blocks',
                 'turnovers', 'points']]

        # get the stats data
        player_stats = nba_scraper.get_player_stats()
        gamelog_data = nba_scraper.prepare_data_for_projections(
            player_stats)

        for nba_id in gamelog_data:

            if str(nba_id) not in nba_name_to_id.values():
                continue

            for game in gamelog_data[nba_id]['allgames']:
                data.append([nba_id, game[1], game[2], game[3],
                             game[4], game[5], game[6], game[7],
                             game[8], game[9], game[10], game[11]])

        # write to csv
        with open(namespace.PLAYER_STATS_CSV, 'wb') as f:
            writer = csv.writer(f)
            writer.writerows(data)

    def prepare_data_from_csvs(self):
        # create player information map from csv
        players = {}

        with open(namespace.PLAYER_INFO_CSV, 'rb') as pi:
            reader = csv.reader(pi)
            reader.next()
            for row in reader:
                slug = row[0]
                name = row[1]
                height = row[2]
                weight = row[3]
                active = row[4]
                years_of_experience = row[5]

                players[slug] = {'name': name, 'height': height,
                                 'weight': weight, 'active': active,
                                 'years_of_experience': years_of_experience,
                                 'gamelogs': []}

        # create nba to stattleship map from csv
        nba_to_stattleship_map = {}

        with open(namespace.NBA_TO_STATTLESHIP_CSV, 'rb') as ns:
            reader = csv.reader(ns)
            reader.next()
            for row in reader:
                nba_to_stattleship_map[row[0]] = row[1]

        # create number fire to nba map from csv
        nf_to_nba_map = {}

        with open(namespace.NUMBERFIRE_TO_NBA_CSV, 'rb') as nn:
            reader = csv.reader(nn)
            reader.next()
            for row in reader:
                nf_to_nba_map[row[0]] = row[1]

        # create number fire to stattleship map
        nf_to_stattleship_map = {}

        for nf_slug, nba_id in nf_to_nba_map.iteritems():
            stattleship_slug = nba_to_stattleship_map[nba_id]
            nf_to_stattleship_map[nf_slug] = stattleship_slug

        with open(namespace.PLAYER_STATS_CSV) as ps:
            reader = csv.reader(ps)
            reader.next()
            for row in reader:
                slug = nba_to_stattleship_map[row[0]]
                if slug in players:
                    players[slug]['gamelogs'].append(row[1:])

        return players, nf_to_stattleship_map
