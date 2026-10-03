import React, { useState } from 'react';
import axios from 'axios';

export default function PurchasePrediction() {
  const [formData, setFormData] = useState({
    Administrative: 0, Administrative_Duration: 0.0,
    Informational: 0, Informational_Duration: 0.0,
    ProductRelated: 0, ProductRelated_Duration: 0.0,
    BounceRates: 0.0, ExitRates: 0.0, PageValues: 0.0, SpecialDay: 0.0,
    Month: 'May', OperatingSystems: 1, Browser: 1, Region: 1, TrafficType: 1,
    VisitorType: 'Returning_Visitor', Weekend: false,
    model_type: 'XGBoost', variant: 'Full'
  });
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : (['Administrative', 'Informational', 'ProductRelated', 'OperatingSystems', 'Browser', 'Region', 'TrafficType'].includes(name) ? parseInt(value) : (['Month', 'VisitorType', 'model_type', 'variant'].includes(name) ? value : parseFloat(value)))
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const res = await axios.post('http://localhost:8000/api/purchase/predict', formData);
      setResult(res.data);
    } catch (err) {
      alert("Error generating prediction. Check console.");
      console.error(err);
    }
    setLoading(false);
  };

  return (
    <div className="p-8">
      <h1 className="text-3xl font-bold mb-6 text-gray-800">Purchase Prediction</h1>
      <div className="flex gap-8">
        <form onSubmit={handleSubmit} className="w-1/2 bg-white p-6 rounded-lg shadow-md space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div><label className="block text-sm">Administrative</label><input type="number" name="Administrative" value={formData.Administrative} onChange={handleChange} className="w-full border p-2 rounded" /></div>
            <div><label className="block text-sm">Admin Duration</label><input type="number" step="0.1" name="Administrative_Duration" value={formData.Administrative_Duration} onChange={handleChange} className="w-full border p-2 rounded" /></div>
            <div><label className="block text-sm">Informational</label><input type="number" name="Informational" value={formData.Informational} onChange={handleChange} className="w-full border p-2 rounded" /></div>
            <div><label className="block text-sm">Info Duration</label><input type="number" step="0.1" name="Informational_Duration" value={formData.Informational_Duration} onChange={handleChange} className="w-full border p-2 rounded" /></div>
            <div><label className="block text-sm">Product Related</label><input type="number" name="ProductRelated" value={formData.ProductRelated} onChange={handleChange} className="w-full border p-2 rounded" /></div>
            <div><label className="block text-sm">Product Duration</label><input type="number" step="0.1" name="ProductRelated_Duration" value={formData.ProductRelated_Duration} onChange={handleChange} className="w-full border p-2 rounded" /></div>
            <div><label className="block text-sm">Bounce Rates</label><input type="number" step="0.01" name="BounceRates" value={formData.BounceRates} onChange={handleChange} className="w-full border p-2 rounded" /></div>
            <div><label className="block text-sm">Exit Rates</label><input type="number" step="0.01" name="ExitRates" value={formData.ExitRates} onChange={handleChange} className="w-full border p-2 rounded" /></div>
            <div><label className="block text-sm">Page Values</label><input type="number" step="0.1" name="PageValues" value={formData.PageValues} onChange={handleChange} className="w-full border p-2 rounded" /></div>
            <div><label className="block text-sm">Month</label><input type="text" name="Month" value={formData.Month} onChange={handleChange} className="w-full border p-2 rounded" /></div>
            <div><label className="block text-sm">Visitor Type</label><input type="text" name="VisitorType" value={formData.VisitorType} onChange={handleChange} className="w-full border p-2 rounded" /></div>
            <div className="flex items-center gap-2 mt-6"><input type="checkbox" name="Weekend" checked={formData.Weekend} onChange={handleChange} /> <label>Weekend</label></div>
          </div>
          <div className="grid grid-cols-2 gap-4 border-t pt-4">
             <div><label className="block text-sm">Model</label>
               <select name="model_type" value={formData.model_type} onChange={handleChange} className="w-full border p-2 rounded">
                 <option>XGBoost</option><option>LightGBM</option>
               </select>
             </div>
             <div><label className="block text-sm">Variant</label>
               <select name="variant" value={formData.variant} onChange={handleChange} className="w-full border p-2 rounded">
                 <option>Full</option><option>No_PageValues</option>
               </select>
             </div>
          </div>
          <button type="submit" disabled={loading} className="w-full bg-blue-600 text-white py-2 rounded mt-4">{loading ? "Predicting..." : "PREDICT PURCHASE"}</button>
        </form>

        <div className="w-1/2">
          {result && (
            <div className="bg-white p-6 rounded-lg shadow-md border-t-4 border-blue-500">
              <h2 className="text-2xl font-bold mb-4">Result: {result.prediction}</h2>
              <p><strong>Purchase Probability:</strong> {(result.purchase_probability * 100).toFixed(2)}%</p>
              <p><strong>Non-Purchase Probability:</strong> {(result.non_purchase_probability * 100).toFixed(2)}%</p>
              <p className="mt-4 text-sm text-gray-500">Model: {result.model} | Variant: {result.variant}</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
