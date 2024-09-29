import csv
import re
from fpdf import FPDF
import os

out_path = f"{os.path.expanduser('~')}\\Desktop\\Ph-Resumes"

def create_pdf(company_name: str, address: str, place: str):
    pdf = FPDF()
    pdf.set_margins(25.0, 20.0, 25.0)
    pdf.add_page()

    # Address bar
    pdf.set_font("Times", size=12)
    text = f"""PHEMMY CHEPKWONY
P.O BOX 2870-20100,
NAKURU, KENYA.
Email: phemmychepkwony78@gmail.com
Contact: 0705 306797/0111 723556

HUMAN RESOURCE,
{(company_name).upper()}
{(address).upper()},
{(place).upper()}.

Dear Sir/Madam,

"""
    pdf.multi_cell(0, 8, text)

    # REF line
    pdf.set_font("Times", "U", 12)
    text = "REF: APPLICATION FOR A ACCOUNTING INTERN POSITION"
    pdf.multi_cell(0, 7, text)

    # Body
    pdf.set_font("Times", size=12)
    text = """I am writing to express my strong interest in working for your company, with my knowledge in accounting, data entry and analysis, and basic computer skills, I am confident in my ability to contribute to the efficient operations for the company. I am looking forward to graduate in December with a degree in accounting and finance from Kabarak university. I have gained valuable experience in customer service and networking, data entry, invoicing, management both in time management and leadership. I am a quick learner, known for my attention to detail and I have demonstrated the ability to adapt to new tasks and responsibilities swiftly.
What sets me apart is my commitment to providing excellent services conveniently. I understand the importance of creating a positive and welcoming working environment and I am dedicated to ensure a pleasant working environment. My caring and self-motivated nature, coupled with strong communication skills make me well-suited for a role to work for the company. With my skills and attributes, I am eager to contribute to the success of the company.
Thank you for considering my application. I look forward to hearing from you through my address.

Yours faithfully, 
Phemmy chepkwony."""

    pdf.multi_cell(0, 7, text)
    pdf.output(f"{out_path}\\{company_name} - AL.pdf")


#create_pdf("ABDIRIZACK BISHAR ARESS & ASSOCIATES", "P.O. BOX 567 - 00622", "NAIROBI")

# Function to extract the city (location) from the address
def extract_location_from_address(address):
    # Split the address by common delimiters (comma, dash, etc.)
    parts = address.split(' ')
    
    # Known cities (can be expanded)
    known_cities = ('NAIROBI', 'MOMBASA', 'KISUMU', 'ELDORET')
    
    # Iterate through the parts to find a valid city name
    for part in parts:
        # Strip and uppercase for comparison
        cleaned_part = part.strip().upper()
        
        # If the part matches a known city, return it
        if cleaned_part in known_cities:
            return cleaned_part
    
    # Default to the last part if no known city is found
    return parts[-1].strip() if parts else ''

# Function to split emails by multiple possible delimiters (comma, semicolon, etc.)
def split_emails(email_string):
    # Split by common separators (comma, semicolon, space) and remove any surrounding whitespace
    emails = re.split(r'[;,/]\s*', email_string)
    return [email.strip() for email in emails if email.strip()]  # Return non-empty emails

raw_data_path = f"{os.path.expanduser('~')}\\Desktop\\Formatted Test Data001.txt"
csv_path = f"{os.path.expanduser('~')}\\Desktop\\Csv Data001.csv"
with open(raw_data_path, 'r', encoding='utf-8') as raw_data:
    lines = raw_data.readlines()

with open(csv_path, 'a', newline='', encoding='utf-8') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['COMPANY NAME', 'ADDRESS', 'LOCATION', 'EMAIL', 'SECONDARY EMAIL', 'FULL PATH'])

    name = address = location = email = secondary_email = full_path = ''
    count = 1
    for line in lines:
        if line.startswith(f"[{count}]Name: "):
            name = line.split("Name: ")[1].strip()
            print(name)

        elif line.startswith(f"[{count}]Address: "):
            address = line.split("Address: ")[1].strip().upper()
            for city in ('NAIROBI', 'MOMBASA', 'KISUMU', 'ELDORET', 'KENYA', ',', '/', 'GPO'):
                if city in address:
                    address = address.replace(city, "")
            print(address)

        elif line.startswith(f"[{count}]Full address: "):
            full_address = line.split("Full address: ")[1].strip()
            location = extract_location_from_address(full_address)
            print(location)

        elif line.startswith(f"[{count}]Email: "):
            email_string = line.split("Email: ")[1].strip()
            emails = split_emails(email_string)  # Use the function to split emails
            email = emails[0] if emails else ''
            secondary_email = (', '.join(map(str, emails[1:]))) if len(emails) > 1 else ''
            print(email)
            print(secondary_email)

            try:
                create_pdf(name, address, location)
            except:
                pass
            if os.path.exists(f"{out_path}\\{name} - AL.pdf"):
                full_path = f"{out_path}\\{name} - AL.pdf"

            csv_writer.writerow([name, address, location, email, secondary_email, full_path])



            name = address = location = email = secondary_email = full_path = ''
            count += 1
        else:
            continue

