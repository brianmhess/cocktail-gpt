import streamlit as st
import openai
import json

st.markdown("## CocktailGPT")

openai.api_key = st.secrets["OPENAI_KEY"]

def get_via_openai_named(name):
    data = {
                "model": "text-davinci-003",
                "prompt": 'Show me a recipe in ounces for a cocktail named ' + name + '. Your answer should be in valid JSON format for Python. For example: {"name": "My Cocktail", "description": "This is a nice cocktail for a cold day", "ingredients": [ {"ingredient": "Bourbon whiskey", "amount": "2 ounces"}, {"ingredient": "Sweet vermouth", "amount": "1 ounce"}, {"ingredient": "Angostura bitters", "amount": "2 dashes"}], "instructions": "Combine all ingredients in a mixing glass with ice. Stir until chilled. Strain into glass", "glass": "Coupe glass", "garnish": "Maraschino cherry", "suggestions": "You can also use Rye instead of Bourbon." }',
                "max_tokens": 256,
                "temperature": 0.10,
                "n": 1
            }
    ai_resp = openai.Completion.create(**data)
    return ai_resp

def show_recipe(rstr):
    rj = json.loads(rstr)
    st.markdown(f'## {rj["name"]}')
    st.markdown(f'Description: {rj["description"]}')

name = st.text_input("Show me a cocktail named")

if (len(name) > 0):
    rec = get_via_openai_named(name)
    for ch in rec["choices"]:
        show_recipe(ch["text"])
