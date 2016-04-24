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


class RedisHelper(object):

    # populate the database with all players using stattleship and numberfire
    def populate_db(self):
        # flush the db
        redis_db.flushall()

        stattleship_data = nba_stattleship.get_player_data()
        stattleship_players = nba_stattleship.get_player_fields(stattleship_data)

        stattleship_ids = set([])
        for player in stattleship_players:

            nba_names = player["slug"].split("nba-")
            name = nba_names[len(nba_names) - 1].replace("-", " ")
            weight = player["weight"]
            height = player["height"]
            active = player["active"]
            years_of_experience = player["years_of_experience"]


            redis_db.hmset(player["slug"], {'name': name,
                                       'height': height,
                                       'weight': weight,
                                       'active': active,
                                       'years_of_experience': years_of_experience})

            nba_id = player["slug"].split("nba-")[-1]
            stattleship_ids.add(nba_id.encode('utf-8'))

        nf_ids = nf_scraper.get_all_player_data()

        id_not_match = list(nf_ids - stattleship_ids)
        assert id_not_match == 16
        # Cristiano Felicio is shown as 'Chistiano Felicio' in Stattleship
        redis_db.set('jj-redick', 'j-j-redick')
        redis_db.set('jose-barea', 'jose-juan-barea')
        redis_db.set('chris-johnson1', 'chris-johnson')
        redis_db.set('amare-stoudemire', 'amar-e-stoudemire')
        redis_db.set('oj-mayo', 'o-j-mayo')
        redis_db.set('nene-hilario', 'nene')
        redis_db.set('cj-miles', 'c-j-miles')
        redis_db.set('jr-smith', 'j-r-smith')
        redis_db.set('cj-watson', 'c-j-watson')
        redis_db.set('dj-augustin', 'd-j-augustin')
        redis_db.set('ishmael-smith', 'ish-smith')
        redis_db.set('cristiano-felicio', 'chistiano-felicio') 
        redis_db.set('louis-amundson', 'lou-amundson')
        redis_db.set('etwaun-moore', 'e-twaun-moore')
        redis_db.set('jj-hickson', 'j-j-hickson')
        redis_db.set('roy-devyn-marble', 'devyn-marble')
