# app.py - Fixed version for Google ADK v1.19.0
import os
import asyncio
import logging
from datetime import datetime
from dotenv import load_dotenv

# ADK imports - v1.19.0
from google.adk.apps import App
from google.adk.runners import InMemoryRunner
from google.adk.sessions import InMemorySessionService

# Import agents
from agents import greeter

load_dotenv()

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler(f'skillbridge_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

async def main():
    logger.info("🤖 SkillBridge Agent Starting...")
    logger.info("=" * 60)
    
    # Create app with ADK v1.19.0
    app = App(
        name="SkillBridgeApp",
        root_agent=greeter
    )
    
    # Create runner with the app - THIS IS THE KEY CHANGE
    runner = InMemoryRunner(app=app)
    
    # User input
    user_input = input("👤 Enter your request (or press Enter for demo): ").strip()
    
    if not user_input:
        user_input = "Hi, I want to pivot my career. My resume is test_resume.pdf and I want to be an AI Engineer."
        logger.info(f"📝 Using demo input: {user_input}")
    
    logger.info("🔄 Starting agent workflow...")
    logger.info("-" * 60)
    
    try:
        # Run the agent using Runner.run_debug() - ADK v1.19.0 method
        response = await runner.run_debug(user_input)
        
        logger.info("-" * 60)
        logger.info("✅ Workflow Finished Successfully!")
        logger.info(f"📊 Final Response:\n{response}")
        
        # Check if output file was created
        if os.path.exists("final_career_plan.txt"):
            with open("final_career_plan.txt", "r") as f:
                content = f.read()
            logger.info(f"📁 Output file created ({len(content)} characters)")
            logger.info("💾 Saved to: final_career_plan.txt")
            logger.info(f"\n📄 Preview:\n{content[:500]}...")
        
    except Exception as e:
        logger.error(f"❌ Error during execution: {str(e)}", exc_info=True)
        import traceback
        traceback.print_exc()
        raise
    
    logger.info("=" * 60)
    logger.info("🎉 SkillBridge session complete!")

if __name__ == "__main__":
    asyncio.run(main())