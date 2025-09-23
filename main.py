import pandas as pd
import json
import requests
import os
from openai import OpenAI

# --- Configuration ---
# It's recommended to use environment variables for sensitive data like API keys.
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
if not OPENAI_API_KEY or "YOUR_OPENAI_API_KEY" in OPENAI_API_KEY:
    print("Error: The OPENAI_API_KEY environment variable is not set or is still a placeholder.")
    print("Please set this environment variable to your actual OpenAI API key to run this script.")
    exit()

INPUT_CSV_PATH = 'input.csv'
POSTMAN_COLLECTION_PATH = 'postman_collection.json'
OUTPUT_CSV_PATH = 'output.csv'

# --- OpenAI Client Initialization ---
# The script will exit if the API key is not valid, so we can assume it's correct here.
client = OpenAI(api_key=OPENAI_API_KEY)

def get_api_request_from_instruction(instruction, postman_collection):
    """
    Uses OpenAI's GPT to find the most relevant API request from the Postman collection
    based on the natural language instruction.

    Args:
        instruction (str): The natural language instruction (e.g., "Get all users").
        postman_collection (dict): The parsed Postman collection JSON.

    Returns:
        dict: The API request item from the Postman collection, or None if not found.
    """
    api_request_names = [item['name'] for item in postman_collection['item']]

    prompt = f"""
    You are an intelligent assistant that maps natural language instructions to API requests.
    Given the user's instruction and a list of available API requests, choose the most appropriate API request from the list.

    Instruction: "{instruction}"

    Available API requests:
    - {', '.join(api_request_names)}

    Respond with only the name of the chosen API request. For example: Get All Users
    """

    try:
        # This is the actual call to the OpenAI API.
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an intelligent assistant that maps natural language instructions to API requests."},
                {"role": "user", "content": prompt}
            ],
            temperature=0,
        )
        chosen_request_name = response.choices[0].message.content.strip()

        # Find the request item with the chosen name
        for item in postman_collection['item']:
            if item['name'] == chosen_request_name:
                return item

        print(f"Warning: GPT chose a request ('{chosen_request_name}') that doesn't exist in the collection.")
        return None

    except Exception as e:
        # Specific check for authentication errors
        if "Incorrect API key" in str(e):
             print("\nError: The provided OpenAI API key is incorrect. Please check your OPENAI_API_KEY environment variable.")
             # We are not exiting here to allow the script to continue and generate a report.
             # The error will be logged in the output CSV.
             return None

        print(f"An error occurred during the OpenAI API call: {e}")
        return None


def execute_api_request(request_item):
    """
    Executes an API request using the details from a Postman request item.
    NOTE: This function mocks the API call for demonstration purposes.

    Args:
        request_item (dict): A request item from the Postman collection.

    Returns:
        tuple: A tuple containing the response JSON and any error message.
               (response_json, error_message)
    """
    if not request_item or 'request' not in request_item:
        return None, "Invalid request item"

    request_details = request_item['request']
    method = request_details.get('method', 'GET')
    url = request_details.get('url', {}).get('raw', '')
    headers = {h['key']: h['value'] for h in request_details.get('header', [])}
    body = request_details.get('body', {}).get('raw', None)

    try:
        # In a real-world scenario, you would use the 'requests' library here to make a live HTTP call.
        print(f"Executing (mocked) {method} request to {url}...")

        # Mocked response logic to simulate a live API
        if "users" in url and method == "GET":
            if url.endswith("/users"):
                # Mock for "Get All Users"
                return {"users": [{"id": 1, "name": "Jane Doe"}, {"id": 2, "name": "John Smith"}]}, None
            else:
                # Mock for "Get User by ID"
                return {"id": 1, "name": "Jane Doe"}, None
        elif "users" in url and method == "POST":
            # Mock for "Create User"
            # In a real implementation, you would parse the instruction to extract data for the body
            return {"message": "User created successfully", "id": 3, "name": "John Doe"}, None
        else:
            return None, f"Mocked endpoint not found for {method} {url}"

    except Exception as e:
        # This will catch any other unexpected errors during the mock execution.
        return None, str(e)


# --- Main Execution Logic ---

def main():
    """
    Main function to run the CI/CD test automation process.

    This script reads natural language instructions from a CSV file, finds the
    corresponding API request in a Postman collection, executes the request,
    and writes the output and any errors to a new CSV file.
    """
    # 1. Load input data from CSV and Postman collection JSON file.
    try:
        df = pd.read_csv(INPUT_CSV_PATH)
        with open(POSTMAN_COLLECTION_PATH, 'r') as f:
            postman_collection = json.load(f)
    except FileNotFoundError as e:
        print(f"Error: {e}. Make sure '{INPUT_CSV_PATH}' and '{POSTMAN_COLLECTION_PATH}' exist.")
        return

    # 2. Process instructions
    results = []
    for index, row in df.iterrows():
        instruction = row['instruction']
        print(f"Processing instruction: '{instruction}'")

        # Find the API request
        api_request = get_api_request_from_instruction(instruction, postman_collection)

        if not api_request:
            results.append({'output': '', 'error': 'Could not find a matching API request.'})
            continue

        # Execute the API request
        response_data, error_message = execute_api_request(api_request)

        # Store the result
        if error_message:
            results.append({'output': '', 'error': error_message})
        else:
            results.append({'output': json.dumps(response_data), 'error': ''})

    # 3. Update DataFrame and save to output CSV
    df[['output', 'error']] = pd.DataFrame(results, index=df.index)
    df.to_csv(OUTPUT_CSV_PATH, index=False)

    print(f"\nProcessing complete. Results saved to '{OUTPUT_CSV_PATH}'.")


def generate_summary_chart(csv_path):
    """
    Generates a pie chart summarizing the test execution results from the output CSV.

    Args:
        csv_path (str): The path to the output CSV file.
    """
    try:
        df = pd.read_csv(csv_path)
        # An empty 'error' column signifies a successful run for that instruction.
        # We handle both empty strings and actual NaN values.
        successful_runs = df['error'].isna() | (df['error'] == '')
        num_successful = successful_runs.sum()
        num_failed = len(df) - num_successful

        labels = ['Successful', 'Failed']
        counts = [num_successful, num_failed]
        colors = ['#4CAF50', '#F44336'] # Green for success, Red for failure

        # Only generate a chart if there are results to show
        if sum(counts) > 0:
            # Import matplotlib here to avoid making it a hard dependency for the whole script
            import matplotlib.pyplot as plt

            plt.figure(figsize=(8, 6))
            plt.pie(counts, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140,
                    wedgeprops={'edgecolor': 'white', 'linewidth': 1})
            plt.title('API Test Execution Summary')
            plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

            chart_path = 'test_summary_chart.png'
            plt.savefig(chart_path)
            print(f"\nGenerated summary chart and saved to '{chart_path}'.")
        else:
            print("\nNo results to generate a chart from.")

    except FileNotFoundError:
        print(f"Error: Could not find '{csv_path}' to generate chart.")
    except Exception as e:
        print(f"An error occurred during chart generation: {e}")


if __name__ == "__main__":
    main()
    # After the main logic, generate the summary chart
    generate_summary_chart(OUTPUT_CSV_PATH)
