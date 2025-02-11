import chromadb
import json
from typing import List, Dict
from pathlib import Path

class ConstructionRegulationManager:
    def __init__(self, db_path: str = "regulations_db"):
        """Initialize ChromaDB client and collection."""
        self.client = chromadb.PersistentClient(path=db_path)
        self.collection = self.client.get_or_create_collection(
            name="construction_regulations",
            metadata={"description": "Indian construction regulations and guidelines"}
        )
        
    def add_regulations_from_json(self, json_file_path: str):
        """Add regulations from a JSON file."""
        with open(json_file_path, 'r', encoding='utf-8') as f:
            regulations = json.load(f)
            
        documents = []
        metadatas = []
        ids = []
        
        for idx, reg in enumerate(regulations):
            documents.append(reg['text'])
            metadatas.append({
                'category': reg['category'],
                'source': reg['source'],
                'section': reg.get('section', ''),
                'relevance': reg.get('relevance', '')
            })
            ids.append(f"reg_{idx}")
            
        self.collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )

# Enhanced construction regulations dataset
CONSTRUCTION_REGULATIONS = [
    # Safety Regulations
    {
        "text": "All construction sites must maintain proper safety barriers, warning signs, and PPE requirements. Sites operating above 2 meters height require fall protection systems.",
        "category": "safety",
        "source": "National Building Code 2016",
        "section": "Chapter 3 - Site Safety",
        "relevance": "Worker and Site Safety"
    },
    {
        "text": "Construction projects must maintain minimum 5% retention money until defect liability period completion (12 months). Progressive payments should align with work completion milestones.",
        "category": "payment_terms",
        "source": "Standard Construction Contract Guidelines",
        "section": "Payment Terms",
        "relevance": "Financial Compliance"
    },
    {
        "text": "All construction activities generating noise must be restricted between 6 AM to 10 PM in residential areas. Noise levels should not exceed 65 dB during daytime.",
        "category": "environmental",
        "source": "Environmental Protection Rules",
        "section": "Noise Regulations",
        "relevance": "Environmental Compliance"
    },
    {
        "text": "Contractors must register all workers under relevant labor laws. Maintain documentation of working hours, wages, and benefits as per Contract Labour Act.",
        "category": "labor",
        "source": "Contract Labour Regulations",
        "section": "Worker Registration",
        "relevance": "Labor Compliance"
    },
    {
        "text": "Construction materials must meet BIS standards. Quality certificates for steel, cement, and other critical materials must be maintained on site.",
        "category": "materials",
        "source": "Material Quality Standards",
        "section": "Material Specifications",
        "relevance": "Quality Control"
    },
    {
        "text": "Project timeline extensions beyond 10% of original duration require formal approval. Delays attracting penalties must be documented with justification.",
        "category": "timeline",
        "source": "Contract Management Guidelines",
        "section": "Project Timeline",
        "relevance": "Project Management"
    },
    {
        "text": "Disputes shall be first resolved through mutual discussion, followed by mediation before arbitration. Arbitration to be conducted under Indian Arbitration Act.",
        "category": "dispute_resolution",
        "source": "Contract Guidelines",
        "section": "Dispute Resolution",
        "relevance": "Legal Compliance"
    }
]

def setup_regulations_db():
    """Setup the regulations database with construction regulations."""
    data_dir = Path("regulations_data")
    data_dir.mkdir(exist_ok=True)
    
    regulations_file = data_dir / "construction_regulations.json"
    with open(regulations_file, 'w', encoding='utf-8') as f:
        json.dump(CONSTRUCTION_REGULATIONS, f, indent=2)
    
    manager = ConstructionRegulationManager()
    manager.collection.delete(ids=[f"reg_{i}" for i in range(len(CONSTRUCTION_REGULATIONS))])
    manager.add_regulations_from_json(str(regulations_file))
    
    return manager

if __name__ == "__main__":
    manager = setup_regulations_db()
    print(f"Database populated with {manager.collection.count()} regulations")

# import chromadb
# import json
# import PyPDF2
# import os
# from pathlib import Path

# class RegulationManager:
#     def __init__(self, db_path: str = "regulations_db"):
#         """Initialize ChromaDB client and collection."""
#         self.client = chromadb.PersistentClient(path=db_path)
#         self.collection = self.client.get_or_create_collection(
#             name="construction_regulations",
#             metadata={"description": "Construction regulations and compliance documents"}
#         )

#     def extract_text_from_pdf(self, pdf_path: str) -> list:
#         """Extracts text from a given PDF file and splits it into sections."""
#         regulations = []
#         try:
#             with open(pdf_path, "rb") as f:
#                 reader = PyPDF2.PdfReader(f)
#                 for i, page in enumerate(reader.pages):
#                     text = page.extract_text()
#                     if text:
#                         regulations.append({"text": text.strip(), "source": Path(pdf_path).stem, "section": f"Page {i+1}"})
#         except Exception as e:
#             print(f"Error reading {pdf_path}: {e}")
#         return regulations

#     def add_regulations_from_pdfs(self, pdf_paths: list):
#         """Extracts and adds regulations from provided PDFs."""
#         for pdf_path in pdf_paths:
#             regulations = self.extract_text_from_pdf(pdf_path)

#             documents = []
#             metadatas = []
#             ids = []

#             for idx, reg in enumerate(regulations):
#                 documents.append(reg['text'])
#                 metadatas.append({'source': reg['source'], 'section': reg['section']})
#                 ids.append(f"{reg['source']}_{idx}")

#             if documents:
#                 self.collection.add(documents=documents, metadatas=metadatas, ids=ids)
#                 print(f"✅ Stored {len(documents)} sections from {pdf_path}")

#     def query_compliance(self, query_text: str, top_k: int = 3):
#         """Retrieves the most relevant compliance sections."""
#         results = self.collection.query(
#             query_texts=[query_text],
#             n_results=top_k
#         )
#         return results

# # Setup and populate the database
# def setup_regulations_db():
#     """Setup the regulations database by extracting text from the uploaded PDFs."""
#     uploaded_pdfs = [
#         "./compliance_check_doc/Contract Labor Regulations.pdf",
#         "./compliance_check_doc/Environmental Protection Act.pdf",
#         # "./compliance_check_doc/National Building Code.pdf",
#         "./compliance_check_doc/Safety on constrution site.pdf",
#         "./compliance_check_doc/Standard Construction Contract Guidelines.pdf",
#     ]

#     manager = RegulationManager()
#     manager.add_regulations_from_pdfs(uploaded_pdfs)

#     return manager

# if __name__ == "__main__":
#     manager = setup_regulations_db()
#     print(f"✅ Database populated with {manager.collection.count()} regulations")

#     # Example query
#     query = "What are the labor law requirements for construction workers?"
#     results = manager.query_compliance(query)
#     print("🔍 Compliance Check Results:", results)
