# FastApi-Seed-Admin

> 基于Vue3+FastApi+SQLModel框架的后台管理模板。

## 项目目录说明

> - **web** - Web管理端目录
    >
- **vue3-element-admin** - 基于Vue3和Element Plus的后台管理前端项目目录。
> - **app** - 应用的主目录，包含应用的核心代码和逻辑。
    >
- **main.py** - 应用的入口文件（主程序），包含应用的初始化和启动逻辑。
>  - **dependencies.py** - 应用的依赖管理文件，包含应用的依赖项和配置。
>  - **core** - 核心功能模块，可能包含应用的基础配置和核心逻辑。
>  - **crud** - CRUD（创建、读取、更新、删除）操作模块，包含与数据库交互的基本操作。
>  - **middleware** - 中间件目录，包含处理请求和响应的中间件逻辑。
>  - **models** - 数据模型目录，包含定义数据库模型的 Python 类。
>  - **routers** - 路由目录，包含定义应用的 API 路由和对应的处理函数。
>  - **schemas** - 模式目录，包含 Pydantic 模型，用于数据验证和序列化。
>  - **utils** - 工具函数目录，包含一些辅助函数和实用工具。
>  - **external_services** - 外部服务目录，包含与外部服务交互的代码。
     >
- **file_uploader** - 文件上传目录，包含处理文件上传的代码。
>- **logs** - 日志目录，用于存放应用生成的日志文件。
   >
- **app.log** - 应用的日志文件，记录应用运行时的日志信息。
>- **static** - 静态文件目录，用于存放静态资源，如上传的文件、图片等。
>- **.env** - 环境变量文件，包含配置环境变量如数据库连接字符串等。
>- **FastApi-Seed.db** - 数据库文件，存储应用的数据。
>- **README.md** - 项目的自述文件，包含项目的基本信息和使用说明。
>- **requirements.txt** - 依赖文件，列出项目依赖的 Python 包及其版本。
>- **test_main.http** - HTTP 请求测试文件，包含用于测试 API 的 HTTP 请求样本。

## 下载项目

```bash
# 使用https协议
git clone https://github.com/moqi-y/FastApi-Seed-Admin.git
# 使用ssh协议
git clone git@github.com:moqi-y/FastApi-Seed-Admin.git
```

## 安装依赖

### 服务端：

**Python版本：** `3.10.11`
> 推荐先创建**虚拟环境**，然后在虚拟环境中安装项目依赖和运行项目,避免污染全局环境。                                    
> 创建虚拟环境： `python -m venv venv`       
> 激活虚拟环境： `source venv/bin/activate` (Linux/MacOS) 或 `venv\Scripts\activate` (Windows)              
> 退出虚拟环境： `deactivate`

```bash
# 安装所有依赖包（推荐）
pip install -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com -r requirements.txt
```

### 安装单个依赖包

```bash
# 安装fastapi依赖包    
pip install fastapi -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com
```

其他国内源：

```
清华大学：https://pypi.tuna.tsinghua.edu.cn/simple/          
阿里云：http://mirrors.aliyun.com/pypi/simple/
中国科技大学 https://pypi.mirrors.ustc.edu.cn/simple/
华中理工大学：http://pypi.hustunique.com/
山东理工大学：http://pypi.sdutlinux.org/
豆瓣：http://pypi.douban.com/simple/
```

### Web管理端

**Node.js版本：** `22.21.1`
> 进入`/web/vue3-element-admin`目录，执行以下命令安装依赖包

```bash
# 1. 将npm配置为淘宝镜像源
npm config set registry https://registry.npmmirror.com/
# 2. 查看配置是否生效
npm config get registry
  # -->输出：https://registry.npmmirror.com/即为生效。
# 3. 安装所有依赖包
npm install
# 4. 恢复官方源（可选）
npm config set registry https://registry.npmjs.org/
```

## 配置环境变量

在项目根目录下创建一个名为`.env`的文件，并添加以下内容：

