from datetime import datetime, timedelta
from app.database import search_log_collection

MAX_SEARCHES_PER_HOUR = 5

async def validate_search_request(user_id: str):
    one_hour_ago = datetime.utcnow() - timedelta(hours=1)

    recent_searches = await search_log_collection.count_documents({
        "user_id": user_id,
        "timestamp": {"$gte": one_hour_ago}
    })

    if recent_searches >= MAX_SEARCHES_PER_HOUR:
        return False, "Search limit exceeded. Try again later."

    # Log this search
    await search_log_collection.insert_one({
        "user_id": user_id,
        "timestamp": datetime.utcnow()
    })

    return True, None
