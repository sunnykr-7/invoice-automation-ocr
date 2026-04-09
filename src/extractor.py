import re
from datetime import datetime

def extract_invoice_data(text):
    data = {}

    lines = [line.strip() for line in text.split("\n") if line.strip()]
    text_lower = text.lower()

    #  Vendor (first meaningful line)
    vendor = "Unknown"
    for line in lines[:5]:
        if any(c.isalpha() for c in line) and len(line) > 5:
            vendor = line
            break
    data["Vendor"] = vendor

    #  Amount (look for TOTAL first)
    amount = "Not Found"
    for line in lines:
        if "total" in line.lower():
            match = re.search(r'\d+\.\d{2}', line)
            if match:
                amount = match.group(0)
                break

    # fallback
    if amount == "Not Found":
        fallback = re.findall(r'\d+\.\d{2}', text)
        if fallback:
            amount = fallback[-1]

    data["Invoice Amount"] = amount

    #  Date (multiple formats)
    date_patterns = [
        r'\d{2}/\d{2}/\d{4}',
        r'\d{4}/\d{2}/\d{2}',
        r'\d{4}-\d{2}-\d{2}',
        r'\d{2}-\d{2}-\d{4}',
    ]

    found_date = None
    for pattern in date_patterns:
        match = re.search(pattern, text)
        if match:
            found_date = match.group(0)
            break

    data["Due Date"] = found_date if found_date else "Not Found"

    #  Category
    if "taxi" in text_lower or "uber" in text_lower:
        data["Category"] = "Transport"
    elif "restaurant" in text_lower or "food" in text_lower:
        data["Category"] = "Food"
    else:
        data["Category"] = "General"

    #  Ageing
    def parse_date(date_str):
        formats = ["%d/%m/%Y", "%Y/%m/%d", "%Y-%m-%d", "%d-%m-%Y"]
        for fmt in formats:
            try:
                return datetime.strptime(date_str, fmt)
            except:
                continue
        return None

    try:
        if found_date:
            due_date = parse_date(found_date)
            if due_date:
                today = datetime.today()
                data["Ageing (days)"] = (today - due_date).days
            else:
                data["Ageing (days)"] = "Unknown"
        else:
            data["Ageing (days)"] = "Unknown"
    except:
        data["Ageing (days)"] = "Unknown"

    #  Status (BONUS FEATURE)
    if isinstance(data["Ageing (days)"], int):
        if data["Ageing (days)"] > 0:
            data["Status"] = "Overdue"
        else:
            data["Status"] = "Upcoming"
    else:
        data["Status"] = "Unknown"

    return data