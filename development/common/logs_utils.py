
from development.constants import STATE


class FilterLogs:

    def __init__(self, data: list) -> None:
        self.logs = data

    @property
    def possible_states(self) -> list:
        possible_states = []
        for log in self.logs:
            if STATE in log.keys():
                possible_states.append(log[STATE])
        possible_states.append('todos')
        return list(set(possible_states))
