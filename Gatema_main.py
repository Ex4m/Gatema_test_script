import re
import argparse








def driller_adjuster(sorted_dict):
    for key, value in sorted_dict.items():
        lines = value.split('\n')
        new_lines = []
        for line in lines:
            match = re.search(r"X(-?\d+\.\d+)Y(-?\d+\.\d+)(T0\d+)?$", line)
            if match:
                x = float(match.group(1))
                y = float(match.group(2))
                t_code = match.group(3)
                if x > 50:
                    y += 10
                    if t_code:
                        line = "X{}Y{}{}".format(x, y, t_code)
                    else:
                        line = "X{}Y{}".format(x, y)
            new_lines.append(line)
        sorted_dict[key] = "\n".join(new_lines)
    return sorted_dict




def section_separator(content):
    blocks =re.findall(r"X.*?T0\d+\n", content)
    # initialize section list with starting position of first match
    section = [re.search(blocks[0], content).start()]
    # loop over remaining matches and add their starting positions to section list
    for i in range(1, len(blocks)):
        match = re.search(blocks[i], content)
        section.append(match.start())
    # add the end of the content string as the final section boundary
    section.append(len(content))
    # split content into sections using the starting positions in the section list
    sections = [content[section[i]:section[i+1]] for i in range(len(section)-1)]
    return sections




def sorted_dictionary(sections):
    pattern = r"T0\d+"
    result_dict = {}
    # Iterate over the list of sections and search for the T0 code
    for section in sections:
        match = re.search(pattern, section)
        if match:
            # Get the matched string using group() ... group returning exact matched value
            matched_string = match.group()
            # Add the matched string as a key to the dictionary, with the corresponding section as the value
            result_dict[matched_string] = section.strip()

    # Sort the dictionary by keys and create a new dictionary with the sorted items
    sorted_dict = {key: result_dict[key] for key in sorted(result_dict)}
    return sorted_dict


def min_max(content):
    lines = content.split('\n')
    x_coords = []
    y_coords = []
    for line in lines:
        match = re.search(r"X(-?\d+\.\d+)Y(-?\d+\.\d+)", line)
        if match:
            x_coords.append(float(match.group(1)))
            y_coords.append(float(match.group(2)))
    x_max = max(x_coords)
    x_min = min(x_coords)
    y_max = max(y_coords)
    y_min = min(y_coords)
    return x_max, x_min, y_max, y_min



def main():
    parser = argparse.ArgumentParser(description='Process D327971_fc1.i file')
    parser.add_argument('-f', '--function', required=True, help='Select function to run (funkce1 or funkce2)')
    args = parser.parse_args()

    with open("D327971_fc1.i") as f:
        full = f.read()

    # Create the pure content of the drill
    start_str = r"(M\d+, Zacatek bloku vrtani)"
    end_str = r"\n+\$\n+\(M\d{1,2}, Konec bloku vrtani\)"
    start_index = re.search(start_str, full)
    end_index = re.search(end_str, full)
    content = full[start_index.end():end_index.start()]
    header = full[0:start_index.end()+2]
    footer = full[end_index.start():]

    if args.function == 'funkce1':
        sections = section_separator(content)
        sorted_dict = sorted_dictionary(sections)
        sorted_dict = driller_adjuster(sorted_dict)
        for value in sorted_dict.values():
            header += "\n" + value + ""
        header_value = header
        final_print = header_value + footer
        with open("cnc.txt", "w") as file:
            file.write(final_print)
        print("\n\nAdjusted values of the driller were exported as cnc.txt")

    elif args.function == 'funkce2':
        x_max, x_min, y_max, y_min = min_max(content)
        print(f"Min_X = <{x_min}>\nMax_X = <{x_max}>\nMin_Y = <{y_min}>\nMax_Y = <{y_max}>\n")

    else:
        print("I'm sorry, but this input is not in my list of functions, please try again")

if __name__ == '__main__':
    main()










































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
    
    
        