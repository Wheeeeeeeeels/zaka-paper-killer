import React from 'react';
import { Layout, Menu, Button, Dropdown } from 'antd';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import {
  HomeOutlined,
  FileTextOutlined,
  UserOutlined,
  LogoutOutlined,
  SettingOutlined,
  ExperimentOutlined,
} from '@ant-design/icons';
import Logo from './Logo';
import { useAuth } from '../contexts/AuthContext';

const { Header } = Layout;

function Navbar() {
  const location = useLocation();
  const navigate = useNavigate();
  const { user, logout } = useAuth();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const userMenu = (
    <Menu>
      <Menu.Item key="profile" icon={<UserOutlined />} onClick={() => navigate('/profile')}>
        个人资料
      </Menu.Item>
      <Menu.Item key="settings" icon={<SettingOutlined />} onClick={() => navigate('/settings')}>
        设置
      </Menu.Item>
      <Menu.Divider />
      <Menu.Item key="logout" icon={<LogoutOutlined />} onClick={handleLogout}>
        退出登录
      </Menu.Item>
    </Menu>
  );

  return (
    <Header style={{ position: 'fixed', zIndex: 1, width: '100%' }}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <div style={{ display: 'flex', alignItems: 'center' }}>
          <Logo />
          <Menu
            theme="dark"
            mode="horizontal"
            selectedKeys={[location.pathname]}
            items={[
              {
                key: '/',
                icon: <HomeOutlined />,
                label: <Link to="/">首页</Link>,
              },
              {
                key: '/papers',
                icon: <FileTextOutlined />,
                label: <Link to="/papers">论文管理</Link>,
              },
              {
                key: '/iclr2025',
                icon: <ExperimentOutlined />,
                label: <Link to="/iclr2025">ICLR 2025</Link>,
              },
            ]}
          />
        </div>
        <div>
          {user ? (
            <Dropdown overlay={userMenu} placement="bottomRight">
              <Button type="text" icon={<UserOutlined />} style={{ color: 'white' }}>
                用户中心
              </Button>
            </Dropdown>
          ) : (
            <Button type="link" onClick={() => navigate('/login')} style={{ color: 'white' }}>
              登录
            </Button>
          )}
        </div>
      </div>
    </Header>
  );
}

export default Navbar; 