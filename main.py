def list_functions_and_variables_in_file(file_path):
    elements = []
    lambda_count = 0
    inside_function = False
    inside_class = False
    
    with open(file_path, 'r') as f:
        lines = f.readlines()
        for line in lines:
            # Detect functions
            func_match = re.search(r'def (\w+)\(', line)
            if func_match:
                inside_function = True
                elements.append(f"[FUNCTION] {func_match.group(1)}")
                
            # Detect classes
            class_match = re.search(r'class (\w+)', line)
            if class_match:
                inside_class = True
                elements.append(f"[CLASS] {class_match.group(1)}")
                
            # Detect lambda functions
            if 'lambda' in line:
                lambda_count += 1
                elements.append(f"[LAMBDA] lambda_{lambda_count}")
                
            # Detect decorators
            dec_match = re.search(r'@(\w+)', line)
            if dec_match:
                elements.append(f"[DECORATOR] @{dec_match.group(1)}")
                
            # Detect variables
            var_match = re.search(r'(\w+) *=', line)
            if var_match:
                scope = "GLOBAL_VARIABLE" if not (inside_function or inside_class) else "LOCAL_VARIABLE"
                elements.append(f"[{scope}] {var_match.group(1)}")
                
                # Detect primitive data structures
                if '[]' in line:
                    elements.append("[LIST]")
                elif '{}' in line:
                    elements.append("[DICTIONARY]")
                elif '()' in line:
                    elements.append("[TUPLE]")
                elif 'set()' in line:
                    elements.append("[SET]")
                    
    return elements

# Updating the write_tree_to_file function to use the new list_functions_and_variables_in_file function
def write_tree_to_file(directory, file, padding='', joint='├── '):
    file.write(padding + joint + directory.split('/')[-1] + '\n')
    new_padding = padding + ('│   ' if joint == '├── ' else '    ')
    for root, dirs, files in os.walk(directory):
        dirs.sort()
        files.sort()
        all_elements = dirs + files
        
        for i, d in enumerate(dirs):
            next_joint = '└── ' if i == len(all_elements) - 1 else '├── '
            write_tree_to_file(os.path.join(root, d), file, new_padding, next_joint)
            
        for i, f in enumerate(files):
            next_joint = '└── ' if i == len(files) - 1 and not dirs else '├── '
            file.write(new_padding + next_joint + f + '\n')
            if f.endswith('.py'):
                elements = list_functions_and_variables_in_file(os.path.join(root, f))
                element_padding = new_padding + '    '
                for j, element in enumerate(elements):
                    element_joint = '└── ' if j == len(elements) - 1 else '├── '
                    file.write(element_padding + element_joint + element + '\n')
