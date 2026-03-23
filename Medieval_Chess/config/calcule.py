# retorne a direção do objeto em relação ao a referencia
def direction(ref, obj) -> int:
    diff = obj - ref
    if diff == 0: return 0
    else: return 1 if diff > 0 else -1
    
def value_exist(data, group, key, value):
    return any(
        d.get(key) == value
        for d in data.get(group, [])
    )