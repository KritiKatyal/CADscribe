import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [prompt, setPrompt] = useState('');
  const [size, setSize] = useState(100.0);
  const [complexity, setComplexity] = useState('medium');
  const [modification, setModification] = useState('');
  const [modelFile, setModelFile] = useState(null);
  const [modifiedFile, setModifiedFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [actionTaken, setActionTaken] = useState('');
  const [error, setError] = useState('');

  const handleGenerateModel = async () => {
    setLoading(true);
    setError('');
    setModelFile(null);
    setModifiedFile(null);
    try {
      const response = await axios.post('http://127.0.0.1:8000/generate_model/', {
        prompt,
        size,
        complexity,
      });
      if (response.data.error?.includes('Shape not recognized')) {
        setError('Shape not recognized. Please describe a valid shape.');
      } else {
        setModelFile(response.data.file);
        setActionTaken('generate');
      }
    } catch (err) {
      setError('Error generating model: ' + (err.response?.data?.detail || 'Server error.'));
      console.error('Error generating model:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleModifyModel = async () => {
    setLoading(true);
    setError('');
    setModelFile(null);
    setModifiedFile(null);
    try {
      const response = await axios.post('http://127.0.0.1:8000/modify_model/', {
        prompt,
        size,
        complexity,
        modification,
      });
      if (response.data.error?.includes('Shape not recognized')) {
        setError('Shape not recognized. Try modifying a valid model.');
      } else {
        setModifiedFile(response.data.modifiedFile);
        setActionTaken('modify');
      }
    } catch (err) {
      setError('Error modifying model: ' + (err.response?.data?.detail || 'Server error.'));
      console.error('Error modifying model:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <div className="notion-container">
        
        <main className="main-content">
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
    <img 
      src="/logo.png" 
      alt="CADscribe Logo" 
      style={{ height: '50px', width: '50px', objectFit: 'contain' }} 
    />
    <h1 style={{ margin: 0 }}>CADscribe: Conversational 3D CAD Modeling</h1>
  </div>
<h1> </h1>
          <div className="input-group">
            <label>Prompt</label>
            <input
              type="text"
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              placeholder="Describe the shape"
            />
          </div>

          <div className="input-group">
            <label>Size (mm)</label>
            <input
              type="number"
              value={size}
              onChange={(e) => setSize(parseFloat(e.target.value))}
            />
          </div>

          <div className="input-group">
            <label>Complexity</label>
            <select
              value={complexity}
              onChange={(e) => setComplexity(e.target.value)}
            >
              <option value="low">Low</option>
              <option value="medium">Medium</option>
              <option value="high">High</option>
            </select>
          </div>

          <div className="input-group">
            <label>Modification</label>
            <input
              type="text"
              value={modification}
              onChange={(e) => setModification(e.target.value)}
              placeholder="e.g., increase size by 10mm"
            />
          </div>

          <div className="button-group">
            <button onClick={handleGenerateModel}>Generate Model</button>
            <button onClick={handleModifyModel}>Modify Model</button>
          </div>

          {loading && <p className="loading">Processing your request...</p>}
          {!loading && error && <p className="error">{error}</p>}

          {!loading && modelFile && actionTaken === 'generate' && (
            <div className="result">
              <h3>Generated Model</h3>
              <a
                href={`http://127.0.0.1:8000/${modelFile}`}
                target="_blank"
                rel="noopener noreferrer"
              >
                Download Model
              </a>
            </div>
          )}

          {!loading && modifiedFile && actionTaken === 'modify' && (
            <div className="result">
              <h3>Modified Model</h3>
              <a
                href={`http://127.0.0.1:8000/${modifiedFile}`}
                target="_blank"
                rel="noopener noreferrer"
              >
                Download Modified Model
              </a>
            </div>
          )}
          {/* Footer Section */}
      <div style={{ marginTop: '40px', padding: '20px', textAlign: 'center', backgroundColor: '#f9f9f9', borderTop: '1px solid #ddd' }}>
        <p style={{ margin: '5px 0', fontSize: '16px' }}>Made with ❤️ by <strong>Kriti</strong></p>
        <p style={{ margin: '5px 0', fontSize: '14px' }}>
          Contact me at: <a href="mailto:kritikatyal06@gmail.com">kritikatyal06@gmail.com</a>
          
        </p>
      </div>
        </main>
      </div>
    </div>
  );
}

export default App;