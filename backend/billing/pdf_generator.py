from io import BytesIO
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_RIGHT
from datetime import datetime


def generate_bill_pdf(bill):
    """Generate PDF for a bill"""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)
    
    # Container for the 'Flowable' objects
    elements = []
    
    # Define styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#2C3E50'),
        spaceAfter=30,
        alignment=TA_CENTER
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#34495E'),
        spaceAfter=12
    )
    
    # Title
    title = Paragraph("CLOTH SHOP INVOICE", title_style)
    elements.append(title)
    elements.append(Spacer(1, 0.2*inch))
    
    # Bill Info
    bill_info_data = [
        ['Bill Number:', bill.bill_number, 'Date:', bill.created_at.strftime('%d-%m-%Y %H:%M')],
        ['Customer:', bill.customer_name, 'Phone:', bill.customer_phone or 'N/A'],
    ]
    
    if bill.customer_email:
        bill_info_data.append(['Email:', bill.customer_email, '', ''])
    
    bill_info_table = Table(bill_info_data, colWidths=[1.5*inch, 2.5*inch, 1*inch, 2*inch])
    bill_info_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (2, 0), (2, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#2C3E50')),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    
    elements.append(bill_info_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Items heading
    items_heading = Paragraph("ITEMS", heading_style)
    elements.append(items_heading)
    
    # Items table
    items_data = [['#', 'Item', 'Size', 'Color', 'Qty', 'Unit Price', 'Subtotal']]
    
    for idx, bill_item in enumerate(bill.items.all(), 1):
        items_data.append([
            str(idx),
            bill_item.item.name,
            bill_item.item.size,
            bill_item.item.color,
            str(bill_item.quantity),
            f'₹{bill_item.unit_price:.2f}',
            f'₹{bill_item.subtotal:.2f}'
        ])
    
    items_table = Table(items_data, colWidths=[0.5*inch, 2*inch, 0.8*inch, 1*inch, 0.6*inch, 1.2*inch, 1.2*inch])
    items_table.setStyle(TableStyle([
        # Header
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498DB')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        
        # Body
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('ALIGN', (0, 1), (0, -1), 'CENTER'),
        ('ALIGN', (4, 1), (-1, -1), 'RIGHT'),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.HexColor('#2C3E50')),
        
        # Grid
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#BDC3C7')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        
        # Alternating row colors
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#ECF0F1')]),
    ]))
    
    elements.append(items_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Totals
    totals_data = [
        ['Subtotal:', f'₹{bill.total_amount:.2f}'],
    ]
    
    if bill.discount > 0:
        discount_amount = (bill.total_amount * bill.discount) / 100
        totals_data.append([f'Discount ({bill.discount}%):', f'-₹{discount_amount:.2f}'])
    
    if bill.tax_rate > 0:
        amount_after_discount = bill.total_amount - ((bill.total_amount * bill.discount) / 100)
        tax_amount = (amount_after_discount * bill.tax_rate) / 100
        totals_data.append([f'Tax ({bill.tax_rate}%):', f'₹{tax_amount:.2f}'])
    
    totals_data.append(['TOTAL:', f'₹{bill.final_amount:.2f}'])
    
    totals_table = Table(totals_data, colWidths=[5.5*inch, 1.5*inch])
    totals_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -2), 'Helvetica'),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -2), 11),
        ('FONTSIZE', (0, -1), (-1, -1), 14),
        ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
        ('TEXTCOLOR', (0, 0), (-1, -2), colors.HexColor('#2C3E50')),
        ('TEXTCOLOR', (0, -1), (-1, -1), colors.HexColor('#27AE60')),
        ('LINEABOVE', (0, -1), (-1, -1), 2, colors.HexColor('#27AE60')),
    ]))
    
    elements.append(totals_table)
    
    # Notes
    if bill.notes:
        elements.append(Spacer(1, 0.3*inch))
        notes_heading = Paragraph("Notes:", heading_style)
        elements.append(notes_heading)
        notes_text = Paragraph(bill.notes, styles['Normal'])
        elements.append(notes_text)
    
    # Footer
    elements.append(Spacer(1, 0.5*inch))
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=9,
        textColor=colors.HexColor('#7F8C8D'),
        alignment=TA_CENTER
    )
    footer = Paragraph("Thank you for your business!", footer_style)
    elements.append(footer)
    
    # Build PDF
    doc.build(elements)
    
    # Get the value of the BytesIO buffer
    pdf = buffer.getvalue()
    buffer.close()
    
    return pdf
