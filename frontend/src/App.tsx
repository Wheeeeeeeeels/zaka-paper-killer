import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { Layout } from 'antd';
import Header from './components/Header';
import Home from './pages/Home';
import Login from './pages/Login';
import PaperList from './pages/PaperList';
import PaperDetail from './pages/PaperDetail';
import PaperEdit from './pages/PaperEdit';
import './App.css';

const { Content, Footer } = Layout;

const App: React.FC = () => {
  const isAuthenticated = !!localStorage.getItem('token');

  return (
    <Layout className="layout">
      {isAuthenticated && <Header />}
      <Content style={{ padding: '0 50px', marginTop: isAuthenticated ? 64 : 0 }}>
        <div className="site-layout-content">
          <Routes>
            <Route path="/login" element={!isAuthenticated ? <Login /> : <Navigate to="/" />} />
            <Route path="/" element={isAuthenticated ? <Home /> : <Navigate to="/login" />} />
            <Route path="/papers" element={isAuthenticated ? <PaperList /> : <Navigate to="/login" />} />
            <Route path="/papers/new" element={isAuthenticated ? <PaperEdit /> : <Navigate to="/login" />} />
            <Route path="/papers/:id" element={isAuthenticated ? <PaperDetail /> : <Navigate to="/login" />} />
          </Routes>
        </div>
      </Content>
      {isAuthenticated && (
        <Footer style={{ textAlign: 'center' }}>
          Zaka Paper Killer ©{new Date().getFullYear()} Created by Your Team
        </Footer>
      )}
    </Layout>
  );
};

export default App; 