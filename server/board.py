from .tile import TileType
from .tile import Tile
from ..DS.circularLinkedList import CircularLinkedList
class Board:
    def __init__(self):
        self.tiles = CircularLinkedList()
        self.createTiles()


    def createTiles(self):
        tile_list = [
            TileType.GO,
            TileType.PROPERTY,
            TileType.CARD,
            TileType.PROPERTY,
            TileType.TAX,
            TileType.PROPERTY,
            TileType.CARD,
            TileType.PROPERTY,
            TileType.JAIL,
            TileType.PROPERTY,
        ]

        while len(tile_list) < 40:
            tile_list.extend(tile_list)

        tile_list = tile_list[:40]

        for t in tile_list:
            data = self.create_tile_data(t)
            tile = Tile(data=data, type=t)
            self.tiles.Add(tile)





    def create_tile_data(self,type):
        if type == TileType.GO:
            return None
        elif type == TileType.PROPERTY:
            return {"price": 100, "owner": None}
        elif type == TileType.CARD:
            return "CARD"
        elif type == TileType.TAX:
            return 200
        elif type == TileType.JAIL:
            return None
