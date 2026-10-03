import React, { useState } from 'react';
import axios from 'axios';

import { Loader2 } from 'lucide-react';

export default function UploadDataset() {
  const [file, setFile] = useState(null);
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleUpload = async (e) => {
    e.preventDefault();
    if (!file) return;
    setLoading(true);
    const formData = new FormData();
    formData.append('file', file);
    try {
      const res = await axios.post('http://localhost:8000/api/datasets/upload', formData);
      setAnalysis(res.data);
    } catch (err) {
      alert("Error uploading file.");
      console.error(err);
    }
    setLoading(false);
  };

  return (
    <div className="p-8">
      <h1 className="text-3xl font-bold mb-6 text-gray-800">Upload Dataset</h1>
      <form onSubmit={handleUpload} className="mb-8 flex flex-col items-start gap-4">
        <input 
          type="file" 
          accept=".csv,.xlsx" 
          onChange={(e) => setFile(e.target.files[0])} 
          className="block w-full max-w-sm text-sm text-gray-500
            file:mr-4 file:py-2 file:px-4
            file:rounded-full file:border-0
            file:text-sm file:font-semibold
            file:bg-blue-50 file:text-blue-700
            hover:file:bg-blue-100 cursor-pointer"
        />
        <button 
          type="submit" 
          disabled={loading || !file} 
          className={`flex items-center justify-center gap-2 px-6 py-2.5 rounded-lg font-medium text-white transition-all duration-300
            ${loading || !file 
              ? 'bg-blue-400 cursor-not-allowed opacity-70' 
              : 'bg-blue-600 hover:bg-blue-700 hover:shadow-lg hover:-translate-y-0.5 cursor-pointer'}`}
        >
          {loading && <Loader2 className="animate-spin" size={18} />}
          {loading ? "Analyzing..." : "Upload & Analyze"}
        </button>
      </form>

      {analysis && (
        <div className="bg-white p-6 rounded-lg shadow-md border-t-4 border-green-500">
          <h2 className="text-2xl font-bold mb-4">Dataset Analysis: {analysis.filename}</h2>
          <p><strong>Dataset ID:</strong> {analysis.id}</p>
          <p><strong>Rows:</strong> {analysis.rows} | <strong>Columns:</strong> {analysis.columns}</p>
          <p><strong>Date Column Detected:</strong> {analysis.date_columns.join(', ') || 'None'}</p>
          <p><strong>Sales Candidates:</strong> {analysis.sales_candidates.join(', ') || 'None'}</p>
          <p><strong>Group Candidates:</strong> {analysis.group_candidates.join(', ') || 'None'}</p>
          
          <div className="mt-4 p-4 bg-gray-100 rounded">
            <strong>Forecast Ready:</strong> {analysis.forecast_ready ? <span className="text-green-600 font-bold">Yes ✓</span> : <span className="text-red-600 font-bold">No ✗</span>}
          </div>
          <p className="text-sm text-gray-500 mt-2">Copy the Dataset ID to configure forecasting in the next tab.</p>
        </div>
      )}
    </div>
  );
}
