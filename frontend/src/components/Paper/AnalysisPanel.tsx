import React, { useState } from 'react';
import { Card, Button, List, message, Spin } from 'antd';
import { ExperimentOutlined } from '@ant-design/icons';
import { analyzePaper } from '../../services/paper';

interface AnalysisResult {
  id: string;
  type: string;
  content: string;
  createdAt: string;
}

const AnalysisPanel: React.FC<{ paperId: string }> = ({ paperId }) => {
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState<AnalysisResult[]>([]);

  const handleAnalyze = async () => {
    try {
      setLoading(true);
      const data = await analyzePaper(paperId);
      setResults(data);
      message.success('分析完成');
    } catch (error) {
      message.error('分析失败');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <div style={{ marginBottom: 16 }}>
        <Button
          type="primary"
          icon={<ExperimentOutlined />}
          onClick={handleAnalyze}
          loading={loading}
        >
          开始分析
        </Button>
      </div>

      <Spin spinning={loading}>
        <List
          grid={{ gutter: 16, column: 2 }}
          dataSource={results}
          renderItem={(item) => (
            <List.Item>
              <Card title={item.type}>
                <div style={{ whiteSpace: 'pre-wrap' }}>{item.content}</div>
              </Card>
            </List.Item>
          )}
        />
      </Spin>
    </div>
  );
};

export default AnalysisPanel; 