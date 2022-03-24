class NoSlotsAvailable(Exception):
    def __init__(self):
        super().__init__("No slots available")