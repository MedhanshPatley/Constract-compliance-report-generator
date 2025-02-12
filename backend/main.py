'''this is the code for generating both in pdf'''
# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import json
# import google.generativeai as genai
# import PyPDF2
# from jsonschema import validate, ValidationError
# import chromadb
# import os
# from pathlib import Path
# from fill_pdf import create_contract_pdf
# from compliance_report_generator import create_compliance_report_pdf
# import base64
# import re
# #from io import BytesIO #You might need it for bytes operations

# app = Flask(__name__)
# CORS(app)

# # Gemini API Key
# GENAI_API_KEY = "AIzaSyBLRXR_EiHaFubhWNTPGUnu8I7QqVxpWlA"  # Replace with your actual API key
# try:
#     genai.configure(api_key=GENAI_API_KEY)
#     model = genai.GenerativeModel('gemini-1.5-flash')
# except Exception as e:
#     print(f"Error configuring Gemini API: {e}")
#     model = None

# # JSON Schema for Data Validation
# CONTRACT_DATA_SCHEMA = {
#     "type": "object",
#     "properties": {
#         "developer_name": {"type": "string", "minLength": 1},
#         "developer_address": {"type": "string", "minLength": 1},
#         "contractor_name": {"type": "string", "minLength": 1},
#         "contractor_address": {"type": "string", "minLength": 1},
#         "project_address": {"type": "string", "minLength": 1},
#         "contract_value": {"type": "number", "minimum": 0},
#         "contract_duration": {"type": "integer", "minimum": 1},
#         "commencement_period": {"type": "integer", "minimum": 0},
#         "payment_processing_days": {"type": "integer", "minimum": 0},
#         "termination_notice_period": {"type": "integer", "minimum": 0},
#         "arbitration_city": {"type": "string"},  # Optional fields
#         "court_jurisdiction": {"type": "string"},  # Optional fields
#         "governing_law": {"type": "string"},      # Optional fields
#         "scope_of_work": {
#             "type": "array",
#             "items": {"type": "string"}
#         },
#         "mobilization_advance": {"type": "number", "minimum": 0},
#         "retention_percentage": {"type": "number", "minimum": 0, "maximum": 100},
#         "penalty_percentage": {"type": "number", "minimum": 0, "maximum": 100},
#         "max_penalty_cap": {"type": "number", "minimum": 0, "maximum": 100},
#         "special_conditions": {
#             "type": "array",
#             "items": {"type": "string"},
#             "default": []
#         },
#         "milestones": {
#             "type": "array",
#             "items": {
#                 "type": "object",
#                 "properties": {
#                     "description": {"type": "string", "minLength": 1},
#                     "percentage": {"type": "number", "minimum": 0, "maximum": 100}
#                 },
#                 "required": ["description", "percentage"]
#             }
#         }
#     },
#     "required": [
#         "developer_name", "developer_address", "contractor_name", "contractor_address",
#         "project_address", "contract_value", "contract_duration", "commencement_period",
#         "payment_processing_days", "termination_notice_period",
#         "scope_of_work", "mobilization_advance", "retention_percentage",
#         "penalty_percentage", "max_penalty_cap", "special_conditions", "milestones"
#     ]
# }

# class RegulationManager:
#     def __init__(self, db_path: str = "regulations_db"):
#         """Initialize ChromaDB client and collection."""
#         self.client = chromadb.PersistentClient(path=db_path)
#         self.collection = self.client.get_or_create_collection(
#             name="construction_regulations",
#             metadata={"description": "Construction regulations and compliance documents"}
#         )

#     def query_compliance(self, query_text: str, top_k: int = 3):
#         """Retrieves the most relevant compliance sections."""
#         results = self.collection.query(
#             query_texts=[query_text],
#             n_results=top_k
#         )
#         return results

# # Helper Functions

# def extract_text_from_pdf(pdf_path):
#     """Extracts text from a PDF file."""
#     text = ""
#     try:
#         with open(pdf_path, 'rb') as file:
#             reader = PyPDF2.PdfReader(file)
#             for page in reader.pages:
#                 text += page.extract_text()
#     except Exception as e:
#             print(f"Error extracting text from PDF: {e}")
#             return None
#     return text

