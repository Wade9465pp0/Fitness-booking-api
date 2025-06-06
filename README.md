# 🧘‍♀️ Fitness Studio Booking API

A FastAPI backend for managing fitness class bookings.

## 🔧 Setup

```bash
Clone the repo
git clone https://github.com/yourusername/fitness-booking-api.git

Go to project directory
cd fitness-booking-api

Install the requirements
pip install -r requirements.txt

Create the virtual environment
python -m venv venv

Activate the venv
.venv\Scripts\activate

Run the server
uvicorn app.main:app --reload

Curl Commands

Get available Classes Slot:
curl -X 'GET' \
  'http://127.0.0.1:8000/classes?tz=Asia%2FKolkata' \
  -H 'accept: application/json'


Book a Class
curl -X 'POST' \
  'http://127.0.0.1:8000/book' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "class_id": 1,
  "client_name": "wade",
  "client_email": "wade@example.com"
}'

Check the bookings
curl -X 'GET' \
  'http://127.0.0.1:8000/bookings?email=wade%40example.com' \
  -H 'accept: application/json'
