from openai import OpenAI
import streamlit as st 

##Read the api key and setup an open ai clent
f=open(r"D:\edu\INNO\Internship_LLM\code_reviewer_app\keys\key_1_kanav_bansal.txt") 
key=f.read()
client=OpenAI(api_key=key)

st.title("Code Scanner")
st.header("Web App powered by AI To Review your Code") 

## Taking Users input
prompt=st.text_input("Enter Your Code Here :") 

##If the button is clicked generate responses
if st.button("Generate")==True:
    response = client.chat.completions.create(
      model="gpt-3.5-turbo-1106",
      messages=[
        {"role": "system", "content": "You are an AI aaaistant.You generate bugs in the given code and also generate the fixed code after that"},
        {"role": "user", "content":prompt}])
##printing the response on the webapp
    st.write(response.choices[0].message.content)