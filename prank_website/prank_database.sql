-- 整蛊网站数据库初始化脚本

-- 创建数据库（如果不存在）
CREATE DATABASE IF NOT EXISTS prank_db;

-- 使用创建的数据库
USE prank_db;

-- 创建用户选择记录表
CREATE TABLE IF NOT EXISTS user_choices (
    id INT AUTO_INCREMENT PRIMARY KEY,
    choice VARCHAR(20) NOT NULL,
    ip_address VARCHAR(50),
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 添加一些测试数据（可选）
INSERT INTO user_choices (choice, ip_address, user_agent) VALUES
('option1', '127.0.0.1', 'Mozilla/5.0 Test Browser'),
('option2', '127.0.0.1', 'Mozilla/5.0 Test Browser')
ON DUPLICATE KEY UPDATE choice = choice;

-- 显示创建的表
SHOW TABLES;

-- 显示表结构
DESCRIBE user_choices;

-- 查询测试数据
SELECT * FROM user_choices;

SELECT '数据库初始化完成！' AS status;