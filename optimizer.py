"""
CS1951A Final Project
Brown University
Spring 2016

Vann, Steffani, JJ, Chaitu

Simple Optimal Lineup Recommender
"""
import random
import json

class SimpleOptimizer(object):
    global salary_cap 
    salary_cap = 60000000;
    lineup_size = 9

    # input: projections.json
    f = open('projections.json', 'r')
    global projections 
    projections= json.load(f)
    
    
    """
    This is a method returns a simple, optimal lineup based on the salaries from swish analytics.
    """

    def get_simple_lineup(self):
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

        update = []
        lineup = []

        j = 0
        while value_2d[0][j][2] >= salary_cap/9:
            j += 1

        lineup.append((value_2d[0][j][0], value_2d[0][j][1], value_2d[0][j][2]))
        update.append(value_2d[0][j][2]) # salary

        for i in range(1, 9):
            k = 0
            while (lineup[i-1] == value_2d[i][k][0] or (value_2d[i][k][2] + update[i-1]) >= (salary_cap/9)*(i+1)):
                k += 1
            lineup.append((value_2d[i][k][0], value_2d[i][k][1], value_2d[i][k][2]))
            update.append(value_2d[i][k][2])

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


    def pack5(items,sizeLimit):
        P = {}
        for nItems in range(len(items)+1):
            for lim in range(sizeLimit+1):
                if nItems == 0:
                    P[nItems,lim] = 0
                elif itemSize(items[nItems-1]) > lim:
                    P[nItems,lim] = P[nItems-1,lim]
                else:
                    P[nItems,lim] = max(P[nItems-1,lim],
                        P[nItems-1,lim-itemSize(items[nItems-1])] +
                        itemValue(items[nItems-1]))
        
        L = []      
        nItems = len(items)
        lim = sizeLimit
        while nItems > 0:
            if P[nItems,lim] == P[nItems-1,lim]:
                nItems -= 1
            else:
                nItems -= 1
                L.append(itemName(items[nItems]))
                lim -= itemSize(items[nItems])

        L.reverse()
        return L

   def knapsack(items, maxweight):
    """
    Solve the knapsack problem by finding the most valuable
    subsequence of `items` subject that weighs no more than
    `maxweight`.

    `items` is a sequence of pairs `(value, weight)`, where `value` is
    a number and `weight` is a non-negative integer.

    `maxweight` is a non-negative integer.

    Return a pair whose first element is the sum of values in the most
    valuable subsequence, and whose second element is the subsequence.

    >>> items = [(4, 12), (2, 1), (6, 4), (1, 1), (2, 2)]
    >>> knapsack(items, 15)
    (11, [(2, 1), (6, 4), (1, 1), (2, 2)])
    """

    # Return the value of the most valuable subsequence of the first i
    # elements in items whose weights sum to no more than j.
    @memoized
    def bestvalue(i, j):
        if i == 0: return 0
        value, weight = items[i - 1]
        if weight > j:
            return bestvalue(i - 1, j)
        else:
            return max(bestvalue(i - 1, j),
                       bestvalue(i - 1, j - weight) + value)

    j = maxweight
    result = []
    for i in xrange(len(items), 0, -1):
        if bestvalue(i, j) != bestvalue(i - 1, j):
            result.append(items[i - 1])
            j -= items[i - 1][1]
    result.reverse()
    return bestvalue(len(items), maxweight), result 
           