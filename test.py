from fastapi import FastAPI

from slotegrator_api.callback.callback_handler import CallbackHandler

app = FastAPI()
handler = CallbackHandler(app, "/callback")
