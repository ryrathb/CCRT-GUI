class Set:
    def __init__(self, name, setID, repPauseTime, routine, leftBound, rightBound, isSitting):
        self.name = name
        self.setID = setID  # 10 digit integer
        self.repPauseTime = repPauseTime  # integer
        self.routine = routine  # Routine object
        self.reps = []  # List of Rep objects, initially empty
        self.leftBound = leftBound  # integer between 0-16
        self.rightBound = rightBound  # integer between 0-16
        self.isSitting = isSitting  # bool