from collections import UserList
from dataclasses import asdict
from dataclasses import dataclass


@dataclass(frozen=True)
class Station:
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
        return "| {:<40.40} | tags: {} \n".format(
            self.name, self.tags
        )


@dataclass(frozen=True)
class Tag:
    name: str
    stationcount: str

    @classmethod
    def fields(cls):
        return cls.__annotations__.keys()

    def serialize(self):
        return asdict(self)

    def __str__(self):
        return "{:>4} | {:<40}\n".format(
            self.stationcount, self.name
        )


class TagList(UserList):
    def __init__(self, *tags):
        self.data = []
        if tags:
            for t in tags:
                kwargs = dict(
                    filter(
                        lambda elem: elem[0] in Tag.fields(), t.items()
                    )
                )
                self.data.append(Tag(**kwargs))
        self.sort(key=lambda t: t.stationcount, reverse=True)

    def new(self, *args):
        return self.__init__(*args)

    def __str__(self):
        return "".join(str(t) for t in self.data).strip()


class StationList(UserList):
    def __init__(self, *stations):
        self.data = []
        if stations:
            for s in stations:
                kwargs = dict(
                    filter(
                        lambda elem: elem[0] in Station.fields(), s.items()
                    )
                )
                self.data.append(Station(**kwargs))

    def new(self, *args):
        return self.__init__(*args)

    def __str__(self):
        return "".join(str(s) for s in self.data).strip()


tags = TagList()
stations = StationList()
