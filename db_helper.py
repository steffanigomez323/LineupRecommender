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
from updater import DailyUpdate


class RedisHelper(object):
    # populate the database with all players using
    # stattleship, nba and numberfire
    def populate_db(self):
        # flush the db
        redis_db.flushall()

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

        # get nba players' names and ids
        nba_players = nba_scraper.get_player_data()
        nba_name_to_id = nba_scraper.get_player_name_id_map(nba_players)

        # get stattleship players' names and slugs
        stattleship_players = nba_stattleship.get_player_data()
        stattleship_name_to_slug = nba_stattleship.get_player_name_slug_map(stattleship_players)

        # set all the nba id to stattleship slug maps in redis
        for nba_name, nba_id in nba_name_to_id.iteritems():
            if nba_name in stattleship_name_to_slug:
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

        # get numberfire players' names and slugs
        nf_name_to_slug = nf_scraper.get_player_name_slug_map()

        # set all the nf slug to nba id maps in redis
        for nf_name, nf_slug in nf_name_to_slug.iteritems():
            if nf_name in nba_name_to_id:
                nba_id = nba_name_to_id[nf_name]
                redis.set(nf_slug, nba_id)

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


        #     if player["active"]:
        #         stattleship_id_list.append(player["slug"])

        # player_stats = nba_scraper.get_player_stats('2015-16')
        # clean_players_stats = nba_scraper.clean_player_stats2(player_stats)

        # nba_names = {}

        # player_names = nba_scraper.get_players()
        # player_names = nba_scraper.clean_players(player_names)

        # nba_id_list = clean_players_stats.keys()
        # nba_names_list = []

        # for id in nba_id_list:
        #     name = clean_players_stats[id]['player_name']
        #     nba_names[id] = name
        #     nba_names_list.append('nba-' + "-".join(name.split(" ")))

        #     nba_id = player["slug"].split("nba-")[-1]
        #     stattleship_ids.add(nba_id.encode('utf-8'))

        # nf_ids = nf_scraper.get_all_player_data()

        # id_not_match = list(nf_ids - stattleship_ids)
        # assert len(id_not_match) == 16
        # Cristiano Felicio is shown as 'Chistiano Felicio' in Stattleship
        # redis_db.set('nf-jj-redick', 'nba-j-j-redick')
        # redis_db.set('nf-jose-barea', 'nba-jose-juan-barea')
        # redis_db.set('nf-chris-johnson1', 'nba-chris-johnson')
        # redis_db.set('nf-amare-stoudemire', 'nba-amar-e-stoudemire')
        # redis_db.set('nf-oj-mayo', 'nba-o-j-mayo')
        # redis_db.set('nf-nene-hilario', 'nba-nene')
        # redis_db.set('nf-cj-miles', 'nba-c-j-miles')
        # redis_db.set('nf-jr-smith', 'nba-j-r-smith')
        # redis_db.set('nf-cj-watson', 'nba-c-j-watson')
        # redis_db.set('nf-dj-augustin', 'nba-d-j-augustin')
        # redis_db.set('nf-ishmael-smith', 'nba-ish-smith')
        # redis_db.set('nf-cristiano-felicio', 'nba-chistiano-felicio') 
        # redis_db.set('nf-louis-amundson', 'nba-lou-amundson')
        # redis_db.set('nf-etwaun-moore', 'nba-e-twaun-moore')
        # redis_db.set('nf-jj-hickson', 'nba-j-j-hickson')
        # redis_db.set('nf-roy-devyn-marble', 'nba-devyn-marble')

        # assert len(stattleship_id_list) == 1049

        # # Store gamelogs in the database
        # du = DailyUpdate()
        # du.store_stattleship_gamelogs(du.create_stattleship_games(stattleship_id_list[:200]))
        # du.store_stattleship_gamelogs(du.create_stattleship_games(stattleship_id_list[200:400]))
        # du.store_stattleship_gamelogs(du.create_stattleship_games(stattleship_id_list[400:600]))
        # du.store_stattleship_gamelogs(du.create_stattleship_games(stattleship_id_list[600:800]))
        # du.store_stattleship_gamelogs(du.create_stattleship_games(stattleship_id_list[800:1000]))
        # du.store_stattleship_gamelogs(du.create_stattleship_games(stattleship_id_list[1000:]))
