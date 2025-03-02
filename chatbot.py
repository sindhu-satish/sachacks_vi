import requests

def call_llm(input_text, model_endpoint):
    """
    Sends the given input_text as a prompt to the LLM at the provided model_endpoint.
    Returns the response text from the LLM.
    """
    json_data = {"query": input_text}
    try:
        response = requests.post(url=model_endpoint, json=json_data)
        response.raise_for_status()
        data = response.json()
        print(data)
        return data.get("answer", "No response returned from the model.")
    except Exception as e:
        print(f"Error calling the LLM: {str(e)}")
        return f"Oops! Try again"
