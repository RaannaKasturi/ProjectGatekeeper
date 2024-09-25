import hashlib

def get_domains(i_domains):
    domains = []
    for domain in i_domains.split(","):
        domain = domain.strip()
        domains.append(domain)
    return domains

def extract_subdomains(domains):
    exchange = min(domains, key=len)
    return exchange

def prefix(domain):
    domain_bytes = domain.encode()
    prefix = hashlib.blake2b(domain_bytes, digest_size=12).hexdigest()
    return prefix

def gen_cname_recs(domains):
    cname_recs = []
    for domain in domains:
        cname_rec = f"_acme-challenge.{domain}"
        cname_recs.append(cname_rec)
    return cname_recs

def gen_cname_values(domains, cf_domain, exchange):
    temp_cname_values = []
    cname_values = []
    for domain in domains:
        cname_value = prefix(domain)
        cname_value = f"{cname_value}.{domain}"
        temp_cname_values.append(cname_value)
    for cname_value in temp_cname_values:
        modified_cname_value = cname_value.replace(exchange, cf_domain)
        cname_values.append(modified_cname_value)
    return cname_values

def gen_cname(domains, cf_domain, exchange):
    cname_recs  = gen_cname_recs(domains)
    cname_values = gen_cname_values(domains, cf_domain, exchange)
    return cname_recs, cname_values

def generate_cnames(i_domains, cf_domain, wildcard):
    domains = get_domains(i_domains)
    exchange = extract_subdomains(domains=domains)
    if wildcard:
        domain = []
        domain.append(f"{exchange}")
        cname_recs, cname_values = gen_cname(domain, cf_domain, exchange)
    else:
        cname_recs, cname_values = gen_cname(domains, cf_domain, exchange)
    return cname_recs, cname_values