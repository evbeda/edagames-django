
from development.constants import (
    ALL_STATES,
    STATE
)


class FilterLogs:

    def __init__(self, data: list) -> None:
        self.logs = data

    @property
    def possible_states(self) -> list:
        possible_states = [log[STATE] for log in self.logs if STATE in log.keys()]
        possible_states.append(ALL_STATES)
        return list(set(possible_states))
