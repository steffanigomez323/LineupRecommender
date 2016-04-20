"""
CS1951A Final Project
Brown University
Spring 2016

Vann, Steffani, JJ, Chaitu

Lineup Optimizer
"""
<<<<<<< HEAD:simple_recommender.py
import random
import json
=======

>>>>>>> 0bbfb3ba6759305f37c6d8852f8bde04bd910817:optimizer.py

class SimpleRecommender(object):
    global salary_cap 
    salary_cap = 60000000;
    lineup_size = 9

<<<<<<< HEAD:simple_recommender.py
    # input: projections.json
    f = open('projections.json', 'r')
    global projections 
    projections= json.load(f)
    
    
=======
    def __init__(self, players):
        self.players = players

    def print_all_players(self):
        for player in self.players:
            print player

>>>>>>> 0bbfb3ba6759305f37c6d8852f8bde04bd910817:optimizer.py
    """
    This is a method returns a simple, optimal lineup based on the salaries from swish analytics.
    """

    def get_simple_lineup(self):
<<<<<<< HEAD:simple_recommender.py
        # lineup = [(None, 0.0)] * lineup_size # need 2 best players for each position except the center
        value_2d = []
        salary_2d = [] # keeps track of the salary given so far to a potential player; same size as value_2d
        for i in range(9):
            salary_2d.append([])

        optimum_2d = []
        for i in range(9):
            optimum_2d.append([])

        C_list = []
        PG_list = []
        SG_list = []
        SF_list = []
        PF_list = []

        # O(number of players)
        for item in projections:
            if item['fd_pos'] == 'C':
                C_list.append((item['player_id'], float(item['proj_fantasy_pts_fd']), int(item['fd_salary'])))
            elif item['fd_pos'] == 'PG':
                PG_list.append((item['player_id'], float(item['proj_fantasy_pts_fd']), int(item['fd_salary'])))
            elif item['fd_pos'] == 'SG':
                SG_list.append((item['player_id'], float(item['proj_fantasy_pts_fd']), int(item['fd_salary'])))
            elif item['fd_pos'] == 'SF':
                SF_list.append((item['player_id'], float(item['proj_fantasy_pts_fd']), int(item['fd_salary'])))
            elif item['fd_pos'] == 'PF':
                PF_list.append((item['player_id'], float(item['proj_fantasy_pts_fd']), int(item['fd_salary'])))

        ### The lists happen to be sorted, but just in case the input data aren't always sorted ###

        # sort the lists by points and added to value_2d to make a 2d array of tuples of (points, salary)
        value_2d.append(sorted(C_list, key=lambda x: x[1], reverse=True)) # C
        value_2d.append(sorted(PG_list, key=lambda x: x[1], reverse=True)) # PG1
        value_2d.append(sorted(PG_list, key=lambda x: x[1], reverse=True)) # PG2
        value_2d.append(sorted(SG_list, key=lambda x: x[1], reverse=True))
        value_2d.append(sorted(SG_list, key=lambda x: x[1], reverse=True)) 
        value_2d.append(sorted(SF_list, key=lambda x: x[1], reverse=True))
        value_2d.append(sorted(SF_list, key=lambda x: x[1], reverse=True)) 
        value_2d.append(sorted(PF_list, key=lambda x: x[1], reverse=True))
        value_2d.append(sorted(PF_list, key=lambda x: x[1], reverse=True)) 

        """
        # create a list of 9 lists that stores salaries; O(number of players)
        for c in value_2d[0]:
            salary_2d[0].append(c[2]) # (point, salary)
            
        for pg in value_2d[1]:
            salary_2d[1].append(pg[2])
            salary_2d[2].append(pg[2])
            
        for sg in value_2d[3]:
            salary_2d[3].append(sg[2])
            salary_2d[4].append(sg[2])

        for sf in value_2d[5]:
            salary_2d[5].append(sf[2])
            salary_2d[6].append(sf[2])
            
        for pf in value_2d[7]:
            salary_2d[7].append(pf[2])
            salary_2d[8].append(pf[2])
"""
=======
        lineup = list()
        salary = 0
        pg = 0
        sg = 0
        sf = 0
        pf = 0
        c = 0

        playersSorted = sorted(self.players, key=lambda x: float(x.projected_points), reverse=True)

        for p in playersSorted:
            if p.injury_status == "Not Injured" and int(p.salary) <= (self.salary_cap / 9):
                if p.position == 'PG':                     
                    if p not in lineup:
                        if (pg <= 1):
                            salary = salary + int(p.salary)
                            lineup.append(p)
                            pg = pg + 1

                elif p.position == 'SG':
                    if p not in lineup:
                        if (sg <= 1):
                            salary = salary + int(p.salary)
                            lineup.append(p)
                            sg = sg + 1
                            
                elif p.position == 'SF':
                    if p not in lineup:
                        if (sf <= 1):
                            salary = salary + int(p.salary)
                            lineup.append(p)
                            sf = sf + 1

                elif p.position == 'PF':
                    if p not in lineup:
                        if (pf <= 1):
                            salary = salary + int(p.salary)
                            lineup.append(p)
                            pf = pf + 1
                            
                else: # the position is C (Center)
                    if p not in lineup:
                        if (c <= 0):
                            salary = salary + int(p.salary)
                            lineup.append(p)
                            c = c + 1
                            
            if c > 0 and pf > 1 and sf > 1 and sg > 1 and pg > 1:
                break
                               
        assert(len(lineup) == 9)
        assert(salary <= self.salary_cap)
