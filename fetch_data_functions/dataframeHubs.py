import pandas as pd
import asyncio
async def get_hub_id(hubService) -> str:
    hubsResponse = await hubService.get_all_hubs()
    return hubsResponse[0]


