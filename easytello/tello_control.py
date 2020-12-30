import numpy as np

class ControlCommand:
    def __init__(self, command_func = lambda : print('command?'), vec3 = np.array([0,0,0])):
        self.command_func = command_func
        self.vec3 = vec3

class TelloControl:
    def __init__(self):
        self.send_state = 0
        self.commands = list()
        self.vec3 = np.array([0, 0, 0])
    
    def on_success(self):
        if self.send_state >= len(self.commands):
            return
        c = self.commands[self.send_state]
        self.vec3 += c.vec3

        print(self.vec3)

        self.send_state += 1
        if self.send_state >= len(self.commands):
            return
        self.commands[self.send_state].command_func()
        
    def on_missing(self):
        self.send_state += 1

    def append(self, command: ControlCommand):
        self.commands.append(command)

    def start(self):
        self.send_state = 0
        self.commands[self.send_state].command_func()

    def get_position(self):
        return self.vec3
