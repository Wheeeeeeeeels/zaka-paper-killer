import React from 'react';
import { Card, Row, Col, Typography, Button } from 'antd';
import { useNavigate } from 'react-router-dom';
import { FileTextOutlined, ExperimentOutlined, TeamOutlined } from '@ant-design/icons';

const { Title, Paragraph } = Typography;

const Home: React.FC = () => {
  const navigate = useNavigate();

  const features = [
    {
      title: '论文管理',
      icon: <FileTextOutlined style={{ fontSize: '48px' }} />,
      description: '管理您的论文，跟踪投稿状态，查看审稿意见',
      action: () => navigate('/papers')
    },
    {
      title: '实验分析',
      icon: <ExperimentOutlined style={{ fontSize: '48px' }} />,
      description: '分析实验结果，生成可视化图表，优化实验方案',
      action: () => navigate('/experiments')
    },
    {
      title: '协作平台',
      icon: <TeamOutlined style={{ fontSize: '48px' }} />,
      description: '与团队成员协作，分享研究成果，共同进步',
      action: () => navigate('/team')
    }
  ];

  return (
    <div style={{ padding: '24px' }}>
      <Title level={1} style={{ textAlign: 'center', marginBottom: '48px' }}>
        欢迎使用 Zaka Paper Killer
      </Title>
      <Paragraph style={{ textAlign: 'center', fontSize: '18px', marginBottom: '48px' }}>
        智能论文辅助系统，助您轻松发表顶会论文
      </Paragraph>
      <Row gutter={[24, 24]}>
        {features.map((feature, index) => (
          <Col xs={24} sm={12} md={8} key={index}>
            <Card
              hoverable
              style={{ textAlign: 'center', height: '100%' }}
              onClick={feature.action}
            >
              <div style={{ marginBottom: '16px' }}>{feature.icon}</div>
              <Title level={3}>{feature.title}</Title>
              <Paragraph>{feature.description}</Paragraph>
              <Button type="primary" onClick={feature.action}>
                开始使用
              </Button>
            </Card>
          </Col>
        ))}
      </Row>
    </div>
  );
};

export default Home; 