```bash
# 项目配置
APP_NAME="FastApi-Seed"
APP_VERSION="1.0.0"
# True 开发环境，False 生产环境,生产环境下不生成swagger接口文档
APP_DEBUG=True

# 数据库配置
SQL_TYPE="sqlite"  # 填写 mysql 或 sqlite
MYSQL_HOST="127.0.0.1"
MYSQL_PORT="3306"
MYSQL_USER="root"
MYSQL_PASSWORD="123456"
MYSQL_DB="FastApi-Seed"

# jwt加密密钥
JWT_SECRET_KEY="12345678"
# jwt过期时间，单位：分钟。
JWT_EXPIRE_MINUTES=120

# 邮箱配置
# 发送者邮箱
SENDER_EMAIL="moqi201@163.com"
# 发送者邮箱密码/授权码
SENDER_PASSWORD="ABCDXXXXXX"

```

> 注意事项：
> - 生产环境部署时需要将`SQL_TYPE`设置为`mysql`，并配置正确的数据库连接信息。
> - 数据库密码中不要包含`@`字符，否则可能会导致数据库连接失败。
> - `JWT_SECRET_KEY`用于加密jwt，请确保其安全性，不要泄露。
> - `JWT_EXPIRE_MINUTES`用于设置jwt的过期时间，单位为分钟。未设置时默认缺省时间为30分钟
> - `.env`文件中的配置项会在项目启动时自动加载到环境变量中，无需手动设置。

## 数据表创建与数据初始化

