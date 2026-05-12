class UserState:
    def __init__(self):
        self.state = None
        self.data = {}

    def set_state(self, state):
        self.state = state

    def clear(self):
        self.state = None
        self.data = {}
