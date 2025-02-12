// this  code working perfectly with the manual entry of the field
// import React, { useState } from 'react';
// import './ContractForm.css';
// import { useNavigate } from 'react-router-dom'; // Import useNavigate

// const ContractForm = () => {
//     const [activeStep, setActiveStep] = useState(1);
//     const [formData, setFormData] = useState({
//         // Basic Details
//         developerName: '',
//         developerAddress: '',
//         contractorName: '',
//         contractorAddress: '',
//         projectAddress: '',
//         startDate: '',

//         // Project Details
//         contractDuration: '',
//         contractValue: '',
//         commencementPeriod: '',

//         // Payment Terms
//         mobilizationAdvance: '',
//         retentionPercentage: '',
//         paymentProcessingDays: '',
//         milestones: [{ description: '', percentage: '' }],

//         // Scope of Work
//         scopeOfWork: [],

//         // Implementation
//         penaltyPercentage: '',
//         maxPenaltyCap: '',
//         specialConditions: '',
//         terminationNoticePeriod: '',
//         arbitrationCity: '',
//         courtJurisdiction: '',
//         governingLaw: ''
//     });

//     const [isLoading, setIsLoading] = useState(false); // Loading state
//     const navigate = useNavigate(); // Initialize useNavigate

//     const handleChange = (e) => {
//         const { name, value } = e.target;
//         setFormData(prev => ({
//             ...prev,
//             [name]: value
//         }));
//     };

//     const handleMilestoneChange = (index, field, value) => {
//         const newMilestones = [...formData.milestones];
//         newMilestones[index][field] = value;
//         setFormData(prev => ({
//             ...prev,
//             milestones: newMilestones
//         }));
//     };

//     const addMilestone = () => {
//         setFormData(prev => ({
//             ...prev,
//             milestones: [...prev.milestones, { description: '', percentage: '' }]
//         }));
//     };

//     const removeMilestone = (index) => {
//         const newMilestones = [...formData.milestones];
//         newMilestones.splice(index, 1);
//         setFormData(prev => ({
//             ...prev,
//             milestones: newMilestones
//         }));
//     };

//     const handleScopeChange = (e) => {
//         const scopes = e.target.value.split('\n').filter(scope => scope.trim());
//         setFormData(prev => ({
//             ...prev,
//             scopeOfWork: scopes
//         }));
//     };

//     const handleSubmit = async (e) => {
//         e.preventDefault();
//         setIsLoading(true); // Start loading

//         try {
//             // Format data for backend
//             const formattedData = {
//                 developer_name: formData.developerName,
//                 developer_address: formData.developerAddress,
//                 contractor_name: formData.contractorName,
//                 contractor_address: formData.contractorAddress,
//                 project_address: formData.projectAddress,
//                 contract_value: parseFloat(formData.contractValue),
//                 contract_duration: parseInt(formData.contractDuration),
//                 start_date: formData.startDate,
//                 scope_of_work: formData.scopeOfWork,
//                 mobilization_advance: formData.mobilizationAdvance ? parseFloat(formData.mobilizationAdvance) : null,
//                 retention_percentage: formData.retentionPercentage ? parseFloat(formData.retentionPercentage) : null,
//                 milestones: formData.milestones
//                     .filter(m => m.description.trim() && m.percentage.trim())
//                     .map(m => ({
//                         description: m.description,
//                         percentage: parseFloat(m.percentage)
//                     })),
//                 penalty_percentage: formData.penaltyPercentage ? parseFloat(formData.penaltyPercentage) : null,
//                 max_penalty_cap: formData.maxPenaltyCap ? parseFloat(formData.maxPenaltyCap) : null,
//                 special_conditions: formData.specialConditions ?
//                   formData.specialConditions.split('\n').filter(c => c.trim()) : [], // Change null to empty array
//                 commencement_period: parseInt(formData.commencementPeriod),
//                 payment_processing_days: parseInt(formData.paymentProcessingDays),
//                 termination_notice_period: parseInt(formData.terminationNoticePeriod),
//                 arbitration_city: formData.arbitrationCity,
//                 court_jurisdiction: formData.courtJurisdiction,
//                 governing_law: formData.governingLaw
//             };

