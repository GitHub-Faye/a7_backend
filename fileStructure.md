# A7_Backend 项目文件结构

## 项目概述

A7_Backend 是一个基于 Django 的教育 AI 助手系统后端，提供教学内容生成、考核题目管理、学情数据分析等功能。该系统通过集成大模型 API，为教师提供智能备课工具，为学生提供个性化学习支持，为管理员提供数据可视化和用户管理功能。

## 目录结构

```
a7_backend/
├── .roo/                    # Roo 工具配置目录
│   ├── rules/               # Roo 规则
│   ├── rules-architect/     # 架构相关规则
│   ├── rules-ask/           # 询问相关规则
│   ├── rules-boomerang/     # Boomerang 工具规则
│   ├── rules-code/          # 代码相关规则
│   ├── rules-debug/         # 调试相关规则
│   └── rules-test/          # 测试相关规则
├── a7/                      # 主要应用目录
│   ├── a7/                  # 项目核心配置
│   │   ├── __init__.py      # Python 包初始化文件
│   │   ├── asgi.py          # ASGI 配置
│   │   ├── settings.py      # Django 项目设置
│   │   ├── urls.py          # URL 路由配置
│   │   └── wsgi.py          # WSGI 配置
│   ├── ai_services/         # AI 服务模块
│   │   ├── __init__.py
│   │   ├── admin.py         # Django 管理界面配置
│   │   ├── apps.py          # 应用配置
│   │   ├── migrations/      # 数据库迁移文件
│   │   ├── models.py        # 数据模型定义
│   │   ├── tests.py         # 测试文件
│   │   └── views.py         # 视图和 API 端点
│   ├── analytics/           # 数据分析模块
│   │   ├── migrations/      # 数据库迁移文件
│   │   └── ...              # 类似于其他模块的文件结构
│   ├── courses/             # 课程管理模块
│   │   ├── migrations/      # 数据库迁移文件
│   │   └── ...              # 类似于其他模块的文件结构
│   ├── resources/           # 资源管理模块
│   │   ├── migrations/      # 数据库迁移文件
│   │   └── ...              # 类似于其他模块的文件结构
│   ├── users/               # 用户管理模块
│   │   ├── __init__.py
│   │   ├── admin.py         # 用户管理界面配置
│   │   ├── apps.py          # 应用配置
│   │   ├── migrations/      # 数据库迁移文件
│   │   ├── models.py        # 用户数据模型
│   │   ├── tests.py         # 用户功能测试
│   │   └── views.py         # 用户相关视图和 API
│   ├── db.sqlite3           # SQLite 数据库文件
│   └── manage.py            # Django 项目管理脚本
├── scripts/                 # 工具脚本目录
│   ├── example_prd.txt      # 示例需求文档
│   └── task-complexity-report.json # 任务复杂度分析报告
├── tasks/                   # 任务管理目录
│   ├── task_001.txt         # 任务详情文件
│   ├── task_002.txt         # 任务详情文件
│   └── ...
│   ├── tasks.json           # 任务定义数据
│   └── tasks.json.bak       # 任务文件备份
├── .env.example             # 环境变量示例文件
├── .gitignore               # Git 忽略文件配置
├── .roomodes                # Roo 模式配置文件
├── .taskmasterconfig        # TaskMaster 配置文件
├── .windsurfrules           # Windsurf 规则配置
├── a7_backend.code-workspace # VS Code 工作区配置
├── library.md               # 项目库文档
└── prd.txt                  # 产品需求文档
```

## 文件和目录用途说明

### 核心应用文件

