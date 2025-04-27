import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { Card, Descriptions, Button, message, Spin, Tabs, Tag, Input, Space, Modal, List, Avatar, Popconfirm } from 'antd';
import { DownloadOutlined, BarChartOutlined, StarOutlined, StarFilled, TagOutlined, ExportOutlined, ShareAltOutlined, UserOutlined, DeleteOutlined, MessageOutlined } from '@ant-design/icons';
import { paperAPI } from '../services/api';

const { TabPane } = Tabs;
const { Search } = Input;
const { TextArea } = Input;

function PaperDetail() {
  const { id } = useParams();
  const [paper, setPaper] = useState(null);
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(true);
  const [newTag, setNewTag] = useState('');
  const [comments, setComments] = useState([]);
  const [newComment, setNewComment] = useState('');
  const [shareModalVisible, setShareModalVisible] = useState(false);
  const [shareLink, setShareLink] = useState('');
  const [replyTo, setReplyTo] = useState(null);

  useEffect(() => {
    fetchPaper();
    fetchAnalysis();
    fetchComments();
  }, [id]);

  const fetchPaper = async () => {
    try {
      const data = await paperAPI.getPaper(id);
      setPaper(data);
    } catch (error) {
      message.error('获取论文详情失败');
    } finally {
      setLoading(false);
    }
  };

  const fetchAnalysis = async () => {
    try {
      const data = await paperAPI.getAnalysis(id);
      setAnalysis(data);
    } catch (error) {
      console.log('获取分析结果失败');
    }
  };

  const fetchComments = async () => {
    try {
      const data = await paperAPI.getComments(id);
      setComments(data);
    } catch (error) {
      message.error('获取评论失败');
    }
  };

  const handleDownload = async () => {
    try {
      const response = await paperAPI.getPaperFile(id);
      const url = window.URL.createObjectURL(new Blob([response]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `${paper.title}.pdf`);
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (error) {
      message.error('下载论文失败');
    }
  };

  const handleExport = async () => {
    try {
      const response = await paperAPI.exportPaper(id);
      const url = window.URL.createObjectURL(new Blob([response]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `${paper.title}_export.pdf`);
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (error) {
      message.error('导出论文失败');
    }
  };

  const handleAnalyze = async () => {
    try {
      await paperAPI.createAnalysis(id);
      message.success('论文分析已开始');
      fetchAnalysis();
    } catch (error) {
      message.error('论文分析失败');
    }
  };

  const handleFavorite = async () => {
    try {
      if (paper.is_favorite) {
        await paperAPI.unfavoritePaper(id);
        message.success('已取消收藏');
      } else {
        await paperAPI.favoritePaper(id);
        message.success('已收藏');
      }
      fetchPaper();
    } catch (error) {
      message.error('操作失败');
    }
  };

  const handleAddTag = async (value) => {
    try {
      await paperAPI.addTag(id, value);
      message.success('标签添加成功');
      setNewTag('');
      fetchPaper();
    } catch (error) {
      message.error('标签添加失败');
    }
  };

  const handleRemoveTag = async (tag) => {
    try {
      await paperAPI.removeTag(id, tag);
      message.success('标签删除成功');
      fetchPaper();
    } catch (error) {
      message.error('标签删除失败');
    }
  };

  const handleShare = async () => {
    try {
      const data = await paperAPI.getShareLink(id);
      setShareLink(data.share_link);
      setShareModalVisible(true);
    } catch (error) {
      message.error('获取分享链接失败');
    }
  };

  const handleUnshare = async () => {
    try {
      await paperAPI.unsharePaper(id);
      message.success('已取消分享');
      setShareModalVisible(false);
    } catch (error) {
      message.error('取消分享失败');
    }
  };

  const handleAddComment = async () => {
    if (!newComment.trim()) {
      message.warning('请输入评论内容');
      return;
    }

    try {
      if (replyTo) {
        await paperAPI.replyComment(id, replyTo.id, newComment);
      } else {
        await paperAPI.addComment(id, newComment);
      }
      message.success('评论成功');
      setNewComment('');
      setReplyTo(null);
      fetchComments();
    } catch (error) {
      message.error('评论失败');
    }
  };

  const handleDeleteComment = async (commentId) => {
    try {
      await paperAPI.deleteComment(id, commentId);
      message.success('评论已删除');
      fetchComments();
    } catch (error) {
      message.error('删除评论失败');
    }
  };

  const handleReply = (comment) => {
    setReplyTo(comment);
    setNewComment('');
  };

  if (loading) {
    return <Spin size="large" />;
  }

  return (
    <div style={{ padding: '24px 0' }}>
      <Card
        title={paper.title}
        extra={
          <Space>
            <Button
              type="text"
              icon={paper.is_favorite ? <StarFilled style={{ color: '#fadb14' }} /> : <StarOutlined />}
              onClick={handleFavorite}
            />
            <Button
              icon={<ShareAltOutlined />}
              onClick={handleShare}
            >
              分享
            </Button>
            <Button
              icon={<DownloadOutlined />}
              onClick={handleDownload}
            >
              下载论文
            </Button>
            <Button
              icon={<ExportOutlined />}
              onClick={handleExport}
            >
              导出
            </Button>
            <Button
              type="primary"
              icon={<BarChartOutlined />}
              onClick={handleAnalyze}
            >
              分析论文
            </Button>
          </Space>
        }
      >
        <Descriptions bordered>
          <Descriptions.Item label="作者" span={3}>
            {paper.authors}
          </Descriptions.Item>
          <Descriptions.Item label="会议/期刊" span={3}>
            {paper.conference}
          </Descriptions.Item>
          <Descriptions.Item label="年份" span={3}>
            {paper.year}
          </Descriptions.Item>
          <Descriptions.Item label="摘要" span={3}>
            {paper.abstract}
          </Descriptions.Item>
          <Descriptions.Item label="标签" span={3}>
            <Space wrap>
              {paper.tags?.map(tag => (
                <Tag
                  key={tag}
                  closable
                  onClose={() => handleRemoveTag(tag)}
                >
                  {tag}
                </Tag>
              ))}
              <Search
                placeholder="添加标签"
                allowClear
                enterButton={<TagOutlined />}
                onSearch={handleAddTag}
                style={{ width: 200 }}
                value={newTag}
                onChange={e => setNewTag(e.target.value)}
              />
            </Space>
          </Descriptions.Item>
        </Descriptions>

        <Tabs defaultActiveKey="1" style={{ marginTop: 24 }}>
          <TabPane tab="论文分析" key="1">
            {analysis ? (
              <div>
                <h3>关键词</h3>
                <p>{analysis.keywords?.join(', ')}</p>
                
                <h3>主要发现</h3>
                <p>{analysis.findings}</p>
                
                <h3>研究方法</h3>
                <p>{analysis.methodology}</p>
                
                <h3>结论</h3>
                <p>{analysis.conclusion}</p>
              </div>
            ) : (
              <p>暂无分析结果</p>
            )}
          </TabPane>
          <TabPane tab="引用信息" key="2">
            <p>引用次数：{paper.citations || 0}</p>
            <p>DOI：{paper.doi || '未提供'}</p>
          </TabPane>
          <TabPane tab="评论" key="3">
            <div style={{ marginBottom: 16 }}>
              <TextArea
                rows={4}
                value={newComment}
                onChange={e => setNewComment(e.target.value)}
                placeholder={replyTo ? `回复 ${replyTo.user.username}：` : '写下你的评论...'}
              />
              <div style={{ marginTop: 8, textAlign: 'right' }}>
                {replyTo && (
                  <Button
                    type="link"
                    onClick={() => setReplyTo(null)}
                    style={{ marginRight: 8 }}
                  >
                    取消回复
                  </Button>
                )}
                <Button type="primary" onClick={handleAddComment}>
                  发表评论
                </Button>
              </div>
            </div>
            <List
              itemLayout="horizontal"
              dataSource={comments}
              renderItem={comment => (
                <List.Item
                  actions={[
                    <Button type="link" onClick={() => handleReply(comment)}>
                      回复
                    </Button>,
                    <Popconfirm
                      title="确定要删除这条评论吗？"
                      onConfirm={() => handleDeleteComment(comment.id)}
                      okText="确定"
                      cancelText="取消"
                    >
                      <Button type="link" danger>
                        删除
                      </Button>
                    </Popconfirm>
                  ]}
                >
                  <List.Item.Meta
                    avatar={<Avatar icon={<UserOutlined />} />}
                    title={
                      <Space>
                        <span>{comment.user.username}</span>
                        {comment.reply_to && (
                          <>
                            <span>回复</span>
                            <span>{comment.reply_to.username}</span>
                          </>
                        )}
                      </Space>
                    }
                    description={
                      <div>
                        <p>{comment.content}</p>
                        <small style={{ color: '#999' }}>
                          {new Date(comment.created_at).toLocaleString()}
                        </small>
                      </div>
                    }
                  />
                </List.Item>
              )}
            />
          </TabPane>
        </Tabs>
      </Card>

      <Modal
        title="分享论文"
        visible={shareModalVisible}
        onCancel={() => setShareModalVisible(false)}
        footer={[
          <Button key="unshare" danger onClick={handleUnshare}>
            取消分享
          </Button>,
          <Button key="copy" type="primary" onClick={() => {
            navigator.clipboard.writeText(shareLink);
            message.success('链接已复制到剪贴板');
          }}>
            复制链接
          </Button>,
          <Button key="close" onClick={() => setShareModalVisible(false)}>
            关闭
          </Button>
        ]}
      >
        <p>分享链接：</p>
        <Input.TextArea
          value={shareLink}
          autoSize
          readOnly
          style={{ marginBottom: 16 }}
        />
        <p>通过此链接，其他人可以查看这篇论文。</p>
      </Modal>
    </div>
  );
}

export default PaperDetail; 