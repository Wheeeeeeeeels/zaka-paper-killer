import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Layout } from 'antd';
import Navbar from './components/Navbar';
import Home from './pages/Home';
import Papers from './pages/Papers';
import PaperDetail from './pages/PaperDetail';
import Login from './pages/Login';
import Register from './pages/Register';
import Profile from './pages/Profile';
import ICLRAnalysis from './pages/ICLRAnalysis';
import WritePaper from './pages/WritePaper';
import ProtectedRoute from './components/ProtectedRoute';
import { AuthProvider } from './contexts/AuthContext';
import './App.css';

const { Content, Footer } = Layout;

function App() {
  return (
    <AuthProvider>
      <Router>
        <Layout className="layout">
          <Navbar />
          <Content style={{ padding: '0 50px', marginTop: 64 }}>
            <div className="site-layout-content">
              <Routes>
                <Route path="/" element={<Home />} />
                <Route path="/login" element={<Login />} />
                <Route path="/register" element={<Register />} />
                <Route
                  path="/papers"
                  element={
                    <ProtectedRoute>
                      <Papers />
                    </ProtectedRoute>
                  }
                />
                <Route
                  path="/papers/:id"
                  element={
                    <ProtectedRoute>
                      <PaperDetail />
                    </ProtectedRoute>
                  }
                />
                <Route
                  path="/profile"
                  element={
                    <ProtectedRoute>
                      <Profile />
                    </ProtectedRoute>
                  }
                />
                <Route path="/iclr2025" element={<ICLRAnalysis />} />
                <Route path="/write-paper" element={<WritePaper />} />
              </Routes>
            </div>
          </Content>
          <Footer style={{ textAlign: 'center' }}>
            Paper Killer ©{new Date().getFullYear()} Created by Your Team
          </Footer>
        </Layout>
      </Router>
    </AuthProvider>
  );
}

export default App; 