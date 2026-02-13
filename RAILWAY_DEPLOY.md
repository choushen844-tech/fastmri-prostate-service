# FastMRI Prostate Service - Railway部署指南

## 快速部署步骤

### 1. 准备工作
- 访问 https://railway.app
- 使用GitHub账户登录或注册

### 2. 一键部署
点击下面的按钮进行一键部署：

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new?templateUrl=https://github.com/shenqiu123/fastmri-prostate-service)

### 3. 手动部署（如果一键部署不可用）

#### 使用Railway CLI：
```bash
# 安装Railway CLI
npm install -g @railway/cli

# 登录Railway
railway login

# 初始化项目
railway init

# 部署
railway up
```

#### 使用GitHub集成：
1. 将代码推送到GitHub仓库
2. 在Railway中连接GitHub仓库
3. 选择此仓库进行部署
4. Railway会自动检测Dockerfile并构建部署

### 4. 获取API URL
部署完成后，Railway会为您生成一个公开URL，格式如：
```
https://your-service-name-production.up.railway.app
```

### 5. 测试API
```bash
# 测试健康检查
curl https://your-service-name-production.up.railway.app/

# 测试预测API（上传文件）
curl -X POST \
  -F "file=@/path/to/mri_image.png" \
  https://your-service-name-production.up.railway.app/predict

# 测试预测API（通过URL）
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"image_url": "https://example.com/image.png"}' \
  https://your-service-name-production.up.railway.app/predict-url
```

## 环境变量配置
如需添加环境变量，在Railway仪表板中：
1. 打开项目设置
2. 找到"Variables"部分
3. 添加所需的环境变量

## 常见问题

### Q: 部署后应用无法启动？
A: 检查Railway日志：
1. 打开Railway仪表板
2. 选择您的服务
3. 查看"Logs"标签中的错误信息

### Q: 如何更新应用？
A: 
- 如果使用GitHub集成，只需推送新代码到GitHub，Railway会自动重新部署
- 如果使用CLI，运行 `railway up` 重新部署

### Q: 如何查看应用日志？
A: 在Railway仪表板中选择您的服务，点击"Logs"标签查看实时日志

## 支持
如有问题，请访问 https://railway.app/docs
