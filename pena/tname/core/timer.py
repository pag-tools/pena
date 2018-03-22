
class Timer:

    delta = 0

    def __init__(self):
        pass
    
    @staticmethod
    def update_delta(seconds):
        minutes = seconds/60.0
        Timer.delta += minutes
    
    @staticmethod
    def get_delta():
        return Timer.delta
