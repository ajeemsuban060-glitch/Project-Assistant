from enum import Enum, auto

class State(Enum):
    IDLE = auto()
    LISTENING = auto()
    TRANSCRIBING = auto()
    THINKING = auto()
    SPEAKING = auto()

class StateMachine:
    def __init__(self):
        self._state = State.IDLE

    @property
    def state(self):
        return self._state

    def transition(self, new_state: State):
        print(f"[State] {self._state.name} -> {new_state.name}")
        self._state = new_state

    def can_listen(self):
        return self._state == State.IDLE

    def can_transcribe(self):
        return self._state == State.LISTENING

    def can_think(self):
        return self._state == State.TRANSCRIBING

    def can_speak(self):
        return self._state == State.THINKING