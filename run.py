import os
import uvicorn
from app.database import init_db
from app.seed_data import seed_demo_data_if_empty

if __name__ == "__main__":
    print("=" * 70)
    print("  Google Maps Competitor Update Intelligence Tool - MapPulse AI")
    print("=" * 70)
    
    # Ensure database tables exist and realistic demo data is seeded
    print("[*] Initializing SQLite database...")
    init_db()
    print("[*] Checking pre-populated demo dataset...")
    seed_demo_data_if_empty(force=False)
    
    port = int(os.environ.get("PORT", 8000))
    host = os.environ.get("HOST", "0.0.0.0")
    
    print(f"\n[+] Server running at: http://localhost:{port}")
    print(f"[+] Interactive API Docs: http://localhost:{port}/docs")
    print(f"[+] Ready for testing, recording, and evaluation!\n")
    
    uvicorn.run("app.main:app", host=host, port=port, reload=True)