//             console.log("Sending data to backend:", formattedData);

//             const response = await fetch('http://127.0.0.1:5000/process-contract', { // Your API endpoint
//                 method: 'POST',
//                 headers: {
//                     'Content-Type': 'application/json',
//                 },
//                 body: JSON.stringify(formattedData),
//             });

//             if (!response.ok) {
//                 const errorText = await response.text();
//                 throw new Error(`Submission failed: ${errorText}`);
//             }

//             const result = await response.json(); // Parse the JSON response
//             console.log("Received response from backend:", result);

//             setIsLoading(false); // End loading

//             // Navigate to the next page, passing the base64 data as state
//             console.log("Navigating with state:", {
//               contractPdfBase64: result.contract_pdf_base64,
//               compliancePdfBase64: result.compliance_pdf_base64
//           });
//             navigate('/pdf-viewer', {
//                 state: {
//                     contractPdfBase64: result.contract_pdf_base64,
//                     compliancePdfBase64: result.compliance_pdf_base64,
//                 },
//             });

//         } catch (error) {
//              console.error('Detailed error:', error);
//               alert(`Error: ${error.message}`);
//             setIsLoading(false); // Stop loading on error

//         }
//     };

//     return (
//         <div className="contract-form">
//             <nav className="form-nav">
//                 <div
//                     className={`nav-item ${activeStep === 1 ? 'active' : ''}`}
//                     onClick={() => setActiveStep(1)}
//                 >
//                     Basic Details
//                 </div>
//                 <div
//                     className={`nav-item ${activeStep === 2 ? 'active' : ''}`}
//                     onClick={() => setActiveStep(2)}
//                 >
//                     Project Details
//                 </div>
//                 <div
//                     className={`nav-item ${activeStep === 3 ? 'active' : ''}`}
//                     onClick={() => setActiveStep(3)}
//                 >
//                     Payment Terms
//                 </div>
//                 <div
//                     className={`nav-item ${activeStep === 4 ? 'active' : ''}`}
//                     onClick={() => setActiveStep(4)}
//                 >
//                     Implementation
//                 </div>
//             </nav>

//             <form onSubmit={handleSubmit} className="form-content">
//                 {activeStep === 1 && (
//                     <div className="form-section">
//                         <h2>Basic Details</h2>
//                         <div className="input-group">
//                             <label>Developer Name</label>
//                             <input
//                                 type="text"
//                                 name="developerName"
//                                 value={formData.developerName}
//                                 onChange={handleChange}
//                                 required
//                             />
//                         </div>
//                         <div className="input-group">
//                             <label>Developer Address</label>
//                             <textarea
//                                 name="developerAddress"
//                                 value={formData.developerAddress}
//                                 onChange={handleChange}
//                                 required
//                             />
//                         </div>
//                         <div className="input-group">
//                             <label>Contractor Name</label>
//                             <input
//                                 type="text"
//                                 name="contractorName"
//                                 value={formData.contractorName}
//                                 onChange={handleChange}
//                                 required
//                             />
//                         </div>
//                         <div className="input-group">
//                             <label>Contractor Address</label>
//                             <textarea
//                                 name="contractorAddress"
//                                 value={formData.contractorAddress}
//                                 onChange={handleChange}
//                                 required
//                             />
//                         </div>
//                         <div className="input-group">
//                             <label>Project Address</label>
//                             <textarea
//                                 name="projectAddress"
//                                 value={formData.projectAddress}
//                                 onChange={handleChange}
//                                 required
//                             />
//                         </div>
//                         <div className="input-group">
//                             <label>Start Date</label>
//                             <input
//                                 type="date"
//                                 name="startDate"
//                                 value={formData.startDate}
//                                 onChange={handleChange}
//                                 required
//                             />
//                         </div>
//                     </div>
//                 )}

