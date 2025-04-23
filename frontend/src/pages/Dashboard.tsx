import React, { useEffect, useState } from 'react';
import { Row, Col, Card, Statistic, List, Typography } from 'antd';
import { FileTextOutlined, CheckCircleOutlined, ClockCircleOutlined } from '@ant-design/icons';
import axios from 'axios';

const { Title } = Typography;

interface PaperStats {
  total: number;
  draft: number;
  submitted: number;
  accepted: number;
  rejected: number;
}

interface RecentPaper {
  id: number;
  title: string;
  status: string;
  created_at: string;
}

const Dashboard: React.FC = () => {
  const [stats, setStats] = useState<PaperStats>({
    total: 0,
    draft: 0,
    submitted: 0,
    accepted: 0,
    rejected: 0
  });
  const [recentPapers, setRecentPapers] = useState<RecentPaper[]>([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [statsResponse, papersResponse] = await Promise.all([
          axios.get('/api/v1/papers/stats', {
            headers: {
              Authorization: `Bearer ${localStorage.getItem('token')}`
            }
          }),
          axios.get('/api/v1/papers/recent', {
            headers: {
              Authorization: `Bearer ${localStorage.getItem('token')}`
            }
          })
        ]);

        setStats(statsResponse.data);
        setRecentPapers(papersResponse.data);
      } catch (error) {
        console.error('获取数据失败:', error);
      }
    };

    fetchData();
  }, []);

  return (
    <div>
      <Title level={2}>仪表盘</Title>
      
      <Row gutter={16} style={{ marginBottom: 24 }}>
        <Col span={6}>
          <Card>
            <Statistic
              title="总论文数"
              value={stats.total}
              prefix={<FileTextOutlined />}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="草稿"
              value={stats.draft}
              prefix={<ClockCircleOutlined />}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="已提交"
              value={stats.submitted}
              prefix={<FileTextOutlined />}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="已接受"
              value={stats.accepted}
              prefix={<CheckCircleOutlined />}
            />
          </Card>
        </Col>
      </Row>

      <Card title="最近论文">
        <List
          dataSource={recentPapers}
          renderItem={(paper) => (
            <List.Item>
              <List.Item.Meta
                title={paper.title}
                description={`状态: ${paper.status} | 创建时间: ${new Date(paper.created_at).toLocaleDateString()}`}
              />
            </List.Item>
          )}
        />
      </Card>
    </div>
  );
};

export default Dashboard; 