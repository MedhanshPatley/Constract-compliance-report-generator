# import os
# import uuid
# from datetime import datetime
# from typing import List, Optional, Union, Dict

# import google.generativeai as genai
# import chromadb
# from fastapi import FastAPI, HTTPException, Depends
# from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel, Field
# from chromadb.config import Settings




# # Gemini AI Configuration
# genai.configure(api_key = 'AIzaSyBLRXR_EiHaFubhWNTPGUnu8I7QqVxpWlA')

# class ConstructionRegulationManager:
#     def __init__(self, persist_directory='./regulation_db'):
#         """
#         Initialize ChromaDB for storing and querying construction regulations
#         """
#         self.client = chromadb.PersistentClient(path=persist_directory)
        
#         # Create or get collection
#         try:
#             self.collection = self.client.get_collection("construction_regulations")
#         except:
#             self.collection = self.client.create_collection("construction_regulations")
        
#         # If collection is empty, populate with some initial regulations
#         if self.collection.count() == 0:
#             self._seed_regulations()

#     def _seed_regulations(self):
#         """
#         Seed the database with some initial construction regulations
#         """
#         initial_regulations = [
#             {
#                 "id": str(uuid.uuid4()),
#                 "text": "Minimum safety protocols require personal protective equipment on all construction sites",
#                 "category": "safety"
#             },
#             {
#                 "id": str(uuid.uuid4()),
#                 "text": "Payment retention shall not exceed 10% of contract value",
#                 "category": "payment_terms"
#             },
#             {
#                 "id": str(uuid.uuid4()),
#                 "text": "Environmental impact assessment required for projects over 5000 sq meters",
#                 "category": "environmental"
#             }
#         ]

#         for reg in initial_regulations:
#             self.collection.add(
#                 ids=[reg["id"]],
#                 documents=[reg["text"]],
#                 metadatas=[{"category": reg["category"]}]
#             )

# def setup_regulations_db():
#     return ConstructionRegulationManager()

# class Milestone(BaseModel):
#     description: str
#     percentage: float

# class ContractRequest(BaseModel):
#     developer_name: str
#     developer_address: str
#     contractor_name: str
#     contractor_address: str
#     project_address: str
#     contract_value: float
#     contract_duration: int
#     start_date: str
#     scope_of_work: List[str]
    
#     # Payment Terms
#     mobilization_advance: Optional[float] = None
#     retention_percentage: Optional[float] = None
#     milestones: Optional[List[Milestone]] = None
    
#     # Implementation Details
#     penalty_percentage: Optional[float] = None
#     max_penalty_cap: Optional[float] = None
#     special_conditions: Optional[List[str]] = None

# class ComplianceCheck(BaseModel):
#     category: str
#     is_compliant: bool
#     details: Optional[str] = None
#     referenced_regulations: List[str] = []

# class ProcessedContract(BaseModel):
#     contract_id: str
#     contract_text: str
#     overall_compliance: bool
#     compliance_checks: List[ComplianceCheck]
#     generated_at: str

# class ContractProcessor:
#     def __init__(self, regulation_manager, llm_model='gemini-1.5-flash'):
#         """
#         Initialize contract processor with regulation manager and LLM
#         """
#         self.regulation_manager = regulation_manager
#         self.llm = genai.GenerativeModel(llm_model)

#     def _query_regulations(self, query_text: str, top_k: int = 3):
#         """
#         Query regulations database for relevant guidelines
#         """
#         results = self.regulation_manager.collection.query(
#             query_texts=[query_text],
#             n_results=top_k
#         )
#         return results['documents'][0] if results['documents'] else []

#     async def generate_contract_text(self, request: ContractRequest) -> str:
#         """
#         Generate comprehensive contract text using Gemini AI
#         """
#         milestones_text = "\n".join([
#             f"- {m.description}: {m.percentage}%" for m in (request.milestones or [])
#         ])

#         prompt = f"""
#         Generate a detailed and legally sound Developer-Contractor Agreement incorporating the following details:

#         Parties:
#         - Developer: {request.developer_name}, Address: {request.developer_address}
#         - Contractor: {request.contractor_name}, Address: {request.contractor_address}

#         Agreement Details:
#         - Date:  {request.start_date}
#         - Contract Duration: {request.contract_duration} months
        

#         Scope of Work:
#         The Contractor agrees to execute and complete construction work for the project at {request.project_address}, including but not limited to:
#         {", ".join(request.scope_of_work)}

#         Contract Value and Payments:
#         - Total Contract Value: INR {request.contract_value} 
#         - Mobilization Advance: {request.mobilization_advance}% 
#         - Payment Milestones:
#         -  {milestones_text or "No specific milestones defined"}
#         - Final balance upon handover
#         - Retention Money: {request.retention_percentage}% 

