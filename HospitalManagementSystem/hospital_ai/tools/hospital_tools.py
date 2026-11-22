from langchain.tools import tool
from data.sample_data import (
    patients,
    doctors,
    appointments,
    medical_records
)


@tool
def register_patient(full_name: str,age: int, phone: str):
    """
    Register a new patient in the hospital system.
    """

    if age <= 0:
        return {
            "message": "Invalid age"
        }

    for patient in patients.values():
        if patient["phone"] == phone:
            return {
                "message": "Phone number already registered"
            }

    patient_id = f"P{1000 + len(patients) + 1}"

    patients[patient_id] = {
        "full_name": full_name,
        "age": age,
        "phone": phone,
    }

    return {
        "status": "success",
        "patient_id": patient_id,
        "message": "Patient registered successfully"
    }


@tool
def check_doctor_availability(
    specialization: str,
    preferred_date: str
):
    """
    Check doctor availability for a specialization and date.
    """

    available_doctors = []

    for doctor_id, doctor in doctors.items():

        if doctor["specialization"].lower() == specialization.lower():

            slots = doctor["available_slots"].get(
                preferred_date,
                []
            )

            if slots:
                available_doctors.append(
                    {
                        "doctor_id": doctor_id,
                        "doctor_name": doctor["doctor_name"],
                        "specialization": doctor["specialization"],
                        "available_slots": slots
                    }
                )

    if not available_doctors:
        return {
            "status": "error",
            "message": "No doctors available"
        }

    return {
        "status": "success",
        "doctors": available_doctors
    }


@tool
def book_appointment(
    patient_id: str,
    doctor_id: str,
    appointment_date: str,
    time_slot: str
):
    """
    Book an appointment for a patient.
    """

    if patient_id not in patients:
        return {
            "status": "error",
            "message": "Invalid patient ID"
        }

    if doctor_id not in doctors:
        return {
            "status": "error",
            "message": "Invalid doctor ID"
        }

    available_slots = doctors[doctor_id]["available_slots"].get(
        appointment_date,
        []
    )

    if time_slot not in available_slots:
        return {
            "status": "error",
            "message": "Selected slot not available"
        }

    appointment_id = f"A{5000 + len(appointments) + 1}"

    appointments[appointment_id] = {
        "patient_id": patient_id,
        "doctor_id": doctor_id,
        "appointment_date": appointment_date,
        "time_slot": time_slot
    }

    doctors[doctor_id]["available_slots"][
        appointment_date
    ].remove(time_slot)

    return {
        "status": "success",
        "appointment_id": appointment_id,
        "patient_id": patient_id,
        "doctor_id": doctor_id,
        "appointment_date": appointment_date,
        "time_slot": time_slot,
        "message": "Appointment booked successfully"
    }


@tool
def get_patient_medical_records(
    patient_id: str,
    authorized_role: str
):
    """
    Fetch patient medical records.
    """

    allowed_roles = [
        "doctor",
        "admin"
    ]

    if authorized_role.lower() not in allowed_roles:
        return {
            "status": "error",
            "message": "Access denied"
        }

    if patient_id not in medical_records:
        return {
            "status": "error",
            "message": "Patient record not found"
        }

    return {
        "status": "success",
        "patient_id": patient_id,
        "records": medical_records[patient_id]
    }


@tool
def calculate_hospital_bill(
    patient_id: str,
    consultation_fee: float,
    lab_charges: float,
    treatment_charges: float,
    discount_percent: float = 0
):
    """
    Calculate the hospital bill.
    """

    if patient_id not in patients:
        return {
            "status": "error",
            "message": "Invalid patient ID"
        }

    if (
        consultation_fee < 0
        or lab_charges < 0
        or treatment_charges < 0
    ):
        return {
            "status": "error",
            "message": "Charges cannot be negative"
        }

    if discount_percent < 0 or discount_percent > 100:
        return {
            "status": "error",
            "message": "Invalid discount percentage"
        }

    subtotal = (
        consultation_fee
        + lab_charges
        + treatment_charges
    )

    discount_amount = (
        subtotal * discount_percent / 100
    )

    total_amount = subtotal - discount_amount

    return {
        "status": "success",
        "patient_id": patient_id,
        "subtotal": subtotal,
        "discount_amount": discount_amount,
        "total_amount": total_amount
    }