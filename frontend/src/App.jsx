import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';
import { Home, Upload, BarChart2, TrendingUp, Search } from 'lucide-react';

function Dashboard() {
  return (
    <div className="p-8">
      <h1 className="text-3xl font-bold mb-4">E-Commerce ML Intelligence Platform</h1>
      <p className="text-gray-600">Select an option from the sidebar to begin.</p>
    </div>
  );
}

function PurchasePrediction() {
  return <div className="p-8">Purchase Prediction UI (Integration ready)</div>;
}

function UploadDataset() {
  return <div className="p-8">Upload Dataset UI (Integration ready)</div>;
}

function Forecasting() {
  return <div className="p-8">Sales Forecasting UI (Integration ready)</div>;
}

function App() {
  return (
    <BrowserRouter>
      <div className="flex h-screen bg-gray-50">
        <aside className="w-64 bg-white shadow-md">
          <div className="p-4 text-xl font-bold text-blue-600">ML Platform</div>
          <nav className="mt-4 flex flex-col gap-2 p-4">
            <Link to="/" className="flex items-center gap-2 p-2 hover:bg-gray-100 rounded">
              <Home size={20} /> Dashboard
            </Link>
            <Link to="/purchase" className="flex items-center gap-2 p-2 hover:bg-gray-100 rounded">
              <Search size={20} /> Purchase Prediction
            </Link>
            <Link to="/upload" className="flex items-center gap-2 p-2 hover:bg-gray-100 rounded">
              <Upload size={20} /> Upload Dataset
            </Link>
            <Link to="/forecast" className="flex items-center gap-2 p-2 hover:bg-gray-100 rounded">
              <TrendingUp size={20} /> Sales Forecasting
            </Link>
          </nav>
        </aside>
        
        <main className="flex-1 overflow-auto">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/purchase" element={<PurchasePrediction />} />
            <Route path="/upload" element={<UploadDataset />} />
            <Route path="/forecast" element={<Forecasting />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
}

export default App;
