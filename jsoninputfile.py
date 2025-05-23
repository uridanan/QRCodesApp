import json

def read_json_from_file(filepath):
    """
    Reads JSON data from a file.

    Args:
        filepath: The path to the JSON file.

    Returns:
        A Python object (usually a dictionary or list) representing the JSON data,
        or None if an error occurs (e.g., file not found, invalid JSON).
        Prints an error message to the console if there's a problem.
    """

    try:
        with open(filepath, 'r', encoding='utf-8') as f:  # Use 'r' for reading, utf-8 encoding
            data = json.load(f) # Parse the JSON data
            return data
    except FileNotFoundError:
        print(f"Error: File not found at {filepath}")
        return None
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in {filepath}")
        return None
    except Exception as e: # Catching a broader range of potential errors
        print(f"An unexpected error occurred: {e}")
        return None


def get_json_value(data, key, default_value=None):
    """
    Retrieves the value of a key from JSON data (dictionary or nested dictionaries).

    Args:
        data: The JSON data (dictionary or nested dictionaries).
        key: The key to search for. Can be a string for a top-level key,
             or a dot-separated string for nested keys (e.g., "address.city").

    Returns:
        The value associated with the key, or None if the key is not found
        or if the data is not a dictionary.  Handles nested keys.
        :param key:
        :param data:
        :param default_value:
    """

    if not isinstance(data, dict):  # Check if data is a dictionary
        return default_value

    if "." in key:  # Handle nested keys
        keys = key.split(".")
        current_data = data
        for k in keys:
            if isinstance(current_data, dict) and k in current_data:
                current_data = current_data[k]
            else:
                return default_value  # Key not found at this level
        return current_data  # Return the value at the end of the chain

    else:  # Handle top-level keys
        if key in data:
            return data[key]
        else:
            return default_value


# Example usage:
if __name__ == "__main__":
    file_path = "data.json"  # Replace with your file path
    json_data = read_json_from_file(file_path)

    if json_data:
        print("JSON data loaded successfully:")
        # Process the data as needed. Here are some examples:
        if isinstance(json_data, dict):
            for key, value in json_data.items():
                print(f"{key}: {value}")
        elif isinstance(json_data, list):
            for item in json_data:
                print(item)
        else:  # Handle other JSON structures if needed
            print("JSON data is not a dictionary or a list.")

        # Example of accessing specific data (if it's a dictionary)
        # if isinstance(json_data, dict) and "name" in json_data:
        #     name = json_data["name"]
        #     print(f"Name: {name}")
    else:
        print("Failed to load JSON data.")