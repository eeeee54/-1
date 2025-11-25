#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
整蛊网站生产服务器启动脚本
使用Waitress作为WSGI服务器，提供高性能生产环境支持
"""

import os
import sys
import logging
from waitress import serve

# 配置日志
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 服务器配置
HOST = '0.0.0.0'
PORT = 5000
THREADS = 10

def start_waitress_server():
    """
    使用Waitress启动生产服务器
    """
    try:
        # 动态导入应用，避免循环导入
        import app
        
        logger.info(f"启动Waitress生产服务器: http://{HOST}:{PORT}")
        logger.info(f"服务器配置: 线程数={THREADS}")
        logger.info("按 Ctrl+C 停止服务")
        
        # 启动Waitress服务器
        serve(
            app.app, 
            host=HOST, 
            port=PORT, 
            threads=THREADS,
            connection_limit=100,  # 连接限制
            cleanup_interval=30,   # 清理间隔（秒）
            inbuf_overflow=500000, # 输入缓冲区溢出阈值
            outbuf_overflow=500000 # 输出缓冲区溢出阈值
        )
    except KeyboardInterrupt:
        logger.info("服务器已被用户中断")
        return True
    except Exception as e:
        logger.error(f"Waitress服务器启动失败: {str(e)}")
        return False

def start_fallback_server():
    """
    启动Flask内置服务器作为备用
    仅在Waitress失败时使用
    """
    try:
        # 动态导入应用
        import app
        
        logger.warning("尝试使用Flask内置服务器作为备用")
        logger.warning("警告: Flask内置服务器仅适用于开发环境，生产环境请使用Waitress")
        
        # 开发环境中可以启用debug
        app.app.run(host=HOST, port=PORT, debug=False)
    except KeyboardInterrupt:
        logger.info("Flask服务器已被用户中断")
    except Exception as e:
        logger.error(f"Flask服务器启动失败: {str(e)}")
        raise

def main():
    """
    主函数
    先尝试启动Waitress，如果失败则尝试Flask
    """
    logger.info("整蛊网站服务启动程序")
    
    # 检查Python版本
    if sys.version_info < (3, 6):
        logger.error("需要Python 3.6或更高版本")
        sys.exit(1)
    
    # 检查必要的依赖
    try:
        import flask
        logger.info(f"已安装Flask版本: {flask.__version__}")
    except ImportError:
        logger.error("未找到Flask，请运行 pip install -r requirements.txt")
        sys.exit(1)
    
    # 启动服务器
    waitress_success = start_waitress_server()
    
    # 如果Waitress启动失败，尝试Flask
    if not waitress_success:
        start_fallback_server()

if __name__ == '__main__':
    main()