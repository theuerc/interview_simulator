"""Write google secret json for gitpod initialization"""
import argparse
import json

def write_to_json(filename, dic_str):
    """write string to json"""
    # Convert the string to a dictionary
    dic = json.loads(dic_str)

    # Write the dictionary to a JSON file
    with open(filename, "w") as json_file:
        json.dump(dic, json_file, indent=4)

if __name__ == "__main__":
    """take in arguments and convert string to json"""
    parser = argparse.ArgumentParser(description="Write a JSON string to a file.")
    parser.add_argument("filename", type=str, help="The name of the file to write to.")
    parser.add_argument("dic_string", type=str, help="The JSON string to write to the file.")

    args = parser.parse_args()

    write_to_json(args.filename, args.dic_string)
