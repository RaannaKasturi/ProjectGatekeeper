from gen_records import gen_cname
from tools import get_domains, extract_subdomains

def gen_client_cnames(i_domains, cf_domain):
    domains = get_domains(i_domains)
    exchange = extract_subdomains(domains=domains)
    cname_recs, cname_values = gen_cname(domains, cf_domain, exchange)
    return cname_recs, cname_values
