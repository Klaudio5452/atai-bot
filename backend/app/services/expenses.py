"""
Expense manager:
 - Accepts ExpenseRequest (list of items)
 - Produces CSV (string) and PDF (base64)
 - Includes a tiny mocked OCR helper (for future upload parsing)
"""
import pandas as pd
import base64
import io
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

def mock_parse_receipt_image(image_bytes: bytes):
    """
    Mock OCR: returns a sample parsed expense. Replace with real OCR later (Tesseract or cloud OCR).
    """
    return {"date":"2025-01-01", "type":"Taxi", "amount":18.5, "currency":"EUR", "description":"Airport taxi"}

class ExpenseManager:
    def __init__(self):
        pass

    def generate_report(self, req):
        # req is pydantic model (ExpenseRequest)
        items = [dict(i) for i in req.items] if getattr(req, "items", None) else []
        df = pd.DataFrame(items)
        if df.empty:
            total = 0.0
        else:
            total = float(df['amount'].sum())

        currency = req.invoice_currency or 'EUR'

        # CSV in-memory
        csv_buffer = io.StringIO()
        df.to_csv(csv_buffer, index=False)
        csv_b64 = base64.b64encode(csv_buffer.getvalue().encode()).decode()

        # PDF generation (simple layout)
        pdf_buffer = io.BytesIO()
        c = canvas.Canvas(pdf_buffer, pagesize=A4)
        c.setFont('Helvetica', 12)
        title = f"Expense report — {req.company or 'Company'}"
        c.drawString(40, 800, title)
        y = 780
        if not df.empty:
            for idx, row in df.iterrows():
                line = f"{row.get('date','')}\t{row.get('type','')}\t{row.get('amount','')} {row.get('currency','')}\t{row.get('description','')}"
                c.drawString(40, y, line)
                y -= 15
                if y < 60:
                    c.showPage()
                    y = 800
        c.drawString(40, max(40, y-20), f"Total: {total} {currency}")
        c.save()
        pdf_buffer.seek(0)
        pdf_b64 = base64.b64encode(pdf_buffer.read()).decode()

        return {"total": total, "currency": currency, "csv": csv_b64, "pdf": pdf_b64}
