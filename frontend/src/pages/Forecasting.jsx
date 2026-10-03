import React, { useState } from 'react';
import axios from 'axios';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

export default function Forecasting() {
  const [formData, setFormData] = useState({
    dataset_id: '',
    date_column: '',
    sales_metric: '',
    group_column: '',
    specific_group: 'All',
    frequency: 'D',
    forecast_horizon: 30,
    model: 'XGBoost'
  });
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const payload = { ...formData, forecast_horizon: parseInt(formData.forecast_horizon) };
      if (!payload.group_column) { delete payload.group_column; delete payload.specific_group; }
      const res = await axios.post('http://localhost:8000/api/forecast/run', payload);
      setResult(res.data);
    } catch (err) {
      alert("Error generating forecast.");
      console.error(err);
    }
    setLoading(false);
  };

  return (
    <div className="p-8">
      <h1 className="text-3xl font-bold mb-6 text-gray-800">Sales Forecasting</h1>
      <div className="flex gap-8">
        <form onSubmit={handleSubmit} className="w-1/3 bg-white p-6 rounded-lg shadow-md space-y-4">
          <div><label className="block text-sm">Dataset ID</label><input type="text" name="dataset_id" value={formData.dataset_id} onChange={handleChange} className="w-full border p-2 rounded" required /></div>
          <div><label className="block text-sm">Date Column</label><input type="text" name="date_column" value={formData.date_column} onChange={handleChange} className="w-full border p-2 rounded" required /></div>
          <div><label className="block text-sm">Sales Metric</label><input type="text" name="sales_metric" value={formData.sales_metric} onChange={handleChange} className="w-full border p-2 rounded" required /></div>
          <div><label className="block text-sm">Group Column (Optional)</label><input type="text" name="group_column" value={formData.group_column} onChange={handleChange} className="w-full border p-2 rounded" /></div>
          <div><label className="block text-sm">Forecast Horizon (Days)</label><input type="number" name="forecast_horizon" value={formData.forecast_horizon} onChange={handleChange} className="w-full border p-2 rounded" required /></div>
          <div><label className="block text-sm">Model</label>
            <select name="model" value={formData.model} onChange={handleChange} className="w-full border p-2 rounded">
              <option>XGBoost</option><option>LightGBM</option>
            </select>
          </div>
          <button type="submit" disabled={loading} className="w-full bg-green-600 text-white py-2 rounded mt-4">{loading ? "Generating..." : "GENERATE FORECAST"}</button>
        </form>

        <div className="w-2/3">
          {result && (
            <div className="bg-white p-6 rounded-lg shadow-md border-t-4 border-green-500">
              <h2 className="text-2xl font-bold mb-4">Forecast Result</h2>
              <p><strong>Total Forecasted Sales:</strong> {result.summary.total_forecast.toFixed(2)}</p>
              <p><strong>Average per Period:</strong> {result.summary.avg_forecast.toFixed(2)}</p>
              <div className="mt-8 h-80">
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={result.forecasts}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="date" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Line type="monotone" dataKey="forecast" stroke="#10b981" name="Forecast Sales" />
                  </LineChart>
                </ResponsiveContainer>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
