# mentor_agent.py
import os
import logging
from datetime import datetime, timezone
from uuid import uuid4
from dotenv import load_dotenv

from uagents import Agent, Context, Protocol
from uagents_core.contrib.protocols.chat import (
    ChatMessage,
    ChatAcknowledgement,
    TextContent,
    StartSessionContent,
    EndSessionContent,
    chat_protocol_spec,
)

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("mentor-agent")

# Create Mentor Agent
MENTOR = Agent(
    name="Mentor Agent (SkillSync)",
    seed=os.getenv("MENTOR_AGENT_SEED", "mentor_secret_seed_v1"),
    mailbox=True,  # ✅ Allows async communication
    publish_agent_details=True,
    port=8001,  # ✅ Different from career agent to avoid port conflict
    readme_path="README.md",
)

# Define chat protocol
chat_proto = Protocol(spec=chat_protocol_spec)

# Get career agent address from environment
CAREER_AGENT_ADDRESS = os.getenv("CAREER_AGENT_ADDRESS", "").strip()

# Keep track of the last sender (ASI user)
last_user_address = None


def create_text_chat(text: str, start_session: bool = False, end_session: bool = False) -> ChatMessage:
    """Create properly formatted chat messages for communication."""
    content = []
    if start_session:
        content.append(StartSessionContent(type="start-session"))
    content.append(TextContent(type="text", text=text))
    if end_session:
        content.append(EndSessionContent(type="end-session"))
    return ChatMessage(timestamp=datetime.now(timezone.utc), msg_id=uuid4(), content=content)


@MENTOR.on_event("startup")
async def on_startup(ctx: Context):
    """Triggered when the mentor agent starts."""
    ctx.logger.info(f"🚀 Mentor Agent started as {ctx.agent.address}")
    ctx.logger.info(
        f"🔍 Inspector: https://agentverse.ai/inspect/?uri=http%3A//127.0.0.1%3A8001&address={ctx.agent.address}"
    )

    if not CAREER_AGENT_ADDRESS:
        ctx.logger.warning("⚠️ CAREER_AGENT_ADDRESS not set in environment. Please check your .env file.")
        return

    # Send a demo question once on startup
    sample_question = "How can I become a data analyst?"
    ctx.logger.info(f"📨 Sending demo question to Career Agent {CAREER_AGENT_ADDRESS}: {sample_question}")
    await ctx.send(CAREER_AGENT_ADDRESS, create_text_chat(sample_question, start_session=True))


@chat_proto.on_message(ChatMessage)
async def on_chat(ctx: Context, sender: str, msg: ChatMessage):
    """Handles incoming chat messages and relays between ASI and Career Agent."""
    global last_user_address

    await ctx.send(sender, ChatAcknowledgement(timestamp=datetime.now(timezone.utc), acknowledged_msg_id=msg.msg_id))

    texts = [c.text for c in msg.content if isinstance(c, TextContent)]
    if not texts:
        return

    user_message = "\n".join(texts)
    ctx.logger.info(f"💬 Received from {sender}: {user_message}")

    # Prevent infinite loop: don't re-forward messages from the same source repeatedly
    if sender == CAREER_AGENT_ADDRESS:
        if last_user_address:
            ctx.logger.info("📤 Relaying Career Agent reply back to ASI user...")
            await ctx.send(last_user_address, create_text_chat(user_message))
        else:
            ctx.logger.warning("⚠️ No ASI user recorded yet to send reply to.")
        return

    # Otherwise, message came from ASI — forward to Career Agent
    if sender != CAREER_AGENT_ADDRESS:
        last_user_address = sender  # Remember ASI user
        ctx.logger.info(f"🔁 Forwarding message to Career Agent ({CAREER_AGENT_ADDRESS})...")
        await ctx.send(CAREER_AGENT_ADDRESS, create_text_chat(user_message))


@chat_proto.on_message(ChatAcknowledgement)
async def on_ack(ctx: Context, sender: str, msg: ChatAcknowledgement):
    """Handles message acknowledgements."""
    ctx.logger.debug(f"✅ Acknowledgement received from {sender} for message ID: {msg.acknowledged_msg_id}")


# Include the chat protocol
MENTOR.include(chat_proto, publish_manifest=True)

# Run the agent
if __name__ == "__main__":
    MENTOR.run()
