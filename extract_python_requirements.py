import os
import re

def extract_python_requirements(directory):
    """
    Extracts python package requirements from all python files in a given directory.

    Args:
    directory (str): The directory path containing the python files.

    Returns:
    set: A set of unique package names extracted from import statements.
    """
    requirements = set()
    regex = re.compile(r'^\s*(?:import|from)\s+(\S+)')

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                with open(os.path.join(root, file), 'r') as f:
                    for line in f:
                        match = regex.match(line)
                        if match:
                            # Extract the base package name (e.g., 'os', 'numpy', 'django.shortcuts')
                            package = match.group(1).split('.')[0]
                            requirements.add(package)

    return requirements

# Example usage
directory = '/Users/m.fuss/PycharmProjects/ShopwareAIConnectorPython'  # Replace with the actual directory path
requirements = extract_python_requirements(directory)
print(requirements)