```bash
# 用户表
create table sys_user
(
    user_id    INTEGER  not null
        primary key,
    username   VARCHAR  not null,
    nickname   VARCHAR,
    avatar     VARCHAR,
    password   VARCHAR  not null,
    email      VARCHAR,
    created_at DATETIME not null,
    gender     integer,
    phone      VARCHAR,
    status     integer
);

create index ix_sys_user_user_id
    on sys_user (user_id);

create index ix_sys_user_username
    on sys_user (username);

INSERT INTO sys_user (user_id, username, nickname, avatar, password, email, created_at, gender, phone, status) VALUES (1, 'admin', '系统管理员', 'https://foruda.gitee.com/images/1723603502796844527/03cdca2a_716974.gif?imageView2/1/w/80/h/80', '$2b$12$07SliP2LHsdVMlrwzzVYhugm0UmB/xbWK8dqIuEHMFAcxB3Sjdw..', 'example.com', '2025-12-26 17:38:43.247202', 1, '13212345678', 1);

# 角色表
create table sys_role
(
    role_id     INTEGER  not null
        primary key,
    role_name   VARCHAR  not null,
    role_code   VARCHAR  not null,
    role_status INTEGER  not null,
    role_desc   VARCHAR  not null,
    create_time DATETIME not null,
    update_time DATETIME not null
);

create index ix_sys_role_role_id
    on sys_role (role_id);

INSERT INTO sys_role (role_id, role_name, role_code, role_status, role_desc, create_time, update_time) VALUES (1, '管理员', 'admin', 1, '系统管理员', '2025-07-25 16:08:47.453241', '2025-07-25 16:08:47.453241');
INSERT INTO sys_role (role_id, role_name, role_code, role_status, role_desc, create_time, update_time) VALUES (2, '普通用户', 'user', 1, '系统后台普通用户', '2025-07-30 11:34:51.342767', '2025-07-30 11:34:51.342767');

# 权限表
create table sys_permission
(
    permission_id INTEGER not null
        primary key,
    parent_id     INTEGER not null,
    name          VARCHAR,
    code          VARCHAR not null,
    type          INTEGER not null,
    path          VARCHAR,
    icon          VARCHAR,
    sort          INTEGER not null,
    status        INTEGER,
    desc          VARCHAR,
    create_time   DATETIME,
    update_time   DATETIME
);

create index ix_sys_permission_id
    on sys_permission (permission_id);

INSERT INTO sys_permission (permission_id, parent_id, name, code, type, path, icon, sort, status, desc, create_time, update_time) VALUES (1, 0, '系统管理', 'sys', 'M', '/system', null, 1, null, null, null, null);
INSERT INTO sys_permission (permission_id, parent_id, name, code, type, path, icon, sort, status, desc, create_time, update_time) VALUES (2, 1, '用户管理', 'sys:user', 'M', '/system/user', null, 10, null, null, null, null);
INSERT INTO sys_permission (permission_id, parent_id, name, code, type, path, icon, sort, status, desc, create_time, update_time) VALUES (3, 2, '查询用户', 'sys:user:query', 'C', null, null, 1, null, null, null, null);
INSERT INTO sys_permission (permission_id, parent_id, name, code, type, path, icon, sort, status, desc, create_time, update_time) VALUES (4, 2, '新增用户', 'sys:user:add', 'C', null, null, 2, null, null, null, null);
INSERT INTO sys_permission (permission_id, parent_id, name, code, type, path, icon, sort, status, desc, create_time, update_time) VALUES (5, 2, '编辑用户', 'sys:user:edit', 'C', null, null, 3, null, null, null, null);
INSERT INTO sys_permission (permission_id, parent_id, name, code, type, path, icon, sort, status, desc, create_time, update_time) VALUES (6, 2, '删除用户', 'sys:user:delete', 'C', null, null, 4, null, null, null, null);
INSERT INTO sys_permission (permission_id, parent_id, name, code, type, path, icon, sort, status, desc, create_time, update_time) VALUES (7, 2, '导出用户', 'sys:user:export', 'C', null, null, 5, null, null, null, null);
INSERT INTO sys_permission (permission_id, parent_id, name, code, type, path, icon, sort, status, desc, create_time, update_time) VALUES (8, 2, '导入用户', 'sys:user:import', 'C', null, null, 6, null, null, null, null);
INSERT INTO sys_permission (permission_id, parent_id, name, code, type, path, icon, sort, status, desc, create_time, update_time) VALUES (9, 2, '重置密码', 'sys:user:reset-password', 'C', null, null, 7, null, null, null, null);
INSERT INTO sys_permission (permission_id, parent_id, name, code, type, path, icon, sort, status, desc, create_time, update_time) VALUES (10, 1, '角色管理', 'sys:role', 'M', '/system/role', null, 20, null, null, null, null);
INSERT INTO sys_permission (permission_id, parent_id, name, code, type, path, icon, sort, status, desc, create_time, update_time) VALUES (11, 3, '查询角色', 'sys:role:query', 'C', null, null, 1, null, null, null, null);
INSERT INTO sys_permission (permission_id, parent_id, name, code, type, path, icon, sort, status, desc, create_time, update_time) VALUES (12, 3, '新增角色', 'sys:role:add', 'C', null, null, 2, null, null, null, null);
INSERT INTO sys_permission (permission_id, parent_id, name, code, type, path, icon, sort, status, desc, create_time, update_time) VALUES (13, 3, '编辑角色', 'sys:role:edit', 'C', null, null, 3, null, null, null, null);
INSERT INTO sys_permission (permission_id, parent_id, name, code, type, path, icon, sort, status, desc, create_time, update_time) VALUES (14, 3, '删除角色', 'sys:role:delete', 'C', null, null, 4, null, null, null, null);

# 角色权限表
create table sys_role_permission
(
    id            INTEGER  not null
        primary key,
    role_id       INTEGER  not null
        references sys_role,
    permission_id INTEGER  not null
        references sys_permission (id),
    created_at    DATETIME not null,
    updated_at    DATETIME not null
);

create index ix_sys_role_permission_role_id
    on sys_role_permission (role_id);

INSERT INTO sys_role_permission (id, role_id, permission_id, created_at, updated_at) VALUES (1, 1, 1, '2025-07-30 03:03:45', '2025-07-30 03:03:45');
INSERT INTO sys_role_permission (id, role_id, permission_id, created_at, updated_at) VALUES (2, 1, 2, '2025-07-30 03:04:47', '2025-07-30 03:04:47');
INSERT INTO sys_role_permission (id, role_id, permission_id, created_at, updated_at) VALUES (3, 1, 3, '2025-07-30 03:04:47', '2025-07-30 03:04:47');
INSERT INTO sys_role_permission (id, role_id, permission_id, created_at, updated_at) VALUES (4, 1, 4, '2025-07-30 03:04:47', '2025-07-30 03:04:47');
INSERT INTO sys_role_permission (id, role_id, permission_id, created_at, updated_at) VALUES (5, 1, 5, '2025-07-30 03:04:47', '2025-07-30 03:04:47');
INSERT INTO sys_role_permission (id, role_id, permission_id, created_at, updated_at) VALUES (6, 1, 6, '2025-07-30 03:04:47', '2025-07-30 03:04:47');
INSERT INTO sys_role_permission (id, role_id, permission_id, created_at, updated_at) VALUES (7, 1, 7, '2025-07-30 03:04:47', '2025-07-30 03:04:47');
INSERT INTO sys_role_permission (id, role_id, permission_id, created_at, updated_at) VALUES (8, 1, 8, '2025-07-30 03:04:47', '2025-07-30 03:04:47');
INSERT INTO sys_role_permission (id, role_id, permission_id, created_at, updated_at) VALUES (9, 1, 9, '2025-07-30 03:04:47', '2025-07-30 03:04:47');
INSERT INTO sys_role_permission (id, role_id, permission_id, created_at, updated_at) VALUES (10, 1, 10, '2025-07-30 03:04:47', '2025-07-30 03:04:47');
INSERT INTO sys_role_permission (id, role_id, permission_id, created_at, updated_at) VALUES (11, 1, 11, '2025-07-30 03:04:47', '2025-07-30 03:04:47');
INSERT INTO sys_role_permission (id, role_id, permission_id, created_at, updated_at) VALUES (12, 1, 12, '2025-07-30 03:04:47', '2025-07-30 03:04:47');
INSERT INTO sys_role_permission (id, role_id, permission_id, created_at, updated_at) VALUES (13, 1, 13, '2025-07-30 03:04:47', '2025-07-30 03:04:47');
INSERT INTO sys_role_permission (id, role_id, permission_id, created_at, updated_at) VALUES (14, 1, 14, '2025-07-30 03:04:47', '2025-07-30 03:04:47');

# 用户角色表
create table sys_role_user
(
    user_role_id INTEGER  not null
        primary key,
    user_id      INTEGER  not null
        references sys_user,
    role_id      INTEGER  not null
        references sys_role,
    created_at   DATETIME not null,
    updated_at   DATETIME not null
);

INSERT INTO sys_role_user (user_role_id, user_id, role_id, created_at, updated_at) VALUES (1, 1, 1, '2025-07-25 02:14:41.178058', '2025-07-25 02:14:41.178058');

# 系统菜单表
create table sys_menu
(
    id          INTEGER not null
        primary key,
    parent_id   INTEGER,
    name        VARCHAR not null,
    path        VARCHAR,
    component   VARCHAR,
    redirect    VARCHAR,
    icon        VARCHAR,
    title       VARCHAR,
    hidden      integer not null,
    keep_alive  INTEGER not null,
    always_show INTEGER not null,
    params      VARCHAR,
    sort        INTEGER not null,
    created_at  DATETIME,
    updated_at  DATETIME,
    is_deleted  INTEGER
);

INSERT INTO sys_menu (id, parent_id, name, path, component, redirect, icon, title, hidden, keep_alive, always_show, params, sort, created_at, updated_at, is_deleted) VALUES (1, 0, '/system', '/system', 'Layout', '/system/user', 'system', '系统管理', 0, 0, 0, null, 1, null, null, null);
INSERT INTO sys_menu (id, parent_id, name, path, component, redirect, icon, title, hidden, keep_alive, always_show, params, sort, created_at, updated_at, is_deleted) VALUES (2, 1, 'User', '/user', 'system/user/index', null, 'el-icon-User', '用户管理', 0, 1, 0, null, 1, null, null, null);
INSERT INTO sys_menu (id, parent_id, name, path, component, redirect, icon, title, hidden, keep_alive, always_show, params, sort, created_at, updated_at, is_deleted) VALUES (3, 1, 'Role', '/role', 'system/role/index', null, 'role', '角色管理', 0, 1, 0, null, 2, null, null, null);
INSERT INTO sys_menu (id, parent_id, name, path, component, redirect, icon, title, hidden, keep_alive, always_show, params, sort, created_at, updated_at, is_deleted) VALUES (4, 1, 'SysMenu', '/menu', 'system/menu/index', null, 'menu', '菜单管理', 0, 1, 0, null, 3, null, null, null);
INSERT INTO sys_menu (id, parent_id, name, path, component, redirect, icon, title, hidden, keep_alive, always_show, params, sort, created_at, updated_at, is_deleted) VALUES (5, 1, 'Dept', '/dept', 'system/dept/index', null, 'tree', '部门管理', 0, 1, 0, null, 4, null, null, null);
INSERT INTO sys_menu (id, parent_id, name, path, component, redirect, icon, title, hidden, keep_alive, always_show, params, sort, created_at, updated_at, is_deleted) VALUES (6, 1, 'Dict', '/dict', 'system/dict/index', null, 'dict', '字典管理', 0, 1, 0, null, 5, null, null, null);
INSERT INTO sys_menu (id, parent_id, name, path, component, redirect, icon, title, hidden, keep_alive, always_show, params, sort, created_at, updated_at, is_deleted) VALUES (7, 1, 'Log', '/log', 'system/log/index', null, 'document', '系统日志', 0, 1, 0, null, 6, null, null, null);
INSERT INTO sys_menu (id, parent_id, name, path, component, redirect, icon, title, hidden, keep_alive, always_show, params, sort, created_at, updated_at, is_deleted) VALUES (8, 1, 'Config', '/config', 'system/config/index', null, 'setting', '系统配置', 0, 1, 0, null, 7, null, null, null);
INSERT INTO sys_menu (id, parent_id, name, path, component, redirect, icon, title, hidden, keep_alive, always_show, params, sort, created_at, updated_at, is_deleted) VALUES (9, 1, 'Notice', '/notice', 'system/notice/index', null, '', '通知公告', 0, 1, 0, null, 8, null, null, null);
INSERT INTO sys_menu (id, parent_id, name, path, component, redirect, icon, title, hidden, keep_alive, always_show, params, sort, created_at, updated_at, is_deleted) VALUES (10, 0, '/codegen', '/codegen', 'Layout', null, 'menu', '系统工具', 0, 0, 0, null, 2, null, null, null);
INSERT INTO sys_menu (id, parent_id, name, path, component, redirect, icon, title, hidden, keep_alive, always_show, params, sort, created_at, updated_at, is_deleted) VALUES (11, 10, 'Codegen', '/codegen', 'codegen/index', null, 'code', '代码生成', 0, 1, 0, null, 1, null, null, null);

# 验证码临时表
create table captcha
(
    id             INTEGER  not null
        primary key,
    captcha_key    VARCHAR  not null,
    captcha_base64 VARCHAR  not null,
    captcha_value  VARCHAR  not null,
    expire_time    DATETIME not null,
    create_time    DATETIME not null
);

create index ix_captcha_captcha_key
    on captcha (captcha_key);

# 邮箱验证码临时表
create table email_code
(
    email_id    INTEGER  not null
        primary key,
    email       VARCHAR  not null,
    code        VARCHAR  not null,
    user_id     INTEGER  not null
        references sys_user,
    expire_time DATETIME not null,
    create_time DATETIME not null
);

create index ix_email_code_email
    on email_code (email);

create index ix_email_code_email_id
    on email_code (email_id);

create index ix_email_code_user_id
    on email_code (user_id);
```

