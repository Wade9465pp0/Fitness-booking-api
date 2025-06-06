# app/utils.py

from datetime import datetime
import pytz
import logging

def get_ist_datetime_now():
    """Returns the current datetime in IST timezone."""
    ist = pytz.timezone("Asia/Kolkata")
    return datetime.now(ist)

def convert_utc_to_ist(utc_dt):
    """Converts UTC datetime to IST."""
    ist = pytz.timezone("Asia/Kolkata")
    return utc_dt.astimezone(ist)

def convert_ist_to_timezone(ist_str: str, target_tz: str) -> str:
    ist = pytz.timezone("Asia/Kolkata")
    try:
        target = pytz.timezone(target_tz)
    except pytz.UnknownTimeZoneError:
        return ist_str  # fallback: no conversion if invalid timezone

    ist_dt = ist.localize(datetime.fromisoformat(ist_str))
    converted = ist_dt.astimezone(target)
    return converted.isoformat()

def setup_logger(name: str):
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger