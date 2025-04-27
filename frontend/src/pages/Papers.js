import React, { useState, useEffect } from 'react';
import { Table, Button, Upload, message, Card, Statistic, Row, Col, Input, Tag, Space, Popconfirm } from 'antd';
import { UploadOutlined, FileTextOutlined, StarOutlined, StarFilled, SearchOutlined, TagOutlined } from '@ant-design/icons';
import { Link } from 'react-router-dom';
import { paperAPI } from '../services/api';

const { Search } = Input;

function Papers() {
  const [papers, setPapers] = useState([]);
  const [stats, setStats] = useState({
    total: 0,
    draft: 0,
    submitted: 0,
    accepted: 0,
    rejected: 0
  });
  const [loading, setLoading] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedRowKeys, setSelectedRowKeys] = useState([]);

  useEffect(() => {
    fetchPapers();
    fetchStats();
  }, []);

  const fetchPapers = async () => {
    setLoading(true);
    try {
      const data = await paperAPI.getPapers();
      setPapers(data);
    } catch (error) {
      message.error('获取论文列表失败');
    } finally {
      setLoading(false);
    }
  };

  const fetchStats = async () => {
    try {
      const data = await paperAPI.getStats();
      setStats(data);
    } catch (error) {
      message.error('获取统计信息失败');
    }
  };

  const handleUpload = async (file) => {
    const formData = new FormData();
    formData.append('file', file);

    try {
      await paperAPI.uploadPaper(formData);
      message.success('论文上传成功');
      fetchPapers();
    } catch (error) {
      message.error('论文上传失败');
    }
    return false;
  };

  const handleSearch = async (value) => {
    setSearchQuery(value);
    setLoading(true);
    try {
      const data = await paperAPI.searchPapers(value);
      setPapers(data);
    } catch (error) {
      message.error('搜索失败');
    } finally {
      setLoading(false);
    }
  };

  const handleFavorite = async (id, isFavorite) => {
    try {
      if (isFavorite) {
        await paperAPI.unfavoritePaper(id);
        message.success('已取消收藏');
      } else {
        await paperAPI.favoritePaper(id);
        message.success('已收藏');
      }
      fetchPapers();
    } catch (error) {
      message.error('操作失败');
    }
  };

  const handleBatchDelete = async () => {
    try {
      await paperAPI.batchOperation('delete', selectedRowKeys);
      message.success('批量删除成功');
      setSelectedRowKeys([]);
      fetchPapers();
    } catch (error) {
      message.error('批量删除失败');
    }
  };

  const columns = [
    {
      title: '标题',
      dataIndex: 'title',
      key: 'title',
      render: (text, record) => (
        <Link to={`/papers/${record.id}`}>{text}</Link>
      ),
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
      title: '标签',
      dataIndex: 'tags',
      key: 'tags',
      render: (tags) => (
        <Space>
          {tags?.map(tag => (
            <Tag key={tag} color="blue">
              {tag}
            </Tag>
          ))}
        </Space>
      ),
    },
    {
      title: '状态',
      dataIndex: 'status',
      key: 'status',
    },
    {
      title: '操作',
      key: 'action',
      render: (_, record) => (
        <Space>
          <Button
            type="text"
            icon={record.is_favorite ? <StarFilled style={{ color: '#fadb14' }} /> : <StarOutlined />}
            onClick={() => handleFavorite(record.id, record.is_favorite)}
          />
          <Button type="link" onClick={() => handleAnalyze(record.id)}>
            分析
          </Button>
        </Space>
      ),
    },
  ];

  const handleAnalyze = async (paperId) => {
    try {
      await paperAPI.createAnalysis(paperId);
      message.success('论文分析已开始');
    } catch (error) {
      message.error('论文分析失败');
    }
  };

  const rowSelection = {
    selectedRowKeys,
    onChange: (newSelectedRowKeys) => {
      setSelectedRowKeys(newSelectedRowKeys);
    },
  };

  return (
    <div style={{ padding: '24px 0' }}>
      <Row gutter={[16, 16]} style={{ marginBottom: '24px' }}>
        <Col span={4}>
          <Card>
            <Statistic title="总论文数" value={stats.total} prefix={<FileTextOutlined />} />
          </Card>
        </Col>
        <Col span={4}>
          <Card>
            <Statistic title="草稿" value={stats.draft} />
          </Card>
        </Col>
        <Col span={4}>
          <Card>
            <Statistic title="已提交" value={stats.submitted} />
          </Card>
        </Col>
        <Col span={4}>
          <Card>
            <Statistic title="已接受" value={stats.accepted} />
          </Card>
        </Col>
        <Col span={4}>
          <Card>
            <Statistic title="已拒绝" value={stats.rejected} />
          </Card>
        </Col>
        <Col span={4}>
          <Card>
            <Upload
              beforeUpload={handleUpload}
              showUploadList={false}
            >
              <Button icon={<UploadOutlined />}>上传论文</Button>
            </Upload>
          </Card>
        </Col>
      </Row>

      <div style={{ marginBottom: 16 }}>
        <Space>
          <Search
            placeholder="搜索论文"
            allowClear
            enterButton={<SearchOutlined />}
            onSearch={handleSearch}
            style={{ width: 300 }}
          />
          {selectedRowKeys.length > 0 && (
            <Popconfirm
              title="确定要删除选中的论文吗？"
              onConfirm={handleBatchDelete}
              okText="确定"
              cancelText="取消"
            >
              <Button danger>批量删除</Button>
            </Popconfirm>
          )}
        </Space>
      </div>

      <Table
        rowSelection={rowSelection}
        columns={columns}
        dataSource={papers}
        rowKey="id"
        pagination={{ pageSize: 10 }}
        loading={loading}
      />
    </div>
  );
}

export default Papers; 