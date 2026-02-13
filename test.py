import asyncio

from slotegrator_api import SlotegratorAPI


async def main() -> None:
    client = SlotegratorAPI(
        merchant_id="b06bced7abc649cc077f2a6aef29d67c",
        merchant_key="a192884aaae353c865e40f22c208d0a41ab29723",
        base_api_url="https://staging.slotegrator.com/api/index.php/v1",
    )

    print(await client.get_limits())

    await client.close()


if __name__ == "__main__":
    asyncio.run(main())
