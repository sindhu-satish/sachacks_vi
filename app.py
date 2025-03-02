from flask import Flask, render_template, request, jsonify
from chatbot import call_llm
import json
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--port", default=8000)
# parser.add_argument("--ml-endpoint", default="http://localhost:5000")
parser.add_argument("--ml-endpoint", default="https://bb88-2601-646-a180-6c90-6980-458c-acad-42ce.ngrok-free.app/ai")
args = parser.parse_args()

app = Flask(__name__)
model_endpoint = args.ml_endpoint

# if '/model/predict' not in model_endpoint:
#     model_endpoint = model_endpoint.rstrip('/') + "/model/predict"

@app.route("/", methods=["POST", "GET", "HEAD"])
def chat():
    if request.method == "POST":
        data = request.get_json()
        input_text = data.get("input", "")
        response_text = call_llm(input_text, model_endpoint)
        return jsonify({"response": response_text})
    else:
        # Display a simple starting message when the app is accessed via GET
        opening_message = "Hi, I'm CareerNavigator! Please share your interests, skills, or aspirations to get started."
        return render_template("index.html", display_text=opening_message)

if __name__ == "__main__":
    app.run(port=args.port, host="0.0.0.0", debug=False)