- **a7/a7/**：Django 项目的核心配置目录
  - `settings.py`：项目的全局配置，包括数据库、中间件、安装的应用等
  - `urls.py`：URL 路由表，定义 API 端点和视图的映射关系
  - `asgi.py` & `wsgi.py`：应用服务器接口，用于部署

- **a7/manage.py**：Django 命令行工具，用于运行服务器、数据库迁移等操作

- **a7/db.sqlite3**：SQLite 数据库文件，存储应用数据

### 应用模块

- **a7/ai_services/**：AI 服务集成模块
  - `models.py`：定义 AI 交互和缓存数据模型
  - `views.py`：实现 AI 相关 API 端点

- **a7/users/**：用户管理模块
  - `models.py`：扩展 Django 用户模型
  - `admin.py`：配置用户管理界面
  - `views.py`：用户相关 API 实现

- **a7/courses/**：课程管理模块，处理课程、章节、知识点等

- **a7/resources/**：资源管理模块，处理讲义、练习、考核等教育资源

- **a7/analytics/**：数据分析模块，处理学习数据和统计分析

### 配置文件

- **.taskmasterconfig**：TaskMaster AI 工具配置，定义使用的 AI 模型和参数

- **.env.example**：环境变量模板，包含必要的 API 密钥和配置参数

- **.gitignore**：定义 Git 版本控制应忽略的文件和目录

### 任务管理

- **tasks/tasks.json**：定义项目任务、依赖关系和状态

- **tasks/task_XXX.txt**：各个任务的详细描述文件

- **scripts/task-complexity-report.json**：任务复杂度分析报告

### 项目文档

- **prd.txt**：详细的产品需求文档，描述系统功能和数据模型

- **library.md**：项目使用的库和依赖说明

## 关键文件之间的关系

1. **配置与执行流程**
   - `a7/a7/settings.py` 定义全局配置
   - `a7/a7/urls.py` 根据配置路由请求到各模块的视图
   - 各模块的 `views.py` 处理请求并与 `models.py` 交互
   - `manage.py` 作为入口点执行各种 Django 命令

2. **数据模型关系**
   - `users/models.py` 定义基础用户模型
   - `courses/models.py` 定义课程相关模型，关联用户模型
   - `resources/models.py` 定义资源模型，关联课程模型
   - `analytics/models.py` 定义分析模型，关联用户和课程模型
   - `ai_services/models.py` 定义 AI 交互模型，关联用户和资源模型

3. **AI 服务集成**
   - `ai_services/models.py` 定义 AI 交互记录和缓存
   - `ai_services/utils.py` 实现 AI API 调用和缓存逻辑
   - `ai_services/views.py` 暴露 AI 服务 API 端点

4. **任务管理与开发流程**
   - `tasks/tasks.json` 定义开发任务和进度
   - `tasks/task_XXX.txt` 详细描述各任务
   - `.taskmasterconfig` 配置 TaskMaster AI 工具

## 目录组织逻辑

1. **Django 应用结构**
   - 遵循 Django 标准应用结构，每个功能模块作为一个独立应用
   - 每个应用包含 `models.py`、`views.py`、`admin.py` 等标准文件
   - 共享配置放在 `a7/a7/` 目录中

2. **模块化设计**
   - 按功能领域划分模块：用户管理、课程管理、资源管理、AI 服务、数据分析
   - 每个模块自包含，具有明确的责任界限
   - 模块间通过模型关系和 API 调用交互

3. **开发工具组织**
   - 开发工具配置文件放在项目根目录
   - 开发任务和文档放在专用目录（`tasks/`、`scripts/`）
   - AI 工具规则放在 `.roo/` 目录下

## 命名约定

1. **文件命名**
   - Django 应用遵循小写字母，单数形式：`users`、`courses`
   - 配置文件使用点前缀：`.gitignore`、`.taskmasterconfig`
   - 任务文件使用下划线加序号格式：`task_001.txt`

2. **模型命名**
   - 模型类使用 PascalCase（大驼峰）：`User`、`Course`、`Resource`
   - 字段名使用 snake_case（下划线）：`created_at`、`knowledge_points`
   - 关联字段名反映实体关系：`course.chapters`（一对多）

3. **API 端点命名**
   - RESTful 风格，使用复数名词：`/api/courses/`
   - 资源操作通过 HTTP 方法表示：GET、POST、PUT、DELETE
   - 子资源使用嵌套路径：`/api/courses/{id}/chapters/`
   - 操作性 API 使用连字符命名：`/api/ai/teaching-design/`

4. **Django 应用命名**
   - 功能相关：`courses`、`resources`
   - 角色相关：`users`
   - 服务相关：`ai_services`、`analytics`

## 数据库迁移管理

- 每个应用有独立的 `migrations/` 目录管理其模型变更
- 迁移文件按顺序编号，通过 `manage.py migrate` 应用
- 新模型和字段变更通过 `manage.py makemigrations` 生成迁移文件

## 配置管理

- 敏感配置（API 密钥等）通过环境变量提供，参考 `.env.example`
- 项目固定配置在 `settings.py` 中定义
- AI 工具配置在 `.taskmasterconfig` 中管理
- 开发工具配置在各自的配置文件中（`.roomodes`、`.windsurfrules`） 