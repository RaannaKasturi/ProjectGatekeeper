from dns import resolver

def get_txt(rec):
    redirect_domain = None
    try:
        txt_answers = resolver.resolve(rec, 'TXT')
        for answer in txt_answers:
            txt_record = answer.to_text().rstrip(".")
            if txt_record.startswith('_acme-challenge'):
                redirect_domain = txt_record.split('.')[-1]
            else:
                redirect_domain = txt_record
        print(f"Resolved {rec} to {redirect_domain.strip('.')}")
        return redirect_domain.strip('"').strip('.')
    except Exception as e:
        print(f"An error occurred while resolving {rec}: {e}")
        return redirect_domain

def verify_txt(rec, expected):
    found = get_txt(rec)
    if found == expected:
        return True
    else:
        return False
