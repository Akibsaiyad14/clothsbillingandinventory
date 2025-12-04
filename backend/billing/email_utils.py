from django.core.mail import EmailMessage
from django.conf import settings


def send_bill_email(bill, pdf_content):
    """
    Send bill PDF to customer via email
    
    Args:
        bill: Bill object
        pdf_content: PDF file content as bytes
        
    Returns:
        bool: True if email sent successfully, False otherwise
    """
    try:
        subject = f'Invoice #{bill.bill_number} - Cloth Shop'
        
        body = f"""
Dear {bill.customer_name},

Thank you for your purchase!

Please find attached your invoice for the order placed on {bill.created_at.strftime('%B %d, %Y')}.

Invoice Details:
- Invoice Number: {bill.bill_number}
- Total Amount: ₹{bill.final_amount}

If you have any questions, please feel free to contact us.

Best regards,
Cloth Shop Team
        """
        
        email = EmailMessage(
            subject=subject,
            body=body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[bill.customer_email],
        )
        
        # Attach PDF
        email.attach(
            filename=f'invoice_{bill.bill_number}.pdf',
            content=pdf_content,
            mimetype='application/pdf'
        )
        
        email.send(fail_silently=False)
        return True
        
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        return False
