import requests
import random
from similarity.metric_lcs import MetricLCS


def get_opening_message():
    '''The variable starting message.'''
    return f"Hi, my name is CareerNavigator!\n\
    I'm an AI-driven virtual career exploration assistant designed to help you discover your ideal career domain.\n\
    To get started, please share some of your interests, skills, or aspirations."



def get_choice():
    '''Return the value of the global `choice` variable'''
    return choice


def get_close_matches(topic, titles, distance_threshold=0.4):
    '''Return matching titles for a topic.'''
    metric_lcs = MetricLCS()
    matches = []
    for full_title in titles:
        dist = metric_lcs.distance(topic, full_title[-1])
        if dist <= distance_threshold:
            matches.append(full_title)
    return matches


def numbered_print(strings):
    '''Display strings in a numbered list.'''
    final = ""
    for i, s in enumerate(strings):
        final += str(i+1) + '. ' + ", ".join(s) + "\n"
    return final


# state 1
def get_topic(model_endpoint, topic, titles):
    if topic.lower() == "stop":
        return "Thank You for using QnAit, Hope your questions were answered!", 5, {}

    # hardcoded fun :)
    if topic == "What is the meaning of life?":
        return "42\n\nIf you are curious about another topic, reply with the topic.", 1, {}

    matches = get_close_matches(topic.title(), titles.keys())
    if len(matches) == 0:
        return "I couldn't find that topic. Can you try rephrasing that or being more specific?", 1, {}
    else:

        return "Ok, which of the following best matches the topic of your question?\n" + numbered_print(matches), 2, matches


# state 3
def narrow(model_endpoint, topic, titles):
    matches = get_close_matches(topic.title(), titles.keys())
    if len(matches) == 0:
        return "I couldn't find that topic. Can you try rephrasing that or being more specific?", 1, {}
    else:
        return "Ok, which of the following best matches the topic of your question?\n" + numbered_print(matches), 2, matches


# state 2
def match(model_endpoint, topic, titles):
    global choice
    choice = tuple(topic)
    if titles[choice][0] != "subsection":
        return "I need more specific information. Could you try to ask more specifically?", 3, {}
    else:
        return "Ok! What's your question?", 4, {}


# state 4
def ask(model_endpoint, question, titles):
    json_data = {"paragraphs": [{"context": titles[choice][1],
                                 "questions": [question]}]}
    r = requests.post(url=model_endpoint, json=json_data).json()
    return r["predictions"][0][0] + "\n\nTo stop this session, type 'Stop'. \n\
              If you are curious about another topic, reply with the topic.", 1, {}


# state 5
def end(model_endpoint, topic, titles):
    return "restarting app...\n\n" + get_opening_message(), 1, {}
