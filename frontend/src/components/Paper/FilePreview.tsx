import React, { useState } from 'react';
import { Modal, Button, Spin } from 'antd';
import { FileTextOutlined } from '@ant-design/icons';

interface FilePreviewProps {
  fileUrl: string;
  fileName: string;
}

const FilePreview: React.FC<FilePreviewProps> = ({ fileUrl, fileName }) => {
  const [isModalVisible, setIsModalVisible] = useState(false);
  const [loading, setLoading] = useState(true);

  const showModal = () => {
    setIsModalVisible(true);
  };

  const handleCancel = () => {
    setIsModalVisible(false);
  };

  const handleIframeLoad = () => {
    setLoading(false);
  };

  return (
    <>
      <Button
        type="link"
        icon={<FileTextOutlined />}
        onClick={showModal}
      >
        预览
      </Button>

      <Modal
        title={fileName}
        open={isModalVisible}
        onCancel={handleCancel}
        width={800}
        footer={null}
        bodyStyle={{ padding: 0, height: '80vh' }}
      >
        <div style={{ position: 'relative', height: '100%' }}>
          {loading && (
            <div style={{
              position: 'absolute',
              top: '50%',
              left: '50%',
              transform: 'translate(-50%, -50%)',
              zIndex: 1
            }}>
              <Spin size="large" />
            </div>
          )}
          <iframe
            src={`${fileUrl}#toolbar=0`}
            style={{
              width: '100%',
              height: '100%',
              border: 'none'
            }}
            onLoad={handleIframeLoad}
          />
        </div>
      </Modal>
    </>
  );
};

export default FilePreview; 