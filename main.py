import argparse
import os
import re
from datetime import datetime

def parse_arguments():
    parser = argparse.ArgumentParser(description='Generate directory tree with details of Python files.',
                                     add_help=False)
    parser.add_argument('--all', action='store_true', help='Include all details (functions, classes, variables, data structures).')
    parser.add_argument('--imports', action='store_true', help='Include imports only.')
    parser.add_argument('--functions', action='store_true', help='Include functions only.')
    parser.add_argument('--classes', action='store_true', help='Include classes only.')
    parser.add_argument('--variables', action='store_true', help='Include variables only.')
    parser.add_argument('--decorators', action='store_true', help='Include decorators only.')
    parser.add_argument('--files-only', action='store_true', help='Include files only, no additional details.')
    parser.add_argument('--help', action='help', default=argparse.SUPPRESS, help='Show this help message and exit.')
    args = parser.parse_args()
    
    # If no arguments are given, print the help message and exit
    if not any(vars(args).values()):
        parser.print_help()
        parser.exit()
    
    return args



def list_functions_and_variables_in_file(file_path, args):
    elements = []
    lambda_count = 0
    inside_function = False
    inside_class = False
    
    with open(file_path, 'r') as f:
        lines = f.readlines()
        for line in lines:

            # Detect import statements
            import_match = re.match(r'^import (\w+)', line)
            from_import_match = re.match(r'^from (\w+) import (\w+|\*)', line)
            if import_match and (args.all or args.imports):
                elements.append(f"[IMPORT] {import_match.group(1)}")
            elif from_import_match:
                elements.append(f"[FROM_IMPORT] {from_import_match.group(1)}.{from_import_match.group(2)}")

            # Detect functions
            func_match = re.search(r'def (\w+)\(', line)
            if func_match and (args.all or args.functions):
                inside_function = True
                elements.append(f"[FUNCTION] {func_match.group(1)}")
                
            # Detect classes
            class_match = re.search(r'class (\w+)', line)
            if class_match and (args.all or args.classes):
                inside_class = True
                elements.append(f"[CLASS] {class_match.group(1)}")
                
            # Detect lambda functions
            if 'lambda' in line and (args.all or args.functions):
                lambda_count += 1
                elements.append(f"[LAMBDA] lambda_{lambda_count}")
                
            # Detect decorators
            dec_match = re.search(r'@(\w+)', line)
            if dec_match and (args.all or args.decorators):
                elements.append(f"[DECORATOR] @{dec_match.group(1)}")
                
            # Detect variables
            var_match = re.search(r'(\w+) *=', line)
            if var_match and (args.all or args.variables):
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

def write_tree_to_file(directory, file, args, padding='', joint='├── '):
    file.write(padding + joint + directory.split('/')[-1] + '\n')
    new_padding = padding + ('│   ' if joint == '├── ' else '    ')
    
    for root, dirs, files in os.walk(directory):
        dirs.sort()
        files.sort()
        all_elements = dirs + files
        
        for i, d in enumerate(dirs):
            next_joint = '└── ' if i == len(all_elements) - 1 else '├── '
            write_tree_to_file(os.path.join(root, d), file, args, new_padding, next_joint)
            
        for i, f in enumerate(files):
            next_joint = '└── ' if i == len(files) - 1 and not dirs else '├── '
            file.write(new_padding + next_joint + f + '\n')
            if f.endswith('.py') and not args.files_only:
                elements = list_functions_and_variables_in_file(os.path.join(root, f), args)
                element_padding = new_padding + '    '
                for j, element in enumerate(elements):
                    element_joint = '└── ' if j == len(elements) - 1 else '├── '
                    file.write(element_padding + element_joint + element + '\n')


def get_current_date():
    return datetime.now().strftime('%m_%d_%Y')

def main():
    args = parse_arguments()
    root_directory = '.'  # Replace with the directory you want to examine
    current_date = get_current_date()
    file_name = f'tree_branch_climb_{current_date}.txt'
    with open(file_name, 'w') as file:
        write_tree_to_file(root_directory, file, args)

if __name__ == "__main__":
    main()
