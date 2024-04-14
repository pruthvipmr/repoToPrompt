import os

def get_file_content(file_path):
    """ Reads the content of a file given its path."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def build_directory_tree(path, indent=0, file_paths=[]):
    """Recursively builds a string representation of the directory tree and collects file paths."""
    tree_str = ""
    items = os.listdir(path)
    for item in items:
        item_path = os.path.join(path, item)
        if os.path.isdir(item_path):
            if item == "node_modules":
                continue  # Skip "node_modules" folder (can remove if not needed)
            tree_str += ' ' * indent + f"[{item}/]\n"
            tree_str += build_directory_tree(item_path, indent + 1, file_paths)[0]
        else:
            tree_str += ' ' * indent + f"{item}\n"
            if item.endswith(('.py', '.ipynb', '.html', '.css', '.js', '.jsx', '.rst', '.md')):
                file_paths.append((indent, item_path))
    return tree_str, file_paths

def retrieve_folder_info(folder_path):
    """Retrieves and formats the folder information, including README, directory tree, and file contents."""
    formatted_string = ""
    readme_path = os.path.join(folder_path, 'README.md')
    if os.path.exists(readme_path):
        readme_content = get_file_content(readme_path)
        formatted_string = f"README.md:\n```\n{readme_content}\n```\n\n"
    else:
        formatted_string = "README.md: Not found or error fetching README\n\n"

    directory_tree, file_paths = build_directory_tree(folder_path)
    formatted_string += f"Directory Structure:\n{directory_tree}\n"

    for indent, file_path in file_paths:
        file_content = get_file_content(file_path)
        formatted_string += '\n' + ' ' * indent + f"{os.path.relpath(file_path, folder_path)}:\n" + ' ' * indent + '```\n' + file_content + '\n' + ' ' * indent + '```\n'

    return formatted_string

# Example usage
folder_path = "path/to/directory"
output_file = "output.txt"

formatted_string = retrieve_folder_info(folder_path)
with open(output_file, 'w', encoding='utf-8') as file:
    file.write(formatted_string)