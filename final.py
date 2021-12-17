import plotly.graph_objs as go
import final_graph


def choose_players(database):
    pg = []
    sg = []
    sf = []
    pf = []
    c = []
    total = 1
    selected = []

    for player in database:
        if database[player]["pos"][:2] == "PG":
            pg.append(player)
        elif database[player]["pos"][:2] == "SG":
            sg.append(player)    
        elif database[player]["pos"][:2] == "SF":
            sf.append(player)  
        elif database[player]["pos"][:2] == "PF":
            pf.append(player)  
        else:
            c.append(player)  

    print("Choose 5 players to build your team.")
    print("Point Guards -----------------------")
    for p in range(len(pg)):
        print(pg[p])
    print("\n")
    print("Shooting Guards --------------------")
    for s in range(len(sg)):
        print(sg[s])
    print("\n")
    print("Small Forwards ---------------------")
    for f in range(len(sf)):
        print(sf[f])
    print("\n")
    print("Power Forwards ---------------------")
    for t in range(len(pf)):
        print(pf[t])
    print("\n")
    print("Centers ----------------------------")
    for ce in range(len(c)):
        print(c[ce]) 

    while total < 6:

        select = input("Pick " + str(total) + ": ")
        if select not in database:
            print("Please enter a valid selection.")
            continue
        elif select in selected:
            print("You have already selected this player.")
            continue

        total += 1

        selected.append(select)

    return selected     
                
def print_connections(graph):
    print("Players and their chemistry with eachother | Based on position and teams played for")
    print("0 = Bad, 2 = Average, 4 = Good, 6+ = Great")
    for p in graph.getVertices():
        vert = graph.getVertex(p)
        print(vert.getName())
        print("--------------------------")
        for c in vert.getConnections():
            print(str(c.getName()) + ": " + str(vert.getWeight(c)))
        print("\n")


