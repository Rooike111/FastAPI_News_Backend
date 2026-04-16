# News Backend

一个基于 FastAPI 构建的新闻资讯后端项目，提供新闻分类、新闻列表、新闻详情、用户注册登录、用户信息维护、新闻收藏、浏览历史等核心能力。项目采用分层结构组织代码，使用异步 SQLAlchemy 连接 MySQL，适合作为 FastAPI 学习项目、课程设计项目，或者前后端分离新闻类应用的后端基础模板。

## 项目简介

本项目是一个典型的新闻类后端服务，主要面向新闻资讯 App / Web 前端提供接口支持。整体采用 `Router -> CRUD -> Model -> Schema -> Utils` 的分层方式组织，职责相对清晰：

- `routers` 负责路由定义和接口入参处理
- `crud` 负责数据库查询与写入逻辑
- `models` 负责 ORM 数据模型定义
- `schemas` 负责接口请求体和响应体结构校验
- `utils` 负责认证、统一响应、异常处理等公共能力
- `config` 负责数据库连接配置

项目当前已经具备一个完整后端服务的基本雏形，适合继续扩展为更完整的新闻系统，例如增加后台管理、内容审核、搜索、推荐、评论等能力。

## 功能特性

- 用户注册与登录
- Token 鉴权与用户身份校验
- 用户信息查询与资料修改
- 用户密码修改
- 新闻分类获取
- 按分类分页获取新闻列表
- 新闻详情查询
- 新闻浏览量累加
- 相关新闻推荐
- 新闻收藏、取消收藏、收藏列表、清空收藏
- 浏览历史新增、分页查询、删除、清空
- 全局异常统一处理
- 统一 JSON 响应结构
- 内置 Swagger 文档能力

## 技术栈

| 类别 | 技术 | 说明 |
| --- | --- | --- |
| Web 框架 | FastAPI | 提供高性能异步接口开发能力 |
| ASGI 服务 | Uvicorn | 用于本地开发和运行 FastAPI 应用 |
| ORM | SQLAlchemy 2.x Async | 使用异步会话访问数据库 |
| 数据库 | MySQL | 业务数据持久化存储 |
| 数据库驱动 | aiomysql | SQLAlchemy 异步 MySQL 驱动 |
| 数据校验 | Pydantic | 请求参数与响应数据模型校验 |
| 密码加密 | Passlib + bcrypt | 用户密码哈希与校验 |
| 中间件 | CORSMiddleware | 处理跨域访问 |
| 接口调试 | `.http` 文件 / Swagger | 用于接口测试与联调 |

## 项目结构

```text
News_backend/
├─ config/
│  └─ db_config.py            # 数据库连接与会话管理
├─ crud/
│  ├─ favorite.py            # 收藏相关数据库操作
│  ├─ history.py             # 浏览历史相关数据库操作
│  ├─ news.py                # 新闻相关数据库操作
│  └─ users.py               # 用户与 token 相关数据库操作
├─ models/
│  ├─ favorite.py            # 收藏表 ORM 模型
│  ├─ history.py             # 历史记录表 ORM 模型
│  ├─ news.py                # 新闻与分类表 ORM 模型
│  └─ users.py               # 用户与用户 token 表 ORM 模型
├─ routers/
│  ├─ favorite.py            # 收藏接口
│  ├─ history.py             # 历史接口
│  ├─ news.py                # 新闻接口
│  └─ users.py               # 用户接口
├─ schemas/
│  ├─ base.py                # 新闻基础响应模型
│  ├─ favorite.py            # 收藏模块请求/响应模型
│  ├─ history.py             # 历史模块请求/响应模型
│  └─ users.py               # 用户模块请求/响应模型
├─ utils/
│  ├─ auth.py                # 当前登录用户依赖
│  ├─ exception.py           # 全局异常处理逻辑
│  ├─ exception_handlers.py  # 异常处理器注册
│  ├─ response.py            # 统一成功响应封装
│  └─ security.py            # 密码加密与校验
├─ main.py                   # FastAPI 应用入口
├─ test_main.http            # 简单接口调试文件
└─ README.md
```

