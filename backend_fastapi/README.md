GTH Scientia TI - FastAPI backend scaffold (POC)
------------------------------------------------

This scaffold provides a minimal FastAPI backend with:
- JWT authentication (register/login)
- SQLite dev database with SQLAlchemy
- User and Company models
- Rules and RuleVersion endpoints (skeleton)
- A very small Rule Engine POC: evaluates simple JSON 'formula' using a safe eval approach
- Seeded admin user: email `admin@local`, password `admin123`

How to run (local dev)
----------------------
1. Create a virtual environment and activate it:
   python -m venv .venv
   # Windows PowerShell:
   .venv\Scripts\Activate.ps1
   # Windows CMD:
   .venv\Scripts\activate.bat
   # macOS / Linux:
   source .venv/bin/activate

2. Install dependencies:
   pip install -r requirements.txt

3. Run the app:
   uvicorn main:app --reload --port 8000

4. Open docs:
   http://localhost:8000/docs

Notes
-----
- This is a POC scaffold: extend models, add migrations, and secure secrets before production.
- The rule engine is intentionally simple for POC. For production, consider a DSL or sandboxed evaluator.
