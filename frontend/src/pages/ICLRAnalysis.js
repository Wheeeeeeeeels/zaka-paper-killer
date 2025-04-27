import React, { useState, useEffect } from 'react';
import { Card, List, Tag, Button, Input, Select, Space, Typography, Row, Col, Progress, message, Tabs, Collapse, Steps } from 'antd';
import { SearchOutlined, FileTextOutlined, BulbOutlined, ExperimentOutlined, EditOutlined, CheckCircleOutlined, PlusOutlined } from '@ant-design/icons';
import styled from 'styled-components';
import { paperAPI } from '../services/api';
import { useNavigate } from 'react-router-dom';

const { Title, Text, Paragraph } = Typography;
const { Search } = Input;
const { Option } = Select;
const { TabPane } = Tabs;
const { Panel } = Collapse;
const { Step } = Steps;

const AnalysisContainer = styled.div`
  padding: 24px;
  background: #f5f5f5;
  min-height: 100vh;
`;

const PaperCard = styled(Card)`
  margin-bottom: 16px;
  transition: all 0.3s;
  
  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  }
`;

const TagContainer = styled.div`
  margin: 8px 0;
`;

const SimilarityScore = styled.div`
  display: flex;
  align-items: center;
  margin-top: 8px;
  
  .ant-progress {
    margin-right: 8px;
  }
`;

const InnovationCard = styled(Card)`
  margin-bottom: 16px;
  background: #f0f5ff;
`;