def team_score(database, select, tree, teamdata):
    team_wins = 0
    for player in select:
        team_wins += float(database[player]['ws'])

    total_pts = 0
    for player in select:
        total_pts += float(database[player]['pts'])

    total_ast = 0
    for player in select:
        total_ast += float(database[player]['ast'])

    total_reb = 0
    for player in select:
        total_reb += float(database[player]['reb'])

    total_stl = 0
    for player in select:
        total_stl += float(database[player]['stl'])

    total_blk = 0
    for player in select:
        total_blk += float(database[player]['blk'])

    three_avg = 0
    for player in select:
        three_avg += float(database[player]['3pt'])
    three_avg = (three_avg / 5)

    fg_avg = 0
    for player in select:
        fg_avg += float(database[player]['fg'])
    fg_avg = (fg_avg / 5)
    

    pts_grade = (total_pts / float(teamdata['pts']))
    #print("points: " + str(pts_grade))
    ast_grade = (total_ast / float(teamdata['ast']))
    #print("assists: " + str(ast_grade))
    reb_grade = (total_reb / float(teamdata['reb']))
    #print("rebounds: " + str(reb_grade))
    stl_grade = (total_stl / float(teamdata['stl']))
    #print("steals: " + str(stl_grade))
    blk_grade = (total_blk / float(teamdata['blk']))
    #print("blocks: " + str(blk_grade))
    tpt_grade = (three_avg / float(teamdata['3pt']))
    #print("3pt%: " + str(tpt_grade))
    fg_grade = (fg_avg / float(teamdata['fg']))
    #print("FG%: " + str(fg_grade))

    o_grade = pts_grade + ast_grade + tpt_grade + fg_grade
    d_grade = reb_grade + stl_grade + blk_grade

    o_bonus = 0
    if o_grade < 2.9:
        o_letter = 'F'
    elif (o_grade >= 2.9) and (o_grade < 3.4):
        o_letter = 'D'
    elif (o_grade >= 3.4) and (o_grade < 3.8):
        o_letter = 'C'
    elif (o_grade >= 3.8) and (o_grade < 4.2):
        o_letter = 'B'
        o_bonus = 1
    elif (o_grade >= 4.2) and (o_grade < 4.6):
        o_letter = 'A'
        o_bonus = 2
    else:
        o_letter = 'A+'
        o_bonus = 3

    d_bonus = 0
    if d_grade < 1.7:
        d_letter = 'F'
    elif (d_grade >= 1.7) and (d_grade < 2.2):
        d_letter = 'D'
    elif (d_grade >= 2.2) and (d_grade < 2.7):
        d_letter = 'C'
    elif (d_grade >= 2.7) and (d_grade < 3.2):
        d_letter = 'B'
        d_bonus = 1
    elif (d_grade >= 3.2) and (d_grade < 3.5):
        d_letter = 'A'
        d_bonus = 2
    else:
        d_letter = 'A+'
        d_bonus = 3
    
    chemistry_bonus = 0
    done = []
    for p in tree.getVertices():
        vert = tree.getVertex(p)
        for c in vert.getConnections():
            if c.getName() not in done:
                chemistry_bonus += float(vert.getWeight(c))
        done.append(p)
    
    if int(team_wins + chemistry_bonus + o_bonus + d_bonus) > 82:
        total_wins = 82
    else:
        total_wins = int(team_wins + chemistry_bonus + o_bonus + d_bonus)

    if chemistry_bonus < 11:
        c_letter = 'F'
        c_grade = .6
    elif (chemistry_bonus >= 11) and (chemistry_bonus < 18):
        c_letter = 'D'
        c_grade = .8
    elif (chemistry_bonus >= 18) and (chemistry_bonus < 23):
        c_letter = 'C'
        c_grade = 1.0
    elif (chemistry_bonus >= 23) and (chemistry_bonus < 28):
        c_letter = 'B'
        c_grade = 1.2
    elif (chemistry_bonus >= 28) and (chemistry_bonus < 33):
        c_letter = 'A'
        c_grade = 1.4
    else:
        c_letter = 'A+'
        c_grade = 1.6

    if team_wins < 20:
        t_grade = -.2
    elif (team_wins >= 20) and (team_wins < 30):
        t_grade = -.1
    elif (team_wins >= 30) and (team_wins < 40):
        t_grade = 0
    elif (team_wins >= 40) and (team_wins < 50):
        t_grade = .1
    elif (team_wins >= 50) and (team_wins < 60):
        t_grade = .25
    elif (team_wins >= 60) and (team_wins < 70):
        t_grade = .37
    else:
        t_grade = .5

    overall_grade = (c_grade + o_grade + d_grade + t_grade)
    
    if overall_grade < 6.2 :
        overall = 'F'
    elif (overall_grade >= 6.2) and (overall_grade < 6.9):
        overall = 'D'
    elif (overall_grade >= 6.9) and (overall_grade < 7.6):
        overall = 'C'
    elif (overall_grade >= 7.6) and (overall_grade < 8.3):
        overall = 'B'
    elif (overall_grade >= 8.3) and (overall_grade < 8.7):
        overall = 'A'
    else:
        overall = 'A+'

    team_name = str(input("Your teams name is the: "))
    print("\n")

    stats = {"name" : team_name, "wins" : total_wins, "pts" : total_pts, 'ast' : total_ast, "reb" : total_reb, "stl" : total_stl, "blk" : total_blk, "3pt" : three_avg, "fg" : fg_avg, "o" : o_letter, "d" : d_letter, "chem" : c_letter, "overall" : overall}
    
    return stats

