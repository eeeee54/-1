# 整蛊网站项目

## 项目简介
这是一个有趣的整蛊网站项目，主要用于娱乐目的。网站会向用户展示一个"两难选择"，无论用户选择哪一个选项，都会触发有趣的互动效果。

## 功能特点
- 交互式问答界面
- 动态展示结果和动画效果
- 响应式设计，支持各种设备
- 多服务器支持（Flask、Waitress、简单HTTP服务器）
- 可选的数据库记录功能

## 技术栈
- **后端**: Python, Flask, Waitress
- **前端**: HTML, CSS, JavaScript
- **数据库**: MySQL（可选）

## 快速开始

### 前提条件
- Python 3.6+
- pip
- MySQL（可选，用于数据存储）

### 安装步骤

1. **克隆项目**
```bash
git clone <repository-url>
cd prank_website
```

2. **安装依赖**
```bash
pip install -r requirements.txt
```

3. **数据库设置**（可选）
   - 导入数据库脚本
   ```bash
   mysql -u username -p < prank_database.sql
   ```
   - 修改数据库连接配置（如果需要）

## 运行项目

### 方法1：使用Flask开发服务器
```bash
python app.py
```

### 方法2：使用Waitress生产服务器
```bash
python start_server.py
```

### 方法3：使用简单HTTP服务器
```bash
python simple_server.py
```

服务器启动后，访问 http://localhost:5000 即可使用网站。

## 项目结构
```
prank_website/
├── app.py              # Flask应用主文件
├── start_server.py     # Waitress服务器启动脚本
├── simple_server.py    # 简单HTTP服务器实现
├── requirements.txt    # 项目依赖
├── prank_database.sql  # 数据库初始化脚本
├── static/             # 静态资源
│   ├── css/            # CSS文件
│   ├── js/             # JavaScript文件
│   └── images/         # 图片资源
└── templates/          # HTML模板
    └── index.html      # 主页面
```

## 使用说明
1. 打开网站后，会看到两个选择按钮
2. 点击任意按钮，将会展示有趣的结果页面
3. 结果页面会显示动画效果和文本信息

## 自定义
- 修改`templates/index.html`自定义HTML内容
- 修改`static/css/style.css`自定义样式
- 修改`static/js/script.js`自定义交互逻辑

## 注意事项
- 本项目仅供娱乐目的，请勿用于商业或不当用途
- 请确保在适当的环境中使用，尊重他人隐私
- 数据库功能为可选功能，可根据需要启用或禁用

## 许可证
MIT License

## 贡献
欢迎提交Issues和Pull Requests来改进这个项目！