>>>>>>> 0bbfb3ba6759305f37c6d8852f8bde04bd910817:optimizer.py

        update = []
        lineup = []

        j = 0
        while value_2d[0][j][2] >= salary_cap/9:
            j += 1

        lineup.append(value_2d[0][j][0])
        update.append(value_2d[0][j][2]) # salary

        for i in range(1, 9):
            k = 0
            while (lineup[i-1] == value_2d[i][k][0] or (value_2d[i][k][2] + update[i-1]) >= (salary_cap/9)*(i+1)):
                k += 1
            lineup.append(value_2d[i][k][0])
            update.append(value_2d[i][k][2])

        print lineup
        return lineup

    '''
    DON'T RUN THIS. IT'S NOT SERIOUS.
    '''
    def get_lineup_bruteforce(self):
        value_2d = []
        C_list = []
        PG_list = []
        SG_list = []
        SF_list = []
        PF_list = []

        # O(number of players)
        for item in projections:
            if item['fd_pos'] == 'C':
                C_list.append((item['player_id'], float(item['proj_fantasy_pts_fd']), int(item['fd_salary'])))
            elif item['fd_pos'] == 'PG':
                PG_list.append((item['player_id'], float(item['proj_fantasy_pts_fd']), int(item['fd_salary'])))
            elif item['fd_pos'] == 'SG':
                SG_list.append((item['player_id'], float(item['proj_fantasy_pts_fd']), int(item['fd_salary'])))
            elif item['fd_pos'] == 'SF':
                SF_list.append((item['player_id'], float(item['proj_fantasy_pts_fd']), int(item['fd_salary'])))
            elif item['fd_pos'] == 'PF':
                PF_list.append((item['player_id'], float(item['proj_fantasy_pts_fd']), int(item['fd_salary'])))

        ### I'm not kidding. This is brute force. Consider _every_ possible combination of lineup ###
        best = []
        for c_index in range(len(C_list)):
            for pg1_index in range(len(PG_list) - 1):
                for pg2_index in range(pg1_index, len(PG_list)):
                    for sg1_index in range(len(SG_list)-1):
                        for sg2_index in range(sg1_index, len(SG_list)):
                            for sf1_index in range(len(SF_list)-1):
                                for sf2_index in range(sf1_index, len(SF_list)):
                                    for pf1_index in range(len(PF_list) - 1):
                                        for pf2_index in range(pf1_index, len(PF_list)):
                                            # calculate salary first to save runtime
                                            salary = sum([C_list[c_index][2],
                                                        PG_list[pg1_index][2],
                                                        PG_list[pg2_index][2],
                                                        SG_list[sg1_index][2],
                                                        SG_list[sg2_index][2],
                                                        SF_list[sf1_index][2],
                                                        SF_list[sf2_index][2],
                                                        PF_list[pf1_index][2],
                                                        PF_list[pf2_index][2]])

                                            if salary <= salary_cap:
                                                lineup = [C_list[c_index][0], 
                                                            PG_list[pg1_index][0], 
                                                            PG_list[pg2_index][0], 
                                                            SG_list[sg1_index][0], 
                                                            SG_list[sg2_index][0], 
                                                            SF_list[sf1_index][0], 
                                                            SF_list[sf2_index][0], 
                                                            PF_list[pf1_index][0], 
                                                            PF_list[pf2_index][0]]

                                                score = sum([C_list[c_index][1],
                                                        PG_list[pg1_index][1],
                                                        PG_list[pg2_index][1],
                                                        SG_list[sg1_index][1],
                                                        SG_list[sg2_index][1],
                                                        SF_list[sf1_index][1],
                                                        SF_list[sf2_index][1],
                                                        PF_list[pf1_index][1],
                                                        PF_list[pf2_index][1]])

                                                if len(best) == 0:
                                                    best.append((lineup, score))
                                                else:
                                                    if best[0][1] < score:
                                                        best[0] = (lineup, score)
                                                        
        # print best
        return best                                               
                                                
    get_simple_lineup(object)
    # get_lineup_bruteforce(object)
                     