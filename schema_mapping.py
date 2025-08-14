def normalize_headers(raw_text):
    lines = raw_text.splitlines()
    headers = ["खाता संख्या", "खेवट", "नाम", "रकबा", "फसल"]  # Example schema
    rows = []

    for line in lines:
        if any(h in line for h in headers):
            continue  # Skip header lines
        row = line.split()[:len(headers)]
        rows.append(row + [""] * (len(headers) - len(row)))  # Pad if short

    return headers, rows
