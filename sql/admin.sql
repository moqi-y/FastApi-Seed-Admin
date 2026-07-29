-- FastAPI Admin initial schema (MySQL 8+)
CREATE DATABASE IF NOT EXISTS `FastApi-Seed-Admin`
  DEFAULT CHARACTER SET utf8mb4
  DEFAULT COLLATE utf8mb4_unicode_ci;
USE `FastApi-Seed-Admin`;

CREATE TABLE sys_user (
  user_id BIGINT PRIMARY KEY AUTO_INCREMENT,
  username VARCHAR(50) NOT NULL UNIQUE,
  nickname VARCHAR(200) NULL,
  gender TINYINT NULL,
  avatar VARCHAR(500) NULL,
  mobile VARCHAR(20) NULL,
  password VARCHAR(255) NOT NULL,
  email VARCHAR(100) NULL,
  created_at DATETIME NOT NULL,
  status TINYINT NOT NULL DEFAULT 1,
  INDEX ix_sys_user_username (username)
);

CREATE TABLE sys_role (
  role_id BIGINT PRIMARY KEY AUTO_INCREMENT,
  name VARCHAR(50) NOT NULL,
  code VARCHAR(50) NOT NULL UNIQUE,
  status TINYINT NOT NULL DEFAULT 1,
  description VARCHAR(255) NULL,
  create_time DATETIME NOT NULL,
  update_time DATETIME NOT NULL
);

CREATE TABLE sys_permission (
  permission_id BIGINT PRIMARY KEY AUTO_INCREMENT,
  parent_id BIGINT NOT NULL DEFAULT 0,
  name VARCHAR(50) NULL,
  code VARCHAR(100) NOT NULL UNIQUE,
  type VARCHAR(10) NOT NULL,
  path VARCHAR(200) NULL,
  icon VARCHAR(100) NULL,
  sort INT NOT NULL DEFAULT 0,
  status TINYINT NOT NULL DEFAULT 1,
  description VARCHAR(255) NULL,
  create_time DATETIME NOT NULL,
  update_time DATETIME NOT NULL
);

CREATE TABLE sys_role_user (
  user_role_id BIGINT PRIMARY KEY AUTO_INCREMENT,
  user_id BIGINT NOT NULL,
  role_id BIGINT NOT NULL,
  created_at DATETIME NOT NULL,
  updated_at DATETIME NOT NULL,
  UNIQUE KEY uk_user_role (user_id, role_id),
  CONSTRAINT fk_role_user_user FOREIGN KEY (user_id) REFERENCES sys_user(user_id),
  CONSTRAINT fk_role_user_role FOREIGN KEY (role_id) REFERENCES sys_role(role_id)
);

CREATE TABLE sys_role_permission (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  role_id BIGINT NOT NULL,
  permission_id BIGINT NOT NULL,
  created_at DATETIME NOT NULL,
  updated_at DATETIME NOT NULL,
  UNIQUE KEY uk_role_permission (role_id, permission_id),
  CONSTRAINT fk_role_permission_role FOREIGN KEY (role_id) REFERENCES sys_role(role_id),
  CONSTRAINT fk_role_permission_permission FOREIGN KEY (permission_id) REFERENCES sys_permission(permission_id)
);

CREATE TABLE sys_menu (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  parent_id BIGINT NULL DEFAULT 0,
  name VARCHAR(50) NOT NULL,
  path VARCHAR(200) NULL,
  component VARCHAR(200) NULL,
  redirect VARCHAR(200) NULL,
  icon VARCHAR(100) NULL,
  title VARCHAR(100) NULL,
  route_name VARCHAR(100) NULL,
  hidden TINYINT NOT NULL DEFAULT 0,
  keep_alive TINYINT NOT NULL DEFAULT 1,
  always_show TINYINT NOT NULL DEFAULT 0,
  params VARCHAR(500) NULL,
  sort INT NOT NULL DEFAULT 0,
  created_at DATETIME NULL,
  updated_at DATETIME NULL,
  is_deleted TINYINT NOT NULL DEFAULT 0
);

CREATE TABLE sys_dict (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  name VARCHAR(100) NOT NULL,
  dict_code VARCHAR(100) NOT NULL UNIQUE,
  remark VARCHAR(255) NULL,
  status TINYINT NOT NULL DEFAULT 1
);

CREATE TABLE sys_dict_data (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  dict_code VARCHAR(100) NOT NULL,
  value VARCHAR(100) NOT NULL,
  label VARCHAR(100) NOT NULL,
  sort INT NOT NULL DEFAULT 0,
  status TINYINT NOT NULL DEFAULT 1,
  tag_type VARCHAR(50) NULL,
  INDEX ix_dict_data_code (dict_code)
);

CREATE TABLE captcha (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  captcha_key VARCHAR(100) NOT NULL,
  captcha_base64 LONGTEXT NOT NULL,
  captcha_value VARCHAR(20) NOT NULL,
  expire_time DATETIME NOT NULL,
  create_time DATETIME NOT NULL,
  INDEX ix_captcha_key (captcha_key)
);

CREATE TABLE email_code (
  email_id BIGINT PRIMARY KEY AUTO_INCREMENT,
  email VARCHAR(100) NOT NULL,
  code VARCHAR(20) NOT NULL,
  user_id BIGINT NOT NULL,
  expire_time DATETIME NOT NULL,
  create_time DATETIME NOT NULL,
  INDEX ix_email_code_email (email),
  CONSTRAINT fk_email_code_user FOREIGN KEY (user_id) REFERENCES sys_user(user_id)
);
