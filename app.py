import streamlit as st
import openai
import json

with st.expander("About CocktailGPT"):
    st.markdown("""
CocktailGPT is an app I built that allows you
to ask ChatGPT for a cocktail recipe. 

There are 3 ways to find a cocktail:
* by name - just enter a name of a cocktail
* by ingredients - choose ingredients to include and/or exclude
* by freeform text - describe what you are looking for
""")

openai.api_key = st.secrets["OPENAI_KEY"]

def get_via_openai(input):
    data = {
                "model": "text-davinci-003",
                "prompt": input + '. Your answer should be in ounces. Your answer should be in valid JSON format for Python. For example: {"name": "My Cocktail", "description": "This is a nice cocktail for a cold day", "ingredients": [ {"ingredient": "Bourbon whiskey", "amount": "2 ounces"}, {"ingredient": "Sweet vermouth", "amount": "1 ounce"}, {"ingredient": "Angostura bitters", "amount": "2 dashes"}], "instructions": "Combine all ingredients in a mixing glass with ice. Stir until chilled. Strain into glass", "glass": "Coupe glass", "garnish": "Maraschino cherry", "suggestions": "You can also use Rye instead of Bourbon." }',
                "max_tokens": 256,
                "temperature": 0.10,
                "n": 1
            }
    ai_resp = openai.Completion.create(**data)
    return ai_resp

def show_recipe(rj):
    st.markdown(f'## :blue[{rj["name"]}]')
    st.markdown(f':blue[**Description**]: {rj["description"]}')
    st.markdown(f'### Ingredients')
    for ii in rj["ingredients"]:
        st.markdown(f'* :blue[**{ii["ingredient"]}**]: {ii["amount"]}')
    st.markdown(f'### Instructions')
    st.markdown(f'{rj["instructions"]}')
    st.markdown(f':blue[**Glass**]: {rj["glass"]}')
    st.markdown(f':blue[**Garnish**]: {rj["garnish"]}')
    st.markdown(f':blue[**Suggestions**]: {rj["suggestions"]}')
    
ingredients = ['Sugar syrup',
'Lime juice',
'Lemon juice',
'London dry gin',
'Vodka',
'Light white rum',
'Angostura Aromatic Bitters',
'Orange juice',
'Triple sec liqueur',
'Dry vermouth',
'Cognac V',
'Pineapple juice',
'Sweet vermouth',
'Bourbon whiskey',
'Apple juice',
'Pomegranate (grenadine) syrup',
'Tequila (reposado)',
'Egg white',
'Orange bitters',
'Cranberry juice (red)',
'Grand Marnier liqueur',
'Soda (club soda)',
'Cream',
'Maraschino liqueur',
'Blended Scotch whisky',
'Fresh mint leaves/sprigs',
'Brut champagne',
'Grapefruit juice (pink)',
'Elderflower liqueur',
'Absinthe',
'Apricot brandy liqueur',
'Coffee liqueur',
'Campari Bitter',
'Calvados apple brandy',
'Amaretto liqueur',
'Milk',
'Black raspberry liqueur',
'Runny honey',
'Bénédictine D',
'White crème de cacao liqueur',
"Peychaud's aromatic bitters",
'Aged rum (+7 year old)',
'Citrus flavoured vodka',
'Chartreuse Vert (green)',
'Cherry brandy liqueur',
'Irish cream liqueur',
'Almond (orgeat) syrup',
'Cachaça',
'Lime cordial',
'Raspberries (fresh)',
'Golden rum',
'Ginger ale',
'Crème de cassis',
'Melon liqueur (green)',
"Galliano L'Autentico liqueur",
'Blue curaçao liqueur',
'Drambuie liqueur',
'Vanilla infused vodka',
'Straight rye whiskey',
'Hazelnut liqueur',
'Żubrówka bison grass vodka',
'Fino sherry',
'Maple syrup',
'Islay single malt Scotch whisky',
'Agave syrup',
'Chartreuse Jaune (yellow)',
'Peach Schnapps liqueur',
'Crème de banane liqueur',
'Port wine',
'White wine (Sauvignon Blanc)',
'Pisco',
'Apple schnapps liqueur',
'Ginger beer',
'Falernum liqueur',
'Lemonade/Sprite/7-Up',
'Coconut rum liqueur',
'White crème de menthe',
'Ginger liqueur',
'Southern Comfort liqueur',
'Dark crème de cacao liqueur',
'Basil leaves',
'Dubonnet Red',
'Passion fruit syrup',
'Jenever',
'Vodka raspberry flavoured',
'Sake',
'Overproof rum (white)',
'Strawberries (fresh)',
'Ginger (fresh root)',
'Navy rum',
'Prosecco sparkling wine',
'Vanilla sugar syrup',
'Passion fruit (fresh)',
'Lillet Blanc',
'Honey sugar syrup',
'Espresso coffee (freshly made)',
'Black pepper',
'Tonic water',
'Anise liqueur',
'Crème de framboise liqueur'
]

prompts = ["Show me a cocktail named", "Show me a cocktail including/excluding", "Show me a cocktail (freeform)"] 
prompt = st.selectbox("What sort of cocktail", options=prompts, index=0)

input = ""
if (prompt == "Show me a cocktail named"):
    name = st.text_input("Show me a cocktail named")
    if (len(name) > 0):
        input = f'Show me a cocktail named {name}'

if (prompt == "Show me a cocktail including/excluding"):
    including = st.multiselect("Include these ingredients", options=ingredients)
    excluding = st.multiselect("Exclude these ingredients", options=ingredients)
    if (len(including)>0):
        input = f"Show me a cocktail including {','.join(including)} and other ingredients"
        if (len(excluding)>0):
            input = input + f" but does not include {','.join(excluding)}"
    else:
        if (len(excluding)>0):
            input = f"Show me a cocktail which does not include {','.join(excluding)}"

if (prompt == "Show me a cocktail (freeform)"):
    freetext = st.text_input("Fill in the blank: Shoe me a cocktail ____")
    if (len(freetext)>0):
        input = f"Show me a cocktail {freetext}"

if (len(input) > 0):
    rec = get_via_openai(input)
    st.sidebar.json(rec["choices"])
    recch = rec["choices"][0]
    choices = json.loads(recch["text"])
    if (type(choices) != "list"):
        choices = [choices]
    for ch in choices:
        show_recipe(ch)