## 核心业务模块

### 1. 新闻模块

新闻模块主要负责对外提供新闻内容读取能力，包括：

- 获取新闻分类列表
- 根据分类分页查询新闻列表
- 根据新闻 ID 获取新闻详情
- 浏览详情时自动增加浏览量
- 返回同分类的相关新闻推荐

这一部分适合作为前端首页、频道页、详情页的数据来源。

### 2. 用户模块

用户模块负责用户身份体系，当前支持：

- 用户注册
- 用户登录
- 获取当前登录用户信息
- 修改个人资料
- 修改密码

项目未使用 JWT，而是采用“数据库持久化 Token”的方式完成鉴权。登录成功后，服务端会生成一个 Token 并写入 `user_token` 表，后续请求通过请求头携带 Token 完成身份识别。

### 3. 收藏模块

收藏模块用于管理用户收藏的新闻，包括：

- 判断某篇新闻是否已收藏
- 添加收藏
- 取消收藏
- 分页获取收藏列表
- 清空全部收藏

适合作为“我的收藏”页面的数据来源。

### 4. 浏览历史模块

浏览历史模块用于记录用户阅读行为，包括：

- 新增浏览记录
- 分页获取浏览历史
- 删除单条浏览记录
- 清空全部浏览记录

如果同一个用户重复浏览同一篇新闻，会更新其浏览时间，便于实现“最近阅读”效果。

## 环境要求

建议使用以下环境：

- Python `3.12.0`
- MySQL `5.7+` 或 `8.x`
- `pip` 或其他 Python 包管理工具
- Windows / macOS / Linux 均可运行

## 安装与启动

### 1. 克隆或进入项目目录

```bash
cd News_backend
```

### 2. 创建虚拟环境

```bash
python -m venv .venv
```

Windows 激活虚拟环境：

```bash
.venv\Scripts\activate
```

macOS / Linux 激活虚拟环境：

```bash
source .venv/bin/activate
```

### 3. 安装依赖

当前项目中提供 `requirements.txt`，可使用以下命令项目进行安装：

```bash
pip install -r requirements.txt
```

### 4. 创建数据库

请先在 MySQL 中创建数据库，例如：

```sql
CREATE DATABASE news_app DEFAULT CHARACTER SET utf8mb4;
```

### 5. 配置数据库连接

项目当前直接在 `config/db_config.py` 中配置数据库连接：

```python
ASYNC_DATABASE_URL = "mysql+aiomysql://root:admin@localhost:3306/news_app?charset=utf8mb4"
```

请根据自己的本地环境修改：

- 数据库用户名
- 数据库密码
- 主机地址
- 端口
- 数据库名

### 6. 准备数据表

当前项目中没有看到 Alembic 迁移脚本，也没有自动建表入口，因此需要你提前准备好 MySQL 表结构，至少包含以下核心表：

- `news_category`
- `news`
- `user`
- `user_token`
- `favorite`
- `history`

如果你后续要长期维护这个项目，建议补充：

- Alembic 数据库迁移
- 初始化 SQL 脚本
- 演示数据脚本

### 7. 启动项目

```bash
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

启动成功后可访问：

- 接口根路径：`http://127.0.0.1:8000/`
- Swagger 文档：`http://127.0.0.1:8000/docs`
- ReDoc 文档：`http://127.0.0.1:8000/redoc`

## 配置说明

### 1. 数据库配置

数据库连接由 `config/db_config.py` 统一管理，使用 `create_async_engine` 创建异步引擎，并通过 `async_sessionmaker` 生成异步会话工厂。

`get_db()` 被设计为 FastAPI 依赖项，路由层可以通过 `Depends(get_db)` 注入数据库会话。