function ICLRAnalysis() {
  const navigate = useNavigate();
  const [papers, setPapers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedTrack, setSelectedTrack] = useState('all');
  const [selectedTopic, setSelectedTopic] = useState('all');
  const [recommendations, setRecommendations] = useState([]);
  const [selectedPaper, setSelectedPaper] = useState(null);
  const [currentStep, setCurrentStep] = useState(0);

  useEffect(() => {
    console.log('组件挂载，开始获取论文数据...');
    fetchPapers();
  }, []);

  const fetchPapers = async () => {
    setLoading(true);
    try {
      console.log('正在获取论文数据...');
      const response = await paperAPI.getICLRPapers();
      console.log('获取到的论文数据:', response);
      setPapers(response);
      // 生成推荐
      generateRecommendations(response);
    } catch (error) {
      console.error('获取论文数据失败:', error);
      message.error('获取论文数据失败');
    } finally {
      setLoading(false);
    }
  };

  const generateRecommendations = (papers) => {
    console.log('正在生成推荐...');
    // 基于论文内容生成推荐
    const recommendations = papers
      .sort((a, b) => b.similarityScore - a.similarityScore)
      .slice(0, 5)
      .map(paper => ({
        ...paper,
        potentialInnovations: paper.gaps.map(gap => `可以解决: ${gap}`)
      }));
    console.log('生成的推荐:', recommendations);
    setRecommendations(recommendations);
  };

  const handleSearch = async (value) => {
    setSearchQuery(value);
    setLoading(true);
    try {
      console.log('正在搜索论文:', value);
      const response = await paperAPI.searchPapers(value);
      console.log('搜索结果:', response);
      setPapers(response);
    } catch (error) {
      console.error('搜索失败:', error);
      message.error('搜索失败');
    } finally {
      setLoading(false);
    }
  };

  const handleTrackChange = async (value) => {
    setSelectedTrack(value);
    if (value === 'all') {
      fetchPapers();
      return;
    }
    setLoading(true);
    try {
      console.log('正在按 track 筛选:', value);
      const response = await paperAPI.getPapersByTrack(value);
      console.log('筛选结果:', response);
      setPapers(response);
    } catch (error) {
      console.error('筛选失败:', error);
      message.error('筛选失败');
    } finally {
      setLoading(false);
    }
  };

  const handleTopicChange = async (value) => {
    setSelectedTopic(value);
    if (value === 'all') {
      fetchPapers();
      return;
    }
    setLoading(true);
    try {
      console.log('正在按主题筛选:', value);
      const response = await paperAPI.getPapersByTopic(value);
      console.log('筛选结果:', response);
      setPapers(response);
    } catch (error) {
      console.error('筛选失败:', error);
      message.error('筛选失败');
    } finally {
      setLoading(false);
    }
  };

  const handleAnalyze = (paper) => {
    console.log('正在分析论文:', paper);
    setSelectedPaper(paper);
    setCurrentStep(0);
  };

  const handleWritePaper = () => {
    navigate('/write-paper');
  };

  const renderPaperCard = (paper) => (
    <PaperCard
      key={paper.id}
      title={
        <Space>
          <FileTextOutlined />
          {paper.title}
        </Space>
      }
      extra={
        <Button type="primary" onClick={() => handleAnalyze(paper)}>
          分析
        </Button>
      }
    >
      <div>
        <Text type="secondary">作者: {paper.authors}</Text>
        <TagContainer>
          {paper.tags.map(tag => (
            <Tag key={tag} color="blue">{tag}</Tag>
          ))}
        </TagContainer>
        <SimilarityScore>
          <Progress
            percent={paper.similarityScore * 100}
            size="small"
            status="active"
          />
          <Text type="secondary">与您的研究方向匹配度</Text>
        </SimilarityScore>
      </div>
    </PaperCard>
  );

  const renderAnalysisPanel = () => {
    if (!selectedPaper) return null;

    return (
      <Card title="论文分析" style={{ marginTop: 24 }}>
        <Steps current={currentStep} style={{ marginBottom: 24 }}>
          <Step title="论文概览" icon={<FileTextOutlined />} />
          <Step title="创新点分析" icon={<BulbOutlined />} />
          <Step title="研究机会" icon={<ExperimentOutlined />} />
          <Step title="实验设计" icon={<ExperimentOutlined />} />
          <Step title="论文规划" icon={<EditOutlined />} />
        </Steps>

        <Tabs defaultActiveKey="1">
          <TabPane tab="论文概览" key="1">
            <Paragraph>
              <Title level={4}>摘要</Title>
              {selectedPaper.abstract}
            </Paragraph>
            <Paragraph>
              <Title level={4}>主要贡献</Title>
              <ul>
                {selectedPaper.innovations.map((innovation, index) => (
                  <li key={index}>{innovation}</li>
                ))}
              </ul>
            </Paragraph>
          </TabPane>
          <TabPane tab="创新点分析" key="2">
            <Collapse>
              <Panel header="创新点" key="1">
                <List
                  dataSource={selectedPaper.innovations}
                  renderItem={item => (
                    <List.Item>
                      <BulbOutlined style={{ color: '#1890ff', marginRight: 8 }} />
                      {item}
                    </List.Item>
                  )}
                />
              </Panel>
              <Panel header="研究空白" key="2">
                <List
                  dataSource={selectedPaper.gaps}
                  renderItem={item => (
                    <List.Item>
                      <ExperimentOutlined style={{ color: '#1890ff', marginRight: 8 }} />
                      {item}
                    </List.Item>
                  )}
                />
              </Panel>
            </Collapse>
          </TabPane>
          <TabPane tab="研究机会" key="3">
            <InnovationCard>
              <Title level={4}>潜在研究方向</Title>
              <List
                dataSource={selectedPaper.gaps}
                renderItem={item => (
                  <List.Item>
                    <CheckCircleOutlined style={{ color: '#52c41a', marginRight: 8 }} />
                    {item}
                  </List.Item>
                )}
              />
            </InnovationCard>
          </TabPane>
          <TabPane tab="实验设计" key="4">
            <Card>
              <Title level={4}>实验建议</Title>
              <List
                dataSource={selectedPaper.experiments.setup}
                renderItem={item => (
                  <List.Item>
                    <ExperimentOutlined style={{ color: '#1890ff', marginRight: 8 }} />
                    {item}
                  </List.Item>
                )}
              />
            </Card>
          </TabPane>
          <TabPane tab="论文规划" key="5">
            <Card>
              <Title level={4}>论文结构建议</Title>
              <Steps direction="vertical" current={0}>
                <Step title="引言" description="介绍研究背景和动机" />
                <Step title="相关工作" description="总结现有方法和局限性" />
                <Step title="方法" description="详细描述提出的方法" />
                <Step title="实验" description="展示实验结果和分析" />
                <Step title="结论" description="总结主要发现和未来工作" />
              </Steps>
            </Card>
          </TabPane>
        </Tabs>
      </Card>
    );
  };

  return (
    <AnalysisContainer>
      <Row gutter={[24, 24]}>
        <Col span={24}>
          <Card>
            <Space style={{ width: '100%', justifyContent: 'space-between' }}>
              <Title level={2}>ICLR 2025 论文分析</Title>
              <Button 
                type="primary" 
                icon={<PlusOutlined />}
                onClick={handleWritePaper}
              >
                写论文
              </Button>
            </Space>
            <Space direction="vertical" style={{ width: '100%' }}>
              <Search
                placeholder="搜索论文标题、作者或关键词"
                allowClear
                enterButton={<SearchOutlined />}
                size="large"
                onSearch={handleSearch}
              />
              <Space>
                <Select
                  defaultValue="all"
                  style={{ width: 200 }}
                  onChange={handleTrackChange}
                >
                  <Option value="all">所有Track</Option>
                  <Option value="oral">Oral</Option>
                  <Option value="poster">Poster</Option>
                  <Option value="workshop">Workshop</Option>
                </Select>
                <Select
                  defaultValue="all"
                  style={{ width: 200 }}
                  onChange={handleTopicChange}
                >
                  <Option value="all">所有主题</Option>
                  <Option value="ml">机器学习</Option>
                  <Option value="nlp">自然语言处理</Option>
                  <Option value="cv">计算机视觉</Option>
                  <Option value="rl">强化学习</Option>
                </Select>
              </Space>
            </Space>
          </Card>
        </Col>

        <Col span={16}>
          <Card title="论文列表" loading={loading}>
            <List
              dataSource={papers}
              renderItem={renderPaperCard}
            />
          </Card>
          {renderAnalysisPanel()}
        </Col>

        <Col span={8}>
          <Card title="个性化推荐">
            <List
              dataSource={recommendations}
              renderItem={item => (
                <List.Item>
                  <List.Item.Meta
                    title={item.title}
                    description={
                      <Space direction="vertical">
                        <Text type="secondary">{item.authors}</Text>
                        <TagContainer>
                          {item.tags.map(tag => (
                            <Tag key={tag} color="blue">{tag}</Tag>
                          ))}
                        </TagContainer>
                        <Text type="secondary">推荐理由: {item.reason}</Text>
                        <Collapse>
                          <Panel header="潜在创新点" key="1">
                            <List
                              dataSource={item.potentialInnovations}
                              renderItem={innovation => (
                                <List.Item>
                                  <BulbOutlined style={{ color: '#1890ff', marginRight: 8 }} />
                                  {innovation}
                                </List.Item>
                              )}
                            />
                          </Panel>
                        </Collapse>
                      </Space>
                    }
                  />
                </List.Item>
              )}
            />
          </Card>
        </Col>
      </Row>
    </AnalysisContainer>
  );
}

export default ICLRAnalysis; 