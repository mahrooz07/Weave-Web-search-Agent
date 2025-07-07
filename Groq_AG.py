# from phi.agent import Agent
# from phi.model.groq import Groq
# from phi.tools.duckduckgo import DuckDuckGo

# from phi.tools.crawl4ai_tools import Crawl4aiTools



# from dotenv import load_dotenv


# load_dotenv()

# websearch_agent = Agent(
#     instructions=[
#         "Fetch the latest and most relevant information from the internet.",
#         "Provide the source link along with the article summary, and include any related images or videos.",
#         "If you don't know the answer, say 'I don't know'.",
#         "The Data should be in the following format: [Source: <source_name>, Link: <link>, Data: <data>]",
#         "Provide Images if possible.",
#         "Provide Video Links if possible.",
#         "Provide image in the following format: [Image: <image_link>]",
#         "Search content from the top ranked results from the search engine.",
#         "Use tables if needed.",
#         ],
#     model=Groq(id="llama-3.3-70b-versatile"),
#     tools = [DuckDuckGo()],
#     show_tool_calls=True,
#     markdown=True
# )

# # websearch_agent.print_response("What is the latest news about the Ukraine-Russia war?")

# # webcrawl_agent = Agent(
# #     instructions=[
# #         "Crawl and retrieve any 1 Link",
# #         "Collect the latest updates from news sites, social media, and blogs across various categories.",
# #         "Gather recent content from diverse sources like news websites, academic articles, and industry reports.",
# #         "Crawl multiple websites to gather data on various topics, including articles, product reviews, market trends, and user opinions.",
# #         "Search for a wide range of information, including updates on ongoing events, popular trends, and expert analyses."
# #     ],  

# #     model=Groq(id="llama-3.3-70b-versatile"),
# #     tools = [Crawl4aiTools()],
# #     show_tool_calls=True,
# #     markdown= True
# # )

# # agent_team = Agent(
# #     team = [websearch_agent, webcrawl_agent],
# #     model=Groq(id="llama-3.3-70b-versatile"),
# #     show_tool_calls=True,
# #     markdown=True
# # )

# query = input("Enter your query: ")
# websearch_agent.print_response(query, stream=True)


import requests
from bs4 import BeautifulSoup
from phi.agent import Agent
from phi.model.groq import Groq
from phi.tools.duckduckgo import DuckDuckGo
from phi.tools.crawl4ai_tools import Crawl4aiTools
from dotenv import load_dotenv

load_dotenv()

# Define your web search agent
websearch_agent = Agent(
    instructions=[
        "Fetch the latest and most relevant information from the internet.",
        "Provide the source link along with the article summary, and include any related images or videos.",
        "If you don't know the answer, say 'I don't know'.",
        "The Data should be in the following format: [Source: <source_name>, Link: <link>, Data: <data>]",
        "Provide Images if possible.",
        "Provide Video Links if possible.",
        "Provide image in the following format: [Image: <image_link>]",
        "Search content from the top ranked results from the search engine.",
        "Use tables if needed.",
    ],
    model=Groq(id="llama-3.3-70b-versatile"),
    tools=[DuckDuckGo()],
    show_tool_calls=True,
    markdown=True,
)

# Prompt the user for a query and fetch results
query = input("Enter your query: ")
# Fetch the response from the web search agent
response = websearch_agent.print_response(query, stream=True)


