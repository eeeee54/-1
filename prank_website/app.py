#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
整蛊网站Flask应用主文件
提供网站的主要功能和API接口
"""

from flask import Flask, request, jsonify
import os
import logging

# 配置日志
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 创建Flask应用实例
app = Flask(__name__)

# 设置应用配置
app.config['JSON_SORT_KEYS'] = False

@app.route('/')
def index():
    """
    首页路由
    读取并返回HTML文件内容
    """
    try:
        # 构建文件的绝对路径
        template_path = os.path.join(os.path.dirname(__file__), 'templates', 'index.html')
        
        # 读取HTML文件内容
        with open(template_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        logger.info("成功加载首页HTML内容")
        return html_content
    except FileNotFoundError as e:
        logger.error(f"找不到HTML模板文件: {e}")
        return "找不到页面资源", 404
    except Exception as e:
        logger.error(f"服务器内部错误: {e}")
        # 在生产环境中不返回详细错误信息
        return "服务器内部错误", 500

@app.route('/record_choice', methods=['POST'])
def record_choice():
    """
    记录用户选择的API接口
    接收POST请求并返回成功响应
    """
    try:
        # 获取请求数据
        data = request.get_json(silent=True) or {}
        logger.info(f"接收到选择记录请求: {data}")
        
        # 这里可以添加数据库记录逻辑（可选）
        # 为了简化，当前仅返回成功响应
        
        return jsonify({
            "status": "success", 
            "message": "选择已记录",
            "timestamp": os.path.getmtime(__file__)
        })
    except Exception as e:
        logger.error(f"处理选择记录时出错: {e}")
        # 即使出错也返回成功响应，以确保前端体验
        return jsonify({
            "status": "success", 
            "message": "选择已处理"
        })

if __name__ == '__main__':
    """
    应用入口
    仅用于开发环境
    生产环境建议使用start_server.py
    """
    logger.info("启动Flask开发服务器")
    # 生产环境中debug必须为False
    app.run(host='0.0.0.0', port=5000, debug=False)
    logger.info("Flask开发服务器已停止")