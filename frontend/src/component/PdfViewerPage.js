// '''THIS CODE IS WORKING''';

// import React, { useState, useEffect } from 'react';
// import { useLocation } from 'react-router-dom';
// import { Document, Page, pdfjs } from 'react-pdf';
// import './PdfViewerPage.css';

// pdfjs.GlobalWorkerOptions.workerSrc = `/pdfjs/pdf.worker.min.js`;

// const PdfViewerPage = () => {
//     const location = useLocation();
//     const { contractPdfBase64, compliancePdfBase64 } = location.state || {};
//     const [contractPdfData, setContractPdfData] = useState(null);
//     const [compliancePdfData, setCompliancePdfData] = useState(null);
//     const [error, setError] = useState(null);
//     const [contractNumPages, setContractNumPages] = useState(null);
//     const [complianceNumPages, setComplianceNumPages] = useState(null);

//     useEffect(() => {
//         if (!contractPdfBase64 || !compliancePdfBase64) {
//             setError("PDF data not found. Please return to the form and submit again.");
//             return;
//         }

//         console.log("Contract PDF Base64 (first 50 chars):", contractPdfBase64.substring(0, 50)); // Check if the string looks right
//         console.log("Compliance PDF Base64 (first 50 chars):", compliancePdfBase64.substring(0, 50));

//         const loadPdfs = async () => {
//             try {
//                 const contractData = base64ToArrayBuffer(contractPdfBase64);
//                 setContractPdfData(contractData);

//                 const complianceData = base64ToArrayBuffer(compliancePdfBase64);
//                 setCompliancePdfData(complianceData);

//             } catch (pdfError) {
//                 console.error("Error loading PDF:", pdfError);
//                 setError("Failed to load PDF documents.");
//             }
//         };

//         loadPdfs();
//     }, [contractPdfBase64, compliancePdfBase64]);

//     const base64ToArrayBuffer = (base64) => {
//         try {
//             const binaryString = window.atob(base64);
//             const len = binaryString.length;
//             const bytes = new Uint8Array(len);
//             for (let i = 0; i < len; i++) {
//                 bytes[i] = binaryString.charCodeAt(i);
//             }
//             return bytes.buffer;
//         } catch (error) {
//             console.error("Error converting base64 to ArrayBuffer:", error);
//             throw error; // Re-throw the error to be caught by the outer try-catch
//         }
//     };

//     const onContractLoadSuccess = ({ numPages }) => {
//         setContractNumPages(numPages);
//     };

//     const onComplianceLoadSuccess = ({ numPages }) => {
//         setComplianceNumPages(numPages);
//     };

//     if (error) {
//         return <div>Error: {error}</div>;
//     }

//     return (
//         <div className="pdf-container">
//             <div className="pdf-window">
//                 <h2>Generated Contract</h2>
//                 {contractPdfData ? (
//                     <div className="pdf-scrollable">
//                         <Document
//                             file={contractPdfData}
//                             onLoadSuccess={onContractLoadSuccess}
//                             onError={(error) => console.error("react-pdf error (Contract):", error)} // More specific error
//                         >
//                             {Array.from(new Array(contractNumPages), (el, index) => (
//                                 <Page key={`contract_page_${index + 1}`} pageNumber={index + 1} />
//                             ))}
//                         </Document>
//                     </div>
//                 ) : (
//                     <p>Loading Contract PDF...</p>
//                 )}
//             </div>

//             <div className="pdf-window">
//                 <h2>Compliance Report</h2>
//                 {compliancePdfData ? (
//                     <div className="pdf-scrollable">
//                         <Document
//                             file={compliancePdfData}
//                             onLoadSuccess={onComplianceLoadSuccess}
//                             onError={(error) => console.error("react-pdf error (Compliance):", error)} // More specific error
//                         >
//                             {Array.from(new Array(complianceNumPages), (el, index) => (
//                                 <Page key={`compliance_page_${index + 1}`} pageNumber={index + 1} />
//                             ))}
//                         </Document>
//                     </div>
//                 ) : (
//                     <p>Loading Compliance PDF...</p>
//                 )}
//             </div>
//         </div>
//     );
// };

// export default PdfViewerPage;


import React, { useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import './PdfViewerPage.css';

const PdfViewerPage = () => {
    const location = useLocation();
    const { contractPdfBase64, compliancePdfBase64 } = location.state || {};
    const [contractPdfUrl, setContractPdfUrl] = useState(null);
    const [compliancePdfUrl, setCompliancePdfUrl] = useState(null);
    const [error, setError] = useState(null);

    useEffect(() => {
        if (!contractPdfBase64 || !compliancePdfBase64) {
            setError("PDF data not found. Please return to the form and submit again.");
            return;
        }

        let contractPdfUrlLocal, compliancePdfUrlLocal; // Declare outside the try block

        try {
            // Create a URL for the contract PDF
            const contractPdfBlob = base64ToBlob(contractPdfBase64, 'application/pdf');
            contractPdfUrlLocal = URL.createObjectURL(contractPdfBlob);
            setContractPdfUrl(contractPdfUrlLocal);

            // Create a URL for the compliance PDF
            const compliancePdfBlob = base64ToBlob(compliancePdfBase64, 'application/pdf');
            compliancePdfUrlLocal = URL.createObjectURL(compliancePdfBlob);
            setCompliancePdfUrl(compliancePdfUrlLocal);

        } catch (e) {
            setError(`Error creating PDF URLs: ${e.message}`);
            console.error("Error creating PDF URLs:", e);
        }

        // Cleanup URLs when component unmounts or base64 strings change
        return () => {
            URL.revokeObjectURL(contractPdfUrlLocal);
            URL.revokeObjectURL(compliancePdfUrlLocal);
        };

    }, [contractPdfBase64, compliancePdfBase64]);

    const base64ToBlob = (base64, type) => {
        const binStr = atob(base64);
        const len = binStr.length;
        const arr = new Uint8Array(len);
        for (let i = 0; i < len; i++) {
            arr[i] = binStr.charCodeAt(i);
        }
        return new Blob([arr], { type: type });
    }

    return (
        <div className="pdf-container">
            <div className="pdf-window">
                <h2>Generated Contract</h2>
                {contractPdfUrl ? (
                    <iframe src={contractPdfUrl} width="100%" height="600px" title="Contract PDF"/>
                ) : (
                    <p>Loading Contract PDF...</p>
                )}
            </div>
            <div className="pdf-window">
                <h2>Compliance Report</h2>
                {compliancePdfUrl ? (
                    <iframe src={compliancePdfUrl} width="100%" height="600px" title="Compliance PDF"/>
                ) : (
                    <p>Loading Compliance PDF...</p>
                )}
            </div>
        </div>
    );
};

export default PdfViewerPage;