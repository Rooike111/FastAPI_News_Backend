# News Backend

基于 FastAPI 构建的新闻资讯后端项目，提供新闻分类、新闻列表、新闻详情、用户注册登录、个人信息维护、新闻收藏、浏览历史等核心能力。项目当前已经补充了 Redis 缓存、接口规范文档和数据库初始化脚本，适合作为 FastAPI 学习项目、课程设计项目，或新闻类前后端分离应用的后端基础模板。

## 项目概览

- 异步后端：FastAPI + SQLAlchemy Async + aiomysql
- 数据持久化：MySQL
- 缓存层：Redis
- 鉴权方式：数据库持久化 Token
- 文档资产：
  - [API接口规范文档.md](./API接口规范文档.md)
  - [database.sql](./database.sql)
  - Swagger：`/docs`
  - ReDoc：`/redoc`

## 当前功能

- 用户注册、登录
- 用户信息查询与更新
- 用户密码修改
- 新闻分类查询
- 按分类分页查询新闻列表
- 新闻详情查询
- 新闻浏览量累加
- 同分类热门相关新闻推荐
- 新闻收藏状态查询、添加、取消、清空、分页列表
- 浏览历史新增、分页查询、删除、清空
- 全局异常处理
- 统一 JSON 响应结构
- FastAPI 自动生成接口文档

## 技术栈

| 类别 | 技术 | 说明 |
| --- | --- | --- |
| Web 框架 | FastAPI | 异步接口开发 |
| ASGI 服务 | Uvicorn | 本地开发与运行 |
| ORM | SQLAlchemy 2.x Async | 异步数据库访问 |
| 数据库 | MySQL | 业务数据持久化 |
| 数据库驱动 | aiomysql | MySQL 异步驱动 |
| 缓存 | Redis + `redis.asyncio` | 新闻分类与新闻列表缓存 |
| 数据校验 | Pydantic v2 | 请求与响应模型校验 |
| 密码加密 | Passlib + bcrypt | 用户密码哈希与校验 |
| 中间件 | CORSMiddleware | 处理跨域请求 |

## 项目结构

```text
News_backend/
├── main.py                    # FastAPI 应用入口
├── config/
│   ├── db_config.py           # MySQL 异步连接配置
│   └── cache_conf.py          # Redis 连接与基础缓存方法
├── routers/
│   ├── news.py                # 新闻接口
│   ├── users.py               # 用户接口
│   ├── favorite.py            # 收藏接口
│   └── history.py             # 历史接口
├── crud/
│   ├── news.py                # 纯数据库新闻查询
│   ├── news_cache.py          # 带 Redis 的新闻查询
│   ├── users.py               # 用户与 Token 逻辑
│   ├── favorite.py            # 收藏逻辑
│   └── history.py             # 浏览历史逻辑
├── cache/
│   └── news_cache.py          # 新闻缓存 key 设计与读写封装
├── models/                    # SQLAlchemy ORM 模型
├── schemas/                   # Pydantic 请求/响应模型
├── utils/                     # 鉴权、异常处理、统一响应等
├── database.sql               # 数据库建库、建表、索引、初始化数据脚本
├── API接口规范文档.md          # 离线接口规范文档
├── requirements.txt           # Python 依赖
└── xwzx-news/                 # 示例前端工程
```

## Redis 缓存与旁路同步策略

项目当前采用 Redis 旁路缓存（Cache Aside）策略，数据库仍然是唯一数据源。

### 读取流程

1. 先查 Redis。
2. 缓存命中，直接返回缓存结果。
3. 缓存未命中，回源 MySQL。
4. 将查询结果序列化后写回 Redis。
5. 返回数据库结果。

### 当前已接入缓存的接口

- `GET /api/news/categories`
- `GET /api/news/list`

### 当前缓存 key 设计

- 新闻分类：`news:categories`
- 新闻列表：`news_list:{category_id}:{page}:{size}`

