from dataclasses import asdict
from dataclasses import dataclass
from collections import UserList


@dataclass(frozen=True)
class Station:
    index: str
    stationuuid: str
    name: str
    url: str
    homepage: str
    tags: str

    @classmethod
    def fields(cls):
        return cls.__annotations__.keys()

    def serialize(self):
        return asdict(self)

    def __str__(self):
        return "{:>4} | {:<40.40} | tags: {} \n".format(
            self.index, self.name, self.tags
        )


class StationList(UserList):
    def __init__(self, *stations):
        self.data = []
        if stations:
            for i, s in enumerate(stations, 1):
                kwargs = dict(
                    filter(
                        lambda elem: elem[0] in Station.fields(), s.items()
                    )
                )
                self.data.append(Station(index=i, **kwargs))

    def new(self, *args):
        return self.__init__(*args)

    def __str__(self):
        return "".join(str(s) for s in self.data)


stations = StationList()
