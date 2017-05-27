# get record info for a given level from speedrun.com

import requests
from math import floor
from random import randrange

class GetData():
    def __init__(self, lvl_code, *costume):
        # level code must be in the format G-W-L (including the hyphens)
        # optional costume argument will get the time for just a single costume
        self.BB_IDs = ['369gjg1l', 'yd4qx56e', '76rpo518']
        self.base_address = 'http://www.speedrun.com/api/v1'


        self.places = ['1st', '2nd', '3rd']
        self.return_data = "```\n"
        try:
            if lvl_code[0] == '1':
                game, world = lvl_code.split('-')
                self.return_data += "World record times for BoxBoy {0}, world {1}\n".format(game, world)
            else:
                game, world, lvl = lvl_code.split('-')
                self.return_data += "World record times for BoxBoy {0}, world {1}, level {2}\n".format(game, world, lvl)
            game = int(game)

            if costume:
                self.costume = costume[0].upper()
                # fix up the discrepancy between naming of the rabbit costume between regions/games
                if game == 1:
                    if 'RABBIT'.startswith(self.costume):
                        self.costume = 'BUNNY'
                elif game ==  2 or game == 3:
                    if 'BUNNY'.startswith(self.costume):
                        self.costume = 'RABBIT'
            else:
                self.costume = 'ALL'

            # for now just assume that we only want IL's
            game_id = self.BB_IDs[game - 1]
            # first get the lists of levels
            levels_list = requests.get('{0}/games/{1}/levels'.format(self.base_address, game_id)).json()['data']
            # next get the list of categories
            game_categories = requests.get('{0}/games/{1}/categories'.format(self.base_address, game_id)).json()['data']
            self.category_dict = dict()        

            for category in game_categories:
                self.category_dict[category['id']] = category['name']
            if game == 1:
                # in this case we don't care about the level number as we only have worlds
                for level in levels_list:
                    split_name = level['name'].split(' ')
                    if split_name[-1] == world and split_name[0] != 'Time' and world[:2] != 'TA':
                        level_id = level['id']
                    elif split_name[-1] == world[2:] and split_name[0] == 'Time' and world[:2] == 'TA':
                        level_id = level['id']
            elif game == 2 or game == 3:
                for level in levels_list:
                    name = level['name']
                    if name == '{0}-{1}'.format(world, lvl):
                        level_id = level['id']
            try:
                self.processData(level_id)
            except:
                # in this case no valid level id was found, so we will just return that the requested level doesn't exist
                self.return_data = "```\nThe level you requested does not exist. Please enter a valid level number```"
            
        except:
            # Something went wrong...
            self.return_data = "```\nYour request was not formatted correctly or did not have enough information. Please enter a valid level number```"        

    def processData(self, level_id):
        num_records = 0
        level_records = requests.get('{0}/levels/{1}/records'.format(self.base_address, level_id)).json()['data']
        for category in level_records:
            cat_name = self.category_dict[category['category']]
            if self.costume == 'ALL' or cat_name.upper().startswith(self.costume):
                self.return_data += "{0}\n".format(cat_name)
                i = 0
                if len(category['runs']) != 0:
                    for run in category['runs']:
                        run_data = run['run']
                        player = self.getUser(run_data['players'][0]['id'])
                        time = self.convertTime(run_data['times']['primary_t'])
                        self.return_data += "{0}: {1} ({2})\n".format(self.places[i], player, time)
                        i += 1
                    num_records += 1
                else:
                    self.return_data += 'No times recorded for this category\n'
        if num_records != 0:
            self.return_data += "```"
        else:
            self.return_data = "```\nNo data available for requested category```"

    def getUser(self, uid):
        # returns the name of the user associated with a specific id
        userdata = requests.get('{0}/users/{1}'.format(self.base_address, uid)).json()['data']
        return userdata['names']['international']

    def convertTime(self, time):
        # this will convert the given time to min:seconds.miliseconds format
        t = float(time)
        mins = floor(t/60)
        secs = t%60
        return('{0}:{1:.2f}'.format(mins, secs))

def GetRandom():
    # this will return a random valid level code
    ranges = {1: 23, 2: 17, 3: 23}


    breakdown = {2: {3: [0], 6: [1,2,3], 7: [4, 5, 6, 7, 8, 9], 8: [10, 11, 12, 13, 14, 15, 16]},
                   3: {6: [1,2,3,4,6,7,10,11,14], 7: [5,8,12,15,16,17,19,20], 8: [9,13,18,21,22]}}

    game = randrange(1, 4)
    world = randrange(1, ranges[game])
    if game != 1:
        for key in breakdown[game]:
            if  world in breakdown[game][key]:
                level = randrange(1, key + 1)
    else:
        level = None

    if level:
        return "Play {0}-{1}-{2}".format(game, world, level)
    else:
        return "Play {0}-{1}".format(game, world)
        

if __name__ == "__main__":
    a = GetRandom()
    #data = GetData('2-13', 'R')
    #print(data.return_data)
