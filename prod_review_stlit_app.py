# for running the program, use python -m streamlit run prod_review_stlit_app.py in the terminal
import os
import pandas as pd
import streamlit as st
import openai
import requests
from tqdm import tqdm
import time
# import docx

#load_dotenv() is a function that loads variables from a .env file into environment variables in a Python script. 
#It allows you to store sensitive information or configuration settings separate from your code
#and access them within your application.

from dotenv import load_dotenv
load_dotenv()

# Set up the OpenAI API
openai.api_key = os.environ["OPENAI_API_KEY"]
GPT_API_URL = "https://api.openai.com/v1/chat/completions"

#By using st.set_page_config(), you can customize the appearance of your Streamlit application's web page
st.set_page_config(page_title="Product Review Analysis", page_icon=":robot:")
st.header("Hey, Input the product review & I will give out the summary and sentiment")

# input_file = "product_review_small_dataset.csv"
# df = pd.read_csv(input_file)
# print(df.head(1))

def summarize_review(review):
    retries = 3
    summary = None

    while retries > 0:
        messages = [
            {"role": "system", "content": "You are an AI language model trained to analyze and summarize the product reviews."},
            {"role": "user", "content": f"Summarize the following product review, highlighting top pros and cons with maximum 3 pros and 3 cons each. Summarize in bulletted form: {review}"}
        ]

        completion2 = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            # We want to limit the summary to about 75 words (which is around 100 openAI tokens). If you want longer review summaries, increase the max_tokens amount
            max_tokens=100,
            n=1,
            stop=None,
            temperature=0.8
        )

        response_text = completion2.choices[0].message.content
       # This is optional but it's nice to see how the reviews are being summarized to make sure something isn't wrong with the input file or API results 
        print(response_text)
        # This is our quality control check. If the API has an error and doesn't generate a summary, we will retry the review 3 times.
        if response_text:
            summary = response_text
            break
        else:
            retries -= 1
            time.sleep(1)
    else:
        summary = "Summary not available."

    retries = 3

    # add a delay of 20 seconds between requests to avoid hitting the openai free tier API call rate limit

    # time.sleep(20)

    return summary

# Keep only the first five rows in the dataframe
# df2 = df.head(5).copy()
# print(df2)
  
#Function to receive input from user and store it in a variable
def get_text():
    input_text = st.text_input("Input the product review text: ", key= input)
    return input_text


user_input=get_text()
submit = st.button('Analyze')  

if submit:
    #If the button is clicked, the below snippet will fetch us the summary & sentiment
    summary = summarize_review(user_input)
    
    st.subheader("Product Review Summary:")
#   
    st.text(summary)
   
# Save the results to a new Excel file
# output_file = "reviews_analyzed_full_summaries.xlsx"
# df2.to_excel(output_file, index=False)

# Save the results to a new Word file
# output_file = "reviews_analyzed_full_summaries.docx"
# vdoc = docx.Document()

# Add table with headers
# table = doc.add_table(rows=1, cols=2)
# header_cells = table.rows[0].cells
# header_cells[0].text = 'Product_Review'
# header_cells[1].text = 'Summary'

# Add table content
# for index, row in df2.iterrows():
#    row_cells = table.add_row().cells
#    row_cells[0].text = str(row['reviews.text'])
#    row_cells[1].text = row['summary']

# doc.save(output_file)
