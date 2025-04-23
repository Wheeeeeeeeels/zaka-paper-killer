import React from 'react';
import { createBrowserRouter, Navigate } from 'react-router-dom';
import PaperList from '../pages/PaperList';
import PaperDetail from '../pages/PaperDetail';
import Login from '../pages/Login';
import Register from '../pages/Register';
import Layout from '../components/Layout';

const router = createBrowserRouter([
  {
    path: '/',
    element: <Layout />,
    children: [
      {
        path: '/',
        element: <Navigate to="/papers" replace />
      },
      {
        path: '/papers',
        element: <PaperList />
      },
      {
        path: '/papers/:id',
        element: <PaperDetail />
      }
    ]
  },
  {
    path: '/login',
    element: <Login />
  },
  {
    path: '/register',
    element: <Register />
  }
]);

export default router; 