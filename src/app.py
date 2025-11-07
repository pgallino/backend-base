"""Application entrypoint shim.

The real FastAPI app and the api_facade are created in
`src.application.api_app`. This module keeps `src.app:app` available for
uvicorn and compatibility.
"""

from src.application.api_app import app  # re-export the FastAPI app
