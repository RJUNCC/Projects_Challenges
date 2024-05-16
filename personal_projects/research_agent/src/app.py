import os
import requests
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain import PromptTemplate
from langchain.chains.summarize import load_summarize_chain
from bs4 import BeautifulSoup
from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv
import json
from autogen import config_list_from_json
from autogen.agentchat.contrib.gpt_assistant_agent import GPTAssistantAgent
from autogen import UserProxyAgent
import autogen
from apify_client import ApifyClient
import streamlit as st


load_dotenv()
browserless_api_key = os.getenv("BROWSERLESS_API_KEY")
apify_api_key = os.getenv("APIFY_API_KEY")
serper_api_key = os.getenv("SERP_API_KEY")
airtable_api_key = os.getenv("AIRTABLE_API_KEY")
config_list = config_list_from_json("OAI_CONFIG_LIST.json", "../")

# Initialize the ApifyClient with your API token

client = ApifyClient(apify_api_key)


# Prepare the Actor input
def init_apify():
    # Prepare the Actor input

    run_input = {

        "runMode": "DEVELOPMENT",

        "startUrls": [{ "url": "https://crawlee.dev" }],

        "keepUrlFragments": False,

        "linkSelector": "a[href]",

        "globs": [{ "glob": "https://crawlee.dev/*/*" }],

        "pseudoUrls": [],

        "excludes": [{ "glob": "/**/*.{png,jpg,jpeg,pdf}" }],

        "pageFunction": """// The function accepts a single argument: the \"context\" object.

        // For a complete list of its properties and functions,

        // see https://apify.com/apify/web-scraper#page-function 

        async function pageFunction(context) {

            // This statement works as a breakpoint when you're trying to debug your code. Works only with Run mode: DEVELOPMENT!

            // debugger; 


            // jQuery is handy for finding DOM elements and extracting data from them.

            // To use it, make sure to enable the \"Inject jQuery\" option.

            const $ = context.jQuery;

            const pageTitle = $('title').first().text();

            const h1 = $('h1').first().text();

            const first_h2 = $('h2').first().text();

            const random_text_from_the_page = $('p').first().text();



            // Print some information to actor log

            context.log.info(`URL: ${context.request.url}, TITLE: ${pageTitle}`);


            // Manually add a new page to the queue for scraping.

        await context.enqueueRequest({ url: 'http://www.example.com' });


            // Return an object with the data extracted from the page.

            // It will be stored to the resulting dataset.

            return {

                url: context.request.url,

                pageTitle,

                h1,

                first_h2,

                random_text_from_the_page

            };

        }""",
        "injectJQuery": True,

        "proxyConfiguration": { "useApifyProxy": True },

        "proxyRotation": "RECOMMENDED",

        "initialCookies": [],

        "useChrome": False,

        "headless": True,

        "ignoreSslErrors": False,

        "ignoreCorsAndCsp": False,

        "downloadMedia": True,

        "downloadCss": True,

        "maxRequestRetries": 3,

        "maxPagesPerCrawl": 0,

        "maxResultsPerCrawl": 0,
    
        "maxCrawlingDepth": 0,

        "maxConcurrency": 50,

        "pageLoadTimeoutSecs": 60,

        "pageFunctionTimeoutSecs": 60,

        "waitUntil": ["networkidle2"],

        "preNavigationHooks": """// We need to return array of (possibly async) functions here.

        // The functions accept two arguments: the \"crawlingContext\" object

        // and \"gotoOptions\".

        [

            async (crawlingContext, gotoOptions) => {

                // ...

            },

        ]

        """,
        "postNavigationHooks": """// We need to return array of (possibly async) functions here.

        // The functions accept a single argument: the \"crawlingContext\" object.

        [

            async (crawlingContext) => {

                // ...

            },

        ]""",
        "breakpointLocation": "NONE",

        "closeCookieModals": False,

        "maxScrollHeightPixels": 5000,

        "debugLog": False,

        "browserLog": False,

        "customData": {},

        }
    
    # Run the Actor and wait for it to finish

    run = client.actor("moJRLRc85AitArpNN").call(run_input=run_input)

    # Fetch and print Actor results from the run's dataset (if there are any)

    for item in client.dataset(run["defaultDatasetId"]).iterate_items():

        print(item)

# ------------------ Create functions ------------------ #

