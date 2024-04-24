from .Rep import Rep
from .Batter import Batter 
from .Set import Set
from .Routine import Routine
import os



def parse_batter_files(file_path):
    content = ""
    with open(file_path, "r") as file:
        content = file.readline()
    
    content_list = content.split(',')
    return Batter(ID=content_list[0], firstName=content_list[1], lastName=content_list[2], PIN=content_list[3], height=content_list[4], weight=content_list[5])

    

def create_batters():
    new_path = "./userData/"
    os.chdir(new_path)
    data_objects = []

    for root, dirs, files in os.walk('.'):
        directory_name = os.path.basename(root)
        expected_file_name = directory_name + '.txt'
        for file_name in files:
            if file_name == expected_file_name:
                full_path = os.path.join(root, file_name)
                batter_object = parse_batter_files(full_path)
                data_objects.append(batter_object)


    return data_objects



batters = create_batters()
batterpins = [batter.PIN for batter in batters]

# Create batters with associated routines, sets, and reps


def add_batter(batter):
    path = f"./userData/{str(batter.firstName).lower() + str(batter.lastName).lower()}/"
    if os.path.exists(path) == False:
        try:
            os.mkdir(path)
            print(f"Directory {path} created")
        except FileExistsError:
            print(f"Directory {path} already exists")   

    batters.append(batter)

    text_file_path = f"./userData/{str(batter.firstName).lower() + str(batter.lastName).lower()}/{str(batter.firstName).lower() + str(batter.lastName).lower()}.txt"
    with open(text_file_path, "w") as file:
        file.write(f"{batter.ID},{batter.firstName},{batter.lastName},{batter.PIN},{batter.height},{batter.weight}")

    print("Batter file has been created and written")


    
    


# Now you have a Batter with a complete data structure down to Reps
