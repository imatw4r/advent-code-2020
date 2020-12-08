import os
from game import GameConsole, InfiteLoopException
from commands import (
    JMPCommand,
    NOPCommand,
    AddCommand,
    CreateNewGameCommand,
    GameCommandFactory,
)

BASE_DIR = os.path.dirname(__file__)


def create_game_console(data):
    console = GameConsole()

    def create_command(line):
        cmd, value = line.split(" ")
        return GameCommandFactory(command_name=cmd)(receiver=console, value=int(value))

    commands = map(create_command, data)
    console.add_commands(commands)
    return console


with open(os.path.join(BASE_DIR, "data.in"), "r") as f:
    data = list(map(str.strip, f))
    console = create_game_console(data)
    try:
        console.run()
    except InfiteLoopException as e:
        print("Task 1 result:", console.counter)
