import asyncio

from slotegrator_api import SlotegratorAPI


async def main() -> None:
    client = SlotegratorAPI(
        merchant_id="b06bced7abc649cc077f2a6aef29d67c",
        merchant_key="a192884aaae353c865e40f22c208d0a41ab29723",
        base_api_url="https://staging.slotegrator.com/api/index.php/v1",
    )

    games = await client.get_games(
        expand=["tags", "parameters", "images", "related_games"],
    )
    for game in games:
        print(game.uuid)

    prep_game = await client.init_game(
        "7487f0fac9049c9ee0dd0635a8ce5f5bfe04cd15",
        "1",
        "test",
        "RUB",
        "123",
    )
    print(prep_game)
    await client.close()


if __name__ == "__main__":
    asyncio.run(main())
