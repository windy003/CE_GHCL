# GitHub Code Line Counter Chrome Extension

Chrome扩展程序，用于将GitHub仓库发送到服务器进行代码行数统计。支持本地运行和远程VPS部署。

## 功能特点

- 自动检测GitHub仓库页面
- 提取仓库信息（URL、所有者、仓库名等）
- 发送仓库信息到服务器（本地或远程）
- 服务器端自动git clone并统计代码行数
- 支持25+种编程语言文件类型
- 显示详细的文件统计信息
- 跨平台支持（Windows/Linux/macOS）

## 安装使用

### 1. Chrome扩展安装

1. 打开Chrome浏览器，进入 `chrome://extensions/`
2. 开启"开发者模式"
3. 点击"加载已解压的扩展程序"
4. 选择项目根目录
5. 扩展程序安装完成

### 2. 服务器部署

#### 方式一：Windows本机运行（推荐用于开发测试）

```cmd
# 确保已安装Python 3.7+和git
cd server
start.bat
```

#### 方式二：Linux/macOS/VPS运行

```bash
# 确保已安装Python 3.7+和git
cd server
chmod +x start.sh
./start.sh
```

#### 方式三：手动启动

```bash
cd server
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

服务器将在端口3000上运行。

### 3. 使用方法

1. 在Chrome中访问任意GitHub仓库页面
2. 点击扩展图标
3. 输入服务器地址：
   - 本地运行：`http://localhost:3000/analyze`
   - VPS部署：`http://your-server.com:3000/analyze`
4. 点击"发送分析"按钮
5. 等待分析结果

## 文件结构

```
├── manifest.json       # Chrome扩展清单文件
├── popup.html         # 弹出窗口HTML
├── popup.js           # 弹出窗口逻辑
├── content.js         # 内容脚本
├── background.js      # 后台脚本
└── server/           # 服务器端代码（Python Flask）
    ├── app.py        # 主服务器文件
    ├── requirements.txt  # Python依赖
    ├── start.sh      # Linux/macOS启动脚本
    └── start.bat     # Windows启动脚本
```

## API接口

### POST /analyze

分析GitHub仓库代码行数

**请求体：**
```json
{
  "repoUrl": "https://github.com/owner/repo",
  "cloneUrl": "https://github.com/owner/repo.git",
  "owner": "owner",
  "repo": "repo"
}
```

**响应：**
```json
{
  "success": true,
  "lines": 1234,
  "fileStats": {
    ".js": {
      "language": "JavaScript",
      "files": 10, 
      "lines": 500
    },
    ".py": {
      "language": "Python",
      "files": 5, 
      "lines": 300
    }
  },
  "timestamp": "2023-12-01T10:00:00.000Z"
}
```

### GET /health

健康检查端点

### GET /stats

获取服务器支持的语言统计信息

## 支持的文件类型

- **Web开发**：JavaScript (.js, .jsx), TypeScript (.ts, .tsx), HTML (.html), CSS (.css, .scss, .less), Vue (.vue)
- **后端语言**：Python (.py), Java (.java), C# (.cs), PHP (.php), Ruby (.rb), Go (.go)
- **系统编程**：C (.c), C++ (.cpp), Rust (.rs), Swift (.swift)
- **移动开发**：Kotlin (.kt), Dart (.dart), Objective-C (.m, .mm)
- **其他**：Scala (.scala), R (.r), Perl (.pl), Lua (.lua), Shell (.sh)

## 部署环境要求

### Windows本机
- Python 3.7+
- Git
- 网络连接

### Linux/VPS
- Python 3.7+
- Git  
- 足够的磁盘空间用于临时克隆仓库

## 注意事项

- 首次运行会自动安装Python依赖
- 大型仓库可能需要较长分析时间
- 服务器会自动清理临时文件
- 支持浅克隆以提高速度
- 建议生产环境使用HTTPS