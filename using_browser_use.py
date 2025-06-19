import asyncio
import os
from browser_use import BrowserSession, Agent
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

async def main():
    load_dotenv()
    
    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key:
        raise ValueError("GOOGLE_API_KEY not found in environment variables. Please add it to your .env file.")
    
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        temperature=0.1,
        google_api_key=os.environ.get('GOOGLE_API_KEY')
    )
    
    browser_session = BrowserSession(keep_alive=True)
    
    await browser_session.start()
    
    try:
        task = "Go to amazon.in, search for 'laptops', sort by best sellers and add the first item to the cart."
        
        agent = Agent(
            task=task,
            llm=llm,
            browser_session=browser_session
        )
        
        result = await agent.run()
        print(f"Task completed: {result}")
        
    finally:
        await browser_session.close()

if __name__ == "__main__":
    asyncio.run(main())