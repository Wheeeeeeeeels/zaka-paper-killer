import React, { createContext, useState, useContext, useEffect } from 'react';
import { message } from 'antd';
import { authAPI } from '../services/api';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      // 这里可以添加验证 token 的逻辑
      setUser({ token });
    }
    setLoading(false);
  }, []);

  const login = async (email, password) => {
    try {
      const formData = new FormData();
      formData.append('email', email);
      formData.append('password', password);

      const response = await authAPI.login(formData);
      localStorage.setItem('token', response.access_token);
      setUser({ token: response.access_token });
      message.success('登录成功');
      return true;
    } catch (error) {
      message.error('登录失败，请检查邮箱和密码');
      return false;
    }
  };

  const register = async (username, email, password) => {
    try {
      await authAPI.register({ username, email, password });
      message.success('注册成功，请登录');
      return true;
    } catch (error) {
      message.error('注册失败，请稍后重试');
      return false;
    }
  };

  const logout = () => {
    localStorage.removeItem('token');
    setUser(null);
    message.success('已退出登录');
  };

  return (
    <AuthContext.Provider value={{ user, loading, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}; 