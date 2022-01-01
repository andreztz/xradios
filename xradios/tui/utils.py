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


@dataclass(frozen=True)
class Tag:
    index: str
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
            for i, t in enumerate(tags, 1):
                kwargs = dict(
                    filter(
                        lambda elem: elem[0] in Tag.fields(), t.items()
                    )
                )
                self.data.append(Tag(index=i, **kwargs))
        self.sort(key=lambda t: t.stationcount, reverse=True)

    def new(self, *args):
        return self.__init__(*args)

    def __str__(self):
        return "".join(str(t) for t in self.data)


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


tags = TagList()
stations = StationList()