# def extract_clauses(contract_text):
#     clauses = {
#         "Commencement and Term (Article I)": r"ARTICLE I: COMMENCEMENT AND TERM(.*?)ARTICLE II:",
#         "Scope of Work (Article II)": r"ARTICLE II: SCOPE OF WORK(.*?)ARTICLE III:",
#         "Contract Value and Payment Terms (Article III)": r"ARTICLE III: CONTRACT VALUE AND PAYMENT TERMS(.*?)ARTICLE IV:",
#         "Implementation Period (Article IV)": r"ARTICLE IV: IMPLEMENTATION PERIOD(.*?)ARTICLE V:",
#         "Responsibilities of Parties (Article V)": r"ARTICLE V: RESPONSIBILITIES OF PARTIES(.*?)ARTICLE VI:",
#         "Force Majeure (Article VI)": r"ARTICLE VI: FORCE MAJEURE(.*?)ARTICLE VII:",
#         "Dispute Resolution (Article VII)": r"ARTICLE VII: DISPUTE RESOLUTION(.*?)ARTICLE VIII:",
#         "Amendments and Termination (Article VIII)": r"ARTICLE VIII: AMENDMENTS AND TERMINATION(.*?)ARTICLE IX:",
#         "General Provisions (Article IX)": r"ARTICLE IX: GENERAL PROVISIONS(.*)IN WITNESS WHEREOF"
#     }

#     extracted_clauses = {}
#     for clause, pattern in clauses.items():
#         match = re.search(pattern, contract_text, re.DOTALL)
#         if match:
#             extracted_clauses[clause] = match.group(1).strip()
#         else:
#             extracted_clauses[clause] = "Clause not found."

#     return extracted_clauses


# def generate_compliance_report(clause_description, clause_text, regulations):
#     """Generates a structured compliance report using a language model."""
#     if model is None:
#         raise ValueError("Gemini API not initialized.")

#     prompt = f"""
#     Analyze the following contract clause and generate a detailed compliance report.
#     Format the report with clear sections and findings.

#     Contract Clause:
#     {clause_text}

#     Regulations:
#     {regulations["documents"]}

#     Please structure the report in the following format:

#     Clause Description:{clause_description}

#     1. Compliance Status: [State if compliant or non-compliant]
#     2. Analysis:
#        - Detailed explanation of compliance status
#        - Specific regulations referenced
#     3. Recommendations (if any):
#        - Suggested improvements
#        - Required changes for compliance
#     4. References:
#        - Relevant regulation sections
#        - Applicable standards

#     Be specific and detailed in your analysis.
#     """

#     try:
#         response = model.generate_content(prompt)
#         compliance_report = response.text
#         return compliance_report
#     except Exception as e:
#         print(f"Error generating compliance report: {e}")
#         return f"Compliance analysis could not be completed due to error: {e}"

# @app.get("/")
# def read_root():
#     return {"message": "Hello, world!"}

# @app.route('/process-contract', methods=['POST'])
# def process_contract():
#     try:
#         data = request.get_json()
#         print("Received data:", data)  # Log the received data

#         # 1. Data Validation using jsonschema
#         try:
#             validate(instance=data, schema=CONTRACT_DATA_SCHEMA)
#         except ValidationError as e:
#             print(f"Data validation error: {e}")
#             return jsonify({"error": f"Invalid data format: {e}"}), 400

#         # 2. Extract Text from PDF Template
#         pdf_path = "./template/DEVELOPER_CONTRACTOR.pdf"  # Replace with the actual path
#         contract_template_text = extract_text_from_pdf(pdf_path)

#         if contract_template_text is None:
#             return jsonify({"error": "Failed to extract text from PDF template"}), 500

#         # 3. Call the Gemini API
#         if model is None:
#             return jsonify({"error": "Gemini API not initialized. Check API key."}), 500

#         try:
#             # Modified prompt to exclude compliance information
#             prompt = f"""
#             Fill in the following contract template with the provided data.
#             Do *NOT* include any compliance checks or compliance related details.
#             ONLY provide the filled in contract.

#             Contract Template:
#             {contract_template_text}

#             Data:
#             {json.dumps(data, indent=2)}
#             """
#             response = model.generate_content(prompt)
#             contract_text = response.text #This part ONLY includes Contract Text
#         except Exception as e:
#             print(f"Gemini API error: {e}")
#             return jsonify({"error": f"Error communicating with Gemini API: {e}"}), 500

#         # 4. Clause Extraction, Regulation Retrieval, and Compliance Report Generation
#         compliance_reports = []
#         full_compliance_report_text = ""  # Initialize the string
#         try:
#             # Initialize RegulationManager
#             reg_manager = RegulationManager()
#             print("✅✅✅✅✅✅Regulation Manager initialized succesfully")

