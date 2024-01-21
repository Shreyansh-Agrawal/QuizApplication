'Generate random id using shortuuid'

import shortuuid


def generate_id(entity: str) -> str:
    'Generate a random id of an entity'

    prefix = entity[0].upper()
    entity_id = prefix + shortuuid.ShortUUID().random(length=5)
    return entity_id