## 启动项目

```bash
# 启动服务端
uvicorn app.main:app --port 8080
# 启动Web客户端
cd /web/vue3-element-admin  
npm run dev
```
## 预览
- http://localhost:3000 | http://127.0.0.1:3000
> 管理员默认账号： admin  密码：123456

### OpenAPI 在线接口文档

- http://localhost:8080/docs | http://127.0.0.1:8080/redoc
- http://localhost:8080/redoc | http://127.0.0.1:8080/redoc

## 部署项目

```bash
# 复制项目到部署目录
cp -r FastApi-Seed-Admin /data/wwwroot/FastApi-Seed-Admin
# 进入项目目录
cd /data/wwwroot/FastApi-Seed-Admin
# 创建虚拟环境 myenv,创建成功后可在当前目录下看到此目录
python3.10 -m venv myenv
# 激活虚拟环境
source myenv/bin/activate
# 安装依赖文件
pip install -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com -r requirements.txt
# 启动运行并保持后台
nohup uvicorn app.main:app --host 0.0.0.0 --port 8080 &

# 前端项目包打包部署
cd /data/wwwroot/FastApi-Seed-Admin/web/vue3-element-admin
npm run build
# 将打包后的文件复制到静态目录
cp -r dist/* /data/wwwroot/FastApi-Seed-Admin/web
# 重启服务
killall uvicorn
nohup uvicorn app.main:app --host 0.0.0.0 --port 8080 &
```

