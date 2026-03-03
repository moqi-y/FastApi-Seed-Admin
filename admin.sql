# 用户表
create table sys_user
(
    user_id    INTEGER  not null
        primary key AUTO_INCREMENT COMMENT '用户ID',
    username   VARCHAR(50)  not null COMMENT '登录账号',
    nickname   VARCHAR(200) COMMENT '用户昵称',
    avatar     VARCHAR(500) COMMENT '头像URL',
    password   VARCHAR(255)  not null COMMENT '加密密码',
    email      VARCHAR(100) COMMENT '邮箱地址',
    gender     integer COMMENT '性别：0-未知，1-男，2-女',
    mobile    VARCHAR(20) COMMENT '手机号码',
    status     integer COMMENT '状态：0-禁用，1-启用',
    created_at DATETIME not null COMMENT '创建时间'
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
        primary key AUTO_INCREMENT COMMENT '角色ID',
    role_name   VARCHAR(50)  not null COMMENT '角色名称',
    role_code   VARCHAR(50)  not null COMMENT '角色编码（唯一标识）',
    role_status INTEGER  not null COMMENT '状态：0-禁用，1-启用',
    role_desc   VARCHAR(255)  not null COMMENT '角色描述',
    create_time DATETIME not null COMMENT '创建时间',
    update_time DATETIME not null COMMENT '更新时间'
);

create index ix_sys_role_role_id
    on sys_role (role_id);

INSERT INTO sys_role (role_id, role_name, role_code, role_status, role_desc, create_time, update_time) VALUES (1, '管理员', 'admin', 1, '系统管理员', '2025-07-25 16:08:47.453241', '2025-07-25 16:08:47.453241');
INSERT INTO sys_role (role_id, role_name, role_code, role_status, role_desc, create_time, update_time) VALUES (2, '普通用户', 'user', 1, '系统后台普通用户', '2025-07-30 11:34:51.342767', '2025-07-30 11:34:51.342767');

# 权限表
create table sys_permission
(
    permission_id INTEGER not null
        primary key AUTO_INCREMENT COMMENT '权限ID',
    parent_id     INTEGER not null COMMENT '父级权限ID，0为顶级',
    name          VARCHAR(50) COMMENT '权限名称',
    code          VARCHAR(100) not null COMMENT '权限编码（如：sys:user:add）',
    type          INTEGER not null COMMENT '类型：1-目录，2-菜单，3-按钮/接口',
    path          VARCHAR(200) COMMENT '路由路径',
    icon          VARCHAR(100) COMMENT '图标名称',
    sort          INTEGER not null COMMENT '显示排序',
    status        INTEGER COMMENT '状态：0-禁用，1-启用',
    description   VARCHAR(255) COMMENT '权限描述',
    create_time   DATETIME,
    update_time   DATETIME
);

create index ix_sys_permission_id
    on sys_permission (permission_id);

