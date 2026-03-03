from fastapi import FastAPI

from slotegrator_api.callback.callback_handler import CallbackHandler

app = FastAPI(title="Slotegrator integration")
handler = CallbackHandler(app, "/callback")
