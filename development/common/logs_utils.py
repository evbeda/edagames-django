
from development.constants import (
    ALL_STATES,
    ACTION,
    ALL_ACTIONS,
    STATE,
)


class FilterLogs:

    def __init__(self, data: list) -> None:
        self.logs = data

    @property
    def possible_states(self) -> list:
        possible_states = [log[STATE] for log in self.logs if STATE in log.keys()]
        possible_states.append(ALL_STATES)
        return list(set(possible_states))

    @property
    def possible_actions(self) -> list:
        possible_actions = [log[ACTION] for log in self.logs if ACTION in log.keys()]
        possible_actions.append(ALL_ACTIONS)
        return list(set(possible_actions))
