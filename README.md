**Agentic AI Maritime Compliance Pipeline** 🚢🤖

📌 Project Overview

This project automates EU ETS (Emission Trading System) compliance verification for maritime fleets. It features a privacy-first, local LLM architecture to process vessel data, migrate it to a structured SQL database, and generate regulatory reports using autonomous AI agents.

🛠️ The Tech Stack

• AI Framework: CrewAI (Multi-Agent System)

• Local LLM: Ollama / Phi-3 (Ensuring 100% data privacy)

• Database: SQLite / SQL Migration

• Language: Python (Pandas, SQL Integration)

🧠 Agentic Architecture

I designed a Dual-Agent Workflow to mimic a real-world regulatory audit:

1. Maritime Data Verifier: Evaluates vessel eligibility based on the 5000 GT threshold and EU MRV laws.

2. Carbon Emissions Analyst: Performs complex math to calculate the 40% carbon phase-in for 2024 using standard emission factors.

📂 Repository Structure

📂 data/: Contains raw fleet data (.csv) and the processed SQLite database (.db).

📂 scripts/: Core Python logic including database setup and the Agentic AI pipeline.

📂 reports/: Sample compliance reports generated automatically by the AI agents.

🚀 Key Highlights

• Privacy-First: Processed sensitive maritime data locally using Ollama, ensuring zero data leakage.

• Automation: Replaced manual SQL entry with an automated Python-to-SQLite migration pipeline.
