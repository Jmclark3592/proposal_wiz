def pull_raw_data_for_analysis(client_id: int) -> dict:
    """
    Pulls raw questionnaire and Google Analytics data for analysis based on client_id from the PostgreSQL database.
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
        print(f"Error: Unable to fetch client data from the database for analysis.\n{e}")
        cur.close()
        return None
    finally:
        conn.close()

def perform_data_analysis(client_data: dict) -> dict:
    """
    Simulates data analysis on the pulled data. This is a placeholder function that can be expanded upon with actual 
    analysis techniques and tools in the future.
    """
    # Mock analysis results
    analysis_results = {
        "key_demographics": "Generation Z and Millennials",
        "preferred_channels": "Social Media, especially Instagram and TikTok",
        "key_interests": "Sustainable fashion, Sports, Music"
    }
    return analysis_results

def save_analysis_results(client_id: int, analysis_results: dict) -> int:
    """
    Saves the results of the data analysis back into the PostgreSQL database and returns the generated analysis_id.
    """
    conn = connect_to_db()
    if not conn:
        return None

    # Insert data into analysis_results table
    query = """
    INSERT INTO analysis_results (client_id, key_demographics, preferred_channels, key_interests)
    VALUES (%s, %s, %s, %s) RETURNING analysis_id;
    """
    cur = conn.cursor()
    try:
        cur.execute(query, (client_id, analysis_results['key_demographics'], 
                            analysis_results['preferred_channels'], analysis_results['key_interests']))
        analysis_id = cur.fetchone()[0]  # Fetch the returned analysis_id
        conn.commit()
        cur.close()
        return analysis_id
    except Exception as e:
        print(f"Error: Unable to save analysis results to the database.\n{e}")
        conn.rollback()
        cur.close()
        return None
    finally:
        conn.close()

def data_analyst_workflow():
    client_id = int(input("Enter the client ID to pull raw data for analysis: "))
    client_data = pull_raw_data_for_analysis(client_id)
    if not client_data:
        print("Error: Unable to fetch client data for analysis.")
        return

    print(f"\nPulled data for client {client_data['client_name']}:")
    print(f"Questionnaire Data: {client_data['questionnaire_data']}")
    print(f"Google Analytics Data: {client_data['analytics_data']}\n")

    print("Performing data analysis...")
    analysis_results = perform_data_analysis(client_data)
    print(f"\nAnalysis Results:")
    for key, value in analysis_results.items():
        print(f"{key}: {value}")

    choice = input("\nWould you like to save these analysis results to the database? (yes/no): ")
    if choice.lower() == "yes":
        analysis_id = save_analysis_results(client_id, analysis_results)
        if analysis_id:
            print(f"Analysis results saved with ID: {analysis_id}")
        else:
            print("Error: Unable to save analysis results to the database.")


