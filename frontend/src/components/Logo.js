import React from 'react';
import { Typography } from 'antd';
import { FileTextOutlined } from '@ant-design/icons';

const { Title } = Typography;

function Logo() {
  return (
    <div style={{ 
      display: 'flex', 
      alignItems: 'center', 
      color: 'white',
      marginRight: '24px'
    }}>
      <FileTextOutlined style={{ fontSize: '24px', marginRight: '8px' }} />
      <Title level={4} style={{ color: 'white', margin: 0 }}>
        Paper Killer
      </Title>
    </div>
  );
}

export default Logo; 