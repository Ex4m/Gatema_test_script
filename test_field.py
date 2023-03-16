import re

with open("D327971_fc1.i") as f:
    full = f.read()
    
    
print(repr(full))




#LEGACY While loop to test the inputs within the code
"""print("Hello, fellow observer")
while True:
    inp = input("What function you would like to call? ")
    if inp == "funkce1":#"python script.py -funkce1":
        sections=section_separator(content)
        sorted_dict = sorted_dictionary(sections)
        sorted_dict = driller_adjuster(sorted_dict)
        for value in sorted_dict.values():
            header += "\n" + value + ""
        header_value = header
        final_print = header_value + footer
        with open("cnc.txt", "w") as file:
            file.write(final_print)          
        print("\n\nAdjusted values of the driller was exported as cnc.txt")
    elif inp == "funkce2":#"python script.py -funkce2":
        x_max, x_min, y_max, y_min = min_max(content)
        print(f"Min_X = <{x_min}>\nMax_X = <{x_max}>\nMin_Y = <{y_min}>\nMax_Y = <{y_max}>\n")
    else:
        print("I´am sorry, but this input is not in my list of functions, please try again")
        sections=section_separator(content)
        sorted_dict = sorted_dictionary(sections)
        print(sorted_dict)"""