### 2. 跨域配置

项目在 `main.py` 中加入了 CORS 中间件，当前为开发阶段配置：

- 允许所有来源访问
- 允许所有请求方法
- 允许所有请求头

这对前后端联调比较方便，但在生产环境中建议收紧为指定域名。

### 3. Token 认证配置

用户登录或注册成功后，会生成一个随机 Token，并写入 `user_token` 表。当前逻辑中：

- Token 有效期为 7 天
- 需要通过请求头 `Authorization: Bearer <token>` 传递
- 受保护接口会通过依赖注入自动解析当前登录用户

## 接口说明

### 公共接口

| 方法 | 路径 | 说明 | 是否需要认证 |
| --- | --- | --- | --- |
| GET | `/` | 服务健康检查 / 默认欢迎接口 | 否 |
| GET | `/api/news/categories` | 获取新闻分类列表 | 否 |
| GET | `/api/news/list` | 获取指定分类的新闻分页列表 | 否 |
| GET | `/api/news/detail` | 获取新闻详情并增加浏览量 | 否 |
| POST | `/api/user/register` | 用户注册 | 否 |
| POST | `/api/user/login` | 用户登录 | 否 |

### 用户接口

| 方法 | 路径 | 说明 | 是否需要认证 |
| --- | --- | --- | --- |
| GET | `/api/user/info` | 获取当前用户信息 | 是 |
| PUT | `/api/user/update` | 更新用户资料 | 是 |
| PUT | `/api/user/password` | 修改当前用户密码 | 是 |

### 收藏接口

| 方法 | 路径 | 说明 | 是否需要认证 |
| --- | --- | --- | --- |
| GET | `/api/favorite/check` | 检查新闻是否已收藏 | 是 |
| POST | `/api/favorite/add` | 添加收藏 | 是 |
| DELETE | `/api/favorite/remove` | 取消收藏 | 是 |
| GET | `/api/favorite/list` | 分页获取收藏列表 | 是 |
| DELETE | `/api/favorite/clear` | 清空收藏 | 是 |

### 浏览历史接口

| 方法 | 路径 | 说明 | 是否需要认证 |
| --- | --- | --- | --- |
| POST | `/api/history/add` | 添加浏览历史 | 是 |
| GET | `/api/history/list` | 分页获取浏览历史 | 是 |
| DELETE | `/api/history/delete/{history_id}` | 删除单条浏览历史 | 是 |
| DELETE | `/api/history/clear` | 清空浏览历史 | 是 |

## 常用请求示例

### 1. 用户注册

```http
POST /api/user/register
Content-Type: application/json

{
  "username": "test_user",
  "password": "123456"
}
```

### 2. 用户登录

```http
POST /api/user/login
Content-Type: application/json

{
  "username": "test_user",
  "password": "123456"
}
```

### 3. 获取当前用户信息

```http
GET /api/user/info
Authorization: Bearer your_token_here
```

### 4. 获取新闻列表

```http
GET /api/news/list?categoryId=1&page=1&pageSize=10
```

### 5. 添加收藏

```http
POST /api/favorite/add
Authorization: Bearer your_token_here
Content-Type: application/json

{
  "newsId": 1
}
```

### 6. 添加历史记录

```http
POST /api/history/add
Authorization: Bearer your_token_here
Content-Type: application/json

{
  "newsId": 1
}
```

## 统一响应格式

项目通过 `utils/response.py` 和全局异常处理器统一了响应结构。无论成功还是失败，接口都尽量返回一致格式，便于前端统一处理。

### 成功响应示例

```json
{
  "code": 200,
  "message": "success",
  "data": {}
}
```

### 错误响应示例

```json
{
  "code": 400,
  "message": "请求失败原因说明",
  "data": null
}
```

## 数据库核心表说明

### 1. `news_category`

新闻分类表，主要字段包括：

