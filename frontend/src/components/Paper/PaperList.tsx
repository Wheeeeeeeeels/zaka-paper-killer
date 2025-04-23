import React, { useEffect, useState } from 'react';
import { Table, Button, Space, message } from 'antd';
import { PlusOutlined, EditOutlined, DeleteOutlined } from '@ant-design/icons';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

interface Paper {
  id: number;
  title: string;
  authors: string;
  conference: string;
  year: number;
  status: string;
  created_at: string;
}

const PaperList: React.FC = () => {
  const [papers, setPapers] = useState<Paper[]>([]);
  const [loading, setLoading] = useState(false);
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

  const columns = [
    {
      title: '标题',
      dataIndex: 'title',
      key: 'title',
    },
    {
      title: '作者',
      dataIndex: 'authors',
      key: 'authors',
    },
    {
      title: '会议/期刊',
      dataIndex: 'conference',
      key: 'conference',
    },
    {
      title: '年份',
      dataIndex: 'year',
      key: 'year',
    },
    {
      title: '状态',
      dataIndex: 'status',
      key: 'status',
    },
    {
      title: '创建时间',
      dataIndex: 'created_at',
      key: 'created_at',
      render: (text: string) => new Date(text).toLocaleDateString(),
    },
    {
      title: '操作',
      key: 'action',
      render: (_: any, record: Paper) => (
        <Space size="middle">
          <Button
            type="link"
            icon={<EditOutlined />}
            onClick={() => navigate(`/papers/${record.id}/edit`)}
          >
            编辑
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

  const handleDelete = async (id: number) => {
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

  return (
    <div>
      <div style={{ marginBottom: 16 }}>
        <Button
          type="primary"
          icon={<PlusOutlined />}
          onClick={() => navigate('/papers/new')}
        >
          新建论文
        </Button>
      </div>
      <Table
        columns={columns}
        dataSource={papers}
        rowKey="id"
        loading={loading}
      />
    </div>
  );
};

export default PaperList; 