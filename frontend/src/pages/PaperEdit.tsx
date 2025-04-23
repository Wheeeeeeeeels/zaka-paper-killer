import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  Form,
  Input,
  Button,
  Select,
  Card,
  message,
  Spin,
  Space,
} from 'antd';
import { ArrowLeftOutlined } from '@ant-design/icons';
import axios from 'axios';

const { TextArea } = Input;
const { Option } = Select;

interface PaperFormData {
  title: string;
  abstract: string;
  keywords: string;
  status: string;
  target_conference: string;
}

const PaperEdit: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const [form] = Form.useForm();
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    if (id !== 'new') {
      fetchPaper();
    } else {
      setLoading(false);
    }
  }, [id]);

  const fetchPaper = async () => {
    try {
      const response = await axios.get(`http://localhost:8000/api/v1/papers/${id}`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });
      form.setFieldsValue(response.data);
    } catch (error) {
      message.error('获取论文信息失败');
    } finally {
      setLoading(false);
    }
  };

  const onFinish = async (values: PaperFormData) => {
    setSubmitting(true);
    try {
      if (id === 'new') {
        await axios.post('http://localhost:8000/api/v1/papers', values, {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        });
        message.success('创建成功');
      } else {
        await axios.put(`http://localhost:8000/api/v1/papers/${id}`, values, {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        });
        message.success('更新成功');
      }
      navigate('/papers');
    } catch (error) {
      message.error(id === 'new' ? '创建失败' : '更新失败');
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) {
    return <Spin size="large" style={{ display: 'flex', justifyContent: 'center', marginTop: '20%' }} />;
  }

  return (
    <div style={{ padding: '24px' }}>
      <Card
        title={id === 'new' ? '新建论文' : '编辑论文'}
        extra={
          <Button
            icon={<ArrowLeftOutlined />}
            onClick={() => navigate('/papers')}
          >
            返回列表
          </Button>
        }
      >
        <Form
          form={form}
          layout="vertical"
          onFinish={onFinish}
          initialValues={{
            status: 'draft',
            target_conference: 'ICML',
          }}
        >
          <Form.Item
            name="title"
            label="标题"
            rules={[{ required: true, message: '请输入论文标题' }]}
          >
            <Input placeholder="请输入论文标题" />
          </Form.Item>

          <Form.Item
            name="abstract"
            label="摘要"
            rules={[{ required: true, message: '请输入论文摘要' }]}
          >
            <TextArea rows={4} placeholder="请输入论文摘要" />
          </Form.Item>

          <Form.Item
            name="keywords"
            label="关键词"
            rules={[{ required: true, message: '请输入关键词' }]}
          >
            <Input placeholder="请输入关键词，用逗号分隔" />
          </Form.Item>

          <Form.Item
            name="status"
            label="状态"
            rules={[{ required: true, message: '请选择论文状态' }]}
          >
            <Select>
              <Option value="draft">草稿</Option>
              <Option value="submitted">已提交</Option>
              <Option value="accepted">已接受</Option>
              <Option value="rejected">已拒绝</Option>
            </Select>
          </Form.Item>

          <Form.Item
            name="target_conference"
            label="目标会议"
            rules={[{ required: true, message: '请选择目标会议' }]}
          >
            <Select>
              <Option value="ICML">ICML</Option>
              <Option value="ICLR">ICLR</Option>
              <Option value="NeurIPS">NeurIPS</Option>
              <Option value="CVPR">CVPR</Option>
              <Option value="ACL">ACL</Option>
            </Select>
          </Form.Item>

          <Form.Item>
            <Space>
              <Button type="primary" htmlType="submit" loading={submitting}>
                {id === 'new' ? '创建' : '保存'}
              </Button>
              <Button onClick={() => navigate('/papers')}>
                取消
              </Button>
            </Space>
          </Form.Item>
        </Form>
      </Card>
    </div>
  );
};

export default PaperEdit; 