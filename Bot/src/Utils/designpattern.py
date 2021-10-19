class Singleton:
    _instance = None

    def __new__(cls):
        if not isinstance(cls._instance, cls):
            cls._instance = super(Singleton, cls).__new__(cls)
        return cls._instance
