from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from django.conf import settings
from django.core.mail import EmailMessage

import os

def generate_ticket_pdf(ticket):
    # generate filename
    filename = f"Ticket_{ticket.ticket_number}.pdf"
    filepath = os.path.join(settings.MEDIA_ROOT, "tickets", filename)

    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    c = canvas.Canvas(filepath, pagesize=A4)
    c.setFont("Helvetica-Bold", 22)
    c.drawString(30, 800, "ACACIA RESORT - BOOKING TICKET")

    c.setFont("Helvetica-Bold", 14)
    c.drawString(30, 770, f"TICKET NUMBER: {ticket.ticket_number}")

    c.setFont("Helvetica", 12)

    # ROOM BOOKING TICKET
    if ticket.booking_type == "room":
        b = ticket.room_booking
        c.drawString(30, 740, f"Booking Type: ROOM BOOKING")
        c.drawString(30, 720, f"Customer: {b.customer_name}")
        c.drawString(30, 705, f"Room Number: {b.room.room_number}")
        c.drawString(30, 690, f"Check-in: {b.check_in}")
        c.drawString(30, 675, f"Check-out: {b.check_out}")
        c.drawString(30, 660, f"Guests: {b.people}")

    # TABLE RESERVATION TICKET
    if ticket.booking_type == "reservation":
        r = ticket.reservation
        c.drawString(30, 740, f"Booking Type: TABLE RESERVATION")
        c.drawString(30, 720, f"Reserved By: {r.reserved_name}")
        c.drawString(30, 705, f"People: {r.people}")
        c.drawString(30, 690, f"Date: {r.date}")
        c.drawString(30, 675, f"Time: {r.time}")

    # EVENT BOOKING TICKET
    if ticket.booking_type == "event":
        e = ticket.event_booking
        c.drawString(30, 740, f"Booking Type: EVENT BOOKING")
        c.drawString(30, 720, f"Customer: {e.customer_name}")
        c.drawString(30, 705, f"Event Type: {e.event_name}")
        c.drawString(30, 690, f"Attendees: {e.attendees}")
        c.drawString(30, 675, f"Date: {e.date}")

    c.setFont("Helvetica-Oblique", 10)
    c.drawString(30, 620, "Please present this ticket during check-in or event entry.")
    c.drawString(30, 605, "Thank you for choosing Acacia Resort.")

    c.showPage()
    c.save()

    return filepath


def email_ticket(ticket, pdf_path):
    subject = f"Your Ticket ({ticket.ticket_number}) - Acacia Resort"
    body = f"""
Hello {ticket.user.username},

Your booking ticket is ready.

Ticket Number: {ticket.ticket_number}

Thank you for booking with Acacia Resort.
"""

    email = EmailMessage(subject, body, "Acacia Resort <no-reply@acaciaresort.co.ke>", [ticket.user.email])
    email.attach_file(pdf_path)
    email.send()

