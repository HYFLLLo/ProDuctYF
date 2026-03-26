-- AI夜宵爆品预测助手 - 数据库初始化脚本

CREATE DATABASE IF NOT EXISTS night_owl_prediction CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE night_owl_prediction;

-- 商家表
CREATE TABLE IF NOT EXISTS merchants (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    merchant_id VARCHAR(64) UNIQUE NOT NULL,
    merchant_name VARCHAR(128) NOT NULL,
    merchant_type ENUM('便利店', '超市', '闪电仓', '其他') DEFAULT '便利店',
    city VARCHAR(32) NOT NULL,
    district VARCHAR(32),
    latitude DECIMAL(10, 7),
    longitude DECIMAL(10, 7),
    delivery_radius_km DECIMAL(5, 2) DEFAULT 3.0,
    status ENUM('active', 'inactive', 'suspended') DEFAULT 'active',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_city (city),
    INDEX idx_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 商品表
CREATE TABLE IF NOT EXISTS products (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    product_id VARCHAR(64) UNIQUE NOT NULL,
    product_name VARCHAR(128) NOT NULL,
    category_id VARCHAR(32) NOT NULL,
    category_name VARCHAR(64) NOT NULL,
    brand VARCHAR(64),
    cost_price DECIMAL(10, 2) NOT NULL,
    retail_price DECIMAL(10, 2) NOT NULL,
    status ENUM('active', 'inactive') DEFAULT 'active',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_category (category_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 库存表
CREATE TABLE IF NOT EXISTS inventory (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    merchant_id VARCHAR(64) NOT NULL,
    product_id VARCHAR(64) NOT NULL,
    usable_stock INT DEFAULT 0,
    reserved_stock INT DEFAULT 0,
    days_in_stock INT DEFAULT 0,
    last_restock_at DATETIME,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY uk_merchant_product (merchant_id, product_id),
    INDEX idx_merchant (merchant_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 事件表
CREATE TABLE IF NOT EXISTS events (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    event_id VARCHAR(32) UNIQUE NOT NULL,
    event_name VARCHAR(255) NOT NULL,
    event_type ENUM('赛事', '娱乐', '天气', '社会', '其他') NOT NULL,
    event_time DATETIME NOT NULL,
    event_location VARCHAR(255),
    event_heat DECIMAL(5,2) DEFAULT 0,
    heat_rank INT DEFAULT 0,
    summary TEXT,
    entities JSON,
    sources JSON,
    confidence DECIMAL(5,2),
    needs_review TINYINT(1) DEFAULT 0,
    review_status ENUM('pending', 'approved', 'rejected') DEFAULT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_event_type (event_type),
    INDEX idx_event_time (event_time),
    INDEX idx_event_heat (event_heat),
    INDEX idx_needs_review (needs_review)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 用户场景表
CREATE TABLE IF NOT EXISTS user_scenes (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    scene_id VARCHAR(64) UNIQUE NOT NULL,
    user_id VARCHAR(64) NOT NULL,
    scene_type ENUM('看球', '加班', '聚会', '独饮', '零食', '其他') NOT NULL,
    scene_reason TEXT,
    confidence DECIMAL(5,2),
    current_products JSON,
    recommended_products JSON,
    event_context JSON,
    order_time DATETIME,
    location VARCHAR(255),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_user_id (user_id),
    INDEX idx_scene_type (scene_type),
    INDEX idx_order_time (order_time)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 商家决策表
CREATE TABLE IF NOT EXISTS merchant_decisions (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    decision_id VARCHAR(64) UNIQUE NOT NULL,
    merchant_id VARCHAR(64) NOT NULL,
    decision_date DATE NOT NULL,
    hot_products JSON,
    restock_recommendations JSON,
    pricing_recommendations JSON,
    bundle_strategies JSON,
    adoption_status ENUM('pending', 'adopted', 'rejected') DEFAULT 'pending',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_merchant_date (merchant_id, decision_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- LLM调用日志表
CREATE TABLE IF NOT EXISTS llm_call_logs (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    call_id VARCHAR(64) UNIQUE NOT NULL,
    agent_name VARCHAR(32) NOT NULL,
    input_tokens INT,
    output_tokens INT,
    call_time_ms INT,
    status ENUM('success', 'fallback', 'failed') DEFAULT 'success',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_agent (agent_name),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
