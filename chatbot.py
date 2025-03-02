import requests

def call_llm(input_text, model_endpoint):
    """
    Sends the given input_text as a prompt to the LLM at the provided model_endpoint.
    Returns the response text from the LLM.
    """
    # Prepare the JSON payload according to the expected input format of the LLM
    json_data = {"prompt": input_text}
    try:
        response = requests.post(url=model_endpoint, json=json_data)
        response.raise_for_status()
        data = response.json()
        return data.get("response", "No response returned from the model.")
    except Exception as e:
        return f"Error calling the LLM: {str(e)}"
