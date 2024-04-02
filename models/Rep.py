class Rep:
    def __init__(self, name, repID, repNum, setObj, armDirection, startPos, endPos, opTorque, avgTorque, peakTorque, timeToStop, initTorqueTime):
        self.name = name
        self.repID = repID  # 10 digit integer
        self.repNum = repNum
        self.set = setObj  # Set object
        self.armDirection = armDirection  # bool
        self.startPos = startPos  # integer between 0-16
        self.endPos = endPos  # integer between 0-16
        self.opTorque = opTorque
        self.avgTorque = avgTorque  # float
        self.peakTorque = peakTorque  # float
        self.timeToStop = timeToStop  # float
        self.initTorqueTime = initTorqueTime  # float

