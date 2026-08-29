import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # parameterized for portability (was a hardcoded Windows path)

#СПИСОК КЛАСІВ
def find_classes(directory): 
    f = open(directory, "r")
    classes = list(f)
    classes.sort()
    class_to_idx = {classes[i]: i for i in range(len(classes))}
    return classes, class_to_idx


path = os.path.join(BASE_DIR, "list_of_classes.txt")
#path = os.path.join(BASE_DIR, "classes_names.txt")
cl, dict_of_classes = (find_classes(path))