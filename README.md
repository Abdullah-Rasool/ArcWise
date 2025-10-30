# 🧠 ArcWise — AI Agentic Financial Automation on Arc
**Team**: Finstream  
**Hackathon**: AI Agents on Arc with USDC 

# 🌐 Overview

ArcWise is an AI agentic financial automation system built on Arc using USDC for stable, frictionless on-chain transactions.
It leverages OpenAI Agents SDK, LangChain, and MCP (Model Context Protocol) to create an ecosystem where multiple AI agents autonomously perform secure financial actions and manage liquidity across chains.

# 💡 Core Idea

ArcWise connects intelligent AI agents with deterministic on-chain execution — enabling:

- 🤖 Autonomous decision-making through OpenAI Agents

- 💸 Secure payments and settlements using USDC

- 🔗 Cross-chain operations via Arc

- 🧩 Data context management with MCP server integration

# 🏗️ Tech Stack

| Layer | Technology | Purpose |
|-------|-------------|----------|
| **AI Agent Layer** | OpenAI Agents SDK | Create 4 specialized AI agents for financial logic and task automation |
| **Orchestration Layer** | LangChain | Manage inter-agent communication and reasoning chain |
| **Infrastructure Layer** | MCP Server | Context storage, history, and API connections for persistent state |
| **Blockchain Layer** | Arc + USDC | Transaction execution, liquidity, and settlement |
| **Backend** | Python (FastAPI) | API routes and backend logic |
| **Frontend (optional)** | React + Tailwind | Dashboard to monitor agent activity and transaction logs |
| **Version Control** | GitHub | Team collaboration and project management |


# 🧩 Architecture (Simplified)

1- User Request → Sent to AI Interface (OpenAI Agent 1).

2- Agent Chain → LangChain connects 4 agents (Analyzer, Decision Maker, Executor, Validator).

3- MCP Server → Stores data, financial logs, and state for Agent 3 (Executor).

4- Arc Network → Executes transactions via USDC with deterministic finality.

5- Result → Returned to dashboard or user endpoint.

# 🧰 Environment Variables (.env.example)
```
OPENAI_API_KEY=your_openai_key_here  
ARC_API_KEY=your_arc_key_here  
MCP_SERVER_URL=http://localhost:8000  
USDC_WALLET_ADDRESS=your_wallet_here
```

# 🧑‍💻 Setup Instructions

1- Clone the repo
```
git clone https://github.com/<your-username>/ArcWise.git
```
2- Switch to dev branch
```
git checkout dev
```
3- Create .env file (based on .env.example).

4- Install dependencies by using pip install -r requirements.txt.

5- Run backend (FastAPI or Flask).

6- Start MCP server.

7- Connect OpenAI Agents and begin interaction.

# 🏁 Goal

To demonstrate autonomous, safe, and traceable financial actions by intelligent AI agents using Arc’s USDC integration.

# 🧑‍🤝‍🧑 Team

Abdullah Rasool (@AbdDevX) — AI & Agentic Systems Developer  
Team Members: 
- Malik Jawad (@malik52923) - AI & Agentic Systems Developer
- Ammar Ahmed (@ammarahmed1448) - Software Engineer & AI Developer


# 📜 License

MIT License © 2025 Team Finstream
