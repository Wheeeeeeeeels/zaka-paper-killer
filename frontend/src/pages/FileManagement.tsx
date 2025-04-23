import React, { useEffect, useState } from 'react';
import {
  Card,
  Table,
  Button,
  Space,
  message,
  Progress,
  Modal,
  Typography,
  Popconfirm
} from 'antd';
import {
  DeleteOutlined,
  ReloadOutlined,
  ExclamationCircleOutlined
} from '@ant-design/icons';
import axios from 'axios';
import FilePreview from '../components/paper/FilePreview';

const { Title } = Typography;
const { confirm } = Modal;

interface FileInfo {
  name: string;
  size: number;
  created_at: string;
  modified_at: string;
  path: string;
}

interface StorageInfo {
  total_size: number;
  file_count: number;
  max_size: number;
  used_percentage: number;
}

const FileManagement: React.FC = () => {
  const [files, setFiles] = useState<FileInfo[]>([]);
  const [storageInfo, setStorageInfo] = useState<StorageInfo | null>(null);
  const [loading, setLoading] = useState(false);
  const [pagination, setPagination] = useState({
    current: 1,
    pageSize: 20,
    total: 0
  });

  const fetchFiles = async (page = 1, pageSize = 20) => {
    setLoading(true);
    try {
      const response = await axios.get(`/api/v1/files?page=${page}&page_size=${pageSize}`, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('token')}`
        }
      });
      setFiles(response.data.files);
      setPagination({
        current: response.data.page,
        pageSize: response.data.page_size,
        total: response.data.total
      });
    } catch (error) {
      message.error('获取文件列表失败');
    } finally {
      setLoading(false);
    }
  };

  const fetchStorageInfo = async () => {
    try {
      const response = await axios.get('/api/v1/storage', {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('token')}`
        }
      });
      setStorageInfo(response.data);
    } catch (error) {
      message.error('获取存储信息失败');
    }
  };

  useEffect(() => {
    fetchFiles();
    fetchStorageInfo();
  }, []);

  const handleTableChange = (pagination: any) => {
    fetchFiles(pagination.current, pagination.pageSize);
  };

  const handleDelete = async (filePath: string) => {
    try {
      await axios.delete(`/api/v1/files/${encodeURIComponent(filePath)}`, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('token')}`
        }
      });
      message.success('文件删除成功');
      fetchFiles(pagination.current, pagination.pageSize);
      fetchStorageInfo();
    } catch (error) {
      message.error('文件删除失败');
    }
  };

  const handleCleanup = async () => {
    confirm({
      title: '确认清理',
      icon: <ExclamationCircleOutlined />,
      content: '确定要清理30天前的文件吗？此操作不可恢复。',
      onOk: async () => {
        try {
          const response = await axios.post('/api/v1/cleanup', null, {
            headers: {
              Authorization: `Bearer ${localStorage.getItem('token')}`
            }
          });
          message.success(response.data.message);
          fetchFiles(pagination.current, pagination.pageSize);
          fetchStorageInfo();
        } catch (error) {
          message.error('清理文件失败');
        }
      }
    });
  };

  const columns = [
    {
      title: '文件名',
      dataIndex: 'name',
      key: 'name',
    },
    {
      title: '大小',
      dataIndex: 'size',
      key: 'size',
      render: (size: number) => `${(size / 1024 / 1024).toFixed(2)} MB`,
    },
    {
      title: '创建时间',
      dataIndex: 'created_at',
      key: 'created_at',
      render: (date: string) => new Date(date).toLocaleString(),
    },
    {
      title: '修改时间',
      dataIndex: 'modified_at',
      key: 'modified_at',
      render: (date: string) => new Date(date).toLocaleString(),
    },
    {
      title: '操作',
      key: 'action',
      render: (_: any, record: FileInfo) => (
        <Space size="middle">
          <FilePreview
            fileUrl={`/api/v1/papers/file/${encodeURIComponent(record.path)}`}
            fileName={record.name}
          />
          <Popconfirm
            title="确定要删除这个文件吗？"
            onConfirm={() => handleDelete(record.path)}
            okText="确定"
            cancelText="取消"
          >
            <Button
              type="link"
              danger
              icon={<DeleteOutlined />}
            >
              删除
            </Button>
          </Popconfirm>
        </Space>
      ),
    },
  ];

  return (
    <div>
      <Title level={2}>文件管理</Title>

      <Card style={{ marginBottom: 24 }}>
        <Title level={4}>存储信息</Title>
        {storageInfo && (
          <div>
            <Progress
              percent={storageInfo.used_percentage}
              status={storageInfo.used_percentage > 90 ? 'exception' : 'normal'}
            />
            <div style={{ marginTop: 16 }}>
              <p>总文件数: {storageInfo.file_count}</p>
              <p>已用空间: {(storageInfo.total_size / 1024 / 1024).toFixed(2)} MB</p>
              <p>总空间: {(storageInfo.max_size / 1024 / 1024).toFixed(2)} MB</p>
            </div>
          </div>
        )}
      </Card>

      <Card
        title="文件列表"
        extra={
          <Space>
            <Button
              icon={<ReloadOutlined />}
              onClick={() => {
                fetchFiles(pagination.current, pagination.pageSize);
                fetchStorageInfo();
              }}
            >
              刷新
            </Button>
            <Button
              type="primary"
              danger
              onClick={handleCleanup}
            >
              清理旧文件
            </Button>
          </Space>
        }
      >
        <Table
          columns={columns}
          dataSource={files}
          rowKey="path"
          pagination={pagination}
          loading={loading}
          onChange={handleTableChange}
        />
      </Card>
    </div>
  );
};

export default FileManagement; 