import re
import time
from genPVTCSR import gen_pvt_csr
from tools import get_domains, get_ca_server, get_kid_hmac, extract_subdomains
from acme_tools import pg_client, new_account
from getTokenCert import get_tokens, verify_tokens
from gen_records import txt_recs
from dns_cf import add_txt, del_txt
from verify_txt import verify_txt
from send_mail import send_email

def cf_non_wildcard(verification_tokens, email, exchange):
    tokens = verification_tokens
    for key, value in tokens.items():
        txt_rec = txt_recs(key, exchange)
        txt_value = value[0].strip()
        try:
            del_txt(txt_rec)
        except Exception as e:
            print(f"Error deleting TXT records or no TXT records exists: {e}")
        add_txt(txt_rec, txt_value, ssl_email=email)

def cf_wildcard(verification_tokens, email, exchange):
    tokens = verification_tokens
    for key, value in tokens.items():
        txt_rec = txt_recs(key, exchange)
        print("\nTXT record:", txt_rec, "\n")
        try:
            del_txt(txt_rec)
        except Exception as e:
            print(f"Error deleting TXT records or no TXT records exists: {e}")
        for txt_value in value:
            add_txt(txt_rec, txt_value, ssl_email=email)

def verify_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email)

def validate_domains(i_domains):
    domains = []
    try:
        domains = get_domains(i_domains)
    except:
        domains = i_domains
    pattern = r'^[a-zA-Z0-9][a-zA-Z0-9-]{1,61}[a-zA-Z0-9](?:\.[a-zA-Z]{2,})+$'
    for domain in domains:
        if re.match(pattern, domain):
            continue
        else:
            return False
    return True

def verify_txt_records(verification_tokens, exchange):
    tokens = verification_tokens
    for key, value in tokens.items():
        txt_rec = key
        txt_value = value[0].strip()
        if not verify_txt(txt_rec, txt_value):
            return False
        else:
            continue
    return True

def handle_error(message):
    err = f"Error: {message}"
    return err, err, err, err

def main(i_domains, wildcard, email, ca_server, key_type, key_size=None, key_curve=None, kid=None, hmac=None):
    if i_domains == "":
        print("domain", i_domains)
        return handle_error("No domain provided")
    elif not validate_domains(i_domains):
        print("domain", i_domains)
        return handle_error("Invalid domains provided")
    else:
        print("domain", i_domains)
        if email == "":
            print("email", email)
            return handle_error("No email provided")
        elif not verify_email(email):
            print("email", email)
            return handle_error("Invalid email provided")
        else:
            print("email", email)
            if ca_server == "":
                print("ca", ca_server)
                return handle_error("No CA server provided")
            else:
                print("ca", ca_server)
                if key_type == "":
                    print("key type", key_type)
                    return handle_error("No key type provided")
                else:
                    print("key type", key_type)
                    if key_curve == "":
                        print("size", key_size)
                        print("curve", key_curve)
                        return handle_error("No key size or curve provided")
                    else:
                        print("size", key_size)
                        print("curve", key_curve)
                        print("All data filled")
    domains = get_domains(i_domains)
    exchange = extract_subdomains(domains=domains)
    if wildcard:
        domains = [exchange, f'*.{exchange}']
    ca_server_url = get_ca_server(ca_server, key_type)
    pgk_client = pg_client(ca_server_url, key_type=key_type, key_size=key_size, key_curve=key_curve)
    if pgk_client is None:
        return handle_error("Cannot create client access")
    nkid, nhmac = get_kid_hmac(ca_server)
    if nkid == 'Error' or nhmac == 'Error':
        return handle_error("Try with another provider or contact us")
    kid = nkid
    hmac = nhmac
    try:
        account = new_account(pgk_client, email, kid=kid, hmac=hmac)
    except Exception as e:
        print(f"Account Error: {e}")
        return handle_error(e)
    private_key, csr = gen_pvt_csr(domains=domains, email=email, key_type=key_type, key_curve=key_curve, key_size=key_size)
    verification_tokens, challs, order = get_tokens(pgk_client, csr, ca_server_url)
    try:
        if wildcard:
            cf_wildcard(verification_tokens, email, exchange)
        else:
            cf_non_wildcard(verification_tokens, email, exchange)
    except Exception as e:
        print(f"Error adding TXT records: {e}")
    for i in range(30):
        print(f"Waiting for {30-i} seconds", end="\r")
        time.sleep(1)
    retries = 0
    while not verify_txt_records(verification_tokens, exchange):
        print("TXT records not verified yet")
        retries = retries+1
        if retries >=50:
            break
        time.sleep(5)
    cert = verify_tokens(pgk_client, challs, order)
    for key in verification_tokens:
        txt_rec = txt_recs(key, exchange)
        try:
            del_txt(txt_rec)
            print("TXT records deleted successfully")
        except Exception as e:
            print(f"Error deleting TXT records or no TXT records exist: {e}")
    private_key = private_key.decode("utf-8")
    csr = csr.decode("utf-8")
    cert = cert.decode("utf-8")
    generation_details = f"""
    SSL Certificate for {i_domains} were generated successfully, using Project Gatekeeper, a free SSL Certificate creator tool.
    SSL Provider = {ca_server}
    Key Type = {key_type}
    Key Curve = {key_curve}
    Key Size = {key_size}
    For more details, visit: https://projectgatekeeper.vercel.app/tool/decode.html
    """
    if send_email(email, private_key, csr, cert, generation_details):
        email_status = f"Email Sent to {email}"
    else:
        email_status = f"Can't sent email to {email}"
    print(email_status)
    return private_key, csr, cert, email_status

if __name__ == "__main__":
    DOMAINS = 'thenayankasturi.eu.org'    
    ca_server = "Google" #Let's Encrypt (Testing), Let's Encrypt, Google (Testing), Google, Buypass (Testing), Buypass, ZeroSSL, SSL.com
    EMAIL = "raannakasturi@gmail.com"
    key_type = "ecc"
    key_curve = "ec384"
    key_size = "4096"
    KID = None
    HMAC = None
    private_key, csr, cert, email_status = main(i_domains=DOMAINS, wildcard=True, email=EMAIL, ca_server=ca_server, key_type=key_type, key_size=key_size,key_curve=key_curve, kid=KID, hmac=HMAC)
    print("Private Key:")
    print(private_key)
    print()
    print("CSR:")
    print(csr)
    print()
    print("Certificate:")
    print(cert)
    print()
    print(email_status)
    print()