#         Implementation and Penalty:
    
#         - Delay Penalty: {request.penalty_percentage}% per week (capped at {request.max_penalty_cap}%)
#         - Extension Policy: Allowed upon mutual agreement for justified delays

#         Responsibilities:
#         - Developer: Provides access, approvals, and timely payments
#         - Contractor: Ensures quality execution, compliance, and rectifies defects within the liability period

#         Legal and Dispute Resolution:h

#         Include all the above details in a structured contract format while ensuring clarity and legal precision.
#         """
#         response = self.llm.generate_content(prompt)
#         return response.text




# # 
#     async def perform_compliance_check(self, contract_text: str) -> List[ComplianceCheck]:
#         """
#         Perform comprehensive compliance checks using regulations and LLM
#         """
#         compliance_checks = []
#         categories = [
#             "safety", "payment_terms", "environmental", 
#             "labor", "materials", "timeline", "dispute_resolution"
#         ]

#         for category in categories:
#             # Query relevant regulations
#             regulation_matches = self._query_regulations(f"Check compliance for {category} in construction contract")

#             # Compliance evaluation prompt
#             compliance_prompt = f"""
#             Evaluate this contract section for {category} compliance:
#             {contract_text}

#             Relevant Regulations:
#             {regulation_matches}

#             Provide a structured compliance assessment:
#             1. Is the contract compliant in this category?
#             2. What specific regulations are most relevant?
#             3. Any critical recommendations or observations?

#             Format your response as a JSON object with:
#             - compliant: boolean
#             - notes: string
#             - regulations: list of regulation texts
#             """

#             response = self.llm.generate_content(compliance_prompt)
            
#             # Parse and create compliance check
#             try:
#                 result = response.text
#                 compliance_checks.append(ComplianceCheck(
#                     category=category,
#                     is_compliant=True,  # Default to True, adjust based on actual implementation
#                     details=result,
#                     referenced_regulations=regulation_matches
#                 ))
#             except Exception as e:
#                 compliance_checks.append(ComplianceCheck(
#                     category=category,
#                     is_compliant=False,
#                     details=f"Error in compliance check: {str(e)}"
#                 ))

#         return compliance_checks

#     async def process_contract(self, request: ContractRequest) -> ProcessedContract:
#         """
#         Main contract processing workflow
#         """
#         # Generate contract text
#         print("Step 1: Starting contract generation...")
#         contract_text = await self.generate_contract_text(request)
        
#         # Perform compliance checks
#         print("\nStep 2: Starting compliance checks...")
#         compliance_checks = await self.perform_compliance_check(contract_text)
        
#         # Determine overall compliance
#         overall_compliance = all(check.is_compliant for check in compliance_checks)

#         return ProcessedContract(
#             contract_id=f"CTR-{datetime.now().strftime('%Y%m%d%H%M%S')}",
#             contract_text=contract_text,
#             overall_compliance=overall_compliance,
#             compliance_checks=compliance_checks,
#             generated_at=datetime.now().isoformat()
#         )



# # FastAPI Application Setup
# app = FastAPI(
#     title="Construction Contract Processing API",
#     description="AI-powered contract generation and compliance checking system",
#     version="1.0.0"
# )

# # CORS Middleware
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # Allows all origins
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # Initialize services
# regulation_manager = setup_regulations_db()
# contract_processor = ContractProcessor(regulation_manager)

# @app.get("/")
# def read_root():
#     return {"message": "Hello, world!"}
# # API Endpoints
# @app.post("/process-contract", response_model=ProcessedContract)
# async def process_contract(request: ContractRequest):
#     """
#     Process and generate a contract with compliance checks
#     """
#     try:
#         print("Received contract request:", request.dict())
        
#         processed_contract = await contract_processor.process_contract(request)
        
#         # Log the response before sending
#         print("Sending response:", {
#             "contract_id": processed_contract.contract_id,
#             "contract_text": processed_contract.contract_text[:100] + "..." if processed_contract.contract_text else None,
#             "overall_compliance": processed_contract.overall_compliance,
#             "compliance_checks": [check.dict() for check in processed_contract.compliance_checks],
#             "generated_at": processed_contract.generated_at
#         })
        
#         return processed_contract
#     except Exception as e:
#         import traceback
#         print("Error processing contract:")
#         print(traceback.format_exc())
#         raise HTTPException(status_code=500, detail=str(e))




# @app.get("/health")
# async def health_check():
#     """
#     Basic health check endpoint
#     """
#     return {
#         "status": "healthy", 
#         "timestamp": datetime.now().isoformat(),
#         "regulations_count": regulation_manager.collection.count()
#     }

# # If running directly
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app,  port=5000)


