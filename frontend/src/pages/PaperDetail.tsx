import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { Card, Tabs, message } from 'antd';
import { getPaper } from '../services/paper';
import AnalysisPanel from '../components/Paper/AnalysisPanel';
import ExperimentPanel from '../components/Paper/ExperimentPanel';
import SubmissionPanel from '../components/Paper/SubmissionPanel';

const { TabPane } = Tabs;

const PaperDetail: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const [paper, setPaper] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchPaper = async () => {
      try {
        const data = await getPaper(id!);
        setPaper(data);
      } catch (error) {
        message.error('获取论文详情失败');
      } finally {
        setLoading(false);
      }
    };

    fetchPaper();
  }, [id]);

  if (loading) {
    return <div>加载中...</div>;
  }

  if (!paper) {
    return <div>论文不存在</div>;
  }

  return (
    <Card title={paper.title}>
      <Tabs defaultActiveKey="analysis">
        <TabPane tab="分析" key="analysis">
          <AnalysisPanel paperId={id!} />
        </TabPane>
        <TabPane tab="实验" key="experiment">
          <ExperimentPanel paperId={id!} />
        </TabPane>
        <TabPane tab="投稿" key="submission">
          <SubmissionPanel paperId={id!} />
        </TabPane>
      </Tabs>
    </Card>
  );
};

export default PaperDetail; 