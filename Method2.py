import subprocess
import json
import os

ChatHistory = []
AI_MODEL = "tinydolphin"

def SendMSG(MSGtoSend):

    # Make sure users message doesn't have any characters that will cause errors
    MSGtoSend = MSGtoSend.replace("'","")
    MSGtoSend = MSGtoSend.replace("`","")
    MSGtoSend = MSGtoSend.replace('"',"")

    # Add the users message to the Chat History List
    ChatHistory.append(
        {
            'role':'user',
            'content':MSGtoSend,
        }
    )

    # We Need to convert the history list into a string before sending to the AI
    HistoryString = str(ChatHistory)
    HistoryString = HistoryString.replace("'",'"')

    # Send the message to the AI
    response = subprocess.check_output("""curl http://localhost:11434/api/chat -d '{"model": "%s","messages":%s }""" % (AI_MODEL, HistoryString))

    # parse the response
    response = response.decode("utf-8")
    response = response.splitlines()

    # Load the response into a string
    sentence = ""
    for res in response:
        try:
            res = json.loads(res)
            sentence += res['message']['content']
        except:
            print("ERROR: ")
            print(res)
            sentence = "Sorry, there was an error with the AI. Try again."

    # Make sure AI response doesn't have any characters that will cause errors
    sentence = sentence.replace("'","")
    sentence = sentence.replace("`","")
    sentence = sentence.replace('"',"")

    # Add the ais response to the chat history
    response = sentence
    ChatHistory.append(
        {
            'role':'assistant',
            'content':response,
        }
    )

    # Return the sentence
    return sentence


# The main chat loop
while True:
    message = input(">> ")
    if message == "/exit":
        os.system("taskkill /F /IM ollama_llama_server.exe")
        os.system('taskkill /F /IM "ollama app.exe"')
        os.system("taskkill /F /IM ollama.exe")
        break
    elif len(message) > 0:
        print(SendMSG(message))
    

