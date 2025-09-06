# Astrbot Wealth and Contract Plugin with Likability System
# This is the main entry point for the plugin

from astrbot_plugin_likability import Plugin

# 为兼容Astrbot，提供多个可能的类名
Main = Plugin
PluginMain = Plugin

# 确保 Plugin 类在模块的全局命名空间中可用
__all__ = ['Plugin', 'Main', 'PluginMain']