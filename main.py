from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
import uuid

app = FastAPI()

appointments: List[Dict] = []
next_id = 1 



class Appointment(BaseModel):
    id: Optional[int] = None  # Change from str to int if no longer using UUIDs
    title: str
    description: str
    date: str
    time: str
    userId: int
    name: str
    phone_number: str
    location: str
    queue_number: Optional[int] = None


@app.post("/appointments")
def create_appointment(appointment: Appointment):
    appointment.id = str(uuid.uuid4())

    appointment.id = str(next_id)  # Convert to string if model expects string
    next_id += 1
    
    queue_number = len(appointments) + 1
    if queue_number > 99:
        raise HTTPException(status_code=400, detail="Queue is full (max 99)")
    appointment.queue_number = int(f"{queue_number:02}")

    appointments.append(appointment.dict())
    return {"msg": "Appointment created", "appointment": appointment}

@app.get("/appointments/{appointment_id}", response_model=Appointment)
def get_appointment(appointment_id: int):  # Now int
    for appt in appointments:
        if appt["id"] == appointment_id:
            return appt
    raise HTTPException(status_code=404, detail="Appointment not found")

    
@app.get("/appointments")
def list_appointments():
    return appointments

@app.get("/appointments/{appointment_id}", response_model=Appointment)
def get_appointment(appointment_id: str):
    for appt in appointments:
        if appt["id"] == appointment_id:
            return appt
    raise HTTPException(status_code=404, detail="Appointment not found")

@app.put("/appointments/{appointment_id}", response_model=Appointment)
def update_appointment(appointment_id: str, updated: Appointment):
    for i, appt in enumerate(appointments):
        if appt["id"] == appointment_id:
            updated.id = appointment_id
            appointments[i] = updated.dict()
            return updated
    raise HTTPException(status_code=404, detail="Appointment not found")

@app.delete("/appointments/{appointment_id}")
def delete_appointment(appointment_id: str):
    for i, appt in enumerate(appointments):
        if appt["id"] == appointment_id:
            del appointments[i]
            return {"detail": "Appointment deleted"}
    raise HTTPException(status_code=404, detail="Appointment not found")

@app.get("/appointments/names")
def list_appointment_names():
    return [appt["name"] for appt in appointments]