- `id`：分类 ID
- `name`：分类名称
- `sort_order`：排序值

### 2. `news`

新闻主表，主要字段包括：

- `id`：新闻 ID
- `title`：新闻标题
- `description`：新闻摘要
- `content`：新闻正文
- `image`：封面图地址
- `author`：作者
- `category_id`：所属分类
- `views`：浏览量
- `publish_time`：发布时间
- `created_at` / `updated_at`：创建与更新时间

### 3. `user`

用户表，主要字段包括：

- `id`：用户 ID
- `username`：用户名
- `password`：加密后的密码
- `nickname`：昵称
- `avatar`：头像
- `gender`：性别
- `bio`：个人简介
- `phone`：手机号
- `created_at` / `updated_at`：创建与更新时间

### 4. `user_token`

用户 Token 表，主要字段包括：

- `id`：Token 主键
- `user_id`：关联用户 ID
- `token`：令牌字符串
- `expires_at`：过期时间
- `created_at`：创建时间

### 5. `favorite`

收藏表，主要字段包括：

- `id`：收藏记录 ID
- `user_id`：用户 ID
- `news_id`：新闻 ID
- `created_at`：收藏时间

该表通过联合唯一约束限制同一个用户不能重复收藏同一篇新闻。

### 6. `history`

浏览历史表，主要字段包括：

- `id`：历史记录 ID
- `user_id`：用户 ID
- `news_id`：新闻 ID
- `view_time`：浏览时间

## 认证机制说明

当前项目采用的是“数据库 Token 鉴权”而不是 JWT，整体流程如下：

1. 用户注册或登录成功
2. 服务端生成随机 Token
3. Token 保存到 `user_token` 表，并附带过期时间
4. 客户端在后续请求头中携带 `Authorization: Bearer <token>`
5. 服务端根据 Token 查询用户并完成身份校验

这种方式实现简单、易理解，适合教学和中小项目入门，但在生产场景下通常还会进一步补充：

- JWT 或更标准的认证体系
- 刷新令牌机制
- 多端登录控制
- Token 主动失效与注销机制

## 异常处理机制

项目已经注册了全局异常处理器，主要覆盖：

- `HTTPException`
- `IntegrityError`
- `SQLAlchemyError`
- 其他未捕获异常

这意味着：

- 路由内部可以直接抛出标准异常
- 数据库约束冲突能够统一转为友好的 JSON 响应
- 服务异常可以集中处理，减少重复代码

当前项目中还保留了调试模式开关，会在开发模式下返回更详细的错误信息，方便定位问题。

## 开发协作建议

如果你计划继续维护或协作开发这个项目，建议优先补充以下内容：

- 增加 `requirements.txt` 或 `pyproject.toml`
- 使用 `.env` 管理数据库连接配置
- 引入 Alembic 管理数据库迁移
- 增加初始化建表脚本和测试数据脚本
- 为接口补充单元测试 / 集成测试
- 区分开发环境和生产环境配置
- 收紧生产环境的 CORS 设置
- 增加日志系统与请求链路追踪

## 当前项目适合的使用场景

这个项目比较适合以下用途：

- FastAPI 入门学习
- SQLAlchemy 异步 ORM 练习
- 新闻类前后端分离项目后端模板
- 课程设计 / 毕业设计 / 个人练手项目
- 作为后续扩展后台管理系统的基础工程

## 后续可扩展方向

如果后续继续升级，可以考虑扩展：

- 新闻搜索
- 评论系统
- 点赞系统
- 推荐算法
- 后台管理系统
- 分类管理与内容发布后台
- JWT 登录体系
- Redis 缓存
- Docker 部署
- CI/CD 自动化发布

## 调试方式

项目根目录中提供了一个简单的接口调试文件：

- `test_main.http`

你也可以优先使用 FastAPI 自动生成的 Swagger 文档进行联调：

- `http://127.0.0.1:8000/docs`


