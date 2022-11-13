class Device:
    def __init__(self, eui64:str):
        self.eui64 = eui64

    def read(self):
        pass

    def write(self):
        pass

    def activate(self, owner: int, location: str, dev_type: int):
        pass

    def is_activated(self):
        pass

    def get_owner(self):
        pass

    def get_group(self):
        pass

    def get_info(self):
        pass