import toml

def convert_poetry_to_requirements(pyproject_path, requirements_path):
    # Read the pyproject.toml file
    with open(pyproject_path, 'r') as file:
        pyproject_data = toml.load(file)
    
    # Extract dependencies
    dependencies = pyproject_data['tool']['poetry']['dependencies']
    
    # Create a list to store the dependencies in requirements.txt format
    requirements = []
    
    for package, version in dependencies.items():
        if package == 'python':
            continue  # Skip the Python version specification
        # Convert versions specified as "^*.*.*" or "*.*.*" to "==*.*.*"
        if isinstance(version, dict) and 'version' in version:
            requirements.append(f"{package}=={version['version'].lstrip('^')}")
        else:
            requirements.append(f"{package}=={version.lstrip('^')}")
    
    # Write the requirements to the requirements.txt file
    with open(requirements_path, 'w') as file:
        file.write("\n".join(requirements))
    
    print(f"Converted {pyproject_path} to {requirements_path}")

# Usage
convert_poetry_to_requirements('pyproject.toml', 'requirements.txt')
