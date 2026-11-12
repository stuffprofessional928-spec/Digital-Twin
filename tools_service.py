
import os
from dotenv import load_dotenv
import requests
import json


load_dotenv(override=True)


pushover_user = os.getenv("PUSHOVER_USER")
pushover_key = os.getenv("PUSHOVER_TOKEN")
pushover_url = "https://api.pushover.net/1/messages.json"




def push(message):
    payload = {"user":pushover_user,"token":pushover_key,"message":message}
    requests.post(pushover_url, data=payload)
    


def record_user_detail(email, name="Not provided" , notes = "Not provided"):
    push(f"Recording intrest from {name} with email {email} and notes {notes}")
    return "OK"

def record_unknown_questions(question):
    push(f"Recording question not answered: {question}")
    return "OK"

def record_email_tool(email):
    print(f"Tool call to record an email {email}\n\n")
    with open("emails.txt","a",encoding="utf-8") as f:
        f.write(email + "\n")
        
    return "Email Received"


record_unknown_questions_json = {
    "name":"record_unknown_questions",
    "description": "Record question when not able to give answer",
    "parameters":{
        "type":"object",
        "properties":{
            "question": {"type":"string", "description":"Question not answered"}
        },
        "required":["question"],
        "additionalProperties":False
    }
}


record_user_detail_json = {
    "name": "record_user_detail",
    "description":"Record the data provided by user like email name and notes",
    "parameters":{
        "type":"object",
        "properties":{
            "email":{"type":"string", "description":"Email address of the user"},
            "name":{"type":"string", "description":"Name of the user"},
            "notes":{"type":"string","description":"notes given by user"}
        },
        "required":["email","name","notes"],
        "additionalProperties":False
    }
}


record_email_tool_json = {
    "name":"record_email_tool",
    "description":"A tool to call when user provided an email id so using this tool we can save it.",
    "parameters":{
        "type":"object",
        "properties":{
            "email":{"type":"string", "description":"The email address of the user"}
        },
        "required":["email"],
        "additionalProperties":False
    }
}

tools = [
    {"type":"function","function": record_email_tool_json},
    {"type":"function","function": record_user_detail_json},
    {"type":"function","function": record_unknown_questions_json},
]

def handle_tool_call(tool_calls):
    print(tool_calls)
    results = []
    for tool_call in tool_calls:
        tool_name = tool_call.function.name
        arguments = json.loads(tool_call.function.arguments)
        print("tool name ========",tool_name)
        print("arguments ========", arguments)
        if tool_name == "record_email_tool":
            result = record_email_tool(**arguments)
            print("first tool ==============",result)
        elif tool_name == "record_user_detail":
            result = record_user_detail(**arguments)
            print("second tool ==============",result)
        elif tool_name == "record_unknown_questions":
            result = record_unknown_questions(**arguments)
            print("second tool ==============",result)
        
        results.append({"role":"tool","content": json.dumps(result),"tool_call_id":tool_call.id})
    return results
