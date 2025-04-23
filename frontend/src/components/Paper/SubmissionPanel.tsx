import React, { useState } from 'react';
import { Card, Button, Form, Input, Select, message, Spin } from 'antd';
import { SendOutlined } from '@ant-design/icons';
import { submitPaper } from '../../services/paper';

const { Option } = Select;

const SubmissionPanel: React.FC<{ paperId: string }> = ({ paperId }) => {
  const [loading, setLoading] = useState(false);
  const [form] = Form.useForm();

  const handleSubmit = async (values: any) => {
    try {
      setLoading(true);
      await submitPaper(paperId, values);
      message.success('投稿成功');
      form.resetFields();
    } catch (error) {
      message.error('投稿失败');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <Card>
        <Form
          form={form}
          onFinish={handleSubmit}
          layout="vertical"
        >
          <Form.Item
            name="conference"
            label="目标会议"
            rules={[{ required: true, message: '请选择目标会议' }]}
          >
            <Select placeholder="请选择目标会议">
              <Option value="iclr">ICLR</Option>
              <Option value="neurips">NeurIPS</Option>
              <Option value="icml">ICML</Option>
              <Option value="cvpr">CVPR</Option>
              <Option value="acl">ACL</Option>
            </Select>
          </Form.Item>

          <Form.Item
            name="track"
            label="投稿赛道"
            rules={[{ required: true, message: '请选择投稿赛道' }]}
          >
            <Select placeholder="请选择投稿赛道">
              <Option value="main">主赛道</Option>
              <Option value="workshop">Workshop</Option>
              <Option value="demo">Demo</Option>
            </Select>
          </Form.Item>

          <Form.Item
            name="abstract"
            label="摘要"
            rules={[{ required: true, message: '请输入摘要' }]}
          >
            <Input.TextArea rows={4} />
          </Form.Item>

          <Form.Item
            name="keywords"
            label="关键词"
            rules={[{ required: true, message: '请输入关键词' }]}
          >
            <Input placeholder="用逗号分隔的关键词" />
          </Form.Item>

          <Form.Item>
            <Button
              type="primary"
              htmlType="submit"
              icon={<SendOutlined />}
              loading={loading}
              block
            >
              提交投稿
            </Button>
          </Form.Item>
        </Form>
      </Card>
    </div>
  );
};

export default SubmissionPanel; 