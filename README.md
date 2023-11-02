# Uproot: Python File System Visualizer and Repository Structure Provider for LLM Software Development 🌳

Command line python script to replicate bash tree command down to functions, variables, methods, etc 

## Overview

Welcome to Uproot! This is your go-to Python library for **file system visualization**, **codebase analysis**, and **project structure mapping**, ideally for LLM code development. Seamlessly navigate your directories and get insights into your Python codebase.

🌟 **Why Uproot?**
- Generate **file tree structures** for easy visualization
- In-depth **Python script analysis** to identify code components
- Tag and identify **primitive Python data structures**
- Perfect for developers, data scientists, and code reviewers

## Features

- **Directory Traversal**: Easily generate a **tree-like structure** for any directory. Great for project management and organization.
- **Code Inspection**: Quickly identify **functions**, **methods**, and **variables** within your `.py` files. Ideal for code review and quality assurance.
- **Data Structure Identification**: Automatically tag **primitive Python data structures** like List, Dictionary, Tuple, and Set. Useful for data manipulation and analysis.

## Installation 🛠️

Installing Uproot is a breeze. Just clone the repository and run it within your Python environment.

```bash
git clone https://github.com/your-username/uproot.git
cd uproot
python main.py
```

## Usage 📚

### Basic Usage

```python
from uproot import main

# Generate a tree for the current directory
main(root_directory='.')
```

Get a complete **file system tree** in a text file right in your current directory.

### Advanced Usage 🚀

For power users, you can also filter to visualize only specific types of files.

```python
from uproot import main

# Generate a tree for the current directory and focus on `.py` files
main(root_directory='.', file_types=['.py'])
```

## Sample Output 📄

Your output will be a neat, easy-to-read text file:

```
├── project
│   ├── script.py
│   │   ├── [FUNCTION] main
│   │   ├── [GLOBAL_VARIABLE] logger
│   │   └── [DICTIONARY] config
│   └── utils.py
│       ├── [FUNCTION] helper
│       └── [LIST] items
```

## Contribute 🤝

Join the Uproot community! Feel free to fork the project, open a PR, or submit an issue.

## License 📜

Licensed under the MIT License. See [LICENSE](LICENSE) for more details.

