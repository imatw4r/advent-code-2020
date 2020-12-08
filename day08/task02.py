import os
from commands import CreateNewGameCommand, SwapProcessCommand, GameCommandFactory
from game import GameProcess, GameConsole, InfiteLoopException

BASE_DIR = os.path.dirname(__file__)


def create_game_console(data):
    console = GameConsole()

    def create_command(line):
        cmd, value = line.split(" ")
        return GameCommandFactory(command_name=cmd)(receiver=console, value=int(value))

    commands = map(create_command, data)
    console.add_commands(commands)
    return console


def find_jmp_or_nop_process(console, start_at):
    processes = console.processes[start_at:]
    for idx, process in enumerate(processes):
        cmd = process.command
        if cmd.is_jmp() or cmd.is_nop():
            return start_at + idx, cmd
    return None, None


def fixme(data):
    original_console = create_game_console(data)
    console = original_console
    fixed = False
    process_nr = 0
    while not fixed:
        try:
            console.run()
        except InfiteLoopException:
            # console.show_instructions()
            process_nr, cmd_to_swap = find_jmp_or_nop_process(
                original_console, start_at=process_nr
            )
            if not cmd_to_swap:
                raise ValueError("Program can't be fixed!")

            # We create a new version of game with the same steps as the original one
            new_console = CreateNewGameCommand(original_console).execute()

            # We create a Process with reversed command (jmp -> nop, nop -> jmp)
            new_process = GameProcess(was_executed=False, command=cmd_to_swap.swap())

            # We swap process in our new game
            SwapProcessCommand(new_console, process_nr, new_process).execute()

            console = new_console
            process_nr += 1
        else:
            fixed = True
    return console


with open(os.path.join(BASE_DIR, "data.in"), "r") as f:
    data = list(map(str.strip, f))
    fixme(data)
