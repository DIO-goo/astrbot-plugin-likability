# Astrbot Wealth and Contract Plugin with Likability System
# This is an init file for the plugin package

# 添加调试信息
print("Loading __init__.py for astrbot_plugin_likability plugin...")

try:
    from .astrbot_plugin_likability import Plugin
    print("Successfully imported Plugin class in __init__.py")
except Exception as e:
    print(f"Error importing Plugin class in __init__.py: {e}")

# 显式地将 Plugin 类添加到全局命名空间
globals()['Plugin'] = Plugin

# 为兼容Astrbot，提供多个可能的类名
Main = Plugin
PluginMain = Plugin

__all__ = ['Plugin', 'Main', 'PluginMain']

# 添加调试信息
print(f"Available classes in __init__.py: {__all__}")
print(f"Plugin class in __init__.py: {Plugin}")
print(f"Main class in __init__.py: {Main}")
print(f"PluginMain class in __init__.py: {PluginMain}")