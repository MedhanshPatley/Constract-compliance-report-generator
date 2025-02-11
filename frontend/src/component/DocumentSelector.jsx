import React, { useState } from "react";
import { ArrowLeft } from 'lucide-react';
import ContractForm from "./ContractForm";
import './DocumentSelector.css'

const DocumentSelector = () => {
  const [selectedDocument, setSelectedDocument] = useState("");
  const [sidebarVisible, setSidebarVisible] = useState(true);

  const renderForm = () => {
    if (!selectedDocument) {
      return <div className="placeholder">Please select a document type.</div>;
    }
    switch (selectedDocument) {
      case "contract":
        return <ContractForm />;
      default:
        return <div className="placeholder">Form not available for this document type.</div>;
    }
  };

  return (
    <div className="document-container">
      {/* Back Arrow Button (Only visible when sidebar is hidden) */}
      {!sidebarVisible && (
        <button className="back-button" onClick={() => setSidebarVisible(true)}>
          <ArrowLeft />
        </button>
      )}
      
      {/* Sidebar for Document Type Selection */}
      {sidebarVisible && (
        <div className="sidebar">
          <h2>Select Document Type</h2>
          <ul>
            <li
              className={selectedDocument === "contract" ? "active" : ""}
              onClick={() => {
                setSelectedDocument("contract");
                setSidebarVisible(false); // Hide sidebar after selection
              }}
            >
              Contract
            </li>
          </ul>
        </div>
      )}
      
      {/* Right Side - Display Form Only After Selection */}
      <div className="form-container">{renderForm()}</div>
    </div>
  );
};

export default DocumentSelector;
