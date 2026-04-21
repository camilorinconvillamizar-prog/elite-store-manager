import locale
import os
from reportlab.lib.pagesizes import mm
from reportlab.pdfgen import canvas
from io import BytesIO
from datetime import datetime

try:
    locale.setlocale(locale.LC_ALL, 'es_CO.UTF-8')
except locale.Error:
    pass

def format_currency(value):
    if value is None: return "$ 0"
    try: return f"$ {value:,.0f}".replace(",", ".")
    except ValueError: return f"$ {value}"

def generate_ticket_pdf(sale_data, items_data, store_info=None):
    if store_info is None:
        store_info = {
            "name": "⚡ ELITE STORE",
            "nit": "NIT: 900.000.000-1",
            "address": "Av. Principal #123",
            "phone": "Tel: 300 000 0000"
        }

    buffer = BytesIO()
    width = 80 * mm
    height = (140 + len(items_data) * 15) * mm
    
    c = canvas.Canvas(buffer, pagesize=(width, height))
    
    # Cabecera
    y_pos = height - 15 * mm
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(width / 2.0, y_pos, store_info["name"])
    y_pos -= 6 * mm
    c.setFont("Helvetica", 9)
    c.drawCentredString(width / 2.0, y_pos, store_info["nit"])
    y_pos -= 4 * mm
    c.drawCentredString(width / 2.0, y_pos, store_info["address"])
    y_pos -= 4 * mm
    c.drawCentredString(width / 2.0, y_pos, store_info["phone"])
    
    y_pos -= 8 * mm
    c.setStrokeColorRGB(0.6, 0.6, 0.6)
    c.line(5 * mm, y_pos, width - 5 * mm, y_pos)
    y_pos -= 6 * mm
    
    # Info Venta
    c.setFont("Helvetica", 9)
    c.drawString(5 * mm, y_pos, f"Ticket: #{sale_data['id']}")
    y_pos -= 4 * mm
    c.drawString(5 * mm, y_pos, f"Fecha: {sale_data['timestamp'].strftime('%Y-%m-%d %H:%M')}")
    y_pos -= 4 * mm
    c.drawString(5 * mm, y_pos, f"Cajero: {sale_data['cashier']}")
    
    y_pos -= 6 * mm
    c.line(5 * mm, y_pos, width - 5 * mm, y_pos)
    y_pos -= 6 * mm
    
    # Items
    c.setFont("Helvetica-Bold", 8)
    c.drawString(5 * mm, y_pos, "CANT  PRODUCTO")
    c.drawRightString(width - 5 * mm, y_pos, "TOTAL")
    y_pos -= 5 * mm
    c.setFont("Helvetica", 8)
    
    subtotal = 0
    for item in items_data:
        subtotal += item['subtotal']
        name = item['name'][:18]
        c.drawString(5 * mm, y_pos, f"{int(item['quantity'])}x")
        c.drawString(15 * mm, y_pos, name)
        c.drawRightString(width - 5 * mm, y_pos, format_currency(item['subtotal']))
        y_pos -= 4 * mm
        c.setFont("Helvetica", 7)
        c.setStrokeColorRGB(0.4, 0.4, 0.4)
        c.drawString(15 * mm, y_pos, f"Unidad: {format_currency(item['price'])}")
        y_pos -= 5 * mm
        c.setFont("Helvetica", 8)
        c.setStrokeColorRGB(0, 0, 0)
    
    y_pos -= 2 * mm
    c.line(5 * mm, y_pos, width - 5 * mm, y_pos)
    y_pos -= 6 * mm
    
    # Totales
    if sale_data.get('discount', 0) > 0:
        c.setFont("Helvetica", 9)
        c.drawString(5 * mm, y_pos, "Subtotal:")
        c.drawRightString(width - 5 * mm, y_pos, format_currency(subtotal))
        y_pos -= 4 * mm
        c.drawString(5 * mm, y_pos, "Descuento:")
        c.drawRightString(width - 5 * mm, y_pos, f"- {format_currency(sale_data['discount'])}")
        y_pos -= 6 * mm

    c.setFont("Helvetica-Bold", 11)
    c.drawString(5 * mm, y_pos, "TOTAL A PAGAR:")
    c.drawRightString(width - 5 * mm, y_pos, format_currency(sale_data['total_amount']))
    y_pos -= 6 * mm
    
    # Métodos de Pago
    c.setFont("Helvetica", 8)
    if 'payment_methods' in sale_data:
        for method, amt in sale_data['payment_methods'].items():
            if amt > 0:
                y_pos -= 4 * mm
                c.drawString(5 * mm, y_pos, f"Pago en {method}:")
                c.drawRightString(width - 5 * mm, y_pos, format_currency(amt))
    
    y_pos -= 10 * mm
    c.setFont("Helvetica-Bold", 9)
    c.drawCentredString(width / 2.0, y_pos, "¡GRACIAS POR SU COMPRA!")
    
    c.showPage()
    c.save()
    
    buffer.seek(0)
    return buffer.getvalue()
