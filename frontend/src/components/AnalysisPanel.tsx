import React, { useEffect, useState } from 'react';
import { Card, List, Tag, Typography, Spin } from 'antd';
import { FileTextOutlined, BulbOutlined, LinkOutlined } from '@ant-design/icons';
import axios from 'axios';

const { Title, Paragraph } = Typography;

interface AnalysisResult {
  keywords: string[];
  summary: string;
  innovation_points: string[];
  related_papers: Array<{
    title: string;
    similarity: number;
  }>;
}

interface AnalysisPanelProps {
  paperId: string;
}

const AnalysisPanel: React.FC<AnalysisPanelProps> = ({ paperId }) => {
  const [loading, setLoading] = useState(true);
  const [analysisResult, setAnalysisResult] = useState<AnalysisResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchAnalysis = async () => {
      try {
        const response = await axios.get(`/api/papers/${paperId}/analysis`);
        setAnalysisResult(response.data);
      } catch (err) {
        setError('获取分析结果失败，请稍后重试');
        console.error('Error fetching analysis:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchAnalysis();
  }, [paperId]);

  if (loading) {
    return (
      <div style={{ textAlign: 'center', padding: '50px' }}>
        <Spin size="large" />
        <p>正在分析论文...</p>
      </div>
    );
  }

  if (error) {
    return (
      <Card>
        <Typography.Text type="danger">{error}</Typography.Text>
      </Card>
    );
  }

  if (!analysisResult) {
    return null;
  }

  return (
    <div style={{ padding: '24px' }}>
      <Card title="论文分析结果" style={{ marginBottom: '24px' }}>
        <div style={{ marginBottom: '24px' }}>
          <Title level={4}>
            <FileTextOutlined /> 关键词提取
          </Title>
          <div>
            {analysisResult.keywords.map((keyword, index) => (
              <Tag key={index} color="blue" style={{ margin: '4px' }}>
                {keyword}
              </Tag>
            ))}
          </div>
        </div>

        <div style={{ marginBottom: '24px' }}>
          <Title level={4}>
            <FileTextOutlined /> 智能摘要
          </Title>
          <Paragraph>{analysisResult.summary}</Paragraph>
        </div>

        <div style={{ marginBottom: '24px' }}>
          <Title level={4}>
            <BulbOutlined /> 创新点分析
          </Title>
          <List
            dataSource={analysisResult.innovation_points}
            renderItem={(item) => (
              <List.Item>
                <Typography.Text>{item}</Typography.Text>
              </List.Item>
            )}
          />
        </div>

        <div>
          <Title level={4}>
            <LinkOutlined /> 相关论文推荐
          </Title>
          <List
            dataSource={analysisResult.related_papers}
            renderItem={(item) => (
              <List.Item>
                <Typography.Text>{item.title}</Typography.Text>
                <Tag color="green" style={{ marginLeft: '8px' }}>
                  相似度: {(item.similarity * 100).toFixed(1)}%
                </Tag>
              </List.Item>
            )}
          />
        </div>
      </Card>
    </div>
  );
};

export default AnalysisPanel; 