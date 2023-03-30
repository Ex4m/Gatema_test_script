import re

with open("D327971_fc1.i") as f:
    full = f.read()
    
    


start_str = r"(M\d+, Zacatek bloku vrtani)"
end_str = r"\n+\$\n+\(M\d{1,2}, Konec bloku vrtani\)"
start_index = re.search(start_str, full)
end_index = re.search(end_str, full)
content = full[start_index.end():end_index.start()]
header = full[0:start_index.end()+2]
footer = full[end_index.start():]

def section_separator(content):
    """Separate the content into sections based on the T-codes in the input text.

    Args:
        content (str): The content of the drill file.

    Returns:
        A list of sections of the input content, separated based on the T-codes.
    """
    blocks =re.findall(r"X.*?T0\d+\n", content)
    section = [re.search(blocks[5], content).start()]
    for i in range(1, len(blocks)):
        match = re.search(blocks[i], content)
        section.append(match.start())
    section.append(len(content))
    # split content into sections using the starting positions in the section list
    sections = [content[section[i]:section[i+1]] for i in range(len(section)-1)]
    return sections
sections = section_separator(content)

pattern = r"T0\d+"
result_dict = {}
for section in sections:
    match = re.search(pattern, section)
    if match:
        # Get the matched string using group() ... group returning exact matched value
        matched_string = match.group()
        result_dict[matched_string] = section.strip()
        
        print(matched_string)    
        
print(sorted(result_dict))    
print(result_dict["T03"])

blocks =re.findall(r"X.*?T0\d+\n", content)
section = [re.search(blocks[0], content).start()]
print(section)   
print(blocks)     
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