import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:3000/api';

export interface LoginResponse {
  token: string;
  user: {
    id: string;
    email: string;
    name: string;
  };
}

export const login = async (credentials: { email: string; password: string }): Promise<LoginResponse> => {
  const response = await axios.post(`${API_URL}/auth/login`, credentials);
  return response.data;
};

export const register = async (userData: { 
  email: string; 
  password: string; 
  name: string;
}): Promise<LoginResponse> => {
  const response = await axios.post(`${API_URL}/auth/register`, userData);
  return response.data;
};

export const getCurrentUser = async (): Promise<LoginResponse['user']> => {
  const token = localStorage.getItem('token');
  const response = await axios.get(`${API_URL}/auth/me`, {
    headers: { Authorization: `Bearer ${token}` }
  });
  return response.data;
}; 