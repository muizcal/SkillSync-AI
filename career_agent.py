# career_agent.py
import os
import re
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

# Load environment
load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("career-agent")

# Create agent
career_agent = Agent(
    name="Career Agent (SkillSync)",
    seed=os.getenv("CAREER_AGENT_SEED", "career_secret_seed_v1"),
    mailbox=True,
    publish_agent_details=True,
    readme_path="README.md",
)

chat_proto = Protocol(spec=chat_protocol_spec)

# Try MeTTa initialization (optional)
HAVE_METTA = False
metta_engine = None
METTA_FILE = "metta_kg.metta"
try:
    from hyperon import MeTTa
    metta_engine = MeTTa()
    if os.path.exists(METTA_FILE):
        with open(METTA_FILE, "r", encoding="utf-8") as f:
            program = f.read()
        try:
            metta_engine.run(program)
        except Exception:
            metta_engine.load(program)
    HAVE_METTA = True
    logger.info("✅ MeTTa engine initialized.")
except Exception:
    logger.info("ℹ️ MeTTa not available, using fallback mapping.")
    HAVE_METTA = False

# --- Expanded Fallback Career Knowledge Base ---
FALLBACK = {
    "data-analyst": {
        "skills": ["Python", "SQL", "Excel", "Pandas", "Power BI", "Tableau"],
        "resources": [
            "https://www.kaggle.com/learn/overview",
            "https://www.coursera.org/specializations/data-science",
            "https://www.coursera.org/professional-certificates/google-data-analytics",
        ],
    },
    "data-scientist": {
        "skills": ["Python", "SQL", "Machine Learning", "Deep Learning", "TensorFlow", "Statistics"],
        "resources": [
            "https://www.kaggle.com/learn/intro-to-machine-learning",
            "https://www.coursera.org/specializations/deep-learning",
            "https://www.deeplearning.ai/",
        ],
    },
    "ml-engineer": {
        "skills": ["Python", "Math", "TensorFlow", "PyTorch", "MLOps", "Model Deployment"],
        "resources": [
            "https://www.fast.ai/",
            "https://www.coursera.org/specializations/machine-learning",
        ],
    },
    "frontend-developer": {
        "skills": ["HTML", "CSS", "JavaScript", "React", "TailwindCSS", "Git"],
        "resources": [
            "https://frontendmasters.com/",
            "https://www.freecodecamp.org/",
            "https://scrimba.com/",
        ],
    },
    "backend-developer": {
        "skills": ["Python", "Node.js", "Databases", "REST APIs", "Docker", "Linux"],
        "resources": [
            "https://www.theodinproject.com/",
            "https://roadmap.sh/backend",
        ],
    },
    "fullstack-developer": {
        "skills": ["HTML", "CSS", "JavaScript", "React", "Node.js", "Databases", "Git", "DevOps"],
        "resources": [
            "https://www.freecodecamp.org/",
            "https://www.theodinproject.com/",
        ],
    },
    "ui-ux-designer": {
        "skills": ["Figma", "Design Thinking", "Wireframing", "Prototyping", "User Research"],
        "resources": [
            "https://www.coursera.org/professional-certificates/google-ux-design",
            "https://www.interaction-design.org/",
        ],
    },
    "blockchain-developer": {
        "skills": ["Solidity", "Rust", "Smart Contracts", "Web3.js", "Cryptography", "Ethereum"],
        "resources": [
            "https://cryptozombies.io/",
            "https://www.alchemy.com/university",
        ],
    },
    "cybersecurity-analyst": {
        "skills": ["Networking", "Linux", "Ethical Hacking", "SIEM Tools", "Incident Response"],
        "resources": [
            "https://tryhackme.com/",
            "https://www.coursera.org/professional-certificates/google-cybersecurity",
        ],
    },
    "product-manager": {
        "skills": ["Market Research", "Agile", "Leadership", "Roadmapping", "User Stories", "Communication"],
        "resources": [
            "https://www.coursera.org/specializations/product-management",
            "https://www.productschool.com/",
        ],
    },
    "digital-marketer": {
        "skills": ["SEO", "Google Ads", "Analytics", "Social Media Marketing", "Content Strategy"],
        "resources": [
            "https://learndigital.withgoogle.com/digitalunlocked",
            "https://www.coursera.org/specializations/digital-marketing",
        ],
    },
    "ai-engineer": {
        "skills": ["Python", "Machine Learning", "LLMs", "Vector Databases", "Prompt Engineering", "LangChain"],
        "resources": [
            "https://www.deeplearning.ai/",
            "https://www.coursera.org/specializations/machine-learning",
        ],
    },
    "cloud-engineer": {
        "skills": ["AWS", "Azure", "GCP", "Terraform", "Docker", "Kubernetes"],
        "resources": [
            "https://www.coursera.org/professional-certificates/aws-cloud-solutions-architect",
            "https://www.freecodecamp.org/learn/cloud/",
        ],
    },
    "devops-engineer": {
        "skills": ["CI/CD", "Docker", "Kubernetes", "Linux", "Jenkins", "Cloud Platforms"],
        "resources": [
            "https://roadmap.sh/devops",
            "https://www.udemy.com/course/docker-and-kubernetes-the-complete-guide/",
        ],
    },
    "mobile-developer": {
        "skills": ["Flutter", "React Native", "Kotlin", "Swift", "Firebase"],
        "resources": [
            "https://flutter.dev/learn",
            "https://reactnative.dev/docs/getting-started",
        ],
    },
    "graphic-designer": {
        "skills": ["Adobe Photoshop", "Illustrator", "Canva", "Typography", "Branding"],
        "resources": [
            "https://www.coursera.org/specializations/graphic-design",
            "https://www.skillshare.com/en/browse/graphic-design",
        ],
    },
    "project-manager": {
        "skills": ["Agile", "Scrum", "Risk Management", "Communication", "Leadership"],
        "resources": [
            "https://www.coursera.org/specializations/project-management",
            "https://www.pmi.org/certifications/project-management-pmp",
        ],
    },
    "game-developer": {
        "skills": ["Unity", "C#", "Game Physics", "3D Modeling", "Unreal Engine"],
        "resources": [
            "https://learn.unity.com/",
            "https://www.udemy.com/course/unrealengine/",
        ],
    },
    "business-analyst": {
        "skills": ["Excel", "SQL", "Power BI", "Requirements Gathering", "Communication"],
        "resources": [
            "https://www.coursera.org/professional-certificates/google-data-analytics",
            "https://www.edx.org/course/business-analytics",
        ],
    },
    "doctor": {
        "skills": ["Medical Science", "Patient Care", "Research", "Anatomy", "Public Health"],
        "resources": [
            "https://www.khanacademy.org/science/health-and-medicine",
            "https://medschoolinsiders.com/",
        ],
    },
    "lawyer": {
        "skills": ["Legal Research", "Critical Thinking", "Writing", "Negotiation", "Public Speaking"],
        "resources": [
            "https://www.coursera.org/specializations/international-law",
            "https://www.edx.org/learn/law",
        ],
    },
}

