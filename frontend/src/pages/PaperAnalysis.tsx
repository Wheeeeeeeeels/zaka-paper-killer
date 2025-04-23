import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { Card, Typography, Spin, Tabs, List, Tag } from 'antd';
import axios from 'axios';

const { Title } = Typography;
const { TabPane } = Tabs;

interface PaperAnalysis {
  keywords: string;
  main_contribution: string;
  methodology: string;
  results: string;
  limitations: string;
  future_work: string;
}

const PaperAnalysis: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const [loading, setLoading] = useState(true);
  const [analysis, setAnalysis] = useState<PaperAnalysis | null>(null);
  const [paper, setPaper] = useState<any>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [paperResponse, analysisResponse] = await Promise.all([
          axios.get(`/api/v1/papers/${id}`, {
            headers: {
              Authorization: `Bearer ${localStorage.getItem('token')}`
            }
          }),
          axios.get(`/api/v1/papers/${id}/analysis`, {
            headers: {
              Authorization: `Bearer ${localStorage.getItem('token')}`
            }
          })
        ]);

        setPaper(paperResponse.data);
        setAnalysis(analysisResponse.data);
      } catch (error) {
        console.error('获取数据失败:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [id]);

  if (loading) {
    return (
      <div style={{ textAlign: 'center', padding: '50px' }}>
        <Spin size="large" />
      </div>
    );
  }

  if (!paper || !analysis) {
    return <div>未找到论文或分析数据</div>;
  }

  return (
    <div>
      <Title level={2}>{paper.title}</Title>
      
      <Card style={{ marginBottom: 24 }}>
        <div style={{ marginBottom: 16 }}>
          <strong>作者：</strong> {paper.authors}
        </div>
        <div style={{ marginBottom: 16 }}>
          <strong>会议/期刊：</strong> {paper.conference}
        </div>
        <div style={{ marginBottom: 16 }}>
          <strong>年份：</strong> {paper.year}
        </div>
        <div>
          <strong>摘要：</strong> {paper.abstract}
        </div>
      </Card>

      <Tabs defaultActiveKey="1">
        <TabPane tab="关键词" key="1">
          <Card>
            <div style={{ marginBottom: 16 }}>
              {analysis.keywords?.split(',').map((keyword: string, index: number) => (
                <Tag key={index} color="blue" style={{ marginBottom: 8 }}>
                  {keyword.trim()}
                </Tag>
              ))}
            </div>
          </Card>
        </TabPane>

        <TabPane tab="主要贡献" key="2">
          <Card>
            <div style={{ whiteSpace: 'pre-wrap' }}>
              {analysis.main_contribution}
            </div>
          </Card>
        </TabPane>

        <TabPane tab="方法论" key="3">
          <Card>
            <div style={{ whiteSpace: 'pre-wrap' }}>
              {analysis.methodology}
            </div>
          </Card>
        </TabPane>

        <TabPane tab="结果" key="4">
          <Card>
            <div style={{ whiteSpace: 'pre-wrap' }}>
              {analysis.results}
            </div>
          </Card>
        </TabPane>

        <TabPane tab="局限性" key="5">
          <Card>
            <div style={{ whiteSpace: 'pre-wrap' }}>
              {analysis.limitations}
            </div>
          </Card>
        </TabPane>

        <TabPane tab="未来工作" key="6">
          <Card>
            <div style={{ whiteSpace: 'pre-wrap' }}>
              {analysis.future_work}
            </div>
          </Card>
        </TabPane>
      </Tabs>
    </div>
  );
};

export default PaperAnalysis; 