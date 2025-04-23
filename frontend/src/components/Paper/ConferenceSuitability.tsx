import React, { useState, useEffect } from 'react';
import { Card, Progress, List, Typography, Spin, message } from 'antd';
import { TrophyOutlined } from '@ant-design/icons';
import axios from 'axios';

const { Title, Text } = Typography;

interface ConferenceSuitabilityProps {
  paperId: number;
}

interface SuitabilityResult {
  conference: string;
  similarity_score: number;
  suggested_conferences: Array<{
    conference: string;
    similarity_score: number;
  }>;
}

const ConferenceSuitability: React.FC<ConferenceSuitabilityProps> = ({ paperId }) => {
  const [loading, setLoading] = useState(true);
  const [result, setResult] = useState<SuitabilityResult | null>(null);

  useEffect(() => {
    fetchSuitability();
  }, [paperId]);

  const fetchSuitability = async () => {
    try {
      const response = await axios.post(
        'http://localhost:8000/api/v1/analysis/conference-suitability',
        { paper_id: paperId },
        {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        }
      );
      setResult(response.data);
    } catch (error) {
      message.error('获取会议匹配度分析失败');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <Spin size="large" style={{ display: 'flex', justifyContent: 'center', marginTop: '20%' }} />;
  }

  if (!result) {
    return <div>暂无分析结果</div>;
  }

  return (
    <div style={{ padding: '24px' }}>
      <Card title="会议匹配度分析">
        <div style={{ marginBottom: '24px' }}>
          <Title level={4}>目标会议匹配度</Title>
          <div style={{ marginTop: '16px' }}>
            <Text strong>{result.conference}</Text>
            <Progress
              percent={Math.round(result.similarity_score * 100)}
              status={result.similarity_score > 0.7 ? 'success' : 'normal'}
              style={{ marginTop: '8px' }}
            />
          </div>
        </div>

        <div>
          <Title level={4}>其他推荐会议</Title>
          <List
            dataSource={result.suggested_conferences}
            renderItem={(item) => (
              <List.Item>
                <div style={{ width: '100%' }}>
                  <Text strong>{item.conference}</Text>
                  <Progress
                    percent={Math.round(item.similarity_score * 100)}
                    status={item.similarity_score > 0.7 ? 'success' : 'normal'}
                    style={{ marginTop: '8px' }}
                  />
                </div>
              </List.Item>
            )}
          />
        </div>
      </Card>
    </div>
  );
};

export default ConferenceSuitability; 