from email import encoders
from email.mime.base import MIMEBase
import os
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from dotenv import load_dotenv

load_dotenv()
mail_api = os.getenv("MAIL_API")

def mail_body(generation_details):
    body = f"""
    Hello,
    Thankyou for using Project Gatekeeper to generate your SSL certificate.
    Your SSL certificate has been generated and is attached to this email. 
    Please find the attached file for your SSL certificate.

    {generation_details}

    Regards,
    Nayan Kasturi (Raanna),
    Developer & Maintainer,
    Project Gatekeeper.
    https://projectgatekeeper.vercel.app/
    """
    return body

def create_attachment(content, filename):
    attachment = MIMEBase('application', 'octet-stream')
    attachment.set_payload(content)
    encoders.encode_base64(attachment)
    attachment.add_header('Content-Disposition', f'attachment; filename="{filename}"')
    return attachment

def send_email(email, private_key, csr, cert, generation_details):
    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key['api-key'] = mail_api
    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))

    data = mail_body(generation_details)
    p_attachment = create_attachment(private_key.encode('utf-8'), "private_key.txt")
    c_attachment = create_attachment(csr.encode('utf-8'), "domain_csr.txt")
    s_attachment = create_attachment(cert.encode('utf-8'), "ssl_certificate_chain.txt")

    subject = "Project Gatekeeper - Your SSL Certificate is ready!"
    sender = {"name": "Project Gatekeeper", "email": "projectgatekeeper@silerudaagartha.eu.org"}
    reply_to = {"name": "Project Gatekeeper", "email": "gatekeeper@raannakasturi.eu.org"}
    text_content = data
    attachments = [
        {"content": p_attachment.get_payload(), "name": p_attachment.get_filename()},
        {"content": c_attachment.get_payload(), "name": c_attachment.get_filename()},
        {"content": s_attachment.get_payload(), "name": s_attachment.get_filename()},
    ]
    to = [{"email": email}]
    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(to=to, reply_to=reply_to, attachment=attachments, text_content=text_content, sender=sender, subject=subject)
    try:
        api_response = api_instance.send_transac_email(send_smtp_email)
        print("Email Sent")
        return True
    except ApiException as e:
        print("Can't send email")
        print("Exception when calling SMTPApi->send_transac_email: %s\n" % e)
        return False