import pathlib
import textwrap
import os
import google.generativeai as genai
from dotenv import load_dotenv

from IPython.display import display
from IPython.display import Markdown

load_dotenv()


def to_markdown(text):
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
if not GOOGLE_API_KEY:
  raise ValueError('GOOGLE_API_KEY environment variable is not set')

genai.configure(api_key=GOOGLE_API_KEY)

# tells the user which models are available
# for m in genai.list_models():
#   if 'generateContent' in m.supported_generation_methods:
#     print(m.name)

model = genai.GenerativeModel('gemini-pro')
chat = model.start_chat(history=[])

response = model.generate_content("i meant the previous question")
# to_markdown(response.text)
print(response.text)
print("PRINTING CHAT HISTORY: ")
print(chat.history)