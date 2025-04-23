import React, { useState } from 'react';
import { Upload, Button, message, Progress, Card, Typography, List } from 'antd';
import { UploadOutlined, InboxOutlined, DeleteOutlined } from '@ant-design/icons';
import type { UploadFile } from 'antd/es/upload/interface';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const { Dragger } = Upload;
const { Text } = Typography;

interface UploadResult {
  paper_id: number;
  title: string;
  status: 'success' | 'error';
  message: string;
}

const FileUpload: React.FC = () => {
  const [fileList, setFileList] = useState<UploadFile[]>([]);
  const [uploading, setUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState<{ [key: string]: number }>({});
  const [uploadResults, setUploadResults] = useState<UploadResult[]>([]);
  const navigate = useNavigate();

  const handleUpload = async () => {
    setUploading(true);
    setUploadProgress({});
    setUploadResults([]);

    const results: UploadResult[] = [];

    for (const file of fileList) {
      const formData = new FormData();
      formData.append('file', file as any);

      try {
        const response = await axios.post('/api/v1/papers/upload', formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
            Authorization: `Bearer ${localStorage.getItem('token')}`
          },
          onUploadProgress: (progressEvent) => {
            if (progressEvent.total) {
              const progress = Math.round((progressEvent.loaded * 100) / progressEvent.total);
              setUploadProgress(prev => ({
                ...prev,
                [file.uid]: progress
              }));
            }
          }
        });

        results.push({
          paper_id: response.data.paper_id,
          title: file.name,
          status: 'success',
          message: '上传成功'
        });
      } catch (error: any) {
        results.push({
          paper_id: 0,
          title: file.name,
          status: 'error',
          message: error.response?.data?.detail || '上传失败'
        });
      }
    }

    setUploadResults(results);
    setUploading(false);
    setFileList([]);

    // 如果有成功上传的文件，刷新论文列表
    if (results.some(r => r.status === 'success')) {
      message.success('部分文件上传成功');
    }
  };

  const props = {
    name: 'file',
    multiple: true,
    fileList,
    onRemove: (file: UploadFile) => {
      const index = fileList.indexOf(file);
      const newFileList = fileList.slice();
      newFileList.splice(index, 1);
      setFileList(newFileList);
    },
    beforeUpload: (file: UploadFile) => {
      // 检查文件类型
      if (file.type !== 'application/pdf') {
        message.error(`${file.name} 不是PDF文件！`);
        return false;
      }

      // 检查文件大小（10MB）
      const isLt10M = file.size! / 1024 / 1024 < 10;
      if (!isLt10M) {
        message.error(`${file.name} 大小超过10MB！`);
        return false;
      }

      return false;
    },
    showUploadList: {
      showPreviewIcon: true,
      showRemoveIcon: true,
      showDownloadIcon: false,
    },
  };

  return (
    <Card>
      <Dragger {...props}>
        <p className="ant-upload-drag-icon">
          <InboxOutlined />
        </p>
        <p className="ant-upload-text">点击或拖拽文件到此区域上传</p>
        <p className="ant-upload-hint">
          支持多个PDF文件上传，每个文件大小不超过10MB
        </p>
      </Dragger>

      {fileList.length > 0 && (
        <div style={{ marginTop: 16 }}>
          <Text type="secondary">
            已选择 {fileList.length} 个文件
          </Text>
        </div>
      )}

      {Object.entries(uploadProgress).map(([uid, progress]) => (
        <div key={uid} style={{ marginTop: 16 }}>
          <Progress percent={progress} status="active" />
        </div>
      ))}

      {uploadResults.length > 0 && (
        <List
          style={{ marginTop: 16 }}
          bordered
          dataSource={uploadResults}
          renderItem={item => (
            <List.Item>
              <List.Item.Meta
                title={item.title}
                description={item.message}
              />
              {item.status === 'success' && (
                <Button
                  type="link"
                  onClick={() => navigate(`/papers/${item.paper_id}/analysis`)}
                >
                  查看分析
                </Button>
              )}
            </List.Item>
          )}
        />
      )}

      <Button
        type="primary"
        onClick={handleUpload}
        disabled={fileList.length === 0}
        loading={uploading}
        style={{ marginTop: 16 }}
      >
        {uploading ? '上传中' : '开始上传'}
      </Button>
    </Card>
  );
};

export default FileUpload; 