> 多工作进程模式
> ```bash
> # 使用 --workers 命令行选项来启动多个工作进程
> uvicorn main:app --host 0.0.0.0 --port 8080 --workers 4
> ```

## 其他

### 使用 SSL 证书

```bash
# 生成证书（这种方式生成的自有证书不建议在生产环境使用）
openssl req -x509 -newkey rsa:4096 -nodes -keyout key.pem -out cert.pem -days 365
# 启动项目
uvicorn app.main:app --host 0.0.0.0 --port 8080 --ssl-keyfile key.pem --ssl-certfile cert.pem
```

### 使用 Docker 部署（仅供参考）

1. Dockerfile:

```bash
# 使用官方 Python 3.10 精简镜像
FROM python:3.10-slim

WORKDIR /code

# 1. 先复制依赖文件，利用缓存
COPY requirements.txt .

# 2. 临时把 pip 源改成清华源（如访问失败可换回阿里云）
RUN pip install --no-cache-dir \
    -i https://pypi.tuna.tsinghua.edu.cn/simple/ \
    --trusted-host pypi.tuna.tsinghua.edu.cn \
    --upgrade pip && \
    pip install --no-cache-dir \
    -i https://pypi.tuna.tsinghua.edu.cn/simple/ \
    --trusted-host pypi.tuna.tsinghua.edu.cn \
    -r requirements.txt

# 3. 复制其余源码
COPY ./app ./app

EXPOSE 8080 3000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
```

