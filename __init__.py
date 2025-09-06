# Astrbot Wealth and Contract Plugin with Likability System
# This is an init file for the plugin package

from .astrbot_plugin_likability import Plugin

# 显式地将 Plugin 类添加到全局命名空间
globals()['Plugin'] = Plugin

__all__ = ['Plugin']