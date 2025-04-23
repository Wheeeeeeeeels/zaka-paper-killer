import React, { useState } from 'react';
import { Card, Button, Table, message, Spin } from 'antd';
import { ExperimentOutlined } from '@ant-design/icons';
import { runExperiment } from '../../services/paper';

interface ExperimentResult {
  id: string;
  name: string;
  parameters: Record<string, any>;
  metrics: Record<string, number>;
  createdAt: string;
}

const ExperimentPanel: React.FC<{ paperId: string }> = ({ paperId }) => {
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState<ExperimentResult[]>([]);

  const handleRunExperiment = async () => {
    try {
      setLoading(true);
      const data = await runExperiment(paperId);
      setResults(data);
      message.success('实验完成');
    } catch (error) {
      message.error('实验失败');
    } finally {
      setLoading(false);
    }
  };

  const columns = [
    {
      title: '实验名称',
      dataIndex: 'name',
      key: 'name',
    },
    {
      title: '参数',
      dataIndex: 'parameters',
      key: 'parameters',
      render: (parameters: Record<string, any>) => (
        <pre>{JSON.stringify(parameters, null, 2)}</pre>
      ),
    },
    {
      title: '指标',
      dataIndex: 'metrics',
      key: 'metrics',
      render: (metrics: Record<string, number>) => (
        <pre>{JSON.stringify(metrics, null, 2)}</pre>
      ),
    },
    {
      title: '创建时间',
      dataIndex: 'createdAt',
      key: 'createdAt',
    },
  ];

  return (
    <div>
      <div style={{ marginBottom: 16 }}>
        <Button
          type="primary"
          icon={<ExperimentOutlined />}
          onClick={handleRunExperiment}
          loading={loading}
        >
          运行实验
        </Button>
      </div>

      <Spin spinning={loading}>
        <Table
          columns={columns}
          dataSource={results}
          rowKey="id"
        />
      </Spin>
    </div>
  );
};

export default ExperimentPanel; 