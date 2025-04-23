import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Layout from '../components/layout/Layout';
import Login from '../pages/Login';
import Register from '../pages/Register';
import Dashboard from '../pages/Dashboard';
import PaperList from '../pages/PaperList';
import PaperForm from '../pages/PaperForm';
import PaperAnalysis from '../pages/PaperAnalysis';
import PrivateRoute from './PrivateRoute';

const AppRoutes: React.FC = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        
        <Route path="/" element={<PrivateRoute><Layout /></PrivateRoute>}>
          <Route index element={<Navigate to="/dashboard" replace />} />
          <Route path="dashboard" element={<Dashboard />} />
          <Route path="papers" element={<PaperList />} />
          <Route path="papers/new" element={<PaperForm />} />
          <Route path="papers/:id/edit" element={<PaperForm />} />
          <Route path="papers/:id/analysis" element={<PaperAnalysis />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
};

export default AppRoutes; 