2. 构建镜像:

```bash
docker build -t FastApi-Seed-Admin .
```

3. 运行容器:

```bash
# 查看镜像
docker images
# 运行容器
docker run -itd -p 8080:8080 -p 3000:3000 --name My-FastApi-Seed-Admin FastApi-Seed-Admin:latest
```

### JWT随机密钥生成

使用以下命令，生成安全的随机密钥,然后，把生成的密钥复制到变量`JWT_SECRET_KEY`。

```bash
openssl rand -hex 32
```

### requirements.txt

```text
fastapi~=0.116.0
uvicorn~=0.35.0
pydantic~=2.11.7
sqlmodel~=0.0.24
passlib~=1.7.4
python-multipart~=0.0.20
python-dotenv~=1.1.1
python-jose[cryptography]~=3.5.0
python-jose~=3.5.0
captcha~=0.7.1
httpx~=0.28.1
pymysql~=1.1.1
```

> #### `requirements.txt`文件中，`fastapi`和`uvicorn`是必须的，其他依赖根据项目需求添加。
> `fastapi`是用于构建API的框架。    
> `uvicorn`是用于运行FastAPI应用的ASGI服务器。
> `pydantic`是用于数据验证和设置管理的库。         
> `sqlmodel`是用于ORM的库。       
> `passlib`是用于密码哈希的库。       
> `python-multipart`是用于处理multipart/form-data的库。     
> `python-dotenv`是用于加载环境变量的库。           
> `python-jose[cryptography]`是用于处理JWT的库。            
> `python-jose`是用于处理JWT的库。           
> `captcha` 是用于生成验证码的库。         
> `httpx` 是用于发送HTTP请求的库。        
> `pymysql` 是用于连接MySQL数据库的库。

### 参考文档

- [FastAPI 官方文档](https://fastapi.tiangolo.com/zh/)
- [SQLModel 官方文档](https://sqlmodel.fastapi.org.cn/)
- [vue3-element-admin 官方文档](https://www.youlai.tech/vue-docs/guide/quick-start.html)
- [接口文档](https://s.apifox.cn/195e783f-4d85-4235-a038-eec696de4ea5)