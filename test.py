import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from slotegrator_api import SlotegratorAPI

app = FastAPI()

# client = SlotegratorAPI(
#     merchant_id="9980c2f2e878978a9f868ae03f53643f",
#     merchant_key="9c34bb658cd274ae23537d4f14e024aa979818d5",
#     base_api_url="https://gis.slotegrator.com/api/index.php/v1",
#     timeout=1000,
# )
client = SlotegratorAPI(
    merchant_id="b06bced7abc649cc077f2a6aef29d67c",
    merchant_key="a192884aaae353c865e40f22c208d0a41ab29723",
    base_api_url="https://staging.slotegrator.com/api/index.php/v1",
    timeout=1000,
)
client.setup_callback(app, "/callback")
