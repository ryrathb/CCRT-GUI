class Batter:
    def __init__(self, ID, firstName, lastName, PIN, height, weight):
        self.ID = ID  # 10 digit integer
        self.firstName = firstName
        self.lastName = lastName
        self.PIN = PIN  # 4 digit integer
        self.height = height  # integer
        self.weight = weight  # float
        self.routines = []  # List of Routine objects, initially empty

    