def output(stats, database, select, teamdata, tree):

    while True:
        print("Choose a display option")
        print("---------------------------------------------------------------------------")
        print("1. Display individual player stats")
        print("2. Display team stats for the " + stats['name'])
        print("3. Show team chemistry")
        print("4. Compare the " + stats['name'] + " to the leauge averages from that year")
        print("Enter \"exit\" to quit")
        choice = input("> ")
        print("\n")


        if choice.isnumeric():
            if (int(choice) < 1) or (int(choice) > 4):
                print("Please input a valid number XXXXXXXXXXXXXXXXXX")
                print("\n")
                continue
        elif choice == "exit":
                break
        else:
            print("Please input a valid number XXXXXXXXXXXXXXXXXX")
            print("\n")
            continue

        choice = int(choice)

        if choice == 1:
            for player in select:
                print(player + " | pts:" + str(database[player]['pts']) + "  reb:" + str(database[player]['reb']) + "  ast:"  + str(database[player]['ast']) + "  stl:" + str(database[player]['stl']) + "  blk:" + str(database[player]['blk']) + "  fg%:" + str(database[player]['fg']) + "  3pt%:" + str(database[player]['3pt']))
            print("\n")

        elif choice == 2:
            print("The " + str(stats['name']))
            print("Team Statistics:")
            print("pts:" + str(round(stats['pts'], 2)) + "  reb:" + str(round(stats['reb'], 2)) + "  ast:"  + str(round(stats['ast'], 2)) + "  stl:" + str(round(stats['stl'], 2)) + "  blk:" + str(round(stats['blk'], 2)) + "  fg%:" + str(round(stats['fg'], 3)) + "  3pt%:" + str(round(stats['3pt'], 3)))
            print("Team Grades: ")
            print("Offense: " + str(stats['o']) + " Defense: " + str(stats['d']) + " Chemistry: " + str(stats['chem']))
            print("Estimated team wins: " + str(stats['wins']))
            print("Overall Team Grade: " + str(stats['overall']))
            print("\n")

        elif choice == 3:
            print_connections(tree)
            print("\n")

        elif choice == 4:
            ptsx = [teamdata['year'], stats['name']]
            ptsy = [float(teamdata['pts']), float(stats['pts'])]
            pts_data = go.Bar(x = ptsx, y = ptsy)
            pts_layout = go.Layout(title = ("Comparing Points Per Game"))
            pts_figure = go.Figure(data = pts_data, layout = pts_layout)
            pts_figure.write_html("points.html", auto_open = True)

            statsx = [teamdata['year'] + " rebounds", stats['name'] + " rebounds", teamdata['year'] + " assists", stats['name'] + " assists"]
            statsy = [float(teamdata['reb']), float(stats['reb']), float(teamdata['ast']), float(stats['ast'])]
            stats_data = go.Bar(x = statsx, y = statsy)
            stats_layout = go.Layout(title = ("Comparing Other Statistics Per Game"))
            stats_figure = go.Figure(data = stats_data, layout = stats_layout)
            stats_figure.write_html("stats.html", auto_open = True)

            defx = [teamdata['year'] + " steals", stats['name'] + " steals", teamdata['year'] + " blocks", stats['name'] + " blocks"]
            defy = [float(teamdata['stl']), float(stats['stl']), float(teamdata['blk']), float(stats['blk'])]
            def_data = go.Bar(x = defx, y = defy)
            def_layout = go.Layout(title = ("Comparing Defensive Statistics Per Game"))
            def_figure = go.Figure(data = def_data, layout = def_layout)
            def_figure.write_html("defense.html", auto_open = True)
            
            fgx = [teamdata['year'] + " fg%", stats['name'] + " fg%", teamdata['year'] + " 3pt%", stats['name'] + " 3pt%"]
            fgy = [float(teamdata['fg']), float(stats['fg']), float(teamdata['3pt']), float(stats['3pt'])]
            fg_data = go.Bar(x = fgx, y = fgy)
            fg_layout = go.Layout(title = ("Comparing Feild Goal Percentages Per Game"))
            fg_figure = go.Figure(data = fg_data, layout = fg_layout)
            fg_figure.write_html("field goal.html", auto_open = True)


    print("Thanks for playing!")
    return 


def main():

    teamdata, database = final_graph.gather_stats()
    select = choose_players(database)
    tree = final_graph.tree_builder(database, select)
    stats = team_score(database, select, tree, teamdata)
    output(stats, database, select, teamdata, tree)
    return 

if __name__ == '__main__':
    main()