//                 {activeStep === 2 && (
//                     <div className="form-section">
//                         <h2>Project Details</h2>
//                         <div className="input-group">
//                             <label>Contract Duration (months)</label>
//                             <input
//                                 type="number"
//                                 name="contractDuration"
//                                 value={formData.contractDuration}
//                                 onChange={handleChange}
//                                 required
//                                 min="1"
//                             />
//                         </div>
//                         <div className="input-group">
//                             <label>Contract Value (INR)</label>
//                             <input
//                                 type="number"
//                                 name="contractValue"
//                                 value={formData.contractValue}
//                                 onChange={handleChange}
//                                 required
//                                 min="0"
//                             />
//                         </div>
//                         <div className="input-group">
//                             <label>Commencement Period (days)</label>
//                             <input
//                                 type="number"
//                                 name="commencementPeriod"
//                                 value={formData.commencementPeriod}
//                                 onChange={handleChange}
//                                 required
//                                 min="0"
//                             />
//                         </div>
//                         <div className="input-group">
//                             <label>Scope of Work (one item per line)</label>
//                             <textarea
//                                 value={formData.scopeOfWork.join('\n')}
//                                 onChange={handleScopeChange}
//                                 rows="5"
//                                 placeholder="Enter scope items..."
//                                 required
//                             />
//                         </div>
//                     </div>
//                 )}

//                 {activeStep === 3 && (
//                     <div className="form-section">
//                         <h2>Payment Terms</h2>
//                         <div className="input-group">
//                             <label>Mobilization Advance (%)</label>
//                             <input
//                                 type="number"
//                                 name="mobilizationAdvance"
//                                 value={formData.mobilizationAdvance}
//                                 onChange={handleChange}
//                                 required
//                                 min="0"
//                                 max="100"
//                             />
//                         </div>
//                         <div className="input-group">
//                             <label>Retention Percentage (%)</label>
//                             <input
//                                 type="number"
//                                 name="retentionPercentage"
//                                 value={formData.retentionPercentage}
//                                 onChange={handleChange}
//                                 required
//                                 min="0"
//                                 max="100"
//                             />
//                         </div>
//                         <div className="input-group">
//                             <label>Payment Processing Days</label>
//                             <input
//                                 type="number"
//                                 name="paymentProcessingDays"
//                                 value={formData.paymentProcessingDays}
//                                 onChange={handleChange}
//                                 required
//                                 min="0"
//                             />
//                         </div>
//                         <div className="milestones-section">
//                             <h3>Payment Milestones</h3>
//                             {formData.milestones.map((milestone, index) => (
//                                 <div key={index} className="milestone-group">
//                                     <input
//                                         type="text"
//                                         placeholder="Milestone description"
//                                         value={milestone.description}
//                                         onChange={(e) => handleMilestoneChange(index, 'description', e.target.value)}
//                                         required
//                                     />
//                                     <input
//                                         type="number"
//                                         placeholder="Percentage"
//                                         value={milestone.percentage}
//                                         onChange={(e) => handleMilestoneChange(index, 'percentage', e.target.value)}
//                                         required
//                                         min="0"
//                                         max="100"
//                                     />
//                                     <button type="button" onClick={() => removeMilestone(index)}>
//                                         Remove
//                                     </button>
//                                 </div>
//                             ))}
//                             <button type="button" onClick={addMilestone}>
//                                 Add Milestone
//                             </button>
//                         </div>
//                     </div>
//                 )}

