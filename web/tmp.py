from json import JSONDecodeError
import streamlit as st
import requests
from PIL import Image
import spacy
#import contextualSpellCheck
import pickle as pkl
import SessionState
import pandas as pd
import altair as alt

# Function to parse Azure Search results and grab speel checked claim

def spell_check(claim,response):

    for flagged_token in response['flaggedTokens']:

        claim = claim.replace(flagged_token['token'],flagged_token['suggestions'][0]['suggestion'])

    return claim


@st.cache(allow_output_mutation=True)
def load_model():
    nlp = spacy.load("en_core_web_md")
#
#    nlp.add_pipe("contextual spellchecker")
#
    return nlp

# Azure Bing-Search API Key. TODO: Read from config file, env variable or something else secure.
key = "21c5ba248b464781bba8d4cd5118e303"

# Params for Bing-Search API request
params = {
    'mkt':'en-us',
    'count': 1,
    'offset': 0,
    }

headers = {
    'Ocp-Apim-Subscription-Key': key,
    }

# Quick CSS hack to hide Streamlit's nav bar
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Generate App Sidebar
image = Image.open('logo-factually-health-dark-1006x194.jpg')
st.sidebar.image(image,
                 use_column_width=True)

#with st.sidebar.beta_expander("NAVIGATING SEARCH RESULTS"):
#    st.markdown("- **Select how you want to sort results.** The options are publication year (from most recent to least recent) or our experimental proprietary relevance score.")
#    st.markdown("- **Click on the article title** to see the original document")
#    st.markdown("- **Sentences on the bullet points:** These are the excerpts from the article, that our algorithm found to be the most relevant to your query")
#    st.markdown("- **Maximum of 10 most relevant sentences** returned per article")

st.title("Factually Health: Research-Helper")

#st.markdown("**Database:** PubMed")
#st.markdown("**Database size:** 5,336 articles on **AoPelvic Floor Dysfunction**")
#st.markdown("**Search scope:**: publication titles and abstracts")


# Generate Body of the App

type_info = "Individual claims"

input_header = "Type your query here:"

input_value = "Men cannot have breast cancer" # Placeholder query text. TODO: Read from config file to make this app agnostic to Topic (or disease)

url = "http://localhost:5000/square/"


claim = st.text_input(input_header, value=input_value)

# Initialize empty button. Use SessionState below to keep search results on-screen until user performs another search.

search_button = st.empty()


# SessionState is now part of the main Streamlit release. TODO: replace local SessionState.py with package-native SessionState
ss = SessionState.get(search_button = False)

# Clicking "Search" sets the button's session state to true
if search_button.button("Search"):

    ss.search_button = True

# While in the same session state, render the below:
if ss.search_button:

    with st.spinner("Processing input..."):

        state = "good" # hardcoding good state. Triggers like bad spelling, or off-topic queries can set it to false.

    if state=="bad":

        st.write("This query does not seem to be about Breast Cancer, please try a diffferent query.") # TODO: read topic/disease from config file

     # The below is two sets of Triggers for a bad state: Multi-claim queries and bad spelling. Uncomment and adjust to activate.


        #if doc._.outcome_spellCheck:
        #    st.write("Please try again. Perhaps you mean " + '"' + doc._.outcome_spellCheck + '"' + "?")
        #    state = "bad"

        #if len(list(doc.sents)) > 1 or " but " in claim or ",but " in claim or ",yet " in claim or ", yet" in claim or ", and "  in claim  or ",and " in claim:

        #    st.write("Your input seems to contain multiple claims. Please verify one claim at a time.")
        #    state = "bad"
        #print("Processing...")

        #if True: #else:

            #params['q'] = claim
            #response = requests.get("https://api.bing.microsoft.com/v7.0/search", headers=headers, params=params).json()


            #if 'alteredQuery' in response['queryContext']:

                #claim = spell_check(claim.lower(),response)

               # claim = response['queryContext']['alteredQuery']

                #st.write(f'Did you mean "{claim}" ?')

                #state = "bad"
            #print("Processing...")


    if state=="good":

        with st.spinner("Scanning Factually Health Database. This might take a few minutes..."):

            topic = 1 # Leaving this here due to an earlier version of the backend that needed this. TODO: Get rid of it on the backend.

            payload = {'number' : claim, 'topic': topic}

            try:
                response = requests.post(url, data=payload).json()
            except JSONDecodeError:
                response = []

            result_string = "Done!"

            #st.markdown(result_string, unsafe_allow_html=True)

            #sort_type = st.sidebar.radio("Sort results by:",('Relevance','Publication Year'), index=1)

            #sort_key = 'pub_year' if sort_type == "Publication Year" else "pertinence_score"
            sort_key = "pertinence_score"
            used_titles = []

            all_responses = [article for model in response for article in response[model]]

            #pub_types_available = list(set([pub_type for output in all_responses for pub_type in output['pub_type']]))
            pub_types_available = []

            #options = st.sidebar.multiselect('Filter by Publication Type:',pub_types_available)

            i = 0

            #responses = list(filter(lambda x: True if [pub_type for pub_type in x['pub_type'] if pub_type in options] else False, all_responses)) if options else all_responses

            #pub_types_filtered = [pub_type for output in responses for pub_type in output['pub_type']]
            pub_types_filtered = []

            # This section contains the code that generates the interactive chart

            #pub_type_distro = pd.DataFrame({'Publication Type' : [pub_type for pub_type in pub_types_available], 'Articles' : [pub_types_filtered.count(pub_type) for pub_type in pub_types_available]})

            #chart = alt.Chart(pub_type_distro).mark_bar().encode(x=alt.X('Articles',axis=alt.Axis(labels=False)),y=alt.Y('Publication Type',axis=alt.Axis(labels=True,title="")),tooltip=['Publication Type','Articles']).interactive()

            #st.sidebar.altair_chart(chart, use_container_width=True)

            # Search Results start here:

            st.subheader(f"Our AIs have found {len(set([x['title'] for x in all_responses]))} papers in our Database about this subject:" )
            sorted_model = sorted(all_responses, key=lambda x: int(x[sort_key] if 'pub_year' in x else 0), reverse=True)

            for outputs in sorted_model:

                if outputs["title"] not in used_titles:

                    i += 1

                    #if "pub_year" in outputs:
                    #    md = f'**{i}:** [{outputs["title"]}]({outputs["url"]}) ({outputs["pub_year"]})'
                    #else:
                    md = f'**{i}:** [{outputs["title"]}]({outputs["url"]})'
                    #st.write(outputs['authors'])

                    if "id" in outputs:
                        md_id = f"**ID**: {outputs['id']}"
                    else:
                        md_id = ""
                    if "authors" in outputs:
                        md_aut = f"**Authors:** {' | '.join([author for author in outputs['authors']])} "
                    else:
                        md_aut = ""

                    md2 = "<ul>" + " ".join([f"<li>{evidence}</li>" for evidence in outputs['evidence']]) + "</ul>"

                    #md3 = f'\n\n[see papers that cite this paper](#)\n\n [see papers cited in this paper](#)\n\n [see more by the same authors](#)'

                    st.markdown(md,unsafe_allow_html=True)
                    st.markdown(md_id)
                    #st.markdown(md_aut)
                    st.markdown(md2, unsafe_allow_html = True)
                    #st.markdown(md3)
                    st.markdown("---")

                    used_titles.append(outputs["title"])
