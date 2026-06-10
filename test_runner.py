
import asyncio

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai.types import Content, Part

from agent import root_agent


APP_NAME = "ai_mentor_app"
USER_ID = "anand"
SESSION_ID = "session_001"


async def run_agent():

    # Create session service
    session_service = InMemorySessionService()

    # Create session
    await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID,
    )

    # Create runner
    runner = Runner(
        agent=root_agent,
        app_name=APP_NAME,
        session_service=session_service,
    )

    # User message
    user_message = Content(
        role="user",
        parts=[
            Part(text="How can I become an AI engineer?")
        ],
    )

    print("User: How can I become an AI engineer?\n")
    print("Agent: ", end="")

    async for event in runner.run_async(
        user_id=USER_ID,
        session_id=SESSION_ID,
        new_message=user_message,
    ):
        if (
            event.is_final_response()
            and event.content
            and event.content.parts
        ):
            print(event.content.parts[0].text)


if __name__ == "__main__":
    asyncio.run(run_agent())