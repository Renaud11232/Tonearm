class Singleton:

    __instances = {}

    def __new__(cls, *args, **kwargs):
        if cls not in cls.__instances:
            cls.__instances[cls] = super(Singleton, cls).__new__(cls, *args, **kwargs)
        return cls.__instances[cls]