#             # Extract Clauses
#             clauses = extract_clauses(contract_text)

#             for clause_description, clause_text in clauses.items():
#                 # Query ChromaDB
#                 results = reg_manager.query_compliance(clause_description)

#                 # Generate Compliance Report
#                 report = generate_compliance_report(clause_description, clause_text, results)  # Pass clause description AND text
#                 compliance_reports.append({"clause_description": clause_description, "report": report})

#                 # Append report to the combined text
#                 full_compliance_report_text += f"Clause Description: {clause_description}\n\n{report}\n\n"  # Add separators

#         except Exception as e:
#             print(f"Error in compliance check process: {e}")
#             compliance_reports = [{"clause_description": "Error", "report": f"Compliance check could not be completed: {e}"}]
#             full_compliance_report_text = f"Error in compliance check process: {e}"

#         # 5. Generate the PDF Contract first!
#         try:

#             # Option 1: Save PDF to a file
#             pdf_filename = "generated_contract.pdf"
#             create_contract_pdf(contract_text, pdf_filename) # Now passing contract_text to pdf_generator
#             print(f"PDF generated successfully: {pdf_filename}")

#         except Exception as e:
#             print(f"Error generating PDF: {e}")
#             return jsonify({"error": f"Error generating PDF: {e}"}), 500

#         # 6. Generate the compliance report pdf - Add full_compliance_report_text implementation with safety in mind
#         try:
#             # Validate final PDF Report before proceeding
#             if isinstance(full_compliance_report_text,str) and len(full_compliance_report_text) > 0:
#             #Call it at the very end - create_compliance_report_pdf and pass the full_compliance_report_text and save it as well
#                 compliance_pdf_filename = "compliance_report.pdf"
#                 create_compliance_report_pdf(full_compliance_report_text, compliance_pdf_filename)
#                 print(f"Compliance PDF file generated successfully: {compliance_pdf_filename}") #Check the console to ensure files has been generated
#             else:
#                 compliance_pdf_filename = "compliance_report.pdf"
#                 create_compliance_report_pdf(f"There was a problem generating the report from the PDF file", compliance_pdf_filename)
#                 print(f"Compliance PDF file had a problem generating, but will create a basic report in PDF {compliance_pdf_filename}") #Report problem
#         except Exception as e:
#             print(f"Error generating compliance report PDF: {e}")
#             return jsonify({"error": f"Error generating compliance report PDF: {e}"}), 500

#         # Create the response, including the extracted clauses and compliance reports
#         result = {
#             "contract_text": contract_text,
#             "compliance_reports": compliance_reports,
#             "pdf_generated": True #Add a message to the result
#         }

#         return jsonify(result)

#     except Exception as e:
#         print("General error:", e)
#         return jsonify({"error": str(e)}), 500

# if __name__ == '__main__':
#     app.run(debug=True, host='0.0.0.0')


'''this below code is responsive for the generating contract and compliance pdf and sending in the frontend'''
from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import google.generativeai as genai
import PyPDF2
from jsonschema import validate, ValidationError
import chromadb
import os
from pathlib import Path
from fill_pdf import create_contract_pdf
from compliance_report_generator import create_compliance_report_pdf
import base64
import re
#from io import BytesIO #You might need it for bytes operations

app = Flask(__name__)
CORS(app)

# Gemini API Key
GENAI_API_KEY = "AIzaSyD_NxnDGvp8huiD9UUvGCw7R98KJzOObSQ"  # Replace with your actual API key
try:
    genai.configure(api_key=GENAI_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    print(f"Error configuring Gemini API: {e}")
    model = None

# JSON Schema for Data Validation
CONTRACT_DATA_SCHEMA = {
    "type": "object",
    "properties": {
        "developer_name": {"type": "string", "minLength": 1},
        "developer_address": {"type": "string", "minLength": 1},
        "contractor_name": {"type": "string", "minLength": 1},
        "contractor_address": {"type": "string", "minLength": 1},
        "project_address": {"type": "string", "minLength": 1},
        "contract_value": {"type": "number", "minimum": 0},
        "contract_duration": {"type": "integer", "minimum": 1},
        "commencement_period": {"type": "integer", "minimum": 0},
        "payment_processing_days": {"type": "integer", "minimum": 0},
        "termination_notice_period": {"type": "integer", "minimum": 0},
        "arbitration_city": {"type": "string"},  # Optional fields
        "court_jurisdiction": {"type": "string"},  # Optional fields
        "governing_law": {"type": "string"},      # Optional fields
        "scope_of_work": {
            "type": "array",
            "items": {"type": "string"}
        },
        "mobilization_advance": {"type": "number", "minimum": 0},
        "retention_percentage": {"type": "number", "minimum": 0, "maximum": 100},
        "penalty_percentage": {"type": "number", "minimum": 0, "maximum": 100},
        "max_penalty_cap": {"type": "number", "minimum": 0, "maximum": 100},
        "special_conditions": {
            "type": "array",
            "items": {"type": "string"},
            "default": []
        },
        "milestones": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "description": {"type": "string", "minLength": 1},
                    "percentage": {"type": "number", "minimum": 0, "maximum": 100}
                },
                "required": ["description", "percentage"]
            }
        }
    },
    "required": [
        "developer_name", "developer_address", "contractor_name", "contractor_address",
        "project_address", "contract_value", "contract_duration", "commencement_period",
        "payment_processing_days", "termination_notice_period",
        "scope_of_work", "mobilization_advance", "retention_percentage",
        "penalty_percentage", "max_penalty_cap", "special_conditions", "milestones"
    ]
}

