import React from 'react';
import { Card, Typography } from 'antd';
import { Link } from 'react-router-dom';
import RegisterForm from '../components/auth/RegisterForm';

const { Title } = Typography;

const Register: React.FC = () => {
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
          注册
        </Title>
        <RegisterForm />
        <div style={{ textAlign: 'center', marginTop: 16 }}>
          已有账号？ <Link to="/login">立即登录</Link>
        </div>
      </Card>
    </div>
  );
};

export default Register; 