import React, { useState, useEffect } from 'react';
import { Card, Avatar, Button, message, Tabs, List, Statistic, Row, Col, Form, Input, Upload, Space, Tag } from 'antd';
import { UserOutlined, MailOutlined, PhoneOutlined, EditOutlined, SaveOutlined, StarOutlined, FileTextOutlined, MessageOutlined, UploadOutlined, TagOutlined } from '@ant-design/icons';
import { userAPI } from '../services/api';
import { useAuth } from '../contexts/AuthContext';

const { TabPane } = Tabs;
const { TextArea } = Input;

function Profile() {
  const { user, updateUser } = useAuth();
  const [loading, setLoading] = useState(false);
  const [stats, setStats] = useState({
    totalPapers: 0,
    favoritePapers: 0,
    totalComments: 0,
    totalTags: 0
  });
  const [favoritePapers, setFavoritePapers] = useState([]);
  const [comments, setComments] = useState([]);
  const [editing, setEditing] = useState(false);
  const [form] = Form.useForm();

  useEffect(() => {
    fetchUserStats();
    fetchFavoritePapers();
    fetchUserComments();
  }, []);

  const fetchUserStats = async () => {
    try {
      const data = await userAPI.getStats();
      setStats(data);
    } catch (error) {
      message.error('获取用户统计信息失败');
    }
  };

  const fetchFavoritePapers = async () => {
    try {
      const data = await userAPI.getFavoritePapers();
      setFavoritePapers(data);
    } catch (error) {
      message.error('获取收藏论文失败');
    }
  };

  const fetchUserComments = async () => {
    try {
      const data = await userAPI.getUserComments();
      setComments(data);
    } catch (error) {
      message.error('获取评论历史失败');
    }
  };

  const handleUpdateProfile = async (values) => {
    setLoading(true);
    try {
      await userAPI.updateProfile(values);
      updateUser({ ...user, ...values });
      message.success('个人资料更新成功');
      setEditing(false);
    } catch (error) {
      message.error('更新个人资料失败');
    } finally {
      setLoading(false);
    }
  };

  const handleAvatarChange = async (info) => {
    if (info.file.status === 'done') {
      try {
        const response = await userAPI.updateAvatar(info.file.response.url);
        updateUser({ ...user, avatar: response.avatar });
        message.success('头像更新成功');
      } catch (error) {
        message.error('头像更新失败');
      }
    }
  };

  return (
    <div style={{ padding: '24px 0' }}>
      <Row gutter={[24, 24]}>
        <Col span={8}>
          <Card>
            <div style={{ textAlign: 'center', marginBottom: 24 }}>
              <Upload
                name="avatar"
                showUploadList={false}
                action="/api/users/avatar"
                onChange={handleAvatarChange}
              >
                <Avatar
                  size={120}
                  src={user?.avatar}
                  icon={<UserOutlined />}
                  style={{ cursor: 'pointer' }}
                />
              </Upload>
              <h2 style={{ marginTop: 16 }}>{user?.username}</h2>
              <p>{user?.email}</p>
            </div>

            <Form
              form={form}
              layout="vertical"
              initialValues={user}
              onFinish={handleUpdateProfile}
            >
              <Form.Item
                name="username"
                label="用户名"
                rules={[{ required: true, message: '请输入用户名' }]}
              >
                <Input prefix={<UserOutlined />} disabled={!editing} />
              </Form.Item>

              <Form.Item
                name="email"
                label="邮箱"
                rules={[
                  { required: true, message: '请输入邮箱' },
                  { type: 'email', message: '请输入有效的邮箱地址' }
                ]}
              >
                <Input prefix={<MailOutlined />} disabled={!editing} />
              </Form.Item>

              <Form.Item
                name="phone"
                label="手机号"
              >
                <Input prefix={<PhoneOutlined />} disabled={!editing} />
              </Form.Item>

              <Form.Item
                name="bio"
                label="个人简介"
              >
                <TextArea rows={4} disabled={!editing} />
              </Form.Item>

              <Form.Item>
                {editing ? (
                  <Space>
                    <Button type="primary" htmlType="submit" loading={loading}>
                      <SaveOutlined /> 保存
                    </Button>
                    <Button onClick={() => setEditing(false)}>
                      取消
                    </Button>
                  </Space>
                ) : (
                  <Button type="primary" onClick={() => setEditing(true)}>
                    <EditOutlined /> 编辑资料
                  </Button>
                )}
              </Form.Item>
            </Form>
          </Card>
        </Col>

        <Col span={16}>
          <Card>
            <Tabs defaultActiveKey="1">
              <TabPane
                tab={
                  <span>
                    <FileTextOutlined />
                    论文统计
                  </span>
                }
                key="1"
              >
                <Row gutter={[16, 16]}>
                  <Col span={6}>
                    <Card>
                      <Statistic
                        title="总论文数"
                        value={stats.totalPapers}
                        prefix={<FileTextOutlined />}
                      />
                    </Card>
                  </Col>
                  <Col span={6}>
                    <Card>
                      <Statistic
                        title="收藏论文"
                        value={stats.favoritePapers}
                        prefix={<StarOutlined />}
                      />
                    </Card>
                  </Col>
                  <Col span={6}>
                    <Card>
                      <Statistic
                        title="评论数"
                        value={stats.totalComments}
                        prefix={<MessageOutlined />}
                      />
                    </Card>
                  </Col>
                  <Col span={6}>
                    <Card>
                      <Statistic
                        title="标签数"
                        value={stats.totalTags}
                        prefix={<TagOutlined />}
                      />
                    </Card>
                  </Col>
                </Row>
              </TabPane>

              <TabPane
                tab={
                  <span>
                    <StarOutlined />
                    收藏论文
                  </span>
                }
                key="2"
              >
                <List
                  itemLayout="horizontal"
                  dataSource={favoritePapers}
                  renderItem={item => (
                    <List.Item>
                      <List.Item.Meta
                        title={<a href={`/papers/${item.id}`}>{item.title}</a>}
                        description={
                          <Space>
                            <span>{item.authors}</span>
                            <span>{item.conference}</span>
                            <span>{item.year}</span>
                          </Space>
                        }
                      />
                    </List.Item>
                  )}
                />
              </TabPane>

              <TabPane
                tab={
                  <span>
                    <MessageOutlined />
                    评论历史
                  </span>
                }
                key="3"
              >
                <List
                  itemLayout="horizontal"
                  dataSource={comments}
                  renderItem={item => (
                    <List.Item>
                      <List.Item.Meta
                        title={<a href={`/papers/${item.paper_id}`}>{item.paper_title}</a>}
                        description={
                          <Space direction="vertical">
                            <span>{item.content}</span>
                            <span style={{ color: '#999' }}>{item.created_at}</span>
                          </Space>
                        }
                      />
                    </List.Item>
                  )}
                />
              </TabPane>
            </Tabs>
          </Card>
        </Col>
      </Row>
    </div>
  );
}

export default Profile; 