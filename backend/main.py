"""
UNCHAINED - Entrypoint.
"""

import uvicorn
from db import init_db
from store import seed_mock_data

# Inizializza database e dati demo all'avvio
init_db()
seed_mock_data()

if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
