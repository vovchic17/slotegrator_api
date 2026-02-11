import asyncio

from slotegrator_api import SlotegratorAPI

async def main() -> None:
    client = SlotegratorAPI(
        merchant_id="b06bced7abc649cc077f2a6aef29d67c",
        merchant_key="a192884aaae353c865e40f22c208d0a41ab29723",
        base_api_url="https://staging.slotegrator.com/api/index.php/v1",
    )

    # games = await client.get_games(
    #     expand=["tags", "parameters", "images", "related_games"],
    # )
    # for game in games:
    #     print(game.uuid)

    # game_tags = await client.get_game_tags(expand=["category"])
    # print(game_tags)

    lobby = await client.get_lobby_tables(
        "cb2d3bc6e2ce0532610c97b412723ac9a57337ac",
        "EUR",
    )
    print(lobby)
    await client.close()


if __name__ == "__main__":
    asyncio.run(main())
