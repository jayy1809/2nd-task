import httpx
from typing import Dict, Any
from fastapi import HTTPException

async def get_json_from_api(url: str) -> Dict[str, Any]:
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()  
            return response.json()  
    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=500, #e.response.status_code , i dont know whether this will work or not
            detail=f"HTTP error occurred while accessing {url}: {e}"
        ) from e
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An unexpected error occurred while getting : {str(e)}"
        ) from e
    # raise httpx.HTTPStatusError(f"An unexpected error occurred: {str(e)}") from e
 