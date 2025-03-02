from flask import Flask, render_template, request, jsonify
from chatbot import call_llm
import json
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--port", default=8000)
# parser.add_argument("--ml-endpoint", default="http://localhost:5000")
ngrok_link = "https://80e9-2601-646-a180-6c90-6980-458c-acad-42ce.ngrok-free.app"
parser.add_argument("--ml-endpoint", default=f"{ngrok_link}/ai")
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
        # response_text = call_llm(input_text, model_endpoint)
        response_text = (
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. "
            "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. "
            "Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. "
            "Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum. "
            "Curabitur pretium tincidunt lacus. Nulla gravida orci a odio. Nullam varius, turpis et commodo pharetra, est eros bibendum elit, "
            "nec luctus magna felis sollicitudin mauris. Integer in mauris eu nibh euismod gravida. Duis ac tellus et risus vulputate vehicula. "
            "Donec lobortis risus a elit. Etiam tempor. Ut ullamcorper, ligula eu tempor congue, eros est euismod turpis, id tincidunt sapien risus a quam. "
            "Maecenas fermentum consequat mi. Donec fermentum. Pellentesque malesuada nulla a mi. Duis sapien sem, aliquet nec, commodo eget, consequat quis, neque. "
            "Aliquam faucibus, elit ut dictum aliquet, felis nisl adipiscing sapien, sed malesuada diam lacus eget erat. Cras mollis scelerisque nunc. "
            "Nullam arcu. Aliquam consequat. Curabitur augue lorem, dapibus quis, laoreet et, pretium ac, nisi. Aenean magna nisl, mollis quis, molestie eu, feugiat in, orci. "
            "In hac habitasse platea dictumst."
        )
        return jsonify({"response": response_text})
    else:
        # Display a simple starting message when the app is accessed via GET
        opening_message = "Hi, I'm CareerNavigator! Please share your interests, skills, or aspirations to get started."
        return render_template("index.html", display_text=opening_message)

if __name__ == "__main__":
    app.run(port=args.port, host="0.0.0.0", debug=False)

# chat box scrollable
