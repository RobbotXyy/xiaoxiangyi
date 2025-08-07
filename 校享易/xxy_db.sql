-- ===============================================================
-- 数据库设计sql版本: `xxy_db` (校享易)
-- ===============================================================

-- 创建数据库 (如果不存在)
CREATE DATABASE IF NOT EXISTS `xxy_db` 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

-- 使用该数据库
USE `xxy_db`;


-- ===============================================================
-- 表: `USERS` (用户表)
-- ===============================================================
CREATE TABLE IF NOT EXISTS `USERS` (
    `user_id` INT AUTO_INCREMENT PRIMARY KEY,
    `username` VARCHAR(50) NOT NULL UNIQUE,
    `password_hash` VARCHAR(255) NOT NULL,
    `email` VARCHAR(100) NOT NULL UNIQUE,
    `school_name` VARCHAR(100) NOT NULL COMMENT '新增：院校名称',  -- <--- 这里是新增的列
    `profile` TEXT NULL COMMENT '个人简介',
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户信息表';


-- ===============================================================
-- 表: `CATEGORIES` (物品分类表)
-- ===============================================================
CREATE TABLE IF NOT EXISTS `CATEGORIES` (
    `category_id` INT AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(50) NOT NULL UNIQUE COMMENT '分类名称',
    `description` VARCHAR(255) NULL COMMENT '分类描述'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='物品分类表';


-- ===============================================================
-- 表: `ITEMS` (闲置物品表)
-- ===============================================================
CREATE TABLE IF NOT EXISTS `ITEMS` (
    `item_id` INT AUTO_INCREMENT PRIMARY KEY,
    `owner_id` INT NOT NULL COMMENT '发布者ID (外键)',
    `category_id` INT NOT NULL COMMENT '分类ID (外键)',
    `title` VARCHAR(100) NOT NULL COMMENT '物品标题',
    `description` TEXT NOT NULL COMMENT '详细描述',
    `price` DECIMAL(10, 2) NOT NULL COMMENT '价格',
    `status` ENUM('在售', '已售') NOT NULL DEFAULT '在售' COMMENT '物品状态',
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '发布时间',
    
    -- 外键约束
    CONSTRAINT `fk_items_owner` FOREIGN KEY (`owner_id`) REFERENCES `USERS`(`user_id`) ON DELETE CASCADE,
    CONSTRAINT `fk_items_category` FOREIGN KEY (`category_id`) REFERENCES `CATEGORIES`(`category_id`) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='闲置物品信息表';


-- ===============================================================
-- 表: `ORDERS` (订单表)
-- ===============================================================
CREATE TABLE IF NOT EXISTS `ORDERS` (
    `order_id` INT AUTO_INCREMENT PRIMARY KEY,
    `item_id` INT NOT NULL UNIQUE COMMENT '物品ID (外键), 一个物品只能有一个订单',
    `buyer_id` INT NOT NULL COMMENT '购买者ID (外键)',
    `status` ENUM('进行中', '已完成', '已取消') NOT NULL DEFAULT '进行中' COMMENT '订单状态',
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '订单创建时间',

    -- 外键约束
    CONSTRAINT `fk_orders_item` FOREIGN KEY (`item_id`) REFERENCES `ITEMS`(`item_id`) ON DELETE CASCADE,
    CONSTRAINT `fk_orders_buyer` FOREIGN KEY (`buyer_id`) REFERENCES `USERS`(`user_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='交易订单表';