#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
简单HTTP服务器实现
用于整蛊网站的基础HTTP服务
不依赖外部框架，使用Python标准库实现
"""

import http.server
import socketserver
import json
import os
import logging
from urllib.parse import urlparse

# 配置日志
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 服务器配置
PORT = 5000
HOST = '0.0.0.0'

# 内容类型映射
CONTENT_TYPES = {
    '.css': 'text/css',
    '.js': 'application/javascript',
    '.html': 'text/html',
    '.json': 'application/json',
    '.png': 'image/png',
    '.jpg': 'image/jpeg',
    '.jpeg': 'image/jpeg',
    '.gif': 'image/gif',
    '.svg': 'image/svg+xml',
    '.ico': 'image/x-icon',
    '.txt': 'text/plain'
}

class SimpleHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    """
    自定义HTTP请求处理器
    处理GET和POST请求，提供静态文件服务
    """
    
    def log_message(self, format, *args):
        """
        重写日志方法，使用Python标准logging模块
        """
        logger.info("%s - - [%s] %s" % (
            self.client_address[0],
            self.log_date_time_string(),
            format % args
        ))
    
    def do_GET(self):
        """
        处理GET请求
        - 首页返回HTML内容
        - 静态文件提供相应资源
        - 特殊路径提供兼容性处理
        """
        # 解析URL，移除查询参数和片段
        parsed_url = urlparse(self.path)
        path = parsed_url.path
        
        # 特殊处理Vite客户端请求（提高兼容性）
        if path == '/@vite/client':
            logger.info(f"特殊请求: {path}")
            self.send_response(200)
            self.send_header('Content-Type', 'application/javascript')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(b'')  # 返回空内容
            return
            
        # 规范化路径：移除尾部斜杠（除了根路径）
        if path.endswith('/') and path != '/':
            path = path[:-1]
        
        # 处理首页
        if path == '/':
            self._serve_homepage()
        # 处理静态文件
        elif path.startswith('/static/'):
            self._serve_static_file(path)
        # 其他路径返回404
        else:
            logger.warning(f"未知路径请求: {path}")
            self.send_error(404, f"路径不存在: {path}")
    
    def _serve_homepage(self):
        """
        提供首页HTML内容
        """
        try:
            # 使用绝对路径确保文件定位准确
            template_path = os.path.join(os.path.dirname(__file__), 'templates', 'index.html')
            
            with open(template_path, 'rb') as f:
                content = f.read()
            
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.send_header('Content-Length', str(len(content)))
            self.end_headers()
            self.wfile.write(content)
            logger.info("成功提供首页内容")
            
        except FileNotFoundError:
            logger.error(f"首页模板文件未找到: {template_path}")
            self.send_error(500, "服务器内部错误: 找不到页面资源")
        except Exception as e:
            logger.error(f"提供首页时出错: {str(e)}")
            self.send_error(500, "服务器内部错误")
    
    def _serve_static_file(self, path):
        """
        提供静态文件资源
        """
        try:
            # 构建文件的绝对路径
            file_path = os.path.join(os.path.dirname(__file__), path[1:])  # 移除前导斜杠
            
            # 安全检查：确保不会访问到父目录
            if '..' in path:
                raise SecurityError("路径包含不安全的引用")
            
            if not os.path.exists(file_path):
                logger.warning(f"静态文件未找到: {file_path}")
                self.send_error(404, f"文件不存在: {path}")
                return
            
            # 读取文件内容
            with open(file_path, 'rb') as f:
                content = f.read()
            
            # 获取文件扩展名并设置内容类型
            _, ext = os.path.splitext(file_path)
            content_type = CONTENT_TYPES.get(ext.lower(), 'application/octet-stream')
            
            # 发送响应
            self.send_response(200)
            self.send_header('Content-Type', content_type)
            self.send_header('Content-Length', str(len(content)))
            self.send_header('Cache-Control', 'max-age=3600')  # 缓存控制
            self.end_headers()
            self.wfile.write(content)
            
            logger.info(f"成功提供静态文件: {path} ({content_type})")
            
        except SecurityError as e:
            logger.error(f"安全错误: {str(e)}")
            self.send_error(403, "禁止访问: 安全限制")
        except Exception as e:
            logger.error(f"提供静态文件时出错: {str(e)}")
            self.send_error(500, "服务器内部错误")
    
    def do_POST(self):
        """
        处理POST请求
        主要用于处理用户选择的记录API
        """
        if self.path == '/record_choice':
            self._handle_choice_record()
        else:
            logger.warning(f"未知POST请求路径: {self.path}")
            self.send_error(404, f"API端点不存在: {self.path}")
    
    def _handle_choice_record(self):
        """
        处理选择记录API请求
        """
        try:
            # 获取请求体数据
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length > 0:
                post_data = self.rfile.read(content_length)
                # 尝试解析JSON数据
                try:
                    request_data = json.loads(post_data.decode('utf-8'))
                    logger.info(f"接收到选择记录请求: {request_data}")
                except json.JSONDecodeError:
                    logger.warning("接收到非JSON格式的POST数据")
            
            # 构建响应数据
            response_data = {
                'status': 'success',
                'message': '选择已记录',
                'timestamp': os.path.getmtime(__file__)
            }
            
            # 发送JSON响应
            response_json = json.dumps(response_data)
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Content-Length', str(len(response_json)))
            self.send_header('Access-Control-Allow-Origin', '*')  # 允许跨域请求
            self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            self.end_headers()
            self.wfile.write(response_json.encode('utf-8'))
            
        except Exception as e:
            logger.error(f"处理选择记录请求时出错: {str(e)}")
            # 即使出错也返回成功响应以确保前端体验
            fallback_response = json.dumps({'status': 'success', 'message': '选择已处理'})
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(fallback_response.encode('utf-8'))

def start_server():
    """
    启动HTTP服务器
    """
    logger.info(f"启动简单HTTP服务器，监听地址: {HOST}:{PORT}")
    logger.info(f"访问URL: http://localhost:{PORT}")
    logger.info("按 Ctrl+C 停止服务器")
    
    # 创建TCPServer实例
    with socketserver.TCPServer((HOST, PORT), SimpleHTTPRequestHandler) as httpd:
        # 允许端口复用，避免地址已在使用错误
        httpd.allow_reuse_address = True
        
        try:
            # 开始提供服务
            httpd.serve_forever()
        except KeyboardInterrupt:
            logger.info("接收到中断信号，正在关闭服务器...")
        finally:
            # 确保服务器正确关闭
            httpd.server_close()
            logger.info("服务器已成功关闭")

if __name__ == '__main__':
    # 检查Python版本
    import sys
    if sys.version_info < (3, 6):
        logger.error("需要Python 3.6或更高版本")
        sys.exit(1)
    
    # 启动服务器
    start_server()