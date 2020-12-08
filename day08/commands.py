from game import GameConsole


class GameCommand(object):
    def __init__(self, receiver: GameConsole, jump_by: int = 1):
        self.jump_by = jump_by
        self.receiver = receiver

    def execute(self):
        self.receiver.jump(self.jump_by)

    def undo(self):
        self.receiver.jump(-self.jump_by)

    def is_jmp(self):
        return False

    def is_nop(self):
        return False


class NOPCommand(GameCommand):
    def __init__(self, receiver: GameConsole, value: int):
        super().__init__(receiver, jump_by=1)
        self.value = value

    def is_nop(self):
        return True

    def swap(self):
        return JMPCommand(self.receiver, self.value)

    def copy(self, receiver):
        return NOPCommand(receiver, self.value)

    def __repr__(self):
        return f"nop {self.value:+}"


class JMPCommand(GameCommand):
    def __init__(self, receiver: GameConsole, value: int):
        super().__init__(receiver, jump_by=value)

    def is_jmp(self):
        return True

    def swap(self):
        return NOPCommand(self.receiver, self.jump_by)

    def copy(self, receiver):
        return JMPCommand(receiver, self.jump_by)

    def __repr__(self):
        return f"jmp {self.jump_by:+}"


class AddCommand(GameCommand):
    def __init__(self, receiver: GameConsole, value: int):
        super().__init__(receiver, jump_by=1)
        self.amount = value

    def execute(self):
        super().execute()
        self.receiver.add(self.amount)

    def undo(self):
        super().undo()
        self.receiver.add(-self.amount)

    def copy(self, receiver):
        return AddCommand(receiver, self.amount)

    def __repr__(self):
        return f"acc {self.amount:+}"


class SwapProcessCommand(GameCommand):
    def __init__(self, receiver, process_nr, new_process):
        super().__init__(receiver)
        self.process_nr = process_nr
        self.new_process = new_process
        self.old_process = None

    def execute(self):
        self.old_process = self.receiver.processes[self.process_nr]
        self.receiver.processes[self.process_nr] = self.new_process

    def undo(self):
        if self.old_process is not None:
            self.receiver.processes[self.process_nr] = self.old_process


class CreateNewGameCommand(GameCommand):
    def __init__(self, receiver):
        super().__init__(receiver)
        self.new_game = GameConsole()

    def execute(self):
        for process in self.receiver.processes:
            cmd = process.command.copy(self.new_game)
            self.new_game.add_command(cmd)
        return self.new_game


class GameCommandFactory(object):
    COMMANDS = {"nop": NOPCommand, "acc": AddCommand, "jmp": JMPCommand}

    def __new__(cls, command_name):
        command = cls.COMMANDS.get(command_name)
        assert command is not None, f"{command_name!r} command not registered!"
        return command
