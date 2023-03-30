import re
import argparse
from decimal import Decimal


def section_separator(content):
    """Separate the content into sections based on the T-codes in the input text.

    Args:
        content (str): The content of the drill file.

    Returns:
        A list of sections of the input content, separated based on the T-codes.
    """
    blocks =re.findall(r"X.*?T0\d+\n", content)
    section = [re.search(blocks[0], content).start()]
    for i in range(1, len(blocks)):
        match = re.search(blocks[i], content)
        section.append(match.start())
    section.append(len(content))
    # split content into sections using the starting positions in the section list
    sections = [content[section[i]:section[i+1]] for i in range(len(section)-1)]
    return sections




def sorted_dictionary(sections):
    """Sorts a dictionary based on the keys that match the pattern T0\d+.

    Args:
        sections (list): A list of sections to be sorted.

    Returns:
        dict: A dictionary containing the sorted sections. The keys of the dictionary are the matched strings
        using the pattern T0\d+ and the values are the corresponding sections.
    """
    pattern = r"T0\d+"
    result_dict = {}
    for section in sections:
        match = re.search(pattern, section)
        if match:
            # Get the matched string using group() ... group returning exact matched value
            matched_string = match.group()
            result_dict[matched_string] = section.strip()

    # Sort the dictionary by keys and create a new dictionary with the sorted items
    #sorted_dict = sorted(result_dict)
    # dict comprehension
    sorted_dict = {key: result_dict[key] for key in sorted(result_dict)}
    return sorted_dict


def driller_adjuster(sorted_dict):
    """Modify the coordinates of the given sections in a sorted dictionary.

    Args:
        sorted_dict: A (un)sorted dictionary of sections with their corresponding codes.

    Returns:
        A modified sorted dictionary where the Y-coordinate of lines with X-coordinate > 50 has been increased by 10 units.
    """
    for key, value in sorted_dict.items():
        lines = value.split("\n")
        new_lines = []
        for line in lines:
            match = re.search(r"X(-?\d+\.\d+)Y(-?\d+\.\d+)(T0\d+)?$", line)
            if match:
                x = Decimal(match.group(1))
                y = Decimal(match.group(2))
                t_code = match.group(3)
                if x > 50:
                    y += Decimal('10')
                    # Have to separate T0"x" values from standard rows
                    if t_code:
                        line = "X{}Y{}{}".format(x, y, t_code)
                    else:
                        line = "X{}Y{}".format(x, y)
            new_lines.append(line)
        sorted_dict[key] = "\n".join(new_lines)
    return sorted_dict


def min_max(content):
    """Extracts the minimum and maximum X and Y coordinates from a string.

    Args:
        content (str): A string containing lines of text with X and Y coordinates.

    Returns:
        tuple: A tuple containing four values: the maximum X coordinate, the minimum X coordinate, the maximum Y coordinate, and the minimum Y coordinate.
    """
    lines = content.split("\n")
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
    """Parse command line arguments, read content from a file, and execute one of two functions based on user input.
    
    The chosen function is specified using the ("-funkce1" or "-funkce2") option followed by the function name .
    
    For "-funkce1", the content is separated into sections and sorted. Then the driller adjuster is applied to the sorted sections
    and the final CNC code is written to a file named cnc.txt. The adjusted values of the driller are also printed to the console.
    
    For "-funkce2", the minimum and maximum values of X and Y coordinates are calculated and printed to the console.
    
    Raises:
        argparse.ArgumentError: If no function is specified using the ("-funkce1" or "-funkce2") option.
    
    Returns:
        None.
    """
    try:
        parser = argparse.ArgumentParser(description="Process D327971_fc1.i file")
        parser.add_argument("-funkce1", action="store_true", help="Run funkce1")
        parser.add_argument("-funkce2", action="store_true", help="Run funkce2")
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

        if args.funkce1:
            sections = section_separator(content)
            sorted_dict = sorted_dictionary(sections)
            sorted_dict = driller_adjuster(sorted_dict)
            for value in sorted_dict.values():
                header += "\n" + value + ""
            header_value = header
            final_print = header_value + footer
            print(final_print)
            with open("cnc.txt", "w") as file:
                file.write(final_print)
            print("\n\nAdjusted values of the driller were exported as cnc.txt")

        elif args.funkce2:
            x_max, x_min, y_max, y_min = min_max(content)
            print(f"Min_X = <{x_min}>\nMax_X = <{x_max}>\nMin_Y = <{y_min}>\nMax_Y = <{y_max}>\n")

        else:
            print("I'm sorry, but this input is not in my list of functions, please try again")
    
    except FileNotFoundError:
        print("The specified file was not found.")
    except Exception as e:
        print("An error occurred while opening the file: ", e)
        
if __name__ == "__main__":
    main()



