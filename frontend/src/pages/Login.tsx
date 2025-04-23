import React from 'react';
import { Card, Typography } from 'antd';
import { Link } from 'react-router-dom';
import LoginForm from '../components/auth/LoginForm';

const { Title } = Typography;

const Login: React.FC = () => {
  return (
    <div style={{ 
      display: 'flex', 
      justifyContent: 'center', 
      alignItems: 'center', 
      minHeight: '100vh',
      background: '#f0f2f5'
    }}>
      <Card style={{ width: 400 }}>
        <Title level={2} style={{ textAlign: 'center', marginBottom: 24 }}>
          登录
        </Title>
        <LoginForm />
        <div style={{ textAlign: 'center', marginTop: 16 }}>
          还没有账号？ <Link to="/register">立即注册</Link>
        </div>
      </Card>
    </div>
  );
};

export default Login; 