### 当前缓存过期时间

- 新闻分类：`7200` 秒
- 新闻列表：`1800` 秒

### 同步策略说明

- 新闻详情接口仍然以数据库为准，浏览量更新直接写入 MySQL。
- Redis 只承担读优化角色，不作为业务真源。
- 当前没有新闻后台写接口，因此缓存一致性主要依赖“数据库主写 + 缓存过期后回填”的方式完成。

## 运行环境

建议使用以下环境：

- Python `3.12+`
- MySQL `5.7+` 或 `8.x`
- Redis `6.x+`
- Windows / macOS / Linux

## 快速开始

### 1. 克隆并进入项目

```bash
cd News_backend
```

### 2. 创建虚拟环境

```bash
python -m venv .venv
```

Windows：

```bash
.venv\Scripts\activate
```

macOS / Linux：

```bash
source .venv/bin/activate
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

由于项目已接入 `redis.asyncio`，如果你的 `requirements.txt` 还未补充 Redis 客户端，请额外执行：

```bash
pip install redis
```

### 4. 启动 MySQL 与 Redis

请确保本机服务可用：

- MySQL：默认 `localhost:3306`
- Redis：默认 `localhost:6379`

### 5. 初始化数据库

项目已提供完整的建库、建表、索引和初始化数据脚本，可直接导入：

```bash
mysql -u root -p < database.sql
```

说明：

- `database.sql` 内已包含 `CREATE DATABASE IF NOT EXISTS news_app`
- 脚本内包含默认分类、新闻测试数据
- 脚本内还包含测试用户记录，但密码保存的是哈希值；如需直接登录，建议重新注册一个账号

### 6. 修改本地配置

数据库连接配置位于 `config/db_config.py`：

```python
ASYNC_DATABASE_URL = "mysql+aiomysql://root:admin@localhost:3306/news_app?charset=utf8mb4"
```

Redis 配置位于 `config/cache_conf.py`：

```python
REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_DB = 0
```

项目当前使用硬编码配置，尚未接入 `.env`，请根据本地环境直接修改上述文件。

### 7. 启动服务

```bash
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

启动成功后可访问：

- 根路径：`http://127.0.0.1:8000/`
- Swagger：`http://127.0.0.1:8000/docs`
- ReDoc：`http://127.0.0.1:8000/redoc`

## 接口文档

项目目前有两套文档入口：

### 1. 仓库内离线文档

- [API接口规范文档.md](./API接口规范文档.md)

适合做接口评审、离线查阅、联调说明。

### 2. FastAPI 自动文档

- Swagger：`/docs`
- ReDoc：`/redoc`

适合直接调试接口、查看参数模型和响应结构。

## 鉴权说明

项目当前采用数据库 Token 鉴权，而不是 JWT。

### 鉴权流程

1. 用户注册或登录成功后，服务端生成 Token。
2. Token 持久化到 `user_token` 表。
3. Token 默认有效期为 7 天。
4. 受保护接口通过请求头中的 `Authorization` 字段识别当前用户。

### 当前请求头写法

```http
Authorization: your_token_here
```

说明：

- 当前代码中的鉴权解析更贴近“直接传 token”模式。
- 如果你想改成标准 `Bearer <token>` 写法，需要同步调整 `utils/auth.py` 的解析逻辑。

## 接口总览

### 公共与新闻接口

| 方法 | 路径 | 说明 | 是否鉴权 |
| --- | --- | --- | --- |
| GET | `/` | 服务欢迎页 / 健康检查 | 否 |
| GET | `/api/news/categories` | 获取新闻分类列表 | 否 |
| GET | `/api/news/list` | 按分类分页获取新闻列表 | 否 |
| GET | `/api/news/detail` | 获取新闻详情与相关新闻 | 否 |

### 用户接口

