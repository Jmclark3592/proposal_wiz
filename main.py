from db_connect import connect_to_db
import requests
import json

# Your OpenAI API key (DO NOT SHARE THIS)
API_KEY = "YOUR_OPENAI_API_KEY"

# Assuming previously defined functions and mock databases are available...
# Mock database represented as dictionaries
clients_db = {}
profiles_db = {}
advertisements_db = {}

# Mock client ID, profile ID, and ad ID counters
client_id_counter = 1
profile_id_counter = 1
ad_id_counter = 1

def add_client_to_db(client_name: str, questionnaire_data: str, analytics_data: str) -> int:
    """
    Inserts client data into the PostgreSQL database and returns the generated client_id.
    """
    conn = connect_to_db()
    if not conn:
        return None

    # Insert data into clients table
    query = """
    INSERT INTO clients (client_name, questionnaire_data, analytics_data)
    VALUES (%s, %s, %s) RETURNING client_id;
    """
    cur = conn.cursor()
    try:
        cur.execute(query, (client_name, questionnaire_data, analytics_data))
        client_id = cur.fetchone()[0]  # Fetch the returned client_id
        conn.commit()
        cur.close()
        return client_id
    except Exception as e:
        print(f"Error: Unable to add client data to the database.\n{e}")
        conn.rollback()
        cur.close()
        return None
    finally:
        conn.close()


def get_client_data(client_id: int) -> dict:
    return clients_db.get(client_id, {})

# Test the add_client function
test_client_id = add_client_to_db("Nike", "Sample questionnaire data", "Sample Google Analytics data")
get_client_data(test_client_id)

def add_profile_to_db(client_id: int, profile_data: str) -> int:
    """
    Inserts profile data for a specific client into the PostgreSQL database and returns the generated profile_id.
    """
    conn = connect_to_db()
    if not conn:
        return None

    # Insert data into profiles table
    query = """
    INSERT INTO profiles (client_id, profile_data)
    VALUES (%s, %s) RETURNING profile_id;
    """
    cur = conn.cursor()
    try:
        cur.execute(query, (client_id, profile_data))
        profile_id = cur.fetchone()[0]  # Fetch the returned profile_id
        conn.commit()
        cur.close()
        return profile_id
    except Exception as e:
        print(f"Error: Unable to add profile data to the database.\n{e}")
        conn.rollback()
        cur.close()
        return None
    finally:
        conn.close()


def add_advertisement_to_db(profile_id: int, advertisement_content: str) -> int:
    """
    Inserts advertisement content for a specific profile into the PostgreSQL database and returns the generated ad_id.
    """
    conn = connect_to_db()
    if not conn:
        return None

    # Insert data into advertisements table
    query = """
    INSERT INTO advertisements (profile_id, advertisement_content)
    VALUES (%s, %s) RETURNING ad_id;
    """
    cur = conn.cursor()
    try:
        cur.execute(query, (profile_id, advertisement_content))
        ad_id = cur.fetchone()[0]  # Fetch the returned ad_id
        conn.commit()
        cur.close()
        return ad_id
    except Exception as e:
        print(f"Error: Unable to add advertisement to the database.\n{e}")
        conn.rollback()
        cur.close()
        return None
    finally:
        conn.close()


# Test the add_profile and add_advertisement functions
test_profile_id = add_profile_to_db(test_client_id, "Profile data for Gen Z audience")
test_ad_id = add_advertisement_to_db(test_profile_id, "New Nike shoes for the Gen Z!")
test_profile_id, test_ad_id

def pull_data_for_strategy(client_id: int) -> dict:
    """
    Function to pull relevant data for strategy creation based on client_id.
    """
    client_data = get_client_data(client_id)
    if not client_data:
        raise ValueError("Client ID not found.")
    return client_data

def interact_with_llm_for_profiles(client_data: dict, num_profiles: int) -> list:
    """
    Simulates interaction with the LLM to generate profiles based on the provided client data.
    For simplicity, we'll just mock the LLM's response in this function.
    """
    # Mocked LLM response for simplicity
    mock_profiles = [f"Profile {i+1} for {client_data['client_name']}" for i in range(num_profiles)]
    return mock_profiles

