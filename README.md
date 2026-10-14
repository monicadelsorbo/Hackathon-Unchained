# UNCHAINED
**AI Multi-Agent Training Plan Generator**

*A project developed for a Hackathon to revolutionize corporate Learning & Development using Artificial Intelligence.*

## The Idea
In modern companies, training is often generic or requires a massive amount of time from HR and Managers to create personalized paths. **Unchained** automates the entire upskilling and reskilling process using an ecosystem of **specialized AI Agents** working together like a real HR department.

## The Solution
A multi-agent system orchestrated via **LangGraph** that takes an employee's profile and desired target role as input, submits them to a dynamic assessment, and generates a comprehensive training roadmap. This includes real courses, cost estimation, and the assignment of an internal mentor.

## The AI Agents Architecture

Unchained uses a shared-state graph architecture, divided into 3 main phases. Each node in the graph is a specialized LLM agent:

```text
Manager/Employee → Plan Request
                          ↓
              ┌─── PHASE 1: Discovery ───┐
              │ 👤 Profile Agent         │ → Extracts current profile and skills
              │ 📝 Assessment Agent      │ → Generates personalized questions to identify gaps
              └──────────────────────────┘
                    ↓ (waits for user answers)
              ┌─── PHASE 2: Planning ────┐
              │ 📊 Assessment Agent      │ → Analyzes answers and defines gaps
              │ 🗺️ Plan Agent            │ → Generates the training roadmap (step-by-step)
              │ 📚 Resource Agent        │ → Matches real courses (e-learning, books, etc.)
              │ 💰 Cost Agent            │ → Calculates costs, timeline, and ROI
              │ 🤝 Mentor Agent          │ → Finds the most suitable corporate mentor
              └──────────────────────────┘
                    ↓ (waits for manager review)
              ┌─── PHASE 3: Validation ──┐
              │ 🕵️‍♂️ Review Agent          │ → Analyzes manager feedback
              │  ├ approved → ✉️ Notify Agent (Saves and notifies)
              │  └ changes  → 🔄 Rework (Plan/Resource/Cost Agent)
              └──────────────────────────┘
```

## Tech Stack

**Backend:**
- **Python 3 / FastAPI:** Robust and fast server.
- **LangGraph & LangChain:** Orchestration of the AI agents' workflow (cyclic and stateful flows).
- **DeepSeek LLM:** Language model for agent reasoning.
- **SQLite:** Lightweight database to save request states and mocked data.

**Frontend:**
- **React 19 & TypeScript:** Modern and typed user interface.
- **Vite:** Ultra-fast bundler.
- **Tailwind CSS:** Rapid and responsive styling.

## How to run the Demo

- Backend:

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Configure your DeepSeek API key (or another supported provider)
export DEEPSEEK_API_KEY="sk-your-key"

# Start the server
python main.py
```
*The backend will run on `http://localhost:8000`. API Docs on `http://localhost:8000/docs`.*

- Frontend:

```bash
cd frontend
npm install
npm run dev
```
*The app will be available at `http://localhost:5173`.*

## Demo Data (Included)

The application starts by automatically populating an in-memory database with test data:
- **3 Employees:** Marco (Junior Dev → Senior), Giulia (UX Designer → UX Lead), Alessandro (Senior Backend → Solutions Architect).
- **5 Corporate Mentors:** With various expertise and availability.
- **Course Catalog (Mock):** Over 30 courses from platforms like Coursera, Udemy, and LinkedIn Learning.

### Recommended Demo Flow
1. Go to `/request` → Select an employee and the desired target position.
2. Watch the AI agents at work in real-time.
3. Complete the custom-generated assessment (`/assessment/:id`).
4. View the incredible level of detail in the generated roadmap (`/roadmap/:id`).
5. Log in as a Manager to approve or request changes to the plan (`/review/:id`).
6. View the approved plan in the employee dashboard (`/dashboard`).
