class Routine:
    def __init__(self, routineID, name, batter, isStatic, setPauseTime):
        self.routineID = routineID  # 10 digit integer
        self.name = name
        self.batter = batter  # Batter object
        self.isStatic = isStatic  # bool
        self.sets = []  # List of Set objects, initially empty
        self.setPauseTime = setPauseTime  # integer
