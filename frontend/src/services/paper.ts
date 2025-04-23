import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:3000/api';

export interface Paper {
  id: string;
  title: string;
  status: string;
  createdAt: string;
}

export interface AnalysisResult {
  id: string;
  type: string;
  content: string;
  createdAt: string;
}

export interface ExperimentResult {
  id: string;
  name: string;
  parameters: Record<string, any>;
  metrics: Record<string, number>;
  createdAt: string;
}

export interface SubmissionData {
  conference: string;
  track: string;
  abstract: string;
  keywords: string;
}

export const getPapers = async (): Promise<Paper[]> => {
  const token = localStorage.getItem('token');
  const response = await axios.get(`${API_URL}/papers`, {
    headers: { Authorization: `Bearer ${token}` }
  });
  return response.data;
};

export const getPaper = async (id: string): Promise<Paper> => {
  const token = localStorage.getItem('token');
  const response = await axios.get(`${API_URL}/papers/${id}`, {
    headers: { Authorization: `Bearer ${token}` }
  });
  return response.data;
};

export const createPaper = async (data: { title: string }): Promise<Paper> => {
  const token = localStorage.getItem('token');
  const response = await axios.post(`${API_URL}/papers`, data, {
    headers: { Authorization: `Bearer ${token}` }
  });
  return response.data;
};

export const updatePaper = async (id: string, data: Partial<Paper>): Promise<Paper> => {
  const token = localStorage.getItem('token');
  const response = await axios.put(`${API_URL}/papers/${id}`, data, {
    headers: { Authorization: `Bearer ${token}` }
  });
  return response.data;
};

export const deletePaper = async (id: string): Promise<void> => {
  const token = localStorage.getItem('token');
  await axios.delete(`${API_URL}/papers/${id}`, {
    headers: { Authorization: `Bearer ${token}` }
  });
};

export const analyzePaper = async (id: string): Promise<AnalysisResult[]> => {
  const token = localStorage.getItem('token');
  const response = await axios.post(`${API_URL}/papers/${id}/analyze`, {}, {
    headers: { Authorization: `Bearer ${token}` }
  });
  return response.data;
};

export const runExperiment = async (id: string): Promise<ExperimentResult[]> => {
  const token = localStorage.getItem('token');
  const response = await axios.post(`${API_URL}/papers/${id}/experiments`, {}, {
    headers: { Authorization: `Bearer ${token}` }
  });
  return response.data;
};

export const submitPaper = async (id: string, data: SubmissionData): Promise<void> => {
  const token = localStorage.getItem('token');
  await axios.post(`${API_URL}/papers/${id}/submissions`, data, {
    headers: { Authorization: `Bearer ${token}` }
  });
}; 