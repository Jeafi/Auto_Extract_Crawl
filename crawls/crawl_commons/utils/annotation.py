
def singleton(cls, *args, **kwargs):
    instances = {}
    def wrapper():
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return wrapper