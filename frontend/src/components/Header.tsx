import React from 'react';
import { Layout, Menu } from 'antd';
import { useNavigate } from 'react-router-dom';
import { HomeOutlined, FileTextOutlined, UserOutlined } from '@ant-design/icons';

const { Header } = Layout;

const AppHeader: React.FC = () => {
  const navigate = useNavigate();

  const menuItems = [
    {
      key: 'home',
      icon: <HomeOutlined />,
      label: '首页',
      onClick: () => navigate('/')
    },
    {
      key: 'papers',
      icon: <FileTextOutlined />,
      label: '论文管理',
      onClick: () => navigate('/papers')
    },
    {
      key: 'profile',
      icon: <UserOutlined />,
      label: '个人中心',
      onClick: () => navigate('/profile')
    }
  ];

  return (
    <Header style={{ position: 'fixed', zIndex: 1, width: '100%' }}>
      <div className="logo" />
      <Menu
        theme="dark"
        mode="horizontal"
        defaultSelectedKeys={['home']}
        items={menuItems}
      />
    </Header>
  );
};

export default AppHeader; 