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
        # set numberfire to nbs mapping
        self.set_nf_to_nba_maps(nba_name_to_id)

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

    def set_nf_to_nba_maps(self, nba_name_to_id):
        # get numberfire players' names and slugs
        nf_name_to_slug = nf_scraper.get_player_name_slug_map()

        # set all the nf slug to nba id maps in redis
        for nf_name, nf_slug in nf_name_to_slug.iteritems():
            if nf_name in nba_name_to_id.iterkeys():
                nba_id = nba_name_to_id[nf_name]
                redis_db.set(nf_slug, nba_id)

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
