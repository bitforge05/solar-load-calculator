import React, { useState } from 'react';
import { Upload, FileText, Download, CheckCircle, AlertCircle, Loader2, Zap } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 
  (['localhost', '127.0.0.1'].includes(window.location.hostname) ? 'http://localhost:8000' : '/api');

// Log warning if production is using localhost
if (import.meta.env.PROD && API_BASE_URL.includes('localhost')) {
  console.warn("WARNING: Frontend is in production but VITE_API_BASE_URL is still pointing to localhost. API calls will likely fail.");
}

function App() {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
      setError(null);
    }
  };

  const handleUpload = async () => {
    if (!file) {
      setError("Please select a file first.");
      return;
    }

    setLoading(true);
    setResult(null);
    setError(null);

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post(`${API_BASE_URL}/upload`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      
      if (response.data.error) {
        setError(response.data.error);
      } else {
        setResult(response.data);
      }
    } catch (err) {
      console.error(err);
      if (err.code === 'ERR_NETWORK') {
        setError(`Connection failed. Current API: ${API_BASE_URL}`);
      } else {
        setError(err.response?.data?.detail || "An error occurred during processing.");
      }
    } finally {
      setLoading(false);
    }
  };

  const downloadFile = () => {
    if (result && result.download_url) {
      window.open(`${API_BASE_URL}${result.download_url}`, '_blank');
    }
  };

  return (
    <div className="min-h-screen bg-[#0f172a] text-slate-200 font-sans p-6 md:p-12 flex flex-col items-center">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="max-w-4xl w-full text-center mb-12"
      >
        <div className="flex justify-center mb-4">
          <div className="bg-emerald-500/20 p-3 rounded-2xl border border-emerald-500/30">
            <Zap className="w-10 h-10 text-emerald-400" />
          </div>
        </div>
        <h1 className="text-4xl md:text-6xl font-bold mb-4 bg-gradient-to-r from-emerald-400 to-teal-400 bg-clip-text text-transparent">
          EnergyBAE Solar Assistant
        </h1>
        <p className="text-slate-400 text-lg md:text-xl">
          AI-Powered MSEDCL Bill Analysis & Solar Load Calculation
        </p>
      </motion.div>

      <div className="max-w-4xl w-full grid grid-cols-1 md:grid-cols-2 gap-8">
        {/* Upload Section */}
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          className="bg-slate-800/50 backdrop-blur-xl border border-slate-700/50 rounded-3xl p-8 shadow-2xl"
        >
          <h2 className="text-2xl font-semibold mb-6 flex items-center gap-2">
            <Upload className="w-6 h-6 text-blue-400" />
            Upload Bill
          </h2>

          <div
            className={`border-2 border-dashed rounded-2xl p-10 text-center transition-all cursor-pointer mb-6 ${file ? 'border-blue-500/50 bg-blue-500/5' : 'border-slate-700 hover:border-slate-500 hover:bg-slate-700/20'
              }`}
            onClick={() => document.getElementById('file-upload').click()}
          >
            <input
              id="file-upload"
              type="file"
              className="hidden"
              onChange={handleFileChange}
              accept=".pdf,image/*"
            />
            {file ? (
              <div className="flex flex-col items-center">
                <FileText className="w-12 h-12 text-blue-400 mb-4" />
                <p className="font-medium text-slate-200">{file.name}</p>
                <p className="text-sm text-slate-500">{(file.size / 1024 / 1024).toFixed(2)} MB</p>
              </div>
            ) : (
              <div className="flex flex-col items-center">
                <Upload className="w-12 h-12 text-slate-600 mb-4" />
                <p className="font-medium text-slate-400">Click or drag PDF/Image</p>
                <p className="text-sm text-slate-600 mt-2">Maximum file size: 10MB</p>
              </div>
            )}
          </div>

          <button
            onClick={handleUpload}
            disabled={!file || loading}
            className={`w-full py-4 rounded-xl font-bold text-lg flex items-center justify-center gap-2 transition-all ${!file || loading
                ? 'bg-slate-700 text-slate-500 cursor-not-allowed'
                : 'bg-gradient-to-r from-blue-600 to-indigo-600 text-white hover:shadow-[0_0_20px_rgba(37,99,235,0.4)] hover:scale-[1.02]'
              }`}
          >
            {loading ? (
              <>
                <Loader2 className="w-6 h-6 animate-spin" />
                Processing with AI...
              </>
            ) : (
              <>
                <Zap className="w-6 h-6 fill-white" />
                Generate Solar Excel
              </>
            )}
          </button>

          {error && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="mt-4 p-4 bg-red-500/10 border border-red-500/20 rounded-xl flex items-center gap-3 text-red-400 text-sm"
            >
              <AlertCircle className="w-5 h-5 flex-shrink-0" />
              {error}
            </motion.div>
          )}
        </motion.div>

        {/* Results Section */}
        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          className="bg-slate-800/50 backdrop-blur-xl border border-slate-700/50 rounded-3xl p-8 shadow-2xl relative flex flex-col h-full"
        >
          <h2 className="text-2xl font-semibold mb-6 flex items-center gap-2">
            <CheckCircle className="w-6 h-6 text-emerald-400" />
            Extraction Result
          </h2>

          <AnimatePresence mode="wait">
            {result ? (
              <motion.div
                key="result"
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                className="flex-grow"
              >
                <div className="grid grid-cols-2 gap-4 mb-8">
                  {Object.entries(result.extracted_data).map(([key, value]) => (
                    <div key={key} className="bg-slate-900/50 p-3 rounded-xl border border-slate-700/30">
                      <p className="text-[10px] uppercase tracking-wider text-slate-500 mb-1">{key.replace(/_/g, ' ')}</p>
                      <p className="text-sm font-medium text-slate-200 truncate">{value === null ? 'N/A' : value.toString()}</p>
                    </div>
                  ))}
                </div>

                <button
                  onClick={downloadFile}
                  className="w-full py-4 bg-emerald-600 hover:bg-emerald-500 text-white rounded-xl font-bold text-lg flex items-center justify-center gap-2 transition-all hover:shadow-[0_0_20px_rgba(16,185,129,0.3)]"
                >
                  <Download className="w-6 h-6" />
                  Download Filled Excel
                </button>
              </motion.div>
            ) : (
              <motion.div
                key="empty"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                className="flex flex-col items-center justify-center flex-grow py-12 opacity-30"
              >
                <FileText className="w-20 h-20 mb-4" />
                <p>Waiting for analysis...</p>
              </motion.div>
            )}
          </AnimatePresence>

          {loading && (
            <div className="absolute inset-0 bg-slate-900/40 backdrop-blur-[2px] rounded-3xl flex items-center justify-center z-10">
              <div className="flex flex-col items-center">
                <Loader2 className="w-10 h-10 text-blue-500 animate-spin mb-4" />
                <p className="text-blue-400 font-medium">Scanning Bill...</p>
              </div>
            </div>
          )}
        </motion.div>
      </div>

      <footer className="mt-12 text-slate-600 text-sm flex flex-col items-center gap-2">
      </footer>
    </div>
  );
}

export default App;
