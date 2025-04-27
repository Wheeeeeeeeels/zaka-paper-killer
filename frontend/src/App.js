import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import { Layout, Menu } from 'antd';
import { FileTextOutlined, EditOutlined } from '@ant-design/icons';
import Navbar from './components/Navbar';
import Home from './pages/Home';
import Papers from './pages/Papers';
import PaperDetail from './pages/PaperDetail';
import Login from './pages/Login';
import Register from './pages/Register';
import Profile from './pages/Profile';
import ICLRAnalysis from './pages/ICLRAnalysis';
import CHIAnalysis from './pages/CHIAnalysis';
import WritePaper from './pages/WritePaper';
import ProtectedRoute from './components/ProtectedRoute';
import { AuthProvider } from './contexts/AuthContext';
import './App.css';

const { Header, Content, Footer } = Layout;

function App() {
  return (
    <AuthProvider>
      <Router>
        <Layout className="layout">
          <Header>
            <Menu theme="dark" mode="horizontal" defaultSelectedKeys={['1']}>
              <Menu.Item key="1" icon={<FileTextOutlined />}>
                <Link to="/iclr">ICLR 2025</Link>
              </Menu.Item>
              <Menu.Item key="2" icon={<FileTextOutlined />}>
                <Link to="/chi">CHI 2025</Link>
              </Menu.Item>
              <Menu.Item key="3" icon={<EditOutlined />}>
                <Link to="/write-paper">写论文</Link>
              </Menu.Item>
            </Menu>
          </Header>
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
                <Route path="/iclr" element={<ICLRAnalysis />} />
                <Route path="/chi" element={<CHIAnalysis />} />
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