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
from updater import DailyUpdate
from data_collector import NBAScraper


class RedisHelper(object):

    # populate the database with all players using stattleship and numberfire
    def populate_db(self):
        # flush the db

        # redis_db.flushall()
        nbascrape = NBAScraper()

        stattleship_data = nba_stattleship.get_player_data()
        stattleship_players = nba_stattleship.get_player_fields(stattleship_data)

        stattleship_id_list = []

        # stattleship_ids = set([])
        for player in stattleship_players:

            # nba_names = player["slug"].split("nba-")
            # name = nba_names[len(nba_names) - 1].replace("-", " ")
            # weight = player["weight"]
            # height = player["height"]
            # active = player["active"]
            # years_of_experience = player["years_of_experience"]


        #     redis_db.hmset(player["slug"], {'name': name,
        #                                'height': height,
        #                                'weight': weight,
        #                                'active': active,
        #                                'years_of_experience': years_of_experience})
            if player["active"] == True:
                stattleship_id_list.append(player["slug"])

        player_stats = nbascrape.get_player_stats('2015-16')
        clean_players_stats = nbascrape.clean_player_stats2(player_stats)

        nba_names = {}

        player_names = nbascrape.get_players()
        player_names = nbascrape.clean_players(player_names)

        nba_id_list = clean_players_stats.keys()
        nba_names_list = []

        for id in nba_id_list:
            name = clean_players_stats[id]['player_name']
            nba_names[id] = name
            nba_names_list.append('nba-' + "-".join(name.split(" ")))

        #print stattleship_id_list

        #print "##########"
        #print ""

        #print nba_names_list

        #print "########"
        #print ""

        # print stattleship_id_list

        # print "########"
        # print ""

        # print nba_names_list

        # print "########"
        # print ""

        missed_ids = list(set(stattleship_id_list) - set(nba_names_list))

        print "### MISSED IDS ###"

        print len(missed_ids)
        print missed_ids

        print "### MATCHED IDS ###"

        correct_ids = list(set(stattleship_id_list) - set(missed_ids))

        print len(correct_ids)
        print correct_ids

        #     nba_id = player["slug"].split("nba-")[-1]
        #     stattleship_ids.add(nba_id.encode('utf-8'))

        # nf_ids = nf_scraper.get_all_player_data()

        # id_not_match = list(nf_ids - stattleship_ids)
        # assert len(id_not_match) == 16
        # # Cristiano Felicio is shown as 'Chistiano Felicio' in Stattleship
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

        # Store gamelogs in the database
        du = DailyUpdate()
        # du.store_stattleship_gamelogs(du.create_stattleship_games(stattleship_id_list[:200]))
        # du.store_stattleship_gamelogs(du.create_stattleship_games(stattleship_id_list[200:400]))
        du.store_stattleship_gamelogs(du.create_stattleship_games(stattleship_id_list[400:600]))
        du.store_stattleship_gamelogs(du.create_stattleship_games(stattleship_id_list[600:800]))
        du.store_stattleship_gamelogs(du.create_stattleship_games(stattleship_id_list[800:1000]))
        du.store_stattleship_gamelogs(du.create_stattleship_games(stattleship_id_list[1000:]))