| 方法 | 路径 | 说明 | 是否鉴权 |
| --- | --- | --- | --- |
| POST | `/api/user/register` | 用户注册 | 否 |
| POST | `/api/user/login` | 用户登录 | 否 |
| GET | `/api/user/info` | 获取当前用户信息 | 是 |
| PUT | `/api/user/update` | 更新当前用户资料 | 是 |
| PUT | `/api/user/password` | 修改当前用户密码 | 是 |

### 收藏接口

| 方法 | 路径 | 说明 | 是否鉴权 |
| --- | --- | --- | --- |
| GET | `/api/favorite/check` | 查询新闻是否已收藏 | 是 |
| POST | `/api/favorite/add` | 添加收藏 | 是 |
| DELETE | `/api/favorite/remove` | 取消收藏 | 是 |
| GET | `/api/favorite/list` | 分页获取收藏列表 | 是 |
| DELETE | `/api/favorite/clear` | 清空收藏 | 是 |

### 浏览历史接口

| 方法 | 路径 | 说明 | 是否鉴权 |
| --- | --- | --- | --- |
| POST | `/api/history/add` | 添加浏览历史 | 是 |
| GET | `/api/history/list` | 分页获取浏览历史 | 是 |
| DELETE | `/api/history/delete/{history_id}` | 删除单条浏览历史 | 是 |
| DELETE | `/api/history/clear` | 清空浏览历史 | 是 |

## 常用请求示例

### 注册

```http
POST /api/user/register
Content-Type: application/json

{
  "username": "test_user",
  "password": "123456"
}
```

### 登录

```http
POST /api/user/login
Content-Type: application/json

{
  "username": "test_user",
  "password": "123456"
}
```

### 获取新闻列表

```http
GET /api/news/list?categoryId=1&page=1&pageSize=10
```

### 获取用户信息

```http
GET /api/user/info
Authorization: your_token_here
```

### 添加收藏

```http
POST /api/favorite/add
Authorization: your_token_here
Content-Type: application/json

{
  "newsId": 1
}
```

### 添加浏览历史

```http
POST /api/history/add
Authorization: your_token_here
Content-Type: application/json

{
  "newsId": 1
}
```

## 统一响应格式

项目通过统一响应封装与全局异常处理，接口默认返回以下结构：

### 成功响应

```json
{
  "code": 200,
  "message": "success",
  "data": {}
}
```

### 失败响应

```json
{
  "code": 400,
  "message": "错误说明",
  "data": null
}
```

## 数据库说明

### 核心业务表

| 表名 | 说明 |
| --- | --- |
| `user` | 用户信息 |
| `user_token` | 用户登录令牌 |
| `news_category` | 新闻分类 |
| `news` | 新闻主表 |
| `favorite` | 收藏记录 |
| `history` | 浏览历史 |

### 扩展预留表

| 表名 | 说明 |
| --- | --- |
| `related_news` | 相关新闻关联表 |
| `ai_chat` | AI 聊天记录表 |

说明：

- `database.sql` 已经包含完整建表语句、索引和初始化数据。
- 当前 FastAPI 已挂载的接口主要围绕 `news`、`user`、`favorite`、`history` 四个模块。
- `related_news` 与 `ai_chat` 已在数据库脚本中预留，但当前后端尚未挂载对应 API。

## 开发说明

### CORS

项目当前在开发环境中允许所有源跨域访问，方便前后端联调；如果用于生产环境，建议将允许域名收紧到指定来源。

### 数据库迁移

当前项目使用 `database.sql` 完成初始化，尚未接入 Alembic。如果后续需要长期维护，建议补充数据库迁移管理。

### 配置管理

当前数据库和 Redis 配置均写在 Python 文件中，建议后续迁移到 `.env` 或配置中心。

## 后续可扩展方向

- 后台新闻管理
- 新闻搜索
- 评论系统
- 点赞系统
- 更精细的缓存失效策略
- JWT 或刷新令牌机制
- Alembic 数据库迁移
- Docker 部署
- 单元测试与集成测试
- CI/CD 自动化发布
