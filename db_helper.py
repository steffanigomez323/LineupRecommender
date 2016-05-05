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


class RedisHelper(object):

    # populate the database with all players using stattleship and numberfire
    def populate_db(self):
        # flush the db

        
        # redis_db.flushall()

        stattleship_data = nba_stattleship.get_player_data()
        stattleship_players = nba_stattleship.get_player_fields(stattleship_data)

        stattleship_id_list = []

        # stattleship_ids = set([])
        for player in stattleship_players:

        #     nba_names = player["slug"].split("nba-")
        #     name = nba_names[len(nba_names) - 1].replace("-", " ")
        #     weight = player["weight"]
        #     height = player["height"]
        #     active = player["active"]
        #     years_of_experience = player["years_of_experience"]


        #     redis_db.hmset(player["slug"], {'name': name,
        #                                'height': height,
        #                                'weight': weight,
        #                                'active': active,
        #                                'years_of_experience': years_of_experience})

            stattleship_id_list.append(player["slug"])

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
        # du.store_stattleship_gamelogs(du.create_stattleship_games(['nba-jeff-adrien']))
        du.store_stattleship_gamelogs(du.create_stattleship_games(stattleship_id_list[1048]))
