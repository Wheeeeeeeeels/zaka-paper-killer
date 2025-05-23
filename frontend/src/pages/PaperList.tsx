import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Table,
  Card,
  Button,
  Input,
  Select,
  Space,
  Tag,
  message,
  Spin,
  Modal,
  Form,
  Typography,
} from 'antd';
import {
  PlusOutlined,
  SearchOutlined,
  EditOutlined,
  DeleteOutlined,
  ExclamationCircleOutlined,
  FileTextOutlined,
} from '@ant-design/icons';
import { getPapers, createPaper } from '../services/paper';
import axios from 'axios';
import FileUpload from '../components/paper/FileUpload';
import FilePreview from '../components/paper/FilePreview';

const { Search } = Input;
const { Option } = Select;
const { confirm } = Modal;
const { Title } = Typography;

interface Paper {
  id: string;
  title: string;
  status: string;
  createdAt: string;
  pdf_url: string;
}

const PaperList: React.FC = () => {
  const [papers, setPapers] = useState<Paper[]>([]);
  const [loading, setLoading] = useState(false);
  const [searchText, setSearchText] = useState('');
  const [statusFilter, setStatusFilter] = useState<string | null>(null);
  const [conferenceFilter, setConferenceFilter] = useState<string | null>(null);
  const [isModalVisible, setIsModalVisible] = useState(false);
  const [form] = Form.useForm();
  const navigate = useNavigate();

  const fetchPapers = async () => {
    setLoading(true);
    try {
      const response = await axios.get('/api/v1/papers', {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('token')}`
        }
      });
      setPapers(response.data);
    } catch (error) {
      message.error('获取论文列表失败');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchPapers();
  }, []);

  const handleSearch = (value: string) => {
    setSearchText(value);
  };

  const handleStatusChange = (value: string | null) => {
    setStatusFilter(value);
  };

  const handleConferenceChange = (value: string | null) => {
    setConferenceFilter(value);
  };

  const handleCreatePaper = async () => {
    try {
      const newPaper = await createPaper({ title: '新建论文' });
      navigate(`/papers/${newPaper.id}`);
    } catch (error) {
      message.error('创建论文失败');
    }
  };

  const handleDelete = async (id: string) => {
    try {
      await axios.delete(`/api/v1/papers/${id}`, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('token')}`
        }
      });
      message.success('删除成功');
      fetchPapers();
    } catch (error) {
      message.error('删除失败');
    }
  };

  const getStatusColor = (status: string) => {
    const colorMap: { [key: string]: string } = {
      draft: 'default',
      submitted: 'processing',
      accepted: 'success',
      rejected: 'error',
    };
    return colorMap[status] || 'default';
  };

  const filteredPapers = papers.filter((paper) => {
    const matchesSearch = paper.title.toLowerCase().includes(searchText.toLowerCase());
    const matchesStatus = !statusFilter || paper.status === statusFilter;
    const matchesConference = !conferenceFilter || paper.target_conference === conferenceFilter;
    return matchesSearch && matchesStatus && matchesConference;
  });

  const columns = [
    {
      title: '标题',
      dataIndex: 'title',
      key: 'title',
    },
    {
      title: '状态',
      dataIndex: 'status',
      key: 'status',
    },
    {
      title: '创建时间',
      dataIndex: 'createdAt',
      key: 'createdAt',
    },
    {
      title: '操作',
      key: 'action',
      render: (_, record: Paper) => (
        <Space size="middle">
          <FilePreview
            fileUrl={record.pdf_url}
            fileName={record.title}
          />
          <Button
            type="link"
            icon={<EditOutlined />}
            onClick={() => navigate(`/papers/${record.id}/edit`)}
          >
            编辑
          </Button>
          <Button
            type="link"
            icon={<FileTextOutlined />}
            onClick={() => navigate(`/papers/${record.id}/analysis`)}
          >
            分析
          </Button>
          <Button
            type="link"
            danger
            icon={<DeleteOutlined />}
            onClick={() => handleDelete(record.id)}
          >
            删除
          </Button>
        </Space>
      ),
    },
  ];

  return (
    <div style={{ padding: '24px' }}>
      <Title level={2}>论文管理</Title>
      
      <Card style={{ marginBottom: 24 }}>
        <Title level={4}>上传论文</Title>
        <FileUpload />
      </Card>

      <Card
        title="论文管理"
        extra={
          <Button
            type="primary"
            icon={<PlusOutlined />}
            onClick={handleCreatePaper}
          >
            新建论文
          </Button>
        }
      >
        <div style={{ marginBottom: '16px' }}>
          <Space>
            <Search
              placeholder="搜索论文标题"
              allowClear
              enterButton={<SearchOutlined />}
              onSearch={handleSearch}
              style={{ width: 300 }}
            />
            <Select
              placeholder="按状态筛选"
              allowClear
              style={{ width: 120 }}
              onChange={handleStatusChange}
            >
              <Option value="draft">草稿</Option>
              <Option value="submitted">已提交</Option>
              <Option value="accepted">已接受</Option>
              <Option value="rejected">已拒绝</Option>
            </Select>
            <Select
              placeholder="按会议筛选"
              allowClear
              style={{ width: 120 }}
              onChange={handleConferenceChange}
            >
              <Option value="ICML">ICML</Option>
              <Option value="ICLR">ICLR</Option>
              <Option value="NeurIPS">NeurIPS</Option>
              <Option value="CVPR">CVPR</Option>
              <Option value="ACL">ACL</Option>
            </Select>
          </Space>
        </div>

        {loading ? (
          <Spin size="large" style={{ display: 'flex', justifyContent: 'center', marginTop: '20%' }} />
        ) : (
          <Table
            columns={columns}
            dataSource={filteredPapers}
            rowKey="id"
            pagination={{
              defaultPageSize: 10,
              showSizeChanger: true,
              showTotal: (total) => `共 ${total} 条记录`,
            }}
          />
        )}
      </Card>

      <Modal
        title="新建论文"
        open={isModalVisible}
        onCancel={() => setIsModalVisible(false)}
        footer={null}
      >
        <Form
          form={form}
          onFinish={handleCreate}
          layout="vertical"
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
            name="keywords"
            label="关键词"
            rules={[{ required: true, message: '请输入关键词' }]}
          >
            <Input />
          </Form.Item>

          <Form.Item>
            <Button type="primary" htmlType="submit">
              创建
            </Button>
          </Form.Item>
        </Form>
      </Modal>
    </div>
  );
};

export default PaperList; 