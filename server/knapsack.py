import mongo
import numpy
import jsonpickle
import json
from flask import jsonify

leagues132 = []

# fixed_quantity:
#  W = Capacity, players = dict of id->player, count = how many elements to collect
def dynamic_program_knapsack(W, players, count):
    numOfItems = len(players)
    matrix = numpy.zeros((numOfItems,W + 1,count+1))
    keys = list(players.keys())
    for i in range(numOfItems):
        for j in range(W+1):
            for k in range(count+1):
                if players[keys[i]]["price"] > j or 1 > k:
                    matrix[i][j][k] = matrix[i-1][j][k]
                else:
                    matrix[i][j][k] = max(matrix[i-1][j][k], players[keys[i]]["performance"] + matrix[i-1][j-players[keys[i]]["price"]][k-1])
    return matrix

def get_used_indexes(W, players, count ,matrix):
    itemIndex = len(players) - 1
    currentCost = -1
    currentCount = -1
    marked = [0] * len(matrix)
    keys = list(players.keys())

    #Locate the cell with the maximun value:
    bestValue = -1
    for j in range(W+1):
        for k in range(count+1):
            value = matrix[itemIndex][j][k]
            if(bestValue == -1 or value > bestValue):
                currentCost = j
                currentCount = k
                bestValue = value
            
    while itemIndex >= 0 and currentCost >= 0 and currentCount >= 0:
        if (itemIndex == 0 and matrix[itemIndex][currentCost][currentCount] > 0) or (matrix[itemIndex][currentCost][currentCount] != matrix[itemIndex-1][currentCost][currentCount]):
            marked[itemIndex] = 1
            currentCost -= players[keys[itemIndex]]["price"]
            currentCount -= 1
        itemIndex -= 1
    
    return marked

def get_players_map():
    players = mongo.create_player_avg_performance_map()
    return players

def get_used_players():
    players = get_players_map()
    values_list = list(players.values())
    final_matrix = dynamic_program_knapsack(100, players, 11)
    used_indexes = get_used_indexes(100, players, 11, final_matrix)
    fantasy_league = []
    for i in range(len(used_indexes)):
        if used_indexes[i] == 1:
            fantasy_league.append(values_list[i])
    print("after fantasy league")
    return jsonpickle.encode(fantasy_league)

# players = get_used_players()
# jsonPlayers = json.dumps(players)
# jsonifyPlayers = jsonify(players)
# print(jsonPlayers)