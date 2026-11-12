import os
from dotenv import load_dotenv
from openai import OpenAI
import gradio as gr
from gradio import themes
from tools_service import tools, handle_tool_call
from context import SYSTEM_PROMPT
from styles import CSS, JS, EXAMPLES


load_dotenv(override=True)

api_key = os.getenv("OPENROUTER_API_KEY")
hf_token = os.getenv("HF_TOKEN")
openrouter_url = os.getenv("OPENROUTER_URL")
server_name = os.getenv("SERVER_NAME")
server_port = os.getenv("SERVER_PORT")



if api_key:
    print(f"API key is there which starts from {api_key[:8]}")
else:
    print("No apikey is there")
    

client = OpenAI(base_url=openrouter_url,api_key=api_key)


def chat(message, history):
    messages = [{"role":"system","content":SYSTEM_PROMPT}] + history + [{"role":"user","content": message}]
    response = client.chat.completions.create(model="gpt-5.4-nano", messages= messages, tools=tools)
    while response.choices[0].finish_reason == "tool_calls":
        message = response.choices[0].message
        messages.append(message)
        tool_calls = message.tool_calls
        # print("tools=========", tool_calls)
        # print("message=========", message)
        result = handle_tool_call(tool_calls=tool_calls)
        messages.extend(result)
        response = client.chat.completions.create(model="gpt-5.4-nano",messages=messages,tools=tools) 
    return response.choices[0].message.content         
        

# def stream_chat(message, history):
#     messages = [{"role":"system","content":SYSTEM_PROMPT}] + history + [{"role":"user","content": message}]
#     response = client.chat.completions.create(model="gpt-5.4-nano", messages= messages, tools=tools, stream=True)
#     for chunk in response:
#         if chunk.choices and chunk.choices[0].delta.content:
#             while response.choices[0].finish_reason == "tool_calls":
#             message = response.choices[0].message
#             messages.append(message)
#             tool_calls = message.tool_calls
#         # print("tools=========", tool_calls)
#         # print("message=========", message)
#             result = handle_tool_call(tool_calls=tool_calls)
#             messages.extend(result)
#             response = client.chat.completions.create(model="gpt-5.4-nano",messages=messages,tools=tools, stream=True) 
#         return chunk.choices[0].delta.content        
        
        
if __name__ == "__main__":
    gr.ChatInterface(
        chat,
        examples=EXAMPLES,
        title="Vijay's Digital Twin",
        description="Talk to my AI twin about my career",
        chatbot=gr.Chatbot(show_label=False),
    ).launch(css=CSS, js=JS, theme=themes.Ocean(), server_name=server_name, server_port=int(server_port), inbrowser=True)
