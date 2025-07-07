from browser_use import Agent
from dotenv import load_dotenv
from langchain_groq import ChatGroq
import asyncio

load_dotenv()


async def main():
    # task = input("Enter a task: ")
    agent = Agent(
        task = "open skillrack.com and login with 2217009@nec and password MahRooz@17102004",
        llm = ChatGroq(model="llama-3.3-70b-versatile"),
    )
    await agent.run()

asyncio.run(main())