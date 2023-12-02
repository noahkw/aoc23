class CubeSet:
    red: int = 0
    blue: int = 0
    green: int = 0

    def __init__(self, red=0, green=0, blue=0):
        self.red = red
        self.green = green
        self.blue = blue

    def __str__(self):
        return f'{self.red} red, {self.green} green, {self.blue} blue'

    @staticmethod
    def parse(in_: str) -> 'CubeSet':
        """
        format: x [blue/red/green], y [blue/red/green], z [blue/red/green], ...
        """
        cube_set = CubeSet()

        cube_tokens = in_.split(',')
        for cube_token in cube_tokens:
            amount, color = cube_token.strip().split(' ')
            amount = int(amount)

            if color == 'red':
                cube_set.red = amount
            elif color == 'green':
                cube_set.green = amount
            elif color == 'blue':
                cube_set.blue = amount
            else:
                raise ValueError(f'unknown color {color}')

        return cube_set


class GameConfig:
    bag_load: CubeSet
    id: int
    runs: list[CubeSet]

    def __str__(self):
        return f'Game {self.id}: {"; ".join([str(run) for run in self.runs])}'

    def __init__(self, bag_load, runs):
        self.bag_load = bag_load
        self.runs = runs

    def is_valid(self) -> bool:
        for run in self.runs:
            if run.red > self.bag_load.red \
                    or run.green > self.bag_load.green \
                    or run.blue > self.bag_load.blue:
                return False

        return True

    @staticmethod
    def parse(bag_load: CubeSet, in_: str) -> 'GameConfig':
        """
        format: Game A: X [blue/red/green], Y [blue/red/green], [...]; W [blue/red/green], V [blue/red/green]; [...]
        """
        game_config = GameConfig(bag_load, [])

        tokens = in_.split(':')
        game_config.id = int(tokens[0].split(' ')[1])

        game_config.runs = [CubeSet.parse(run) for run in tokens[1].split(';')]

        return game_config


def main():
    with open('input.txt') as f:
        lines = f.readlines()

    cube_set = CubeSet(red=12, green=13, blue=14)

    possible_games_id_sum = 0

    for line in lines:
        game = GameConfig.parse(cube_set, line.strip())

        if game.is_valid():
            possible_games_id_sum += game.id

    print(f'Sum IDs of valid games: {possible_games_id_sum}')


if __name__ == '__main__':
    main()
