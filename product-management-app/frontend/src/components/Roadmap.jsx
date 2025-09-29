import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const API_BASE_URL = 'http://localhost:8000';

const Roadmap = () => {
  const [roadmapData, setRoadmapData] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchRoadmapData = async () => {
      try {
        setLoading(true);
        const response = await axios.get(`${API_BASE_URL}/api/roadmap`);
        const data = response.data;

        const chartData = [
          { name: 'High Priority', count: data.High.length },
          { name: 'Medium Priority', count: data.Medium.length },
          { name: 'Low Priority', count: data.Low.length },
        ];

        setRoadmapData(chartData);
        setError(null);
      } catch (err) {
        setError('Failed to fetch roadmap data.');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchRoadmapData();
  }, []);

  if (loading) return <div className="text-center p-4">Loading Roadmap...</div>;
  if (error) return <div className="text-center p-4 text-red-600">{error}</div>;

  return (
    <div className="bg-white p-4 rounded-lg shadow">
      <h2 className="text-xl font-semibold mb-4">Roadmap Overview (by Priority)</h2>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart
          data={roadmapData}
          margin={{
            top: 5, right: 30, left: 20, bottom: 5,
          }}
        >
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="name" />
          <YAxis allowDecimals={false} />
          <Tooltip />
          <Legend />
          <Bar dataKey="count" fill="#8884d8" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};

export default Roadmap;
