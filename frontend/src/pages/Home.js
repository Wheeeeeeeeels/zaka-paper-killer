import React from 'react';
import { Typography, Card, Row, Col, Button } from 'antd';
import { Link } from 'react-router-dom';
import {
  FileTextOutlined,
  BarChartOutlined,
  TeamOutlined,
} from '@ant-design/icons';

const { Title, Paragraph } = Typography;

function Home() {
  return (
    <div style={{ padding: '24px 0' }}>
      <Title level={2} style={{ textAlign: 'center', marginBottom: '48px' }}>
        欢迎使用 Paper Killer
      </Title>
      
      <Row gutter={[24, 24]}>
        <Col xs={24} sm={8}>
          <Card
            hoverable
            cover={<FileTextOutlined style={{ fontSize: '48px', padding: '24px' }} />}
          >
            <Card.Meta
              title="论文管理"
              description="上传、存储和管理您的学术论文，支持多种格式"
            />
            <div style={{ marginTop: '16px', textAlign: 'center' }}>
              <Link to="/papers">
                <Button type="primary">开始使用</Button>
              </Link>
            </div>
          </Card>
        </Col>
        
        <Col xs={24} sm={8}>
          <Card
            hoverable
            cover={<BarChartOutlined style={{ fontSize: '48px', padding: '24px' }} />}
          >
            <Card.Meta
              title="论文分析"
              description="自动分析论文内容，提取关键信息，生成分析报告"
            />
            <div style={{ marginTop: '16px', textAlign: 'center' }}>
              <Link to="/papers">
                <Button type="primary">查看分析</Button>
              </Link>
            </div>
          </Card>
        </Col>
        
        <Col xs={24} sm={8}>
          <Card
            hoverable
            cover={<TeamOutlined style={{ fontSize: '48px', padding: '24px' }} />}
          >
            <Card.Meta
              title="团队协作"
              description="与团队成员共享论文，协同工作，提高效率"
            />
            <div style={{ marginTop: '16px', textAlign: 'center' }}>
              <Link to="/register">
                <Button type="primary">加入我们</Button>
              </Link>
            </div>
          </Card>
        </Col>
      </Row>
      
      <div style={{ marginTop: '48px', textAlign: 'center' }}>
        <Title level={3}>为什么选择 Paper Killer？</Title>
        <Paragraph style={{ fontSize: '16px', maxWidth: '800px', margin: '0 auto' }}>
          Paper Killer 是一个强大的学术论文管理工具，它不仅能帮助您整理和管理论文，
          还能通过智能分析功能提取论文的关键信息，生成分析报告，帮助您更好地理解和利用论文内容。
          无论是个人研究还是团队协作，Paper Killer 都能为您提供全方位的支持。
        </Paragraph>
      </div>
    </div>
  );
}

export default Home; 