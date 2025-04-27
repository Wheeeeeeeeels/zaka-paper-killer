import axios from 'axios';

const API_BASE_URL = 'http://localhost:8003/api';

// 创建 axios 实例
const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
});

// 请求拦截器
api.interceptors.request.use(
  (config) => {
    console.log('发送请求:', config.url, config.params);
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    console.error('请求错误:', error);
    return Promise.reject(error);
  }
);

// 响应拦截器
api.interceptors.response.use(
  (response) => {
    console.log('收到响应:', response.config.url, response.data);
    return response.data;
  },
  (error) => {
    console.error('响应错误:', error.response?.status, error.response?.data);
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// 认证相关接口
export const authAPI = {
  login: (data) => api.post('/auth/token', data),
  register: (data) => api.post('/auth/register', data),
  updateProfile: (data) => api.put('/auth/profile', data),
  changePassword: (data) => api.put('/auth/password', data),
  getProfile: () => api.get('/auth/profile'),
};

// 用户相关接口
export const userAPI = {
  // 获取用户统计信息
  getStats: () => api.get('/users/stats'),
  
  // 获取用户收藏的论文
  getFavoritePapers: () => api.get('/users/favorites'),
  
  // 获取用户评论历史
  getUserComments: () => api.get('/users/comments'),
  
  // 更新用户资料
  updateProfile: (data) => api.put('/users/profile', data),
  
  // 更新用户头像
  updateAvatar: (avatarUrl) => api.put('/users/avatar', { avatar: avatarUrl }),
  
  // 获取用户标签
  getUserTags: () => api.get('/users/tags'),
};

// 论文相关接口
export const paperAPI = {
  // 获取ICLR 2025论文列表
  getICLRPapers: async () => {
    try {
      const response = await api.get('/papers/iclr2025');
      console.log('获取到的论文列表:', response);
      return response;
    } catch (error) {
      console.error('获取论文列表失败:', error);
      throw error;
    }
  },
  
  // 获取特定论文
  getPaper: async (id) => {
    try {
      const response = await api.get(`/papers/iclr2025/${id}`);
      console.log('获取到的论文详情:', response);
      return response;
    } catch (error) {
      console.error('获取论文详情失败:', error);
      throw error;
    }
  },
  
  // 搜索论文
  searchPapers: async (query) => {
    try {
      const response = await api.get('/papers/iclr2025/search', { params: { q: query } });
      console.log('搜索结果:', response);
      return response;
    } catch (error) {
      console.error('搜索论文失败:', error);
      throw error;
    }
  },
  
  // 按主题筛选论文
  getPapersByTopic: async (topic) => {
    try {
      const response = await api.get(`/papers/iclr2025/topic/${topic}`);
      console.log('按主题筛选结果:', response);
      return response;
    } catch (error) {
      console.error('按主题筛选失败:', error);
      throw error;
    }
  },
  
  // 按track筛选论文
  getPapersByTrack: async (track) => {
    try {
      const response = await api.get(`/papers/iclr2025/track/${track}`);
      console.log('按track筛选结果:', response);
      return response;
    } catch (error) {
      console.error('按track筛选失败:', error);
      throw error;
    }
  },
  
  // 更新论文数据
  updatePapers: async () => {
    try {
      const response = await api.post('/papers/iclr2025/update');
      console.log('更新论文数据结果:', response);
      return response;
    } catch (error) {
      console.error('更新论文数据失败:', error);
      throw error;
    }
  },
  
  // 获取论文列表
  getPapers: () => api.get('/papers'),
  
  // 上传论文
  uploadPaper: (formData) => api.post('/papers/upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  }),
  
  // 获取论文文件
  getPaperFile: (id) => api.get(`/papers/${id}/file`, {
    responseType: 'blob',
  }),
  
  // 创建论文分析
  createAnalysis: (id) => api.post(`/papers/${id}/analysis`),
  
  // 获取论文分析结果
  getAnalysis: (id) => api.get(`/papers/${id}/analysis`),
  
  // 获取论文统计信息
  getStats: () => api.get('/papers/stats'),
  
  // 获取最近论文
  getRecentPapers: () => api.get('/papers/recent'),

  // 收藏论文
  favoritePaper: (id) => api.post(`/papers/${id}/favorite`),
  
  // 取消收藏
  unfavoritePaper: (id) => api.delete(`/papers/${id}/favorite`),
  
  // 获取收藏列表
  getFavorites: () => api.get('/papers/favorites'),
  
  // 添加论文标签
  addTag: (id, tag) => api.post(`/papers/${id}/tags`, { tag }),
  
  // 删除论文标签
  removeTag: (id, tag) => api.delete(`/papers/${id}/tags/${tag}`),
  
  // 获取论文标签
  getTags: () => api.get('/papers/tags'),
  
  // 导出论文
  exportPaper: (id) => api.get(`/papers/${id}/export`, { responseType: 'blob' }),
  
  // 批量操作
  batchOperation: (operation, ids) => api.post('/papers/batch', { operation, ids }),

  // 分享论文
  sharePaper: (id, data) => api.post(`/papers/${id}/share`, data),
  
  // 获取分享链接
  getShareLink: (id) => api.get(`/papers/${id}/share`),
  
  // 取消分享
  unsharePaper: (id) => api.delete(`/papers/${id}/share`),
  
  // 获取分享列表
  getSharedPapers: () => api.get('/papers/shared'),
  
  // 添加评论
  addComment: (id, content) => api.post(`/papers/${id}/comments`, { content }),
  
  // 获取评论列表
  getComments: (id) => api.get(`/papers/${id}/comments`),
  
  // 删除评论
  deleteComment: (id, commentId) => api.delete(`/papers/${id}/comments/${commentId}`),
  
  // 回复评论
  replyComment: (id, commentId, content) => api.post(`/papers/${id}/comments/${commentId}/reply`, { content }),

  // ICLR相关接口
  analyzePaper: (id) => api.post(`/papers/${id}/analyze`),
  getUserInterests: () => api.get('/users/interests'),
  updateUserInterests: (interests) => api.put('/users/interests', { interests }),
  getPaperRecommendations: (paperId) => api.get(`/papers/${paperId}/recommendations`),
  getSimilarPapers: (paperId) => api.get(`/papers/${paperId}/similar`),
  getPaperInsights: (paperId) => api.get(`/papers/${paperId}/insights`),

  // 创建新论文
  createPaper: async (data) => {
    try {
      const response = await api.post('/papers/iclr2025/create', data);
      console.log('创建的论文:', response);
      return response;
    } catch (error) {
      console.error('创建论文失败:', error);
      throw error;
    }
  },
};

export default api; 