# --- Helpers ---
def normalize_goal_from_text(text: str) -> str:
    text = text.lower()
    for key in FALLBACK.keys():
        if key.replace("-", " ") in text:
            return key
    tokens = re.findall(r"[a-zA-Z\-]+", text)
    return tokens[0] if tokens else "data-analyst"


def query_metta_for_goal(goal: str):
    skills, resources = [], []
    if HAVE_METTA and metta_engine:
        try:
            sk_res = metta_engine.run(f"(skills {goal})")
            if sk_res:
                skills = [str(x) for x in sk_res[0]] if isinstance(sk_res[0], (list, tuple)) else [str(sk_res[0])]
        except Exception as e:
            logger.warning("MeTTa skills query failed: %s", e)

        try:
            r_res = metta_engine.run(f'(resources {goal})')
            if r_res:
                def unwrap(r):
                    try:
                        if hasattr(r, "get_object"):
                            obj = r.get_object()
                            if hasattr(obj, "value"):
                                return str(obj.value)
                        return str(r)
                    except Exception:
                        return str(r)
                if isinstance(r_res[0], (list, tuple)):
                    resources = [unwrap(x) for x in r_res[0]]
                else:
                    resources = [unwrap(r_res[0])]
        except Exception as e:
            logger.warning("MeTTa resources query failed: %s", e)

    fb = FALLBACK.get(goal)
    if fb:
        if not skills:
            skills = fb["skills"]
        if not resources:
            resources = fb["resources"]

    return skills, resources


def create_text_chat(text: str, end_session: bool = False) -> ChatMessage:
    content = [TextContent(type="text", text=text)]
    if end_session:
        content.append(EndSessionContent(type="end-session"))
    return ChatMessage(timestamp=datetime.now(timezone.utc), msg_id=uuid4(), content=content)


@chat_proto.on_message(ChatMessage)
async def on_chat(ctx: Context, sender: str, msg: ChatMessage):
    await ctx.send(sender, ChatAcknowledgement(timestamp=datetime.now(timezone.utc), acknowledged_msg_id=msg.msg_id))

    if any(isinstance(c, StartSessionContent) for c in msg.content):
        await ctx.send(sender, create_text_chat("👋 Hi! I'm SkillSync, your AI career mentor. Tell me what career path interests you or ask: 'How to become a <role>?'."))
        return

    user_text = " ".join([c.text for c in msg.content if isinstance(c, TextContent)]).strip()
    if not user_text:
        return

    logger.info("🔎 Received query from %s: %s", sender, user_text)
    goal = normalize_goal_from_text(user_text)
    logger.info("→ Normalized goal: %s", goal)

    skills, resources = query_metta_for_goal(goal)

    if skills and resources:
        resp_text = (
            f"💡 Here's a roadmap to becoming a **{goal.replace('-', ' ').title()}**:\n\n"
            f"**Core Skills:** {', '.join(skills)}\n\n"
            f"📚 **Top Learning Resources:**\n" + "\n".join(resources) +
            "\n\nKeep learning and stay consistent — you’ll get there! 🚀"
        )
    else:
        resp_text = "🤔 I couldn’t find a detailed plan for that yet. Try asking 'How to become a Data Analyst' or specify a clear career title."

    await ctx.send(sender, create_text_chat(resp_text, end_session=True))
    logger.info("✅ Sent recommendation to %s", sender)


@chat_proto.on_message(ChatAcknowledgement)
async def on_ack(ctx: Context, sender: str, msg: ChatAcknowledgement):
    logger.debug("Ack received from %s for %s", sender, msg.acknowledged_msg_id)


career_agent.include(chat_proto, publish_manifest=True)

if __name__ == "__main__":
    career_agent.run()
