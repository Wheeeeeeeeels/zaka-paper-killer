import React, { useState } from 'react';
import { Card, Steps, Form, Input, Button, Space, Typography, message, Select, Divider } from 'antd';
import { FileTextOutlined, BulbOutlined, ExperimentOutlined, EditOutlined, CheckCircleOutlined } from '@ant-design/icons';
import styled from 'styled-components';
import { paperAPI } from '../services/api';
import { useNavigate } from 'react-router-dom';

const { Title, Text, Paragraph } = Typography;
const { TextArea } = Input;
const { Option } = Select;
const { Step } = Steps;

const WriteContainer = styled.div`
  padding: 24px;
  background: #f5f5f5;
  min-height: 100vh;
`;

const StepContent = styled.div`
  margin-top: 24px;
  padding: 24px;
  background: white;
  border-radius: 4px;
`;

function WritePaper() {
  const navigate = useNavigate();
  const [currentStep, setCurrentStep] = useState(0);
  const [form] = Form.useForm();
  const [submitting, setSubmitting] = useState(false);

  const steps = [
    {
      title: '研究主题',
      icon: <FileTextOutlined />,
      content: (
        <Form.Item
          name="topic"
          label="研究主题"
          rules={[{ required: true, message: '请输入研究主题' }]}
        >
          <Input placeholder="例如：基于Transformer的视觉语言模型" />
        </Form.Item>
      )
    },
    {
      title: '创新点',
      icon: <BulbOutlined />,
      content: (
        <Form.Item
          name="innovations"
          label="创新点"
          rules={[{ required: true, message: '请输入创新点' }]}
        >
          <TextArea
            rows={4}
            placeholder="请列出您的研究创新点，每行一个"
          />
        </Form.Item>
      )
    },
    {
      title: '实验设计',
      icon: <ExperimentOutlined />,
      content: (
        <>
          <Form.Item
            name="datasets"
            label="数据集"
            rules={[{ required: true, message: '请选择数据集' }]}
          >
            <Select mode="multiple" placeholder="选择要使用的数据集">
              <Option value="imagenet">ImageNet</Option>
              <Option value="coco">COCO</Option>
              <Option value="cifar">CIFAR</Option>
              <Option value="mnist">MNIST</Option>
            </Select>
          </Form.Item>
          <Form.Item
            name="metrics"
            label="评估指标"
            rules={[{ required: true, message: '请选择评估指标' }]}
          >
            <Select mode="multiple" placeholder="选择评估指标">
              <Option value="accuracy">准确率</Option>
              <Option value="precision">精确率</Option>
              <Option value="recall">召回率</Option>
              <Option value="f1">F1分数</Option>
            </Select>
          </Form.Item>
        </>
      )
    },
    {
      title: '论文结构',
      icon: <EditOutlined />,
      content: (
        <Form.Item
          name="outline"
          label="论文大纲"
          rules={[{ required: true, message: '请输入论文大纲' }]}
        >
          <TextArea
            rows={6}
            placeholder="请列出论文的主要章节和内容"
          />
        </Form.Item>
      )
    }
  ];

  const handleNext = async () => {
    try {
      await form.validateFields();
      setCurrentStep(currentStep + 1);
    } catch (error) {
      message.error('请完成当前步骤的所有必填项');
    }
  };

  const handlePrev = () => {
    setCurrentStep(currentStep - 1);
  };

  const handleSubmit = async () => {
    try {
      setSubmitting(true);
      const values = await form.validateFields();
      console.log('提交的论文信息:', values);
      
      // 调用API创建论文
      const response = await paperAPI.createPaper(values);
      message.success('论文创建成功');
      
      // 跳转到论文列表页面
      navigate('/iclr2025');
    } catch (error) {
      console.error('创建论文失败:', error);
      message.error('创建论文失败，请重试');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <WriteContainer>
      <Card>
        <Title level={2}>写论文</Title>
        <Steps current={currentStep} style={{ marginBottom: 24 }}>
          {steps.map(step => (
            <Step key={step.title} title={step.title} icon={step.icon} />
          ))}
        </Steps>
        <Form
          form={form}
          layout="vertical"
          initialValues={{
            topic: '',
            innovations: '',
            datasets: [],
            metrics: [],
            outline: ''
          }}
        >
          <StepContent>
            {steps[currentStep].content}
          </StepContent>
          <div style={{ marginTop: 24, textAlign: 'right' }}>
            {currentStep > 0 && (
              <Button style={{ marginRight: 8 }} onClick={handlePrev}>
                上一步
              </Button>
            )}
            {currentStep < steps.length - 1 && (
              <Button type="primary" onClick={handleNext}>
                下一步
              </Button>
            )}
            {currentStep === steps.length - 1 && (
              <Button 
                type="primary" 
                onClick={handleSubmit}
                loading={submitting}
              >
                提交
              </Button>
            )}
          </div>
        </Form>
      </Card>
    </WriteContainer>
  );
}

export default WritePaper; 