import React from 'react';
import { Form, Input, Button, message } from 'antd';
import { useNavigate, useParams } from 'react-router-dom';
import axios from 'axios';

interface PaperFormData {
  title: string;
  abstract: string;
  authors: string;
  conference: string;
  year: number;
  doi: string;
  pdf_url: string;
  status: string;
}

const PaperForm: React.FC = () => {
  const navigate = useNavigate();
  const { id } = useParams();
  const [form] = Form.useForm();

  const onFinish = async (values: PaperFormData) => {
    try {
      if (id) {
        await axios.put(`/api/v1/papers/${id}`, values, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`
          }
        });
        message.success('更新成功');
      } else {
        await axios.post('/api/v1/papers', values, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`
          }
        });
        message.success('创建成功');
      }
      navigate('/papers');
    } catch (error) {
      message.error(id ? '更新失败' : '创建失败');
    }
  };

  React.useEffect(() => {
    if (id) {
      const fetchPaper = async () => {
        try {
          const response = await axios.get(`/api/v1/papers/${id}`, {
            headers: {
              Authorization: `Bearer ${localStorage.getItem('token')}`
            }
          });
          form.setFieldsValue(response.data);
        } catch (error) {
          message.error('获取论文信息失败');
          navigate('/papers');
        }
      };
      fetchPaper();
    }
  }, [id, form, navigate]);

  return (
    <Form
      form={form}
      layout="vertical"
      onFinish={onFinish}
      style={{ maxWidth: 800, margin: '0 auto' }}
    >
      <Form.Item
        name="title"
        label="标题"
        rules={[{ required: true, message: '请输入论文标题' }]}
      >
        <Input />
      </Form.Item>

      <Form.Item
        name="abstract"
        label="摘要"
        rules={[{ required: true, message: '请输入论文摘要' }]}
      >
        <Input.TextArea rows={4} />
      </Form.Item>

      <Form.Item
        name="authors"
        label="作者"
        rules={[{ required: true, message: '请输入作者信息' }]}
      >
        <Input />
      </Form.Item>

      <Form.Item
        name="conference"
        label="会议/期刊"
      >
        <Input />
      </Form.Item>

      <Form.Item
        name="year"
        label="年份"
      >
        <Input type="number" />
      </Form.Item>

      <Form.Item
        name="doi"
        label="DOI"
      >
        <Input />
      </Form.Item>

      <Form.Item
        name="pdf_url"
        label="PDF链接"
      >
        <Input />
      </Form.Item>

      <Form.Item
        name="status"
        label="状态"
        initialValue="draft"
      >
        <Input />
      </Form.Item>

      <Form.Item>
        <Button type="primary" htmlType="submit">
          {id ? '更新' : '创建'}
        </Button>
        <Button
          style={{ marginLeft: 8 }}
          onClick={() => navigate('/papers')}
        >
          取消
        </Button>
      </Form.Item>
    </Form>
  );
};

export default PaperForm; 