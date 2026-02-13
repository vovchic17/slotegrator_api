import asyncio

from slotegrator_api import SlotegratorAPI


async def main() -> None:
    client = SlotegratorAPI(
        merchant_id="b06bced7abc649cc077f2a6aef29d67c",
        merchant_key="a192884aaae353c865e40f22c208d0a41ab29723",
        base_api_url="https://staging.slotegrator.com/api/index.php/v1",
    )

    tags = await client.get_freespin_bets(
        "bdad4dcaca47b264f54b39789446a7e0551ed5b0",
        "RUB",
    )
    print(tags)

    await client.close()


if __name__ == "__main__":
    asyncio.run(main())
