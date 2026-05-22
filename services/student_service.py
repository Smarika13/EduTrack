from logger import logger
from utils import paginate
import json
import models


async def get_my_attendance(current_user, db, pg, cache):
    cache_key = (f"attendance:{current_user.id}")
    cached_data = await cache.get(cache_key)
    if cached_data:
        logger.info(f"Student {current_user.email} fetched attendance and cache hit")
        return json.loads(cached_data)
    else:
        data = paginate(db.query(models.Attendance).filter(models.Attendance.student_id == current_user.id), *pg)
        await cache.set(cache_key, json.dumps(data), ex=86400)
        logger.info(f"Student {current_user.email} fetched attendance and cache miss")
        return data


def get_my_scores(current_user, db, pg):
    logger.info(f"Student {current_user.email} fetched scores")
    return paginate(db.query(models.Score).filter(models.Score.student_id == current_user.id), *pg)


def get_my_submissions(current_user, db, pg):
    logger.info(f"Student {current_user.email} fetched submissions")
    return paginate(db.query(models.Submission).filter(models.Submission.student_id == current_user.id), *pg)