INSERT INTO sys_permission (permission_id, parent_id, name, code, type, path, icon, sort, status, description, create_time, update_time) VALUES (1, 0, '系统管理', 'sys', 1, '/system', null, 1, null, null, null, null);
INSERT INTO sys_permission (permission_id, parent_id, name, code, type, path, icon, sort, status, description, create_time, update_time) VALUES (2, 1, '用户管理', 'sys:user', 1, '/system/user', null, 10, null, null, null, null);
INSERT INTO sys_permission (permission_id, parent_id, name, code, type, path, icon, sort, status, description, create_time, update_time) VALUES (3, 2, '查询用户', 'sys:user:query', 3, null, null, 1, null, null, null, null);
INSERT INTO sys_permission (permission_id, parent_id, name, code, type, path, icon, sort, status, description, create_time, update_time) VALUES (4, 2, '新增用户', 'sys:user:add', 3, null, null, 2, null, null, null, null);
INSERT INTO sys_permission (permission_id, parent_id, name, code, type, path, icon, sort, status, description, create_time, update_time) VALUES (5, 2, '编辑用户', 'sys:user:edit', 3, null, null, 3, null, null, null, null);
INSERT INTO sys_permission (permission_id, parent_id, name, code, type, path, icon, sort, status, description, create_time, update_time) VALUES (6, 2, '删除用户', 'sys:user:delete', 3, null, null, 4, null, null, null, null);
INSERT INTO sys_permission (permission_id, parent_id, name, code, type, path, icon, sort, status, description, create_time, update_time) VALUES (7, 2, '导出用户', 'sys:user:export', 3, null, null, 5, null, null, null, null);
INSERT INTO sys_permission (permission_id, parent_id, name, code, type, path, icon, sort, status, description, create_time, update_time) VALUES (8, 2, '导入用户', 'sys:user:import', 3, null, null, 6, null, null, null, null);
INSERT INTO sys_permission (permission_id, parent_id, name, code, type, path, icon, sort, status, description, create_time, update_time) VALUES (9, 2, '重置密码', 'sys:user:reset-password', 3, null, null, 7, null, null, null, null);
INSERT INTO sys_permission (permission_id, parent_id, name, code, type, path, icon, sort, status, description, create_time, update_time) VALUES (10, 1, '角色管理', 'sys:role', 1, '/system/role', null, 20, null, null, null, null);
INSERT INTO sys_permission (permission_id, parent_id, name, code, type, path, icon, sort, status, description, create_time, update_time) VALUES (11, 3, '查询角色', 'sys:role:query', 3, null, null, 1, null, null, null, null);
INSERT INTO sys_permission (permission_id, parent_id, name, code, type, path, icon, sort, status, description, create_time, update_time) VALUES (12, 3, '新增角色', 'sys:role:add', 3, null, null, 2, null, null, null, null);
INSERT INTO sys_permission (permission_id, parent_id, name, code, type, path, icon, sort, status, description, create_time, update_time) VALUES (13, 3, '编辑角色', 'sys:role:edit', 3, null, null, 3, null, null, null, null);
INSERT INTO sys_permission (permission_id, parent_id, name, code, type, path, icon, sort, status, description, create_time, update_time) VALUES (14, 3, '删除角色', 'sys:role:delete', 3, null, null, 4, null, null, null, null);

# 角色权限表
create table sys_role_permission
(
    id            INTEGER  not null
        primary key AUTO_INCREMENT,
    role_id       INTEGER  not null
        references sys_role,
    permission_id INTEGER  not null
        references sys_permission (permission_id),
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
        primary key AUTO_INCREMENT COMMENT '关联ID',
    user_id      INTEGER  not null
        COMMENT '角色ID',
    role_id      INTEGER  not null
        COMMENT '权限ID',
    created_at   DATETIME not null,
    updated_at   DATETIME not null
);

INSERT INTO sys_role_user (user_role_id, user_id, role_id, created_at, updated_at) VALUES (1, 1, 1, '2025-07-25 02:14:41.178058', '2025-07-25 02:14:41.178058');


# 系统菜单表
create table sys_menu
(
    id          INTEGER not null
        primary key AUTO_INCREMENT COMMENT '菜单ID',
    parent_id   INTEGER,
    name        VARCHAR(50) not null COMMENT '菜单名称（路由名）',
    path        VARCHAR(200) COMMENT '路由路径',
    component   VARCHAR(200) COMMENT '组件路径',
    redirect    VARCHAR(200) COMMENT '重定向地址',
    icon        VARCHAR(100) COMMENT '图标类名',
    title       VARCHAR(50) COMMENT '显示标题',
    hidden      integer not null,
    keep_alive  INTEGER not null,
    always_show INTEGER not null,
    params      VARCHAR(500) COMMENT '路由参数（JSON格式）',
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
        primary key AUTO_INCREMENT COMMENT '记录ID',
    captcha_key    VARCHAR(100)  not null COMMENT '验证码Key（UUID）',
    captcha_base64 TEXT  not null COMMENT 'Base64图片数据',
    captcha_value  VARCHAR(20)  not null COMMENT '验证码答案',
    expire_time    DATETIME not null COMMENT '过期时间',
    create_time    DATETIME not null COMMENT '创建时间'
);

create index ix_captcha_captcha_key
    on captcha (captcha_key);

# 邮箱验证码临时表
create table email_code
(
    email_id    INTEGER  not null
        primary key AUTO_INCREMENT COMMENT '记录ID',
    email       VARCHAR(100)  not null COMMENT '邮箱地址',
    code        VARCHAR(20)  not null COMMENT '验证码',
    user_id     INTEGER  not null
                COMMENT '关联用户ID',
    expire_time DATETIME not null COMMENT '过期时间',
    create_time DATETIME not null COMMENT '创建时间'
);

create index ix_email_code_email
    on email_code (email);

create index ix_email_code_email_id
    on email_code (email_id);

create index ix_email_code_user_id
    on email_code (user_id);