# Function for google search
def google_search(search_keyword):    
    url = "https://google.serper.dev/search"

    payload = json.dumps({
        "q": search_keyword
    })

    headers = {
        'X-API-KEY': serper_api_key,
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    print("RESPONSE:", response.text)
    return response.text

# Function for scraping
def summary(objective, content):
    llm = ChatOpenAI(temperature = 0, model = "gpt-3.5-turbo-16k-0613")

    text_splitter = RecursiveCharacterTextSplitter(separators=["\n\n", "\n"], chunk_size = 10000, chunk_overlap=500)
    docs = text_splitter.create_documents([content])
    
    map_prompt = """
    Write a summary of the following text for {objective}:
    "{text}"
    SUMMARY:
    """
    map_prompt_template = PromptTemplate(template=map_prompt, input_variables=["text", "objective"])
    
    summary_chain = load_summarize_chain(
        llm=llm, 
        chain_type='map_reduce',
        map_prompt = map_prompt_template,
        combine_prompt = map_prompt_template,
        verbose = False
    )

    output = summary_chain.run(input_documents=docs, objective=objective)

    return output

def web_scraping(objective: str, url: str):
    #scrape website, and also will summarize the content based on objective if the content is too large
    #objective is the original objective & task that user give to the agent, url is the url of the website to be scraped

    print("Scraping website...")
    # Define the headers for the request
    headers = {
        'Cache-Control': 'no-cache',
        'Content-Type': 'application/json',
    }

    # Define the data to be sent in the request
    data = {
        "url": url        
    }

    # Convert Python object to JSON string
    data_json = json.dumps(data)

    # Send the POST request
    response = requests.post(f"https://api.apify.com/v2/acts/apify~web-scraper/runs?token={apify_api_key}", headers=headers, data=data_json)
    
    # Check the response status code
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        text = soup.get_text()
        print("CONTENTTTTTT:", text)
        if len(text) > 10000:
            output = summary(objective,text)
            return output
        else:
            return text
    else:
        print(f"HTTP request failed with status code {response.status_code}")         


# Function for get airtable records
def get_airtable_records(base_id, table_id):
    url = f"https://api.airtable.com/v0/{base_id}/{table_id}"

    headers = {
        'Authorization': f'Bearer {airtable_api_key}',
    }

    response = requests.request("GET", url, headers=headers)
    data = response.json()
    print(data)
    return data


# Function for update airtable records

def update_single_airtable_record(base_id, table_id, id, fields):
    url = f"https://api.airtable.com/v0/{base_id}/{table_id}"

    headers = {
        'Authorization': f'Bearer {airtable_api_key}',
        "Content-Type": "application/json"
    }

    data = {
        "records": [{
            "id": id,
            "fields": fields
        }]
    }

    response = requests.patch(url, headers=headers, data=json.dumps(data))
    data = response.json()
    return data


# ------------------ Create agent ------------------ #

# Create user proxy agent
user_proxy = UserProxyAgent(name="user_proxy",
    is_termination_msg=lambda msg: "TERMINATE" in msg["content"],
    human_input_mode="ALWAYS",
    max_consecutive_auto_reply=1,
    description="User proxy agent"
    )

# Create researcher agent
researcher = GPTAssistantAgent(
    name = "researcher",
    llm_config = {
        "config_list": config_list,
        "assistant_id": "asst_VgUt7B3waJ9iQrg7UX0HHjTq"
    },
    description="Researcher agent"
)

researcher.register_function(
    function_map={
        "web_scraping": web_scraping,
        "google_search": google_search
    }
)

# Create research manager agent
research_manager = GPTAssistantAgent(
    name="research_manager",
    llm_config = {
        "config_list": config_list,
        "assistant_id": "asst_eFXSOip3LEWNRGg5AwkE39Iw"
    },
    description="Research manager agent"
)


# Create director agent
director = GPTAssistantAgent(
    name = "director",
    llm_config = {
        "config_list": config_list,
        "assistant_id": "asst_nY8mKItVmN688xIj4IFvh5PU",
    },
    description="Director agent"
)

director.register_function(
    function_map={
        "get_airtable_records": get_airtable_records,
        "update_single_airtable_record": update_single_airtable_record
    }
)


# Create group chat
groupchat = autogen.GroupChat(agents=[user_proxy, researcher, research_manager, director], messages=[], max_round=15)
group_chat_manager = autogen.GroupChatManager(groupchat=groupchat, llm_config={"config_list": config_list})


# ------------------ start conversation ------------------ #
# st.title("Research Assistant")
# message = st.text_input("Enter message for chat assistant:")
# if st.button("Submit Message"):
#     st.markdown(user_proxy.initiate_chat(group_chat_manager, message=message))
message = "Research me some YouTube video ideas about Data Science, Music, or Statistics."
user_proxy.initiate_chat(group_chat_manager, message=message)