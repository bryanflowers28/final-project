from bs4 import BeautifulSoup
import bs4.element 
import requests
import json

class Vertex:
    def __init__(self, name):
        self.name = name
        self.connectedTo = {}

    def addNeighbor(self, nbr, weight=0):
        self.connectedTo[nbr] = weight

    def getName(self):
        return self.name

    def getWeight(self, nbr):
        return self.connectedTo[nbr]

    def getConnections(self):
        return self.connectedTo.keys()

class Graph:
    def __init__(self):
        self.vertList = {}
        self.numVertices = 0

    def addVertex(self, name):
        self.numVertices = self.numVertices + 1
        newVertex = Vertex(name)
        self.vertList[name] = newVertex
        return newVertex

    def getVertex(self, vert):
        if vert in self.vertList:
            return self.vertList[vert]
        else:
            return None

    def __contains__(self,n):
        return n in self.vertList

    def addEdge(self, vert1, vert2, weight=0):
        if vert1 not in self.vertList:
            new_vertex1 = self.addVertex(vert1)
        if vert2 not in self.vertList:
            new_vertex2 = self.addVertex(vert2)
        self.vertList[vert1].addNeighbor(self.vertList[vert2], weight)
        self.vertList[vert2].addNeighbor(self.vertList[vert1], weight)

    def getVertices(self):
        return self.vertList.keys()

    def __iter__(self):
        return iter(self.vertList.values())


def gather_stats():

    while True:
            year = input("Choose a year (1980 - 2021) : ")
            if year.isnumeric():
                if (int(year) >= 1980) and (int(year) <= 2021):
                    break
                else:
                    print("Please input a valid year XXXXXXXXXXXXXXXXXX")
            else:
                print("Please input a valid year XXXXXXXXXXXXXXXXXX")

    year_file = str(year) + ".json"

    teamdata = team_stats(year)

    database = open_cache(year_file)
    if not database:

        r = requests.get("https://www.basketball-reference.com/leagues/NBA_" + str(year) + "_per_game.html")

        data = r.text
        soup = BeautifulSoup(data , 'html.parser')

        player_data = soup.find_all('tr', class_ = "full_table")

        player_data = sort(player_data)

        for total_player in player_data:
            player_name = total_player.find('a').contents[0]
            #print(player_name)

            pts_gm = total_player.find('td', {'data-stat' : "pts_per_g"}).contents[0]
            #print(pts_gm)

            reb_gm = total_player.find('td', {'data-stat' : "trb_per_g"}).contents[0]
            #print(reb_gm)

            a_gm = total_player.find('td', {'data-stat' : "ast_per_g"}).contents[0]
            #print(a_gm)
            
            pos = total_player.find('td', {'data-stat' : "pos"}).contents[0]
            #print(pos)

            stl_gm = total_player.find('td', {'data-stat' : "stl_per_g"}).contents[0]

            blk_gm = total_player.find('td', {'data-stat' : "blk_per_g"}).contents[0]

            tpp_temp = total_player.find('td', {'data-stat' : "fg3_pct"}).contents
            if len(tpp_temp) == 0:
                tpp = 0
            else:
                tpp = tpp_temp[0]

            fg = total_player.find('td', {'data-stat' : "fg_pct"}).contents[0]

            teams = player_connections(total_player)

            ws = win_shares(total_player, year)

            database[player_name] = {"pos" : pos, "pts" : pts_gm, "reb" : reb_gm, "ast" : a_gm, "stl" : stl_gm, "blk" : blk_gm, "3pt" : tpp , "fg" : fg, "ws" : ws, "teams" : teams}

        save_cache(database, year_file)

        return teamdata, database

    else:
        return teamdata, database