class RegulationManager:
    def __init__(self, db_path: str = "regulations_db"):
        """Initialize ChromaDB client and collection."""
        self.client = chromadb.PersistentClient(path=db_path)
        self.collection = self.client.get_or_create_collection(
            name="construction_regulations",
            metadata={"description": "Construction regulations and compliance documents"}
        )

    def query_compliance(self, query_text: str, top_k: int = 3):
        """Retrieves the most relevant compliance sections."""
        results = self.collection.query(
            query_texts=[query_text],
            n_results=top_k
        )
        return results

# Helper Functions

def extract_text_from_pdf(pdf_path):
    """Extracts text from a PDF file."""
    text = ""
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                text += page.extract_text()
    except Exception as e:
            print(f"Error extracting text from PDF: {e}")
            return None
    return text

def extract_clauses(contract_text):
    clauses = {
        "Commencement and Term (Article I)": r"ARTICLE I: COMMENCEMENT AND TERM(.*?)ARTICLE II:",
        "Scope of Work (Article II)": r"ARTICLE II: SCOPE OF WORK(.*?)ARTICLE III:",
        "Contract Value and Payment Terms (Article III)": r"ARTICLE III: CONTRACT VALUE AND PAYMENT TERMS(.*?)ARTICLE IV:",
        "Implementation Period (Article IV)": r"ARTICLE IV: IMPLEMENTATION PERIOD(.*?)ARTICLE V:",
        "Responsibilities of Parties (Article V)": r"ARTICLE V: RESPONSIBILITIES OF PARTIES(.*?)ARTICLE VI:",
        "Force Majeure (Article VI)": r"ARTICLE VI: FORCE MAJEURE(.*?)ARTICLE VII:",
        "Dispute Resolution (Article VII)": r"ARTICLE VII: DISPUTE RESOLUTION(.*?)ARTICLE VIII:",
        "Amendments and Termination (Article VIII)": r"ARTICLE VIII: AMENDMENTS AND TERMINATION(.*?)ARTICLE IX:",
        "General Provisions (Article IX)": r"ARTICLE IX: GENERAL PROVISIONS(.*)IN WITNESS WHEREOF"
    }

    extracted_clauses = {}
    for clause, pattern in clauses.items():
        match = re.search(pattern, contract_text, re.DOTALL)
        if match:
            extracted_clauses[clause] = match.group(1).strip()
        else:
            extracted_clauses[clause] = "Clause not found."

    return extracted_clauses


def generate_compliance_report(clause_description, clause_text, regulations):
    """Generates a structured compliance report using a language model."""
    if model is None:
        raise ValueError("Gemini API not initialized.")

    prompt = f"""
    Analyze the following contract clause and generate a detailed compliance report.
    Format the report with clear sections and findings.

    Contract Clause:
    {clause_text}

    Regulations:
    {regulations["documents"]}

    Please structure the report in the following format:

    Clause Description:{clause_description}

    1. Compliance Status: [State if compliant or non-compliant]
    2. Analysis:
       - Detailed explanation of compliance status
       - Specific regulations referenced
    3. Recommendations (if any):
       - Suggested improvements
       - Required changes for compliance
    4. References:
       - Relevant regulation sections
       - Applicable standards

    Be specific and detailed in your analysis.
    """

    try:
        response = model.generate_content(prompt)
        compliance_report = response.text
        return compliance_report
    except Exception as e:
        print(f"Error generating compliance report: {e}")
        return f"Compliance analysis could not be completed due to error: {e}"

