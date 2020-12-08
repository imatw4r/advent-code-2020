from dataclasses import dataclass
from itertools import islice
import time


@dataclass
class GameProcess:
    was_executed: bool
    command: None


class InfiteLoopException(Exception):
    pass


class GameConsole(object):
    def __init__(self):
        self.counter = 0
        self.processes = []
        self.current_process = 0

    def jump(self, jump):
        self.current_process += jump

    def add(self, value):
        self.counter += value

    def add_command(self, command):
        self.processes.append(GameProcess(was_executed=False, command=command))

    def add_commands(self, commands):
        for cmd in commands:
            self.add_command(cmd)

    def run(self):
        while self.current_process < len(self.processes):
            process = self.processes[self.current_process]
            if process.was_executed:
                raise InfiteLoopException()

            process.command.execute()
            process.was_executed = True

    def undo(self):
        process = self.processes.pop(-1)
        if process.was_executed:
            process.command.undo()
            return process.command

    def show_instructions(self):
        for process in self.processes:
            print(process.command)
