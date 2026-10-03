import React, { useState, useEffect } from 'react';

export default function Dashboard() {
  const [health, setHealth] = useState("Checking...");

  useEffect(() => {
    fetch('http://localhost:8000/api/health')
      .then(res => res.json())
      .then(data => setHealth(data.status))
      .catch(() => setHealth("Backend Offline"));
  }, []);

  return (
    <div className="p-8">
      <h1 className="text-3xl font-bold mb-6 text-gray-800">Platform Dashboard</h1>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-white p-6 rounded-lg shadow-md border-t-4 border-blue-500">
          <h2 className="text-xl font-semibold mb-2">System Status</h2>
          <p className="text-gray-600">Backend: <span className={`font-bold ${health === 'ok' ? 'text-green-500' : 'text-red-500'}`}>{health}</span></p>
        </div>
        <div className="bg-white p-6 rounded-lg shadow-md border-t-4 border-purple-500">
          <h2 className="text-xl font-semibold mb-2">Purchase Models</h2>
          <p className="text-gray-600">XGBoost & LightGBM</p>
          <p className="text-gray-600 text-sm mt-2">Loaded and ready for predictions.</p>
        </div>
        <div className="bg-white p-6 rounded-lg shadow-md border-t-4 border-green-500">
          <h2 className="text-xl font-semibold mb-2">Forecasting Engine</h2>
          <p className="text-gray-600">Time-series generic engine</p>
          <p className="text-gray-600 text-sm mt-2">Ready for dataset upload.</p>
        </div>
      </div>
    </div>
  );
}
