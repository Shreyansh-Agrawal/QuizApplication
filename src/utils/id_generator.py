'Generate random id using shortuuid'

import shortuuid


def generate_id(entity: str | None = None, length: int = 5) -> str:
    'Generate a random id of an entity'

    entity_id = shortuuid.ShortUUID().random(length)

    if entity:
        prefix = entity[0].upper()
        entity_id = prefix + entity_id

    return entity_id
