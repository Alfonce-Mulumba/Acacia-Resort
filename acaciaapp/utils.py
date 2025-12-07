from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A5, landscape
from reportlab.lib.units import mm
from reportlab.lib import colors
from django.conf import settings
from django.core.mail import EmailMessage
import os

def generate_ticket_pdf(ticket):

    # ===============================
    # 1. FILE SETUP (unchanged)
    # ===============================
    filename = f"Ticket_{ticket.ticket_number}.pdf"
    filepath = os.path.join(settings.MEDIA_ROOT, "tickets", filename)
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    c = canvas.Canvas(filepath, pagesize=landscape(A5))
    width, height = landscape(A5)

    BLUE = colors.HexColor("#1E4CCF")

    # ===============================
    # 2. LOGO — Moved higher (0.25cm from top)
    # ===============================
    # Change: shift logo UP by reducing the top offset
    logo_path = os.path.join(settings.BASE_DIR, "static", "assets", "img", "img.png")

    logo_w = 35 * mm
    logo_h = 35 * mm

    # Position: 3mm below top edge
    c.drawImage(
        str(logo_path),
        (width - logo_w) / 2,
        height - logo_h - 3 * mm,   # <-- updated
        width=logo_w,
        height=logo_h,
        preserveAspectRatio=True,
        mask="auto"
    )

    # ===============================
    # 3. TITLE — “Acacia Resort” styled
    # ===============================
    c.setFont("Helvetica-Bold", 26)

    # ---- ACACIA RESORT (same line with different colors) ----
    c.setFont("Helvetica-Bold", 26)

    text1 = "ACACIA"
    text2 = " RESORT"  # add leading space for nice separation

    # Measure widths
    w1 = c.stringWidth(text1, "Helvetica-Bold", 26)
    w2 = c.stringWidth(text2, "Helvetica-Bold", 26)

    total_width = w1 + w2
    start_x = (width - total_width) / 2  # center the combined text

    y = height - 45 * mm  # vertical position

    # Draw ACACIA (black)
    c.setFillColor(colors.black)
    c.drawString(start_x, y, text1)

    # Draw RESORT (blue)
    c.setFillColor(BLUE)
    c.drawString(start_x + w1, y, text2)

    # Subtitle
    c.setFont("Helvetica-Bold", 15)
    c.drawCentredString(width / 2, height - 65 * mm, "BOOKING TICKET")

    # ===============================
    # 4. TICKET NUMBER (top-right)
    # ===============================
    c.setFont("Helvetica-Bold", 12)
    c.setFillColor(colors.black)
    c.drawRightString(width - 10 * mm, height - 8 * mm, f"Ticket No: {ticket.ticket_number}")

    # ===============================
    # 5. CONTENT BOX — cleaner margins
    # ===============================
    box_left = 18 * mm
    box_right = width - 18 * mm
    box_top = height - 75 * mm
    box_bottom = 25 * mm

    box_w = box_right - box_left
    box_h = box_top - box_bottom

    c.roundRect(box_left, box_bottom, box_w, box_h, 10, stroke=1, fill=0)

    # Text start point, shifted down slightly for better layout
    y = box_top - 12 * mm

    c.setFont("Helvetica", 12)

    def line(text):
        nonlocal y
        c.drawCentredString(width / 2, y, text)
        y -= 7 * mm     # reduced spacing so content fits and looks tight

    # ===============================
    # 6. BOOKING CONTENT (unchanged logic)
    # ===============================
    if ticket.booking_type == "room":
        b = ticket.room_booking
        line("ROOM BOOKING")
        line(f"Customer: {b.customer_name}")
        line(f"Room Number: {b.room.room_number}")
        line(f"Check-in: {b.check_in}")
        line(f"Check-out: {b.check_out}")
        line(f"Guests: {b.people}")

    elif ticket.booking_type == "reservation":
        r = ticket.reservation_booking
        line("TABLE RESERVATION")
        line(f"Reserved By: {r.reserved_name}")
        line(f"Guests: {r.people}")
        line(f"Date: {r.date}")
        line(f"Time: {r.time}")

    elif ticket.booking_type == "event":
        e = ticket.event_booking
        line("EVENT BOOKING")
        line(f"Customer: {e.customer_name}")
        line(f"Event Type: {e.event_name}")
        line(f"Attendees: {e.attendees}")
        line(f"Date: {e.date}")

    # ===============================
    # 7. FOOTER — repositioned & aligned
    # ===============================
    c.setFont("Helvetica-Oblique", 10)
    c.setFillColor(colors.black)

    c.drawCentredString(width / 2, box_bottom - 6 * mm,
                        "Please present this ticket during check-in or event entry.")
    c.drawCentredString(width / 2, box_bottom - 11 * mm,
                        "Thank you for choosing Acacia Resort.")

    # Save PDF
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

    email = EmailMessage(
        subject,
        body,
        "Acacia Resort <no-reply@acaciaresort.co.ke>",
        [ticket.user.email]
    )

    email.attach_file(pdf_path)
    email.send()

