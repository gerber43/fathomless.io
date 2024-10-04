import json


def delete_blank_object(game_map):
    for x, row in enumerate(game_map):
        for y, tile in enumerate(row):
            keys_to_delete = set()
            for key, value in tile.items():
                if isinstance(value, dict) and value.get('textureIndex') == 8:
                    keys_to_delete.add(key)
            for key in keys_to_delete:
                del tile[key]
    return game_map

