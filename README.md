![tag:innovationlab](https://img.shields.io/badge/innovationlab-3D8BD3)
![tag:hackathon](https://img.shields.io/badge/hackathon-2E5CK3)
![tag:career-guidance](https://img.shields.io/badge/domain-career_guidance-3C9EE7)
![tag:education](https://img.shields.io/badge/domain-education-6A0DAD)
![tag:mentorship](https://img.shields.io/badge/domain-mentorship-008000)

# SkillSync AI – Career Mentor Agent 🤖🎓

## 🧠 Overview
**SkillSync AI** is an intelligent, multi-agent mentorship system that helps users discover and pursue personalized career paths using **uAgents**, **ASI Chat Protocol**, and **MeTTa Knowledge Graph reasoning**.  
It dynamically recommends skills, learning resources, and step-by-step career guidance based on user goals such as becoming a *Data Analyst*, *ML Engineer*, or *Frontend Developer*.  

The agent ecosystem ensures real-time, context-aware reasoning and can be expanded with new knowledge via MeTTa for adaptive learning.

---

## 🚀 Key Capabilities
- **Career Discovery:** Understands user intent (e.g., “I want to become a data analyst”) and matches it with relevant skill paths.  
- **Dynamic Knowledge Reasoning:** Uses **MeTTa Knowledge Graphs** for structured skill-resource mapping and inference.  
- **Conversational Guidance:** Engages users in interactive chats through the **uAgents Chat Protocol**, offering real-time mentorship.  
- **Extensible Framework:** Easily add new professions and learning pathways by updating `metta_kg.metta`.  
- **Fetch.ai & SingularityNET Integration Ready:** Fully compliant with the **ASI Alliance hackathon** requirements.

---

## 🧩 Architecture Overview

+--------------------------+
| User Interface (CLI / ASI Chat) |
+--------------------------+
|
v
+--------------------------+
| SkillSync Mentor Agent |
| (uAgents + dotenv + logging) |
+--------------------------+
|
v
+--------------------------+
| MeTTa Knowledge Graph |
| (career-skill-resource rules) |
+--------------------------+


Agents communicate over **ASI Chat Protocol**, reason with **MeTTa**, and provide tailored mentorship responses.

---

## 🛠️ Technologies Used
| Technology | Purpose |
|-------------|----------|
| **uAgents** | Core agent framework for communication & reasoning |
| **Chat Protocol (ASI:One)** | Enables structured agent conversations |
| **MeTTa Knowledge Graph** | Stores and infers skill mappings |
| **Python-dotenv** | Loads environment configurations securely |
| **Logging** | Provides detailed event tracking |
| **Agentverse Registration** | Enables public access and ASI discoverability |

---

## 🧩 MeTTa Knowledge Graph (`metta_kg.metta`)
Sample rules used for reasoning:

<pre>metta
(= (skills data-analyst) (python sql pandas matplotlib))
(= (resources data-analyst) ("https://www.kaggle.com/learn/overview" "https://www.coursera.org/specializations/data-science"))
(= (skills ml-engineer) (python math statistics tensorflow))
(= (resources ml-engineer) ("https://www.coursera.org/specializations/machine-learning" "https://www.fast.ai/"))
(= (skills frontend-dev) (html css javascript react))
(= (resources frontend-dev) ("https://frontendmasters.com" "https://scrimba.com/"))
(= (skills backend-dev) (python nodejs databases docker))
(= (resources backend-dev) ("https://www.udemy.com/course/rest-api-flask" "https://www.pluralsight.com/"))
(= (skills data-scientist) (python sql statistics machine-learning visualization))
(= (resources data-scientist) ("https://www.coursera.org/specializations/jhu-data-science" "https://www.kaggle.com/"))
(= (skills blockchain-dev) (solidity smart-contracts web3 ethers.js))
(= (resources blockchain-dev) ("https://cryptozombies.io" "https://www.udemy.com/course/blockchain-a-z/"))
(= (skills cybersecurity-analyst) (networking linux cryptography threat-analysis))
(= (resources cybersecurity-analyst) ("https://tryhackme.com" "https://www.coursera.org/specializations/ibm-cybersecurity-analyst"))
(= (skills ui-ux-designer) (figma prototyping user-research design-thinking))
(= (resources ui-ux-designer) ("https://www.interaction-design.org" "https://www.coursera.org/specializations/ui-ux-design"))
(= (skills devops-engineer) (ci-cd docker kubernetes aws monitoring))
(= (resources devops-engineer) ("https://www.edx.org/learn/devops" "https://www.coursera.org/specializations/devops"))</pre>



This structure ensures high adaptability and semantic inference power during chat sessions.



🧪 Local Development Setup
# 1. Clone
git clone https://github.com/muizcal/SkillSync-AI.git
cd SkillSync-AI

# 2. Create venv and activate
python3 -m venv venv
source venv/bin/activate

# 3. Install dependencies (make sure to run inside venv)
python -m pip install --force-reinstall --no-cache-dir uagents python-dotenv hyperon  # hyperon only if available/needed

# 4. Start the main agent (career_agent) first
python career_agent.py

# 5. Copy the printed agent address and register it on Agentverse (enable mailbox)
# 6. Add that address to .env for Mentor/Patient agents (e.g., CAREER_AGENT_ADDRESS=agent1...)

⚙️ Example .env (copy .env.example to .env and edit)
ASI_ONE_API_KEY=      # optional (LLM usage)
AGENTVERSE_API_KEY=sk_xxx
CAREER_AGENT_ADDRESS=agent1xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
CAREER_AGENT_SEED=career_secret_seed_v1
MENTOR_AGENT_SEED=mentor_secret_seed_v1
PATIENT_AGENT_SEED=patient_secret_seed_v1

# 7. Start mentor_agent (and/or patient_agent)
python mentor_agent.py
python patient_agent.py


After start career_agent.py (server agent). Copy its printed agent address url.

Register it in Agentverse and enable mailbox.

Set MENTOR_AGENT  .env to point to that career agent address (e.g., CAREER_AGENT_ADDRESS=<address>) 

Start mentor_agent.py. It sends the demo query to career_agent.

Confirm reply both in backend logs and in Agentverse UI.

Example chat:
User (on Agentverse or ASI ONE): @Mentor Agent How can I become a data analyst?
Mentor Agent -> Career Agent (backend)
Career Agent -> Mentor Agent -> reply visible on Agentverse



**📖 Use Case Examples**
Scenario	            Description
🎯 Career Switcher	    Helps professionals pivot to new roles by learning new skills.
🧑‍🎓 Student Mentor	Guides students in picking relevant courses to achieve job readiness.
💼 Recruiter Assistant	Maps candidate profiles to relevant learning paths for upskilling.


**⚙️ Interaction Modes**

Direct ASI Chat (User ↔ SkillSync AI)

CLI Terminal Interface

Future Scope: Integration into web dashboards or Discord agents.



## 🎬 Demo video
[Click here to view the demo](https://drive.google.com/file/d/1VT1ufyoEDJMBdG7jazQuu85uccw6zzyw/view?usp=sharing)





**🚫 Limitations**

Currently supports predefined careers listed in MeTTa knowledge base.

Does not yet perform resume parsing or dynamic data scraping.

Internet-based resource links are static for this version.

**🧩 Future Enhancements**

Add personalized skill scoring and progress tracking.

Expand to include AI-driven resume analysis.

Integrate with SingularityNET AI models for richer reasoning.

Deploy a multi-agent collaboration system (Mentor + Recruiter + Trainer).

**🔑 Keywords & Tags**

career, mentorship, education, learning-paths, MeTTa, uAgents, ASI, hackathon, Agentverse, Fetch.ai, SingularityNET

**📄 License**

This project is released under the MIT License.


Created by:
👨‍💻 Shittu Abdulmuiz Oyekunle (Muizcal)
🌐 SkillSync AI | ASI Hackathon 2025