# Test the functions
test_client_data = pull_data_for_strategy(test_client_id)
test_llm_profiles = interact_with_llm_for_profiles(test_client_data, 3)
test_llm_profiles

def pull_data_from_db(client_id: int) -> dict:
    """
    Pulls relevant data for strategy creation based on client_id from the PostgreSQL database.
    """
    conn = connect_to_db()
    if not conn:
        return None

    # Query to fetch data for the specified client_id
    query = """
    SELECT client_name, questionnaire_data, analytics_data
    FROM clients
    WHERE client_id = %s;
    """
    cur = conn.cursor()
    try:
        cur.execute(query, (client_id,))
        data = cur.fetchone()
        if data:
            client_data = {
                'client_name': data[0],
                'questionnaire_data': data[1],
                'analytics_data': data[2]
            }
            cur.close()
            return client_data
        else:
            cur.close()
            return None
    except Exception as e:
        print(f"Error: Unable to fetch client data from the database.\n{e}")
        cur.close()
        return None
    finally:
        conn.close()


def interact_with_llm_for_profiles(client_data: dict, num_profiles: int) -> list:
    """
    Simulates interaction with the LLM to generate profiles based on the provided client data.
    For simplicity, we'll just mock the LLM's response in this function.
    """
    # Mocked LLM response for simplicity
    mock_profiles = [f"Profile {i+1} for {client_data['client_name']}" for i in range(num_profiles)]
    return mock_profiles

# Test the functions
test_client_data = pull_data_for_strategy(test_client_id)
test_llm_profiles = interact_with_llm_for_profiles(test_client_data, 3)
test_llm_profiles


def input_client_data():
    client_name = input("Enter client name: ")
    questionnaire_data = input("Enter questionnaire data: ")
    analytics_data = input("Enter Google Analytics data: ")
    client_id = add_client_to_db(client_name, questionnaire_data, analytics_data)
    print(f"Client data added with ID: {client_id}")

def strategist_workflow():
    client_id = int(input("Enter the client ID to pull data for strategy: "))
    client_data = pull_data_for_strategy(client_id)
    print(f"Pulled data for client {client_data['client_name']}:")
    print(f"Questionnaire Data: {client_data['questionnaire_data']}")
    print(f"Google Analytics Data: {client_data['analytics_data']}")

    num_profiles = int(input("How many profiles do you want to work on? "))
    generated_profiles = interact_with_llm_for_profiles(client_data, num_profiles)
    print("Generated profiles:")
    for profile in generated_profiles:
        print(profile)
        # For demonstration purposes, we're saving each profile to the profiles_db
        add_profile_to_db(client_id, profile)



def interact_with_openai(prompt: str) -> str:
    """
    Interacts with OpenAI's API using the provided prompt and returns the model's response.
    """
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "prompt": prompt,
        "max_tokens": 150  # You can adjust this based on your needs
    }

    response = requests.post("https://api.openai.com/v1/engines/davinci/completions", headers=headers, data=json.dumps(data))
    response_json = response.json()

    if response.status_code == 200:
        return response_json["choices"][0]["text"].strip()
    else:
        print(f"Error interacting with OpenAI API: {response_json['error']}")
        return None


def main():
    while True:
        print("\nOptions:")
        print("1. Input Client Data")
        print("2. Strategist Workflow")
        print("3. Data Analyst Workflow")
        print("4. Copywriter Workflow")
        print("5. Exit")
        choice = int(input("Enter your choice: "))
        if choice == 1:
            input_client_data()
        elif choice == 2:
            strategist_workflow()
        elif choice == 3:
            data_analyst_workflow()
        elif choice == 4:
            copywriter_workflow()
        elif choice == 5:
            break
        else:
            print("Invalid choice. Please try again.")

# Uncomment the next line to run the CLI interface.
# main()