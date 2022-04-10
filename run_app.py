import uvicorn
from fastapi import FastAPI
from notebook_error_reporter.serverside import create_db, create_app

create_db()
app:FastAPI = create_app(debug=False, max_transparency=True)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")