@app.get("/")
def read_root():
    return {"message": "Hello, world!"}

@app.route('/process-contract', methods=['POST'])
def process_contract():
    try:
        data = request.get_json()
        print("Received data:", data)  # Log the received data

        # 1. Data Validation using jsonschema
        try:
            validate(instance=data, schema=CONTRACT_DATA_SCHEMA)
        except ValidationError as e:
            print(f"Data validation error: {e}")
            return jsonify({"error": f"Invalid data format: {e}"}), 400

        # 2. Extract Text from PDF Template
        pdf_path = "./template/DEVELOPER_CONTRACTOR.pdf"  # Replace with the actual path
        contract_template_text = extract_text_from_pdf(pdf_path)

        if contract_template_text is None:
            return jsonify({"error": "Failed to extract text from PDF template"}), 500

        # 3. Call the Gemini API
        if model is None:
            return jsonify({"error": "Gemini API not initialized. Check API key."}), 500

        try:
            # Modified prompt to exclude compliance information
            prompt = f"""
            Fill in the following contract template with the provided data.
            Do *NOT* include any compliance checks or compliance related details.
            ONLY provide the filled in contract.

            Contract Template:
            {contract_template_text}

            Data:
            {json.dumps(data, indent=2)}
            """
            response = model.generate_content(prompt)
            contract_text = response.text #This part ONLY includes Contract Text
        except Exception as e:
            print(f"Gemini API error: {e}")
            return jsonify({"error": f"Error communicating with Gemini API: {e}"}), 500

        # 4. Clause Extraction, Regulation Retrieval, and Compliance Report Generation
        compliance_reports = []
        full_compliance_report_text = ""  # Initialize the string
        try:
            # Initialize RegulationManager
            reg_manager = RegulationManager()
            print("✅✅✅✅✅✅Regulation Manager initialized succesfully")

            # Extract Clauses
            clauses = extract_clauses(contract_text)

            for clause_description, clause_text in clauses.items():
                # Query ChromaDB
                results = reg_manager.query_compliance(clause_description)

                # Generate Compliance Report
                report = generate_compliance_report(clause_description, clause_text, results)  # Pass clause description AND text
                compliance_reports.append({"clause_description": clause_description, "report": report})

                # Append report to the combined text
                full_compliance_report_text += f"Clause Description: {clause_description}\n\n{report}\n\n"  # Add separators

        except Exception as e:
            print(f"Error in compliance check process: {e}")
            compliance_reports = [{"clause_description": "Error", "report": f"Compliance check could not be completed: {e}"}]
            full_compliance_report_text = f"Error in compliance check process: {e}"

        # 5. Generate the PDF Contract first!
        contract_pdf_base64 = None
        try:
            pdf_filename = "generated_contract.pdf"
            create_contract_pdf(contract_text, pdf_filename)
            print(f"PDF generated successfully: {pdf_filename}")

            with open(pdf_filename, "rb") as pdf_file:
                contract_pdf_base64 = base64.b64encode(pdf_file.read()).decode('utf-8')  # Encode the PDF to base64

            os.remove(pdf_filename)  # Clean up the temporary file

        except Exception as e:
            print(f"Error generating PDF: {e}")
            return jsonify({"error": f"Error generating PDF: {e}"}), 500

       # 6. Generate the compliance report pdf
        compliance_pdf_base64 = None  # Initialize
        try:
            compliance_pdf_filename = "compliance_report.pdf"
            create_compliance_report_pdf(full_compliance_report_text, compliance_pdf_filename)
            print(f"Compliance PDF file generated successfully: {compliance_pdf_filename}")

            with open(compliance_pdf_filename, "rb") as pdf_file:
                compliance_pdf_base64 = base64.b64encode(pdf_file.read()).decode('utf-8')  # Encode to Base64

            os.remove(compliance_pdf_filename)  # Clean up the temporary file

        except Exception as e:
            print(f"Error generating compliance report PDF: {e}")
            return jsonify({"error": f"Error generating compliance report PDF: {e}"}), 500

        # Create the response, including the extracted clauses, compliance reports and PDFs in base64
        result = {
            "contract_text": contract_text,
            "compliance_reports": compliance_reports,
            "pdf_generated": True,
            "contract_pdf_base64": contract_pdf_base64,  # base64 encoded string
            "compliance_pdf_base64": compliance_pdf_base64   # base64 encoded string
        }

        return jsonify(result)

    except Exception as e:
        print("General error:", e)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')