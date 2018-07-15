from typing import Dict, List, Optional, Tuple


class Player:
    __slots__ = ["name", "value", "salary"]

    def __init__(self, name: str, value: int, salary: int) -> None:
        self.name = name
        self.value = value
        self.salary = salary


class Result:
    __slot__ = ["value", "players"]

    def __init__(self, value: int, players: List[Player]) -> None:
        self.value = value
        self.players = players


DP = List[List[List[Optional[Result]]]]


class Optimizer:
    def __init__(
        self, filename: Optional[str] = None, tournament: Optional[str] = None
    ) -> None:
        if not filename and not tournament:
            raise ValueError("You must specify a tournament name or a filename!")
        # TODO: Remove this once this feature is supported
        if tournament:
            raise ValueError("Tournaments by name are not supported yet")
        self.filename = filename
        self.tournament = tournament
        self.players: List[Player] = []

    def scrape(self) -> None:
        # Scrape the data for the tournament
        if self.filename:
            self._scrape_file()
        else:
            self._scrape_tournament()

    def _scrape_file(self) -> None:
        if not self.filename:
            raise ValueError("No filename provided!")
        with open(self.filename, "r") as f:
            vals: List[str] = f.readline().strip().split(" ")
            self.roster_size: int = int(vals[0])
            self.cap: int = int(vals[1])
            # build up the players array
            self.players = []
            for line in f:
                line = line.strip()
                vals = line.split(" ")
                # vals = [place, name, salary, value]
                self.players.append(
                    Player(" ".join(vals[1:-2]), int(vals[-2]), int(vals[-1]))
                )

    def _scrape_tournament(self):
        # TODO: Scrape smash.gg for the results of the tournament
        # https://help.smash.gg/faq/misc/api-access
        raise NotImplementedError(
            "Scraping tournaments from smash.gg is not supported yet"
        )

    def optimize(self) -> Result:
        self.scrape()
        dp: DP = []
        num = len(self.players)
        # build up the dynamic programming matrix
        # dp[players left to choose from][roster spots left][cap room left]
        for i in range(num + 1):
            dp.append([])
            for j in range(self.roster_size + 1):
                dp[i].append([])
                for k in range(self.cap + 1):
                    dp[i][j].append(None)
        # base cases initialization
        # No spots on roster -> 0 score and empty roster
        for i in range(num + 1):
            for k in range(self.cap + 1):
                dp[i][0][k] = Result(0, [])
        # Fewer players left to choose from than roster spot -> invalid
        for i in range(self.roster_size):
            for j in range(i + 1, self.roster_size + 1):
                for k in range(self.cap + 1):
                    dp[i][j][k] = Result(-1, [])
        result: Optional[Result] = self._optimize(
            self.players, self.roster_size, self.cap, dp
        )
        return result or Result(-1, [])

    def _optimize(
        self, players: List[Player], players_left: int, cap: int, dp: DP
    ) -> Optional[Result]:
        """
        Optimizes the fantasy lineup for the results of the tournament
        """
        num_players = len(players)
        # base cases
        # not enough players left to fill out the roster
        # or no more players left to look at
        # or no more room on the roster
        # or we have already solved this case
        this_value = dp[num_players][players_left][cap]
        if this_value is not None:
            return this_value
        # either the first player in the player array is in the optimal
        # solution or isn't
        # if we don't sign this player, will there be enough players left to
        # fill the roster
        excludable: bool = num_players > players_left
        not_in: Optional[Result] = None
        if excludable:
            not_in = self._optimize(players[1:], players_left, cap, dp)
        not_in = not_in or Result(-1, [])
        # Was there actually a solution without this player (or is the cap too small
        # for the remaining players)
        if not_in.value < 0:
            excludable = False
        # is there enough salary cap for this player
        signable = cap - players[0].salary >= 0
        is_in: Optional[Result] = None
        if signable:
            is_in = self._optimize(
                players[1:], players_left - 1, cap - players[0].salary, dp
            )
        is_in = is_in or Result(-1, [])
        # Signing this player made the solution impossible
        if is_in.value < 0:
            signable = False
        # compare the values and return larger
        # cannot make a 12-player team with these picks
        if not excludable and not signable:
            dp[num_players][players_left][cap] = Result(-1, [])
        elif excludable and (
            not signable or not_in.value > is_in.value + players[0].value
        ):
            dp[num_players][players_left][cap] = not_in
        else:
            dp[num_players][players_left][cap] = Result(
                is_in.value + players[0].value, is_in.players + [players[0]]
            )
        return dp[num_players][players_left][cap]


__all__ = ["Optimizer", "Player", "Result"]
