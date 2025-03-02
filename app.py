

from flask import Flask, render_template, request, jsonify
from chatbot import get_opening_message, get_choice, get_topic, match, narrow, ask, end, get_next_text
import json
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--port", default=8000)
parser.add_argument("--ml-endpoint", default="http://localhost:5000")
args = parser.parse_args()

app = Flask(__name__)

states = {
    1: get_topic,
    2: match,
    3: narrow,
    4: ask,
    5: end
}

textbook_data = None
titles = None
model_endpoint = args.ml_endpoint

if '/model/predict' not in model_endpoint:
    model_endpoint = model_endpoint.rstrip('/') + "/model/predict"

@app.route("/", methods=["POST", "GET", "HEAD"])
def chat():
    if request.method == "POST":
        data = json.loads(request.data)
        input_text = data["input"]
        state = int(data["state"])

        get_next_text = states.get(state)
        narrowed_titles = titles

        # narrow titles if necessary
        if state == 3:
            narrowed_titles = get_subtitles(textbook_data, titles, get_choice())

        response, new_state, matches = get_next_text(model_endpoint, input_text, narrowed_titles)
        return jsonify({"response": response, "state": new_state, "matches": matches})

    else:
        '''Start a conversation.'''
        return render_template("index.html", display_text=get_opening_message(), state=1)


if __name__ == "__main__":
    app.run(port=args.port, host="0.0.0.0", debug=False)
