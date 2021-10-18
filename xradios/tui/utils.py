from dataclasses import asdict
from dataclasses import dataclass
from dataclasses import field
from collections import UserList


@dataclass(frozen=True)
class Station:
    index: str
    stationuuid: str
    name: str
    url: str
    homepage: str
    tags: str


    def serialize(self):
        return asdict(self)

    def __str__(self):
        return "{:>4} | {:<30} | tags: {} \n".format(
            self.index, self.name[0:30], self.tags
        )


class StationList:
    def __init__(self, *args):
        self.new(*args)

    def new(self, *args):
        if not args:
            return

        self._list = []
        for index, obj in enumerate(args, 1):
            o = Station(
                index=index,
                stationuuid=obj["stationuuid"],
                name=obj["name"],
                url=obj["url"],
                homepage=obj["homepage"],
                tags=obj["tags"],
            )
            self._list.append(o)

    def __getitem__(self, index):
        return self._list[index]

    def __len__(self):
        return len(self._list)

    def __repr__(self):
        return "<StationList()>"

    def __str__(self):
        return "".join(str(s) for s in self)


stations = StationList()