def team_stats(year):
    teamstats = {}
    r = requests.get("https://www.basketball-reference.com/leagues/NBA_" + str(year) + ".html#all_per_poss_team-opponent")

    data = r.text
    soup = BeautifulSoup(data , 'html.parser')

    whole_table = soup.find_all('table', id = "per_game-team")[0]
    row = whole_table.find('tfoot').contents[0]
    teamstats['year'] = year
    leauge_pts = row.find('td', {'data-stat' : "pts"}).contents[0]
    teamstats['pts'] = leauge_pts

    leauge_ast = row.find('td', {'data-stat' : "ast"}).contents[0]
    teamstats['ast'] = leauge_ast

    leauge_orb = row.find('td', {'data-stat' : "orb"}).contents[0]
    leauge_drb = row.find('td', {'data-stat' : "drb"}).contents[0]
    teamstats['reb'] = float(leauge_orb) + float(leauge_drb)

    leauge_stl = row.find('td', {'data-stat' : "stl"}).contents[0]
    teamstats['stl'] = leauge_stl

    leauge_blk = row.find('td', {'data-stat' : "blk"}).contents[0]
    teamstats['blk'] = leauge_blk

    leauge_3pt_temp = row.find('td', {'data-stat' : "fg3_pct"}).contents
    if len(leauge_3pt_temp) == 0:
        leauge_3pt = 0
    else:
        leauge_3pt = leauge_3pt_temp[0]
    teamstats['3pt'] = leauge_3pt

    leauge_fg = row.find('td', {'data-stat' : "fg_pct"}).contents[0]
    teamstats['fg'] = leauge_fg

    return teamstats


def sort(player_data):
    for i in range(len(player_data)):
        if i == 0:
            continue
        current = player_data[i]
        before = i - 1
        while before >= 0 and (float(current.contents[-1].contents[0]) > float(player_data[before].contents[-1].contents[0])):
            temp = player_data[before + 1]
            player_data[before + 1] = player_data[before]
            player_data[before] = temp
            before -= 1
        player_data[before + 1] == current

    new_data = []
    for x in range(50):
        new_data.append(player_data[x])

    return new_data


def player_connections(total_player):

    link = total_player.find('a', href = True)['href']
    r = requests.get("https://www.basketball-reference.com" + link)
    
    d = r.text
    soup = BeautifulSoup(d, 'html.parser')

    player_past = soup.find_all('tr', class_ = "full_table")

    lot = []
    for i in player_past:
        team_tag = i.find('td', {'data-stat' : "team_id"}).contents[0]
        if team_tag == 'TOT':
            continue
        lot.append(team_tag.contents[0])

    teams = []
    for t in lot:
        if t not in teams:
            teams.append(t)
    
    return teams

#need to find a way to shorten this if I have time
def win_shares(total_player, year):

    link = total_player.find('a', href = True)['href']
    r = requests.get("https://www.basketball-reference.com" + link)
    
    d = r.text
    soup = BeautifulSoup(d, 'html.parser')

    player_past = soup.find_all('tr', id = "advanced." + str(year))[0]

    ws = player_past.find('td', {'data-stat' : "ws"}).contents[0] 

    if isinstance(ws, bs4.element.Tag):
        return ws.contents[0]
    
    return ws


def open_cache(year_file):
    try:
        cache_file = open(year_file, 'r')
        cache_contents = cache_file.read()
        cache_dict = json.loads(cache_contents)
        cache_file.close
    except:
        cache_dict = {}
    return cache_dict


def save_cache(cache_dict, year_file):
    dumped = json.dumps(cache_dict)
    fw = open(year_file, "w")
    fw.write(dumped)
    fw.close()

def tree_builder(database, select):
    g = Graph()
    for player in select:
        g.addVertex(player)
    
    for player in select:
        for other in select:
            score = 0
            if player == other:
                continue
            else: 
                if database[player]['pos'] != database[other]['pos']:
                    score += 2
                for team in database[player]['teams']:
                    if team in database[other]['teams']:
                        score += 2
            g.addEdge(player, other, weight = score)
    return g 