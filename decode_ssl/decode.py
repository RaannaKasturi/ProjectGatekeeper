import os
import subprocess
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat
from cryptography.hazmat.primitives.asymmetric import ec, rsa
from datetime import datetime
import pytz

def get_date(date):
    date = datetime.fromisoformat(date)
    timezone = pytz.timezone('Asia/Kolkata')
    local_datetime = date.astimezone(timezone)
    formatted_date = local_datetime.strftime('%d %B, %Y %H:%M:%S %z')
    day = local_datetime.day
    ordinal_suffix = 'th' if 4 <= day <= 20 else {1: 'st', 2: 'nd', 3: 'rd'}.get(day % 10, 'th')
    formatted_date_with_suffix = formatted_date.replace(f"{day}", f"{day}{ordinal_suffix}")
    return formatted_date_with_suffix

def check_expiry(date):
    date = datetime.fromisoformat(date)
    timezone = pytz.timezone('Asia/Kolkata')
    current_date = datetime.now(timezone)
    days_left = (date - current_date).days
    if days_left > 0:
        return f"No ({days_left} days till expiration)"
    else:
        return f"Yes ({abs(days_left)} days since expired)"
    
def get_key_data(public_key):
    if isinstance(public_key, ec.EllipticCurvePublicKey):
        public_key_curve = public_key.curve.name
        public_key_size = public_key.curve.key_size
        data = {
            "type": f"ECDSA ({public_key_curve})",
            "size": f"{public_key_size} bits"
        }
    elif isinstance(public_key, rsa.RSAPublicKey):
        public_key_size = public_key.key_size
        data = {
            "type": "RSA",
            "size": f"{public_key_size} bits"
        }
    else:
        data = {
            "type": "Unknown",
            "size": "Unknown"
        }
    return data

def general_info(cert, public_key):
    common_name = cert.subject.get_attributes_for_oid(x509.NameOID.COMMON_NAME)[0].value
    print(common_name)
    sans = cert.extensions.get_extension_for_class(x509.SubjectAlternativeName).value.get_values_for_type(x509.DNSName)
    not_valid_after = get_date(str(cert.not_valid_after_utc))
    not_valid_before = get_date(str(cert.not_valid_before_utc))
    expiry = check_expiry(str(cert.not_valid_after_utc))
    key_data = get_key_data(public_key)
    signature_algorithm = cert.signature_algorithm_oid._name
    serial_number = f"{cert.serial_number} ({hex(cert.serial_number)})"
    gen_info = {
        "common_name": common_name,
        "sans": sans,
        "not_valid_after": not_valid_after,
        "not_valid_before": not_valid_before,
        "expiry": expiry,
        "key_data": key_data,
        "signature_algorithm": signature_algorithm,
        "serial_number": serial_number
    }
    return gen_info

def issuer_info(cert):
    issuer = None; organization = None; country = None
    issuer = cert.issuer.get_attributes_for_oid(x509.NameOID.COMMON_NAME)[0].value
    organization = cert.issuer.get_attributes_for_oid(x509.NameOID.ORGANIZATION_NAME)[0].value
    country = cert.issuer.get_attributes_for_oid(x509.NameOID.COUNTRY_NAME)[0].value
    return {
        "issuer": issuer,
        "organization": organization,
        "country": country
    }

def extenstions_data(cert):
    authorityinfo = None; ocsp_url = None; ca_issuer_url = None; subject_alt_name = None
    if (tempdata1 := cert.extensions.get_extension_for_oid(x509.OID_AUTHORITY_KEY_IDENTIFIER).value.key_identifier):
        authorityKeyIdentifier = ':'.join(f'{b:02X}' for b in tempdata1)
    else:
        authorityKeyIdentifier = None
    if (subject := cert.extensions.get_extension_for_oid(x509.OID_SUBJECT_KEY_IDENTIFIER).value.digest):
        subjectKeyIdentifier = ':'.join(f'{b:02X}' for b in subject)
    else:
        subjectKeyIdentifier = None
    if (key_usage := cert.extensions.get_extension_for_oid(x509.OID_KEY_USAGE).value):
        key_usage_info = list(vars(key_usage).items())
        key_usage_data =[]
        for item in key_usage_info:
            key_usage_data.append(f"{item[0][1:]} : {item[1]}")
        key_usage_data = key_usage_data
    else:
        key_usage_data = None
    if (ext_key_usage := cert.extensions.get_extension_for_oid(x509.OID_EXTENDED_KEY_USAGE).value):
        ext_key_usage_data = [oid._name for oid in ext_key_usage]
    else:
        ext_key_usage_data = None
    crl_distribution_points = []
    try:
        crl_extension = cert.extensions.get_extension_for_oid(x509.OID_CRL_DISTRIBUTION_POINTS)
        for distribution_point in crl_extension.value:
            # Extracting the full names (URIs)
            if distribution_point.full_name:
                uris = [name.value for name in distribution_point.full_name]
                crl_distribution_points.extend(uris)
    except x509.ExtensionNotFound:
        crl_distribution_points.append("No CRL Distribution Points extension")
    authorityinfo = cert.extensions.get_extension_for_oid(x509.OID_AUTHORITY_INFORMATION_ACCESS).value
    ocsp_url = authorityinfo[0].access_location.value
    ca_issuer_url = authorityinfo[1].access_location.value
    authority_info_data = {
        "ocsp_url": ocsp_url,
        "ca_issuer_url": ca_issuer_url
    }
    subject_alt_name = cert.extensions.get_extension_for_oid(x509.OID_SUBJECT_ALTERNATIVE_NAME).value.get_values_for_type(x509.DNSName)    
    return {
        "authorityKeyIdentifier": authorityKeyIdentifier,
        "subjectKeyIdentifier": subjectKeyIdentifier,
        "key_usage": key_usage_data,
        "extended_key_usage": ext_key_usage_data,
        "crl_distribution_points": crl_distribution_points,
        "authority_info": authority_info_data,
        "subject_alt_name": subject_alt_name
    }

def get_openssl_data(cert_file):
    result1 = subprocess.run(["openssl", "x509", "-in", cert_file, "-text", "-noout"], capture_output=True, text=True)
    result2 = subprocess.run(['openssl', 'asn1parse', '-in', cert_file], capture_output=True, text=True)
    data = {
        'raw_openssl_data': result1.stdout,
        'openssl_asn1parse_data': result2.stdout
    }
    return data

def decode_ssl_certificate(cert):
    subject = cert.subject.get_attributes_for_oid(x509.NameOID.COMMON_NAME)[0].value
    with open(f'{subject}.pem', 'wb') as cert_file:
        cert_file.write(cert.public_bytes(Encoding.PEM))
    public_key = cert.public_key()
    general_info_data = general_info(cert, public_key)
    issuer_info_data = issuer_info(cert)
    extensions_data_data = extenstions_data(cert)
    raw_openssl_data = get_openssl_data(f'{subject}.pem')
    os.remove(f'{subject}.pem')
    data = {
        "general_info": general_info_data,
        "issuer_info": issuer_info_data,
        "extensions_data": extensions_data_data,
        "raw_openssl_data": raw_openssl_data
    }
    return data
