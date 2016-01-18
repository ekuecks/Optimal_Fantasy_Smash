import sys
# dp array nxWx13
dp = []

# players -> array of all players as a tuple of (name, salary, value)
# players_left -> roster space left
# cap -> cap room left
def optimal(players, players_left, cap):
    num_players = len(players)
    # base cases
    # not enough players left to fill out the roster
    # or no more players left to look at
    # or no more room on the roster
    # or we have already solved this case
    if dp[num_players][players_left][cap] != None:
        return dp[num_players][players_left][cap]
    # either the first player in the player array is in the optimal solution or isn't
    # if we don't sign this player, will there be enough players left to fill the roster
    excludable = num_players > players_left
    not_in = (-1, [])
    if excludable:
        not_in = optimal(players[1:], players_left, cap)
    if not_in[0] < 0:
        excludable = False
    # is there enough slary cap for this player
    signable = cap - players[0][1] >= 0
    is_in = (-1, [])
    if signable:
        is_in = optimal(players[1:], players_left - 1, cap - players[0][1])
    if is_in[0] < 0:
        signable = False
    # compare the values and return larger
    # cannot make a 12-player team with these picks
    if not excludable and not signable:
        dp[num_players][players_left][cap] = (-1, [])
    elif excludable and (not signable or not_in[0] > is_in[0] + players[0][2]):
        dp[num_players][players_left][cap] = not_in
    else:
        dp[num_players][players_left][cap] = (is_in[0] + players[0][2], is_in[1] + [players[0]])
    return dp[num_players][players_left][cap]

def main():
    ROSTER_SIZE = 12
    # players.txt holds the file with all players and their value and salary
    # as well as the salary cap
    filename = 'players.txt'
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    f = open(filename, 'r')
    cap = int(f.readline().strip())
    # build up the players array
    players = []
    for line in f:
        line = line.strip()
        vals = line.split(' ')
        # vals = [place, name, salary, value]
        players.append((' '.join(vals[1:-2]), int(vals[-2]), int(vals[-1])))
    num = len(players)
    # build up the dynamic programming matrix
    for i in range(num + 1):
        dp.append([])
        for j in range(ROSTER_SIZE + 1):
            dp[i].append([])
            for k in range(cap + 1):
                dp[i][j].append(None)
    # base cases initialization
    for j in range(ROSTER_SIZE + 1):
        for k in range(cap + 1):
            dp[0][j][k] = (0, [])
    for i in range(1, ROSTER_SIZE):
        for j in range(i):
            for k in range(cap + 1):
                dp[i][j][k] = (-1, [])
    for i in range(num + 1):
        for k in range(cap + 1):
            dp[i][0][k] = (0, [])
    opt = optimal(players, ROSTER_SIZE, cap)
    for player in opt[1]:
        print(player[0] + " " + "$" + str(player[1]) + ": " + str(player[2]))
    print("Optimal Score: " + str(opt[0]))

if __name__ == "__main__":
    main()
