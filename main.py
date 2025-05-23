# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import argparse
from qrcodes import generate_qr_code_file, generate_qr_code_bytes
from jsoninputfile import read_json_from_file, get_json_value


# TODO: QR code should be around the logo, not under the logo
# TODO: logo should preserve proportions when resized
# TODO: create UI (ask gemini or Claude to create it in HTML)

def setup_input_args():
    parser = argparse.ArgumentParser(description="My QR Code Generator")
    parser.add_argument("--input_file", help="Input file path")
    parser.add_argument("--output_dir", help="Output directory")
    arguments = parser.parse_args()
    return arguments


if __name__ == "__main__":

    # link_to_encode = input("Enter the link you want to convert to a QR code: ")
    # output_filename = input("Enter the desired filename for the QR code (e.g., my_qr.png): ") or "qr_code.png"  # Default filename if user doesn't provide one.

    args = setup_input_args()
    if args.input_file:
        json_data = read_json_from_file(args.input_file)

        if json_data:
            print("JSON data loaded successfully:")
            # Process the data as needed. Here are some examples:
            if isinstance(json_data, dict):
                url = get_json_value(json_data,"url")
                logo_file = get_json_value(json_data,"logo_file")
                filename = get_json_value(json_data,"filename","qr_code.png")
                fill_color = get_json_value(json_data,"fill_color","black")
                back_color = get_json_value(json_data,"back_color","white")
                size = get_json_value(json_data,"size",10)
                border = get_json_value(json_data,"border",1)

                # generate_qr_code(url, filename, "purple")
                generate_qr_code_file(data=url,
                                           logo_file=logo_file,
                                           output_file=filename,
                                           fill_color=fill_color,
                                           back_color=back_color,
                                           size=size,
                                           border=border)

                # for key, value in json_data.items():
                #     print(f"{key}: {value}")
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
    else:
        print("Input file argument missing.")

