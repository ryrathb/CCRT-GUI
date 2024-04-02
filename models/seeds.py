from .Rep import Rep
from .Batter import Batter 
from .Set import Set
from .Routine import Routine

# A function to create Reps for a given Set and Routine
def create_reps_for_set_routine(set_num, routine_num):
    base_id = int(f"{set_num}{routine_num}0000000")
    reps = [
        Rep(f"Rep 1", base_id + 1, 1, None, "CCW", 0, 16, 10, 5.5, 8.2, 2.3, 1.1),
        Rep(f"Rep 2", base_id + 2, 2, None, "CW", 16, 0, 10, 6.0, 9.0, 2.5, 1.2)
    ]
    return reps

# A function to create Sets for a given Routine
def create_sets_for_routine(routine_num):
    sets = []
    for set_num in range(1, 3):  # Two sets per routine
        base_id = int(f"{routine_num}0{set_num}000000")
        reps = create_reps_for_set_routine(set_num, routine_num)
        set_obj = Set(f"Set {set_num}", base_id, 30 + set_num * 5, None, 0, 16, set_num % 2 == 0)
        set_obj.reps = reps
        sets.append(set_obj)
    return sets

# A function to initialize a Batter with Routines, Sets, and Reps
def create_batter(name, pin):
    first_name, last_name = name.split()
    batter = Batter(pin, first_name, last_name, pin, 180, 75.5)
    batter.routines = []
    
    for routine_num in range(1, 3):  # Two routines per batter
        base_id = pin + routine_num * 100000
        sets = create_sets_for_routine(routine_num)
        routine = Routine(base_id, f"Routine {routine_num}", None, routine_num % 2 == 0, 60 + routine_num * 5)
        routine.sets = sets
        for set_obj in sets:
            set_obj.routine = routine  # Associate each set with its routine
        batter.routines.append(routine)
    
    return batter

# Names and PINs for batters
batters_info = [
    ("John Doe", 1234),
    ("Jane Doe", 2234),
    ("Alex Smith", 3234),
    ("Chris Johnson", 4234),
    ("Pat Lee", 5234)
]

batters = []
batterpins = []

# Create batters with associated routines, sets, and reps
for name, pin in batters_info:
    new_batter = create_batter(name, pin)
    batters.append(new_batter)
    batterpins.append(new_batter.PIN)

# Now you have a Batter with a complete data structure down to Reps
