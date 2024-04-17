import streamlit as st 
import google.generativeai as genai

st.title("Your Data Science Tutor")
st.header("I am powered by Google's gemini-1.5-pro-latest")

#reading the api key 
f=open(r"D:\edu\INNO\Internship_LLM\keys\gemini_key.txt")
key=f.read() 

#configure the api key
genai.configure(api_key=key) 

##Initialize the gemini model 
model=genai.GenerativeModel(model_name="gemini-1.5-pro-latest",
                            system_instruction="You are a helpful Data Science Teaching Assistance .You give explanation about the given data science topic.If the topic is not related to data science then reply politely that you only help with data science topic")


#If there is no chat history in sesion then initialize one
if "chat_history" not in st.session_state:
    st.session_state["chat_history"]=[]  

#initializing the chat object 
chat=model.start_chat(history=st.session_state["chat_history"])


for msg in chat.history:
    st.chat_message(msg.role).write(msg.parts[0].text)

user_prompt=st.chat_input() 

if user_prompt: 
    st.chat_message("user").write(user_prompt) 
    response=chat.send_message(user_prompt) 
    st.chat_message("ai").write(response.text)
    st.session_state["chat_history"]=chat.history 