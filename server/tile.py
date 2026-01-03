from enum import Enum

class TileType(Enum):
    GO = "GO"
    PROPERTY = "PROPERTY"
    CARD = "CARD"
    TAX = "TAX"
    JAIL = "JAIL"

class Tile:
    ID=0
    def __init__(self, data, type):
        Tile.ID = Tile.ID + 1
        self.tile_id = Tile.ID
        self.tile_type= type
        self.next_tile = None
        self.data = data
