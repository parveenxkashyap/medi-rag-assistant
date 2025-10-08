import pdfplumber
import json
import re

pdf_path = "input/file.pdf"

data = {
    "patient_info": {},
    "tests": []
}

with pdfplumber.open(pdf_path) as pdf:
    page = pdf.pages[0]
    text = page.extract_text()
    
    def extract(regex, text):
        m = re.search(regex, text, re.IGNORECASE)
        return m.group(1).strip() if m else ""
    
    data["patient_info"] = {
        "name": extract(r"Name\s*:\s*(.*)", text).split("Collected")[0].strip(),
        "age": extract(r"Age\s*:\s*(\d+)", text),
        "gender": extract(r"Gender\s*:\s*([A-Za-z]+)", text),
        "lab_no": extract(r"Lab\s*No\.\s*:\s*([A-Za-z0-9]+)", text),
        "collected": extract(r"Collected\s*:\s*([\d:/AMPamp\s]+)", text),
        "received": extract(r"Received\s*:\s*([\d:/AMPamp\s]+)", text),
        "reported": extract(r"Reported\s*:\s*([\d:/AMPamp\s]+)", text),
        "report_status": extract(r"Report\s*Status\s*:\s*([A-Za-z]+)", text)
    }
    
    words = page.extract_words()
    
    TEST_COL_END = 272
    RESULTS_COL_END = 385
    UNITS_COL_END = 484
    
    TABLE_START_Y = 238  
    TABLE_END_Y = 678    
    
    # Group words by row 
    rows = {}
    row_threshold = 10  # Words within 10 pixels vertically are same row
    
    for word in words:
        # Only process words in table range
        if TABLE_START_Y <= word["top"] <= TABLE_END_Y:
            x0 = word["x0"]
            top = word["top"]
            text = word["text"]
            
            # Skip "TestName" header itself
            if text == "TestName" or text == "Results" or text == "Units" or text == "Bio.Ref.Interval":
                continue
            
            # Find which row this word belongs to
            row_key = None
            for existing_row_y in rows.keys():
                if abs(top - existing_row_y) < row_threshold:
                    row_key = existing_row_y
                    break
            
            if row_key is None:
                row_key = top
            
            if row_key not in rows:
                rows[row_key] = {"test_name": "", "result": "", "units": "", "interval": ""}
            
            # Assign word to column based on x0 position
            if x0 < TEST_COL_END:
                rows[row_key]["test_name"] += " " + text
            elif x0 < RESULTS_COL_END:
                rows[row_key]["result"] += " " + text
            elif x0 < UNITS_COL_END:
                rows[row_key]["units"] += " " + text
            else:  # >= 484
                rows[row_key]["interval"] += " " + text
    
    # Clean and add valid test rows
    for row_y in sorted(rows.keys()):
        row = rows[row_y]
        test_name = row["test_name"].strip()
        result = row["result"].strip()
        units = row["units"].strip()
        interval = row["interval"].strip()
        
        # Skip method lines (start with parenthesis) and LIVERPANEL
        if test_name and not test_name.startswith("(") and "LIVERPANEL" not in test_name:
            data["tests"].append({
                "test_name": test_name,
                "result": result,
                "units": units,
                "bio_ref_interval": interval
            })

# Save
with open("final_output.json", "w") as f:
    json.dump(data, f, indent=4, ensure_ascii=False)

print("Done!")
print(json.dumps(data, indent=4))
