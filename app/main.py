from fastapi import FastAPI, HTTPException, Query
from app.database import init_db, get_classes, book_class, get_bookings_by_email
from app.models import BookingRequest
from app.utils import convert_ist_to_timezone, setup_logger

app = FastAPI(title="Fitness Studio Booking API")
logger = setup_logger("booking-api")

init_db()

@app.get("/classes")
def list_classes():
    return get_classes()

@app.post("/book")
def book(request: BookingRequest):
    logger.info(f"Booking request received: {request}")
    try:
        result = book_class(request)
        logger.info(f"Booking successful for {request.client_email} in class ID {request.class_id}")
        return result
    except ValueError as ve:
        logger.warning(f"Booking failed for {request.client_email}: {ve}")
        raise HTTPException(status_code=400, detail=str(ve))

@app.get("/bookings")
def bookings(email: str = Query(..., description="Client email to fetch bookings")):
    try:
        logger.info(f"Fetching bookings for email: {email}")
        bookings = get_bookings_by_email(email)
        logger.info(f"Found {len(bookings)} bookings for {email}")
        return bookings
    except ValueError as ve:
        logger.error(f"Error fetching bookings for {email}: {ve}")
        raise HTTPException(status_code=400, detail=str(ve))    

@app.get("/classes")
def list_classes(tz: str = Query("Asia/Kolkata", description="Timezone to convert class times to")):
    logger.info(f"Fetching classes in timezone: {tz}")
    classes = get_classes()
    for c in classes:
        c["datetime"] = convert_ist_to_timezone(c["datetime"], tz)
    logger.info(f"Found {len(classes)} classes")
    return classes


@app.get("/")
def root():
    return {"message": "Fitness Booking API is running!"}
# This code sets up a FastAPI application with endpoints to list classes, book a class, and retrieve bookings by email.
# It initializes the database and uses Pydantic models for request validation.