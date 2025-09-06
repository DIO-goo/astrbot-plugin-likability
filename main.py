# Astrbot Wealth and Contract Plugin with Likability System
# This is the main entry point for the plugin

# 添加调试信息
print("Loading astrbot_plugin_likability plugin...")

try:
    from astrbot_plugin_likability import Plugin
    print("Successfully imported Plugin class")
except Exception as e:
    print(f"Error importing Plugin class: {e}")

# 为兼容Astrbot，提供多个可能的类名
Main = Plugin
PluginMain = Plugin

# 确保 Plugin 类在模块的全局命名空间中可用
__all__ = ['Plugin', 'Main', 'PluginMain']

# 添加调试信息
print(f"Available classes: {__all__}")
print(f"Plugin class: {Plugin}")
print(f"Main class: {Main}")
print(f"PluginMain class: {PluginMain}")