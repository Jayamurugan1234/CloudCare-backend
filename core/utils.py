# # import random
# # import string
# # from django.core.mail import send_mail

# # def generate_patient_id():
# #     return "PAT" + "".join(random.choices(string.digits, k=6))

# # def generate_doctor_id():
# #     return "DOC" + "".join(random.choices(string.digits, k=6))

# # def generate_staff_id():
# #     return "STF" + "".join(random.choices(string.digits, k=6))

# # def generate_pharmacy_id():
# #     return "PHM" + "".join(random.choices(string.digits, k=6))


# # def send_patient_email(to_email, patient_name, specialist, doctor_name, doctor_id,
# #                         patient_id, preferred_date, preferred_time, availability_line):
# #     if doctor_name and doctor_id:
# #         doctor_line = f"Doctor: Dr. {doctor_name} (ID: {doctor_id})\n"
# #     else:
# #         doctor_line = "No approved doctor is currently registered for this specialist yet. We'll update you soon.\n"

# #     subject = "Your Appointment Request — CareCloud Hospital"
# #     message = (
# #         f"Hello {patient_name},\n\n"
# #         f"Patient ID: {patient_id}\n"
# #         f"Specialist requested: {specialist}\n"
# #         f"{doctor_line}"
# #         f"Requested date: {preferred_date}\n"
# #         f"Requested time: {preferred_time}\n"
# #         f"{availability_line}\n"
# #         f"Please keep your Patient ID for reference.\n\n"
# #         f"- CareCloud Hospital"
# #     )
# #     send_mail(subject, message, None, [to_email], fail_silently=False)


# # def send_doctor_pending_email(to_email, doctor_name):
# #     subject = "CareCloud Hospital — Registration Received"
# #     message = (
# #         f"Hello Dr. {doctor_name},\n\n"
# #         f"We've received your registration and degree certificate.\n"
# #         f"Your account is pending admin verification. You'll receive your Doctor ID "
# #         f"by email once approved.\n\n"
# #         f"- CareCloud Hospital"
# #     )
# #     send_mail(subject, message, None, [to_email], fail_silently=False)


# # def send_doctor_email(to_email, doctor_name, doctor_id):
# #     subject = "You're Approved — CareCloud Hospital"
# #     message = (
# #         f"Hello Dr. {doctor_name},\n\n"
# #         f"Your account has been verified and approved.\n"
# #         f"Your Doctor ID is: {doctor_id}\n\n"
# #         f"You can now log in using your email, password, and this Doctor ID.\n\n"
# #         f"- CareCloud Hospital"
# #     )
# #     send_mail(subject, message, None, [to_email], fail_silently=False)


# # def send_staff_email(to_email, staff_name, staff_role, staff_id):
# #     subject = "Your Staff Account — CareCloud Hospital"
# #     message = (
# #         f"Hello {staff_name},\n\n"
# #         f"Your staff account has been created successfully.\n"
# #         f"Staff ID: {staff_id}\n"
# #         f"Role: {staff_role}\n\n"
# #         f"You can now log in using your registered email and password.\n\n"
# #         f"- CareCloud Hospital"
# #     )
# #     send_mail(subject, message, None, [to_email], fail_silently=False)


# # def send_pharmacy_email(to_email, pharmacy_name, pharmacy_id):
# #     subject = "Welcome to CareCloud Hospital"
# #     message = (
# #         f"Hello {pharmacy_name},\n\n"
# #         f"Your CareCloud account has been created.\n"
# #         f"Your Pharmacy ID is: {pharmacy_id}\n\n"
# #         f"Please keep this ID for reference.\n\n"
# #         f"- CareCloud Hospital"
# #     )
# #     send_mail(subject, message, None, [to_email], fail_silently=False)































# import os
# import random
# import string
# import requests

# BREVO_API_KEY = os.environ.get("BREVO_API_KEY")
# BREVO_API_URL = "https://api.brevo.com/v3/smtp/email"


# def _send_email_via_brevo(to_email, subject, message):
#     if not BREVO_API_KEY:
#         print("BREVO_API_KEY not set — skipping email send.")
#         return

#     payload = {
#         "sender": {"name": "CareCloud Hospital", "email": "vjayamurugan83@gmail.com"},
#         "to": [{"email": to_email}],
#         "subject": subject,
#         "textContent": message,
#     }
#     headers = {
#         "accept": "application/json",
#         "api-key": BREVO_API_KEY,
#         "content-type": "application/json",
#     }
#     try:
#         response = requests.post(BREVO_API_URL, json=payload, headers=headers, timeout=10)
#         response.raise_for_status()
#     except requests.RequestException as e:
#         print(f"Email send failed: {e}")


# def generate_patient_id():
#     return "PAT" + "".join(random.choices(string.digits, k=6))

# def generate_doctor_id():
#     return "DOC" + "".join(random.choices(string.digits, k=6))

# def generate_staff_id():
#     return "STF" + "".join(random.choices(string.digits, k=6))

# def generate_pharmacy_id():
#     return "PHM" + "".join(random.choices(string.digits, k=6))


# def send_patient_email(to_email, patient_name, specialist, doctor_name, doctor_id,
#                         patient_id, preferred_date, preferred_time, availability_line):
#     if doctor_name and doctor_id:
#         doctor_line = f"Doctor: Dr. {doctor_name} (ID: {doctor_id})\n"
#     else:
#         doctor_line = "No approved doctor is currently registered for this specialist yet. We'll update you soon.\n"

