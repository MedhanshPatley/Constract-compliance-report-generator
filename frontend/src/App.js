// import ContractForm from "./ContractForm";
// import React from 'react';

// function App() {
//   return (
//     <div className="min-h-screen flex items-center justify-center bg-gray-100">
//       <ContractForm />
//     </div>
//   );
// }

// export default App;

// import React from "react";
// import DocumentSelector from "../src/component/DocumentSelector"; // Import the new component

// function App() {
//   return (
//     <div>
//       <DocumentSelector /> {/* Now, the document selection UI is included */}
//     </div>
//   );
// }

// export default App;

import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import DocumentSelector from "../src/component/DocumentSelector";
import PdfViewerPage from '../src/component/PdfViewerPage'; // Import the new component

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<DocumentSelector />} />
        <Route path="/pdf-viewer" element={<PdfViewerPage />} />
      </Routes>
    </Router>
  );
}

export default App;
