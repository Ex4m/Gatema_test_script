import re

with open("D327971_fc1.i") as f:
    content = f.read()
    
    
def find_data(content):
    pattern = r"X.*?T0\d+\n"
    matches = re.findall(pattern, content)
    sections = []
    for i in range(len(matches)):
        start_index = content.find(matches[i])
        if i < len(matches)-1:
            end_index = content.find(matches[i+1])
        else:
            end_index = len(content)
        section = content[start_index:end_index]
        sections.append(section.strip())
    return sections    
        
    
    
    
  
    
    
    
sections = find_data(content)    
    
print(sections[0])
#print(repr(content))