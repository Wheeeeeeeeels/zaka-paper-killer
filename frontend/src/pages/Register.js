import React, { useState } from 'react';
import { Form, Input, Button, message, Card, Typography, Space, Divider } from 'antd';
import { UserOutlined, LockOutlined, MailOutlined, PhoneOutlined, SafetyOutlined } from '@ant-design/icons';
import { Link, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { userAPI } from '../services/api';
import styled from 'styled-components';

const { Title, Text } = Typography;

const RegisterContainer = styled.div`
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
  padding: 20px;
`;

const RegisterCard = styled(Card)`
  width: 100%;
  max-width: 480px;
  background: rgba(255, 255, 255, 0.95);
  border-radius: 16px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(10px);
`;

const Logo = styled.div`
  text-align: center;
  margin-bottom: 32px;
  img {
    height: 48px;
  }
`;

const StyledForm = styled(Form)`
  .ant-form-item {
    margin-bottom: 24px;
  }
  
  .ant-input-affix-wrapper {
    border-radius: 8px;
    height: 48px;
    background: rgba(255, 255, 255, 0.9);
    border: 1px solid rgba(0, 0, 0, 0.1);
    transition: all 0.3s;
    
    &:hover, &:focus {
      border-color: #1890ff;
      box-shadow: 0 0 0 2px rgba(24, 144, 255, 0.1);
    }
  }
  
  .ant-btn {
    height: 48px;
    border-radius: 8px;
    font-size: 16px;
    font-weight: 500;
  }
`;

const SocialLogin = styled.div`
  text-align: center;
  margin-top: 24px;
`;

const SocialButton = styled(Button)`
  margin: 0 8px;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
`;

function Register() {
  const [loading, setLoading] = useState(false);
  const [form] = Form.useForm();
  const navigate = useNavigate();

  const onFinish = async (values) => {
    setLoading(true);
    try {
      await userAPI.register(values);
      message.success('注册成功！');
      navigate('/login');
    } catch (error) {
      message.error(error.response?.data?.message || '注册失败，请重试');
    } finally {
      setLoading(false);
    }
  };

  return (
    <RegisterContainer>
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <RegisterCard>
          <Logo>
            <img src="/logo.png" alt="Logo" />
          </Logo>
          
          <Title level={2} style={{ textAlign: 'center', marginBottom: 32 }}>
            创建账号
          </Title>

          <StyledForm
            form={form}
            name="register"
            onFinish={onFinish}
            scrollToFirstError
          >
            <Form.Item
              name="username"
              rules={[
                { required: true, message: '请输入用户名' },
                { min: 3, message: '用户名至少3个字符' },
                { max: 20, message: '用户名最多20个字符' },
                { pattern: /^[a-zA-Z0-9_-]+$/, message: '用户名只能包含字母、数字、下划线和连字符' }
              ]}
            >
              <Input
                prefix={<UserOutlined />}
                placeholder="用户名"
                size="large"
              />
            </Form.Item>

            <Form.Item
              name="email"
              rules={[
                { required: true, message: '请输入邮箱' },
                { type: 'email', message: '请输入有效的邮箱地址' }
              ]}
            >
              <Input
                prefix={<MailOutlined />}
                placeholder="邮箱"
                size="large"
              />
            </Form.Item>

            <Form.Item
              name="phone"
              rules={[
                { required: true, message: '请输入手机号' },
                { pattern: /^1[3-9]\d{9}$/, message: '请输入有效的手机号' }
              ]}
            >
              <Input
                prefix={<PhoneOutlined />}
                placeholder="手机号"
                size="large"
              />
            </Form.Item>

            <Form.Item
              name="password"
              rules={[
                { required: true, message: '请输入密码' },
                { min: 8, message: '密码至少8个字符' },
                { 
                  pattern: /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]+$/,
                  message: '密码必须包含大小写字母、数字和特殊字符'
                }
              ]}
            >
              <Input.Password
                prefix={<LockOutlined />}
                placeholder="密码"
                size="large"
              />
            </Form.Item>

            <Form.Item
              name="confirm"
              dependencies={['password']}
              rules={[
                { required: true, message: '请确认密码' },
                ({ getFieldValue }) => ({
                  validator(_, value) {
                    if (!value || getFieldValue('password') === value) {
                      return Promise.resolve();
                    }
                    return Promise.reject(new Error('两次输入的密码不一致'));
                  },
                }),
              ]}
            >
              <Input.Password
                prefix={<LockOutlined />}
                placeholder="确认密码"
                size="large"
              />
            </Form.Item>

            <Form.Item
              name="captcha"
              rules={[{ required: true, message: '请输入验证码' }]}
            >
              <Space>
                <Input
                  prefix={<SafetyOutlined />}
                  placeholder="验证码"
                  size="large"
                  style={{ width: '200px' }}
                />
                <Button type="primary" size="large">
                  获取验证码
                </Button>
              </Space>
            </Form.Item>

            <Form.Item>
              <Button
                type="primary"
                htmlType="submit"
                size="large"
                block
                loading={loading}
              >
                注册
              </Button>
            </Form.Item>

            <Divider>
              <Text type="secondary">或</Text>
            </Divider>

            <SocialLogin>
              <SocialButton type="default" icon={<img src="/google.png" alt="Google" style={{ width: 20 }} />} />
              <SocialButton type="default" icon={<img src="/github.png" alt="GitHub" style={{ width: 20 }} />} />
              <SocialButton type="default" icon={<img src="/wechat.png" alt="WeChat" style={{ width: 20 }} />} />
            </SocialLogin>

            <div style={{ textAlign: 'center', marginTop: 24 }}>
              <Text type="secondary">
                已有账号？ <Link to="/login">立即登录</Link>
              </Text>
            </div>
          </StyledForm>
        </RegisterCard>
      </motion.div>
    </RegisterContainer>
  );
}

export default Register; 