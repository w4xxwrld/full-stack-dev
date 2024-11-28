from utils.helpers import greet
from utils.utils import brush_teeth, cook_breakfast, do_laundry, dress_up, go_to_university

name = "Shakh"

def start_day():
    routine = [
        brush_teeth(name),
        cook_breakfast(name),
        do_laundry(name),
        dress_up(name),
        go_to_university(name)
    ]
    print(routine)
    

if __name__ == "__main__":
    message = greet(name)
    print(message)
    start_day()