//                 {activeStep === 4 && (
//                     <div className="form-section">
//                         <h2>Implementation</h2>
//                         <div className="input-group">
//                             <label>Penalty Percentage (per week)</label>
//                             <input
//                                 type="number"
//                                 name="penaltyPercentage"
//                                 value={formData.penaltyPercentage}
//                                 onChange={handleChange}
//                                 required
//                                 min="0"
//                                 max="100"
//                                 step="0.1"
//                             />
//                         </div>
//                         <div className="input-group">
//                             <label>Maximum Penalty Cap (%)</label>
//                             <input
//                                 type="number"
//                                 name="maxPenaltyCap"
//                                 value={formData.maxPenaltyCap}
//                                 onChange={handleChange}
//                                 required
//                                 min="0"
//                                 max="100"
//                             />
//                         </div>
//                         <div className="input-group">
//                             <label>Termination Notice Period</label>
//                             <input
//                                 type="number"
//                                 name="terminationNoticePeriod"
//                                 value={formData.terminationNoticePeriod}
//                                 onChange={handleChange}
//                                 required
//                                 min="0"
//                             />
//                         </div>
//                         <div className="input-group">
//                             <label>Arbitration City</label>
//                             <input
//                                 type="text"
//                                 name="arbitrationCity"
//                                 value={formData.arbitrationCity}
//                                 onChange={handleChange}
//                                 required
//                             />
//                         </div>
//                         <div className="input-group">
//                             <label>Court Jurisdiction</label>
//                             <input
//                                 type="text"
//                                 name="courtJurisdiction"
//                                 value={formData.courtJurisdiction}
//                                 onChange={handleChange}
//                                 required
//                             />
//                         </div>
//                         <div className="input-group">
//                             <label>Governing Law</label>
//                             <input
//                                 type="text"
//                                 name="governingLaw"
//                                 value={formData.governingLaw}
//                                 onChange={handleChange}
//                                 required
//                             />
//                         </div>
//                         <div className="input-group">
//                             <label>Special Conditions (optional, one per line)</label>
//                             <textarea
//                                 name="specialConditions"
//                                 value={formData.specialConditions}
//                                 onChange={handleChange}
//                                 rows="4"
//                                 placeholder="Enter special conditions..."
//                             />
//                         </div>
//                     </div>
//                 )}

//                 <div className="form-navigation">
//                     {activeStep > 1 && (
//                         <button
//                             type="button"
//                             onClick={() => setActiveStep(prev => prev - 1)}
//                             className="nav-button"
//                         >
//                             Previous
//                         </button>
//                     )}
//                     {activeStep < 4 ? (
//                         <button
//                             type="button"
//                             onClick={() => setActiveStep(prev => prev + 1)}
//                             className="nav-button"
//                         >
//                             Next
//                         </button>
//                     ) : (
//                         <button type="submit" className="submit-button" disabled={isLoading}>
//                             {isLoading ? 'Generating Contract...' : 'Generate Contract'}
//                         </button>
//                     )}
//                 </div>
//             </form>
//         </div>
//     );
// };

// export default ContractForm;

// """This code for automation of the field"""
import React, { useState, useEffect } from 'react';
import './ContractForm.css';
import { useNavigate } from 'react-router-dom';

const ContractForm = () => {
    const [activeStep, setActiveStep] = useState(1);
    const [formData, setFormData] = useState({
        // Basic Details
        developerName: '',
        developerAddress: '',
        contractorName: '',
        contractorAddress: '',
        projectAddress: '',
        startDate: '',

        // Project Details
        contractDuration: '',
        contractValue: '',
        commencementPeriod: '',

        // Payment Terms
        mobilizationAdvance: '',
        retentionPercentage: '',
        paymentProcessingDays: '',
        milestones: [{ description: '', percentage: '' }],

        // Scope of Work
        scopeOfWork: [],

        // Implementation
        penaltyPercentage: '',
        maxPenaltyCap: '',
        specialConditions: '',
        terminationNoticePeriod: '',
        arbitrationCity: '',
        courtJurisdiction: '',
        governingLaw: ''
    });

    const [isLoading, setIsLoading] = useState(false);
    const navigate = useNavigate();
    const [selectedClient, setSelectedClient] = useState('');

    const clientData = [
        {
            clientName: "Client A",
            developerName: "ABC Developers",
            developerAddress: "123 Main St",
            contractorName: "XYZ Construction",
            contractorAddress: "456 Oak Ave",
            projectAddress: "789 Pine Ln",
            arbitrationCity: "New York",
            courtJurisdiction: "NY Supreme Court",
            governingLaw: "New York Law",
        },
        {
            clientName: "Client B",
            developerName: "PQR Group",
            developerAddress: "456 Elm St",
            contractorName: "LMN Builders",
            contractorAddress: "789 Maple Dr",
            projectAddress: "101 Cedar Rd",
            arbitrationCity: "Los Angeles",
            courtJurisdiction: "CA Superior Court",
            governingLaw: "California Law",
        },
        {
            clientName: "Client C",
            developerName: "GHI Builders",
            developerAddress: "789 Oak St",
            contractorName: "STU Construction",
            contractorAddress: "101 Pine Ave",
            projectAddress: "222 Maple Ln",
            arbitrationCity: "Chicago",
            courtJurisdiction: "IL Circuit Court",
            governingLaw: "Illinois Law",
        },
        {
            clientName: "Client D",
            developerName: "JKL Developers",
            developerAddress: "101 Maple St",
            contractorName: "VWX Contractors",
            contractorAddress: "222 Oak Ave",
            projectAddress: "333 Pine Ln",
            arbitrationCity: "Houston",
            courtJurisdiction: "TX District Court",
            governingLaw: "Texas Law",
        },
        {
            clientName: "Client E",
            developerName: "MNO Group",
            developerAddress: "222 Pine St",
            contractorName: "YZA Builders",
            contractorAddress: "333 Elm Ave",
            projectAddress: "444 Maple Ln",
            arbitrationCity: "Miami",
            courtJurisdiction: "FL Circuit Court",
            governingLaw: "Florida Law",
        }
    ];

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData(prev => ({
            ...prev,
            [name]: value
        }));
    };

    const handleMilestoneChange = (index, field, value) => {
        const newMilestones = [...formData.milestones];
        newMilestones[index][field] = value;
        setFormData(prev => ({
            ...prev,
            milestones: newMilestones
        }));
    };

    const addMilestone = () => {
        setFormData(prev => ({
            ...prev,
            milestones: [...prev.milestones, { description: '', percentage: '' }]
        }));
    };

    const removeMilestone = (index) => {
        const newMilestones = [...formData.milestones];
        newMilestones.splice(index, 1);
        setFormData(prev => ({
            ...prev,
            milestones: newMilestones
        }));
    };

    const handleScopeChange = (e) => {
        const scopes = e.target.value.split('\n').filter(scope => scope.trim());
        setFormData(prev => ({
            ...prev,
            scopeOfWork: scopes
        }));
    };

    useEffect(() => {
        if (selectedClient) {
            const selectedClientData = clientData.find(
                (client) => client.clientName === selectedClient
            );

            if (selectedClientData) {
                setFormData((prev) => ({
                    ...prev,
                    developerName: selectedClientData.developerName || '',
                    developerAddress: selectedClientData.developerAddress || '',
                    contractorName: selectedClientData.contractorName || '',
                    contractorAddress: selectedClientData.contractorAddress || '',
                    projectAddress: selectedClientData.projectAddress || '',
                    arbitrationCity: selectedClientData.arbitrationCity || '',
                    courtJurisdiction: selectedClientData.courtJurisdiction || '',
                    governingLaw: selectedClientData.governingLaw || '',
                    // Keep startDate empty
                }));
                setActiveStep(2);
            }
        }
    }, [selectedClient]);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setIsLoading(true);

        try {
            const formattedData = {
                developer_name: formData.developerName,
                developer_address: formData.developerAddress,
                contractor_name: formData.contractorName,
                contractor_address: formData.contractorAddress,
                project_address: formData.projectAddress,
                contract_value: parseFloat(formData.contractValue),
                contract_duration: parseInt(formData.contractDuration),
                start_date: formData.startDate,
                scope_of_work: formData.scopeOfWork,
                mobilization_advance: formData.mobilizationAdvance ? parseFloat(formData.mobilizationAdvance) : null,
                retention_percentage: formData.retentionPercentage ? parseFloat(formData.retentionPercentage) : null,
                milestones: formData.milestones
                    .filter(m => m.description.trim() && m.percentage.trim())
                    .map(m => ({
                        description: m.description,
                        percentage: parseFloat(m.percentage)
                    })),
                penalty_percentage: formData.penaltyPercentage ? parseFloat(formData.penaltyPercentage) : null,
                max_penalty_cap: formData.maxPenaltyCap ? parseFloat(formData.maxPenaltyCap) : null,
                special_conditions: formData.specialConditions ?
                  formData.specialConditions.split('\n').filter(c => c.trim()) : [],
                commencement_period: parseInt(formData.commencementPeriod),
                payment_processing_days: parseInt(formData.paymentProcessingDays),
                termination_notice_period: parseInt(formData.terminationNoticePeriod),
                arbitration_city: formData.arbitrationCity,
                court_jurisdiction: formData.courtJurisdiction,
                governing_law: formData.governingLaw
            };

            console.log("Sending data to backend:", formattedData);

            const response = await fetch('http://127.0.0.1:5000/process-contract', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formattedData),
            });

            if (!response.ok) {
                const errorText = await response.text();
                throw new Error(`Submission failed: ${errorText}`);
            }

            const result = await response.json();
            console.log("Received response from backend:", result);

            setIsLoading(false);

            console.log("Navigating with state:", {
              contractPdfBase64: result.contract_pdf_base64,
              compliancePdfBase64: result.compliance_pdf_base64
          });
            navigate('/pdf-viewer', {
                state: {
                    contractPdfBase64: result.contract_pdf_base64,
                    compliancePdfBase64: result.compliance_pdf_base64,
                },
            });

        } catch (error) {
             console.error('Detailed error:', error);
              alert(`Error: ${error.message}`);
            setIsLoading(false);

        }
    };

    return (
        <div className="contract-form">
            <div className="client-selection">
                <label>Select Client</label>
                <select
                    value={selectedClient}
                    onChange={(e) => setSelectedClient(e.target.value)}
                >
                    <option value="">Select a client</option>
                    {clientData.map((client) => (
                        <option key={client.clientName} value={client.clientName}>
                            {client.clientName}
                        </option>
                    ))}
                </select>
            </div>

            <nav className="form-nav">
                <div
                    className={`nav-item ${activeStep === 1 ? 'active' : ''}`}
                    onClick={() => setActiveStep(1)}
                >
                    Basic Details
                </div>
                <div
                    className={`nav-item ${activeStep === 2 ? 'active' : ''}`}
                    onClick={() => setActiveStep(2)}
                >
                    Project Details
                </div>
                <div
                    className={`nav-item ${activeStep === 3 ? 'active' : ''}`}
                    onClick={() => setActiveStep(3)}
                >
                    Payment Terms
                </div>
                <div
                    className={`nav-item ${activeStep === 4 ? 'active' : ''}`}
                    onClick={() => setActiveStep(4)}
                >
                    Implementation
                </div>
            </nav>

            <form onSubmit={handleSubmit} className="form-content">
                {activeStep === 1 && (
                    <div className="form-section">
                        <h2>Basic Details</h2>
                        <div className="input-group">
                            <label>Developer Name</label>
                            <input
                                type="text"
                                name="developerName"
                                value={formData.developerName}
                                onChange={handleChange}
                                required
                            />
                        </div>
                        <div className="input-group">
                            <label>Developer Address</label>
                            <textarea
                                name="developerAddress"
                                value={formData.developerAddress}
                                onChange={handleChange}
                                required
                            />
                        </div>
                        <div className="input-group">
                            <label>Contractor Name</label>
                            <input
                                type="text"
                                name="contractorName"
                                value={formData.contractorName}
                                onChange={handleChange}
                                required
                            />
                        </div>
                        <div className="input-group">
                            <label>Contractor Address</label>
                            <textarea
                                name="contractorAddress"
                                value={formData.contractorAddress}
                                onChange={handleChange}
                                required
                            />
                        </div>
                        <div className="input-group">
                            <label>Project Address</label>
                            <textarea
                                name="projectAddress"
                                value={formData.projectAddress}
                                onChange={handleChange}
                                required
                            />
                        </div>
                        <div className="input-group">
                            <label>Start Date</label>
                            <input
                                type="date"
                                name="startDate"
                                value={formData.startDate}
                                onChange={handleChange}
                                required
                            />
                        </div>
                    </div>
                )}

                {activeStep === 2 && (
                    <div className="form-section">
                        <h2>Project Details</h2>
                        <div className="input-group">
                            <label>Contract Duration (months)</label>
                            <select
                                name="contractDuration"
                                value={formData.contractDuration}
                                onChange={handleChange}
                                required
                            >
                                <option value="">Select Duration</option>
                                <option value="6">6 months</option>
                                <option value="12">12 months</option>
                                <option value="18">18 months</option>
                                <option value="24">24 months</option>
                            </select>
                        </div>
                        <div className="input-group">
                            <label>Contract Value (INR)</label>
                            <input
                                type="number"
                                name="contractValue"
                                value={formData.contractValue}
                                onChange={handleChange}
                                required
                                min="0"
                            />
                        </div>
                        <div className="input-group">
                            <label>Commencement Period (days)</label>
                            <select
                                name="commencementPeriod"
                                value={formData.commencementPeriod}
                                onChange={handleChange}
                                required
                            >
                                <option value="">Select Period</option>
                                <option value="7">7 days</option>
                                <option value="14">14 days</option>
                                <option value="21">21 days</option>
                            </select>
                        </div>
                        <div className="input-group">
                            <label>Scope of Work (one item per line)</label>
                            <textarea
                                value={formData.scopeOfWork.join('\n')}
                                onChange={handleScopeChange}
                                rows="5"
                                placeholder="Enter scope items..."
                                required
                            />
                        </div>
                    </div>
                )}

                {activeStep === 3 && (
                    <div className="form-section">
                        <h2>Payment Terms</h2>
                        <div className="input-group">
                            <label>Mobilization Advance (%)</label>
                            <select
                                name="mobilizationAdvance"
                                value={formData.mobilizationAdvance}
                                onChange={handleChange}
                                required
                                min="0"
                                max="100"
                            >
                                <option value="">Select Advance</option>
                                <option value="10">10%</option>
                                <option value="15">15%</option>
                                <option value="20">20%</option>
                            </select>
                        </div>
                        <div className="input-group">
                            <label>Retention Percentage (%)</label>
                            <select
                                name="retentionPercentage"
                                value={formData.retentionPercentage}
                                onChange={handleChange}
                                required
                                min="0"
                                max="100"
                            >
                                <option value="">Select Percentage</option>
                                <option value="5">5%</option>
                                <option value="10">10%</option>
                                <option value="15">15%</option>
                            </select>
                        </div>
                        <div className="input-group">
                            <label>Payment Processing Days</label>
                            <select
                                name="paymentProcessingDays"
                                value={formData.paymentProcessingDays}
                                onChange={handleChange}
                                required
                                min="0"
                            >
                                <option value="">Select Days</option>
                                <option value="3">3 days</option>
                                <option value="5">5 days</option>
                                <option value="7">7 days</option>
                            </select>
                        </div>
                        <div className="milestones-section">
                            <h3>Payment Milestones</h3>
                            {formData.milestones.map((milestone, index) => (
                                <div key={index} className="milestone-group">
                                    <select
                                        placeholder="Milestone description"
                                        value={milestone.description}
                                        onChange={(e) => handleMilestoneChange(index, 'description', e.target.value)}
                                        required
                                    >
                                        <option value="">Select Milestone</option>
                                        <option value="Design Completion">Design Completion</option>
                                        <option value="Foundation Laying">Foundation Laying</option>
                                        <option value="Structure Completion">Structure Completion</option>
                                        {/* Add more milestone options */}
                                    </select>
                                    <select
                                        placeholder="Percentage"
                                        value={milestone.percentage}
                                        onChange={(e) => handleMilestoneChange(index, 'percentage', e.target.value)}
                                        required
                                        min="0"
                                        max="100"
                                    >
                                        <option value="">Select Percentage</option>
                                        <option value="25">25%</option>
                                        <option value="50">50%</option>
                                        <option value="75">75%</option>
                                    </select>
                                    <button type="button" onClick={() => removeMilestone(index)}>
                                        Remove
                                    </button>
                                </div>
                            ))}
                            <button type="button" onClick={addMilestone}>
                                Add Milestone
                            </button>
                        </div>
                    </div>
                )}

                {activeStep === 4 && (
                    <div className="form-section">
                        <h2>Implementation</h2>
                        <div className="input-group">
                            <label>Penalty Percentage (per week)</label>
                            <select
                                name="penaltyPercentage"
                                value={formData.penaltyPercentage}
                                onChange={handleChange}
                                required
                                min="0"
                                max="100"
                                step="0.1"
                            >
                                <option value="">Select Percentage</option>
                                <option value="0.5">0.5%</option>
                                <option value="1">1%</option>
                                <option value="1.5">1.5%</option>
                            </select>
                        </div>
                        <div className="input-group">
                            <label>Maximum Penalty Cap (%)</label>
                            <select
                                name="maxPenaltyCap"
                                value={formData.maxPenaltyCap}
                                onChange={handleChange}
                                required
                                min="0"
                                max="100"
                            >
                                <option value="">Select Cap</option>
                                <option value="5">5%</option>
                                <option value="10">10%</option>
                                <option value="15">15%</option>
                            </select>
                        </div>
                        <div className="input-group">
                            <label>Termination Notice Period</label>
                            <select
                                name="terminationNoticePeriod"
                                value={formData.terminationNoticePeriod}
                                onChange={handleChange}
                                required
                                min="0"
                            >
                                <option value="">Select Period</option>
                                <option value="30">30 days</option>
                                <option value="60">60 days</option>
                                <option value="90">90 days</option>
                            </select>
                        </div>
                        <div className="input-group">
                            <label>Arbitration City</label>
                            <input
                                type="text"
                                name="arbitrationCity"
                                value={formData.arbitrationCity}
                                onChange={handleChange}
                                required
                                readOnly
                            />
                        </div>
                        <div className="input-group">
                            <label>Court Jurisdiction</label>
                            <input
                                type="text"
                                name="courtJurisdiction"
                                value={formData.courtJurisdiction}
                                onChange={handleChange}
                                required
                                readOnly
                            />
                        </div>
                        <div className="input-group">
                            <label>Governing Law</label>
                            <input
                                type="text"
                                name="governingLaw"
                                value={formData.governingLaw}
                                onChange={handleChange}
                                required
                                readOnly
                            />
                        </div>
                        <div className="input-group">
                            <label>Special Conditions (optional, one per line)</label>
                            <textarea
                                name="specialConditions"
                                value={formData.specialConditions}
                                onChange={handleChange}
                                rows="4"
                                placeholder="Enter special conditions..."
                            />
                        </div>
                    </div>
                )}

                <div className="form-navigation">
                    {activeStep > 1 && (
                        <button
                            type="button"
                            onClick={() => setActiveStep(prev => prev - 1)}
                            className="nav-button"
                        >
                            Previous
                        </button>
                    )}
                    {activeStep < 4 ? (
                        <button
                            type="button"
                            onClick={() => setActiveStep(prev => prev + 1)}
                            className="nav-button"
                        >
                            Next
                        </button>
                    ) : (
                        <button type="submit" className="submit-button" disabled={isLoading}>
                            {isLoading ? 'Generating Contract...' : 'Generate Contract'}
                        </button>
                    )}
                </div>
            </form>
        </div>
    );
};

export default ContractForm;