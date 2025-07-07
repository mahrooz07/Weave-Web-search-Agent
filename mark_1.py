

# # Define your web search agent
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
#     ],
#     model=Groq(id="llama-3.3-70b-versatile"),
#     tools=[DuckDuckGo()],
#     show_tool_calls=True,
#     markdown=True,
# )

from flask import Flask, request, jsonify
from flask_cors import CORS
from phi.agent import Agent
from phi.model.groq import Groq
from phi.tools.duckduckgo import DuckDuckGo
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

CORS(app)  # Enable CORS for all routes

# Define your web search agent
websearch_agent = Agent(
    instructions=[
        "Fetch the latest and most relevant information from the internet.",
        "Provide the source link along with the article summary, and include any related images or videos.",
        "If you don't know the answer, say 'I don't know'.",
        "Format your response in proper markdown.",
        "For sources, use the format: **Source**: [Title](URL)",
        "For images, use the format: ![Description](image_url)",
        "For videos, use the format: [Video: Title](video_url)",
        "Search content from the top ranked results from the search engine.",
        "Use markdown tables if needed.",
        "Use markdown headers (## and ###) for section organization.",
    ],
    model=Groq(id="llama-3.3-70b-versatile"),
    tools=[DuckDuckGo()],
    show_tool_calls=True,
    markdown=True,
)

def get_agent_response(agent, query):
    # Get the response directly from the agent
    response = agent.run(query)
    
    # Return the markdown content
    return response.content

@app.route('/mr', methods=['POST'])
def search():
    data = request.get_json()
    query = data.get('query')
    
    if not query:
        return jsonify({"error": "No query provided"}), 400
    
    # Get the response directly
    markdown_content = get_agent_response(websearch_agent, query)
    
    return jsonify({"response": markdown_content})

if __name__ == '__main__':
    app.run(debug=True)

    
