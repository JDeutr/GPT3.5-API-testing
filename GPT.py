import argparse
import re
import json
from openai import OpenAI

# Set your OpenAI API key
client = OpenAI(
    api_key="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"
)

def make_api_tests(input_file, output_file):
    # Read input JSON file
    with open(input_file, 'r') as f:
        data = json.load(f)
    json_string = json.dumps(data, indent=2)
    
    # Generate Python code for API tests
    response = client.chat.completions.create(
        model ="gpt-3.5-turbo",
        messages = [
            {"role": "system", "content": "You are an API tester that has to make API-tests based on json files of an API response"},
            {"role": "user", "content": "Can you make API-tests in python to test an API with the following response: " + json_string}
        ]
    )


    file_path = output_file

    pattern = r"```python(.*?)```"
    matches = re.findall(pattern, response.choices[0].message.content, re.DOTALL)

    with open(file_path, 'w') as file:
        file.write(matches[0].strip())

    print("Document " + file_path + " made!")
    

def main():
    parser = argparse.ArgumentParser(description='Generate Python code for API tests using OpenAI API from a JSON file.')
    parser.add_argument('input_file', help='Path to the input JSON file')
    parser.add_argument('output_file', help='Name of the new output JSON file')

    args = parser.parse_args()

    make_api_tests(args.input_file, args.output_file)

if __name__ == '__main__':
    main()