#     subject = "Your Appointment Request — CareCloud Hospital"
#     message = (
#         f"Hello {patient_name},\n\n"
#         f"Patient ID: {patient_id}\n"
#         f"Specialist requested: {specialist}\n"
#         f"{doctor_line}"
#         f"Requested date: {preferred_date}\n"
#         f"Requested time: {preferred_time}\n"
#         f"{availability_line}\n"
#         f"Please keep your Patient ID for reference.\n\n"
#         f"- CareCloud Hospital"
#     )
#     _send_email_via_brevo(to_email, subject, message)


# def send_doctor_pending_email(to_email, doctor_name):
#     subject = "CareCloud Hospital — Registration Received"
#     message = (
#         f"Hello Dr. {doctor_name},\n\n"
#         f"We've received your registration and degree certificate.\n"
#         f"Your account is pending admin verification. You'll receive your Doctor ID "
#         f"by email once approved.\n\n"
#         f"- CareCloud Hospital"
#     )
#     _send_email_via_brevo(to_email, subject, message)


# def send_doctor_email(to_email, doctor_name, doctor_id):
#     subject = "You're Approved — CareCloud Hospital"
#     message = (
#         f"Hello Dr. {doctor_name},\n\n"
#         f"Your account has been verified and approved.\n"
#         f"Your Doctor ID is: {doctor_id}\n\n"
#         f"You can now log in using your email, password, and this Doctor ID.\n\n"
#         f"- CareCloud Hospital"
#     )
#     _send_email_via_brevo(to_email, subject, message)


# def send_staff_email(to_email, staff_name, staff_role, staff_id):
#     subject = "Your Staff Account — CareCloud Hospital"
#     message = (
#         f"Hello {staff_name},\n\n"
#         f"Your staff account has been created successfully.\n"
#         f"Staff ID: {staff_id}\n"
#         f"Role: {staff_role}\n\n"
#         f"You can now log in using your registered email and password.\n\n"
#         f"- CareCloud Hospital"
#     )
#     _send_email_via_brevo(to_email, subject, message)


# def send_pharmacy_email(to_email, pharmacy_name, pharmacy_id):
#     subject = "Welcome to CareCloud Hospital"
#     message = (
#         f"Hello {pharmacy_name},\n\n"
#         f"Your CareCloud account has been created.\n"
#         f"Your Pharmacy ID is: {pharmacy_id}\n\n"
#         f"Please keep this ID for reference.\n\n"
#         f"- CareCloud Hospital"
#     )
#     _send_email_via_brevo(to_email, subject, message)






import random
import string
from django.core.mail import send_mail
from django.core.mail import BadHeaderError
import logging

logger = logging.getLogger(__name__)


def _safe_send_mail(subject, message, to_email):
    try:
        send_mail(subject, message, None, [to_email], fail_silently=False)
    except Exception as e:
        logger.error(f"Email send failed for {to_email}: {e}")


def generate_patient_id():
    return "PAT" + "".join(random.choices(string.digits, k=6))

def generate_doctor_id():
    return "DOC" + "".join(random.choices(string.digits, k=6))

def generate_staff_id():
    return "STF" + "".join(random.choices(string.digits, k=6))

def generate_pharmacy_id():
    return "PHM" + "".join(random.choices(string.digits, k=6))


def send_patient_email(to_email, patient_name, specialist, doctor_name, doctor_id,
                        patient_id, preferred_date, preferred_time, availability_line):
    if doctor_name and doctor_id:
        doctor_line = f"Doctor: Dr. {doctor_name} (ID: {doctor_id})\n"
    else:
        doctor_line = "No approved doctor is currently registered for this specialist yet. We'll update you soon.\n"

    subject = "Your Appointment Request — CareCloud Hospital"
    message = (
        f"Hello {patient_name},\n\n"
        f"Patient ID: {patient_id}\n"
        f"Specialist requested: {specialist}\n"
        f"{doctor_line}"
        f"Requested date: {preferred_date}\n"
        f"Requested time: {preferred_time}\n"
        f"{availability_line}\n"
        f"Please keep your Patient ID for reference.\n\n"
        f"- CareCloud Hospital"
    )
    _safe_send_mail(subject, message, to_email)


def send_doctor_pending_email(to_email, doctor_name):
    subject = "CareCloud Hospital — Registration Received"
    message = (
        f"Hello Dr. {doctor_name},\n\n"
        f"We've received your registration and degree certificate.\n"
        f"Your account is pending admin verification. You'll receive your Doctor ID "
        f"by email once approved.\n\n"
        f"- CareCloud Hospital"
    )
    _safe_send_mail(subject, message, to_email)


def send_doctor_email(to_email, doctor_name, doctor_id):
    subject = "You're Approved — CareCloud Hospital"
    message = (
        f"Hello Dr. {doctor_name},\n\n"
        f"Your account has been verified and approved.\n"
        f"Your Doctor ID is: {doctor_id}\n\n"
        f"You can now log in using your email, password, and this Doctor ID.\n\n"
        f"- CareCloud Hospital"
    )
    _safe_send_mail(subject, message, to_email)


def send_staff_email(to_email, staff_name, staff_role, staff_id):
    subject = "Your Staff Account — CareCloud Hospital"
    message = (
        f"Hello {staff_name},\n\n"
        f"Your staff account has been created successfully.\n"
        f"Staff ID: {staff_id}\n"
        f"Role: {staff_role}\n\n"
        f"You can now log in using your registered email and password.\n\n"
        f"- CareCloud Hospital"
    )
    _safe_send_mail(subject, message, to_email)


def send_pharmacy_email(to_email, pharmacy_name, pharmacy_id):
    subject = "Welcome to CareCloud Hospital"
    message = (
        f"Hello {pharmacy_name},\n\n"
        f"Your CareCloud account has been created.\n"
        f"Your Pharmacy ID is: {pharmacy_id}\n\n"
        f"Please keep this ID for reference.\n\n"
        f"- CareCloud Hospital"
    )
    _safe_send_mail(subject, message, to_email)