import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Roadmap from './components/Roadmap';
import { Button } from './components/ui/button';
import { Textarea } from './components/ui/textarea';

const API_BASE_URL = 'http://localhost:8000'; // The FastAPI backend runs on port 8000 by default

function App() {
  const [tasks, setTasks] = useState([]);
  const [inputText, setInputText] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchTasks = async () => {
    try {
      setLoading(true);
      const response = await axios.get(`${API_BASE_URL}/api/tasks`);
      setTasks(response.data);
      setError(null);
    } catch (err) {
      setError('Failed to fetch tasks. Make sure the backend server is running.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchTasks();
  }, []);

  const handleProcessText = async () => {
    if (!inputText.trim()) {
      alert('Please enter some text to process.');
      return;
    }
    try {
      setLoading(true);
      // In Phase 2, the backend expects unstructured text.
      const response = await axios.post(`${API_BASE_URL}/api/process`, { text: inputText });
      setTasks([...tasks, response.data]);
      setInputText('');
      setError(null);
    } catch (err) {
      setError('Failed to process text. Please try again.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const getPriorityColor = (priority) => {
    switch (priority?.toLowerCase()) {
      case 'high': return 'bg-red-100 text-red-800';
      case 'medium': return 'bg-yellow-100 text-yellow-800';
      case 'low': return 'bg-gray-100 text-gray-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const getTypeColor = (type) => {
    switch (type?.toLowerCase()) {
      case 'feature': return 'bg-blue-100 text-blue-800';
      case 'pain_point': return 'bg-orange-100 text-orange-800';
      case 'enhancement': return 'bg-green-100 text-green-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };


  return (
    <div className="min-h-screen bg-gray-50 text-gray-900">
      <header className="bg-white shadow-sm">
        <div className="max-w-4xl mx-auto px-4 py-4">
          <h1 className="text-2xl font-bold tracking-tight">Product Management Assistant</h1>
          <p className="text-gray-500">Your "vibe coding" space for product ideas.</p>
        </div>
      </header>
      <main className="max-w-4xl mx-auto px-4 py-8">
        <div id="input-section">
          <div className="bg-white p-4 rounded-lg shadow">
            <Textarea
              placeholder="Paste your customer feedback, meeting notes, or feature ideas here..."
              rows="5"
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              disabled={loading}
            />
            <Button
              className="mt-2"
              onClick={handleProcessText}
              disabled={loading}
            >
              {loading ? 'Processing...' : 'Process Text'}
            </Button>
          </div>
        </div>

        {error && <div className="mt-4 text-red-600 bg-red-100 p-3 rounded-md">{error}</div>}

        <div id="roadmap-section" className="mt-12">
          <Roadmap />
        </div>

        <div id="backlog-section" className="mt-12">
          <h2 className="text-xl font-semibold mb-4">Backlog</h2>
          <div className="space-y-4">
            {tasks.length === 0 && !loading && (
              <div className="text-center text-gray-500">No tasks yet. Process some text to get started!</div>
            )}
            {loading && tasks.length === 0 && (
              <div className="text-center text-gray-500">Loading tasks...</div>
            )}
            {tasks.map((task) => (
              <div key={task.id} className="bg-white p-4 rounded-lg shadow">
                <h3 className="font-bold">{task.description}</h3>
                <p className="text-sm text-gray-600 mt-1">{task.user_story}</p>
                <div className="mt-2 flex items-center space-x-4">
                  <span className={`text-xs font-semibold px-2 py-1 ${getTypeColor(task.type)} rounded-full`}>{task.type}</span>
                  <span className={`text-xs font-semibold px-2 py-1 ${getPriorityColor(task.priority)} rounded-full`}>{task.priority}</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;
