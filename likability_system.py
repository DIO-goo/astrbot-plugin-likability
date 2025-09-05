import json
import os
import random
from datetime import datetime, date
from typing import Dict, Any, Optional, Tuple

class LikabilitySystem:
    def __init__(self, config: dict = None, data_dir: str = "data/plugins_WealthAndContract_data"):
        """
        初始化好感度系统
        
        Args:
            config: 配置字典
            data_dir: 数据存储目录
        """
        self.data_dir = data_dir
        self.likability_file = os.path.join(data_dir, "likability_data.json")
        self.user_profile_file = os.path.join(data_dir, "user_profile_data.json")
        self.blacklist_file = os.path.join(data_dir, "blacklist_data.json")
        
        # 确保数据目录存在
        os.makedirs(data_dir, exist_ok=True)
        
        # 加载数据
        self.likability_data = self._load_data(self.likability_file)
        self.user_profile_data = self._load_data(self.user_profile_file)
        self.blacklist_data = self._load_data(self.blacklist_file)
        
        # 默认配置
        if config is None:
            config = {}
            
        self.default_config = {
            "max_likability": config.get("LIKABILITY_CONFIG", {}).get("max_likability", 100),  # 好感度上限
            "initial_likability": config.get("LIKABILITY_CONFIG", {}).get("initial_likability", 20),  # 新用户初始好感度
            "rp_results": {  # 抽卡结果配置
                0: {"change": -8, "message": "是布丁！【好感度-8】"},
                (1, 10): {"change": -4, "message": "是布丁！【好感度-4】"},
                (11, 20): {"change": -3, "message": "是布丁！【好感度-3】"},
                (21, 30): {"change": -2, "message": "是布丁！【好感度-2】"},
                (31, 40): {"change": -1, "message": "是布丁！【好感度-1】"},
                (41, 50): {"change": 0, "message": "是布丁！【好感度+0】"},
                (51, 60): {"change": 1, "message": "是布丁！【好感度+1】"},
                (61, 70): {"change": 2, "message": "是布丁！【好感度+2】"},
                (71, 80): {"change": 3, "message": "是布丁！【好感度+3】"},
                (81, 90): {"change": 4, "message": "是布丁！【好感度+4】"},
                (91, 99): {"change": 5, "message": "是布丁！【好感度+5】"},
                100: {"change": 10, "message": "是布丁！【好感度+10】"}
            },
            "likability_levels": {  # 好感度等级配置
                "疏离回避": (-float('inf'), 0),
                "泛泛而识": (0, 0.2),
                "普通熟人": (0.2, 0.4),
                "可靠伙伴": (0.4, 0.6),
                "亲密伙伴": (0.6, 0.8),
                "信任挚友": (0.8, 1.0),
                "灵魂共鸣": (1.0, float('inf'))
            },
            "admin_list": config.get("LIKABILITY_CONFIG", {}).get("admin_list", [])  # 管理员列表
        }
    
    def _load_data(self, file_path: str) -> Dict[str, Any]:
        """
        从JSON文件加载数据
        
        Args:
            file_path: 文件路径
            
        Returns:
            数据字典
        """
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"加载数据文件失败: {e}")
                return {}
        return {}
    
    def _save_data(self, data: Dict[str, Any], file_path: str) -> None:
        """
        保存数据到JSON文件
        
        Args:
            data: 要保存的数据
            file_path: 文件路径
        """
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存数据文件失败: {e}")
    
    def _get_user_likability_data(self, uid: str) -> Dict[str, Any]:
        """
        获取用户好感度数据
        
        Args:
            uid: 用户ID
            
        Returns:
            用户好感度数据
        """
        if uid not in self.likability_data:
            # 初始化新用户数据
            self.likability_data[uid] = {
                "current_likability": self.default_config["initial_likability"],
                "total_sign_days": 0,
                "last_sign_date": None
            }
            self._save_data(self.likability_data, self.likability_file)
        
        return self.likability_data[uid]
    
    def _get_user_profile_data(self, uid: str) -> Dict[str, Any]:
        """
        获取用户画像数据
        
        Args:
            uid: 用户ID
            
        Returns:
            用户画像数据
        """
        if uid not in self.user_profile_data:
            self.user_profile_data[uid] = {
                "nickname": "",
                "impression": ""
            }
            self._save_data(self.user_profile_data, self.user_profile_file)
        
        return self.user_profile_data[uid]
    
    def is_user_blacklisted(self, uid: str) -> bool:
        """
        检查用户是否在黑名单中
        
        Args:
            uid: 用户ID
            
        Returns:
            是否在黑名单中
        """
        return uid in self.blacklist_data
    
    def rp_draw(self, uid: str) -> Dict[str, Any]:
        """
        抽卡功能
        
        Args:
            uid: 用户ID
            
        Returns:
            抽卡结果
        """
        # 检查是否已签到
        user_data = self._get_user_likability_data(uid)
        today = date.today().isoformat()
        
        if user_data["last_sign_date"] == today:
            return {
                "success": False,
                "message": "今天已经抽过卡了哦~明天再来吧！"
            }
        
        # 生成随机数（使用uid+日期作为种子）
        seed_str = f"{uid}{today}"
        seed = hash(seed_str) % (2**32)
        random.seed(seed)
        result = random.randint(0, 100)
        
        # 获取结果配置
        rp_config = self.default_config["rp_results"]
        change = 0
        message = ""
        
        for key, value in rp_config.items():
            if isinstance(key, int) and key == result:
                change = value["change"]
                message = value["message"]
                break
            elif isinstance(key, tuple) and key[0] <= result <= key[1]:
                change = value["change"]
                message = value["message"]
                break
        
        # 更新用户数据
        user_data["current_likability"] = max(0, user_data["current_likability"] + change)
        user_data["total_sign_days"] += 1
        user_data["last_sign_date"] = today
        
        # 保存数据
        self._save_data(self.likability_data, self.likability_file)
        
        return {
            "success": True,
            "result": result,
            "change": change,
            "message": message,
            "current_likability": user_data["current_likability"],
            "max_likability": self.default_config["max_likability"]
        }
    
    def get_likability(self, uid: str) -> Dict[str, Any]:
        """
        获取用户好感度信息
        
        Args:
            uid: 用户ID
            
        Returns:
            好感度信息
        """
        user_data = self._get_user_likability_data(uid)
        max_likability = self.default_config["max_likability"]
        current_likability = user_data["current_likability"]
        
        # 计算好感度比例
        ratio = current_likability / max_likability if max_likability > 0 else 0
        
        # 获取好感度等级
        level = "未知"
        for level_name, (min_ratio, max_ratio) in self.default_config["likability_levels"].items():
            if min_ratio <= ratio < max_ratio:
                level = level_name
                break
        
        return {
            "current_likability": current_likability,
            "max_likability": max_likability,
            "ratio": ratio,
            "level": level,
            "total_sign_days": user_data["total_sign_days"]
        }
    
    def set_likability(self, operator_uid: str, target_uid: str, change_value: int) -> Dict[str, Any]:
        """
        设置用户好感度（仅管理员）
        
        Args:
            operator_uid: 操作者ID
            target_uid: 目标用户ID
            change_value: 调整数值
            
        Returns:
            操作结果
        """
        # 检查操作者是否为管理员
        if operator_uid not in self.default_config["admin_list"]:
            return {
                "success": False,
                "message": "权限不足，仅管理员可执行此操作"
            }
        
        # 获取目标用户数据并更新
        user_data = self._get_user_likability_data(target_uid)
        new_likability = max(0, user_data["current_likability"] + change_value)
        user_data["current_likability"] = new_likability
        
        # 保存数据
        self._save_data(self.likability_data, self.likability_file)
        
        return {
            "success": True,
            "message": f"好感度设置成功，当前好感度为{new_likability}/{self.default_config['max_likability']}",
            "current_likability": new_likability,
            "max_likability": self.default_config["max_likability"]
        }
    
    def set_user_nickname(self, uid: str, nickname: str) -> Dict[str, Any]:
        """
        设置用户昵称
        
        Args:
            uid: 用户ID
            nickname: 昵称
            
        Returns:
            操作结果
        """
        user_profile = self._get_user_profile_data(uid)
        user_profile["nickname"] = nickname
        
        # 保存数据
        self._save_data(self.user_profile_data, self.user_profile_file)
        
        return {
            "success": True,
            "message": f"昵称设置成功：{nickname}"
        }
    
    def set_user_impression(self, uid: str, impression: str) -> Dict[str, Any]:
        """
        设置用户印象
        
        Args:
            uid: 用户ID
            impression: 印象
            
        Returns:
            操作结果
        """
        user_profile = self._get_user_profile_data(uid)
        user_profile["impression"] = impression
        
        # 保存数据
        self._save_data(self.user_profile_data, self.user_profile_file)
        
        return {
            "success": True,
            "message": f"印象设置成功：{impression}"
        }
    
    def get_user_profile(self, uid: str) -> Dict[str, str]:
        """
        获取用户画像信息
        
        Args:
            uid: 用户ID
            
        Returns:
            用户画像信息
        """
        user_profile = self._get_user_profile_data(uid)
        return {
            "nickname": user_profile["nickname"],
            "impression": user_profile["impression"]
        }
    
    def add_to_blacklist(self, operator_uid: str, target_uid: str) -> Dict[str, Any]:
        """
        添加用户到黑名单（仅管理员）
        
        Args:
            operator_uid: 操作者ID
            target_uid: 目标用户ID
            
        Returns:
            操作结果
        """
        # 检查操作者是否为管理员
        if operator_uid not in self.default_config["admin_list"]:
            return {
                "success": False,
                "message": "权限不足，仅管理员可执行此操作"
            }
        
        # 添加到黑名单
        self.blacklist_data[target_uid] = True
        self._save_data(self.blacklist_data, self.blacklist_file)
        
        return {
            "success": True,
            "message": f"用户 {target_uid} 已添加到黑名单"
        }
    
    def remove_from_blacklist(self, operator_uid: str, target_uid: str) -> Dict[str, Any]:
        """
        从黑名单移除用户（仅管理员）
        
        Args:
            operator_uid: 操作者ID
            target_uid: 目标用户ID
            
        Returns:
            操作结果
        """
        # 检查操作者是否为管理员
        if operator_uid not in self.default_config["admin_list"]:
            return {
                "success": False,
                "message": "权限不足，仅管理员可执行此操作"
            }
        
        # 从黑名单移除
        if target_uid in self.blacklist_data:
            del self.blacklist_data[target_uid]
            self._save_data(self.blacklist_data, self.blacklist_file)
        
        return {
            "success": True,
            "message": f"用户 {target_uid} 已从黑名单移除"
        }
    
    def add_admin(self, admin_uid: str) -> None:
        """
        添加管理员
        
        Args:
            admin_uid: 管理员ID
        """
        if admin_uid not in self.default_config["admin_list"]:
            self.default_config["admin_list"].append(admin_uid)
    
    def get_prompt_addition(self, uid: str) -> str:
        """
        获取提示词附加内容
        
        Args:
            uid: 用户ID
            
        Returns:
            提示词附加内容
        """
        # 检查是否在黑名单
        if self.is_user_blacklisted(uid):
            return "（当前用户惹你生气了，你暂时不想理他）"
        
        # 获取好感度信息
        likability_info = self.get_likability(uid)
        level_description = f"（{likability_info['level']}）"
        
        # 获取用户画像
        profile = self.get_user_profile(uid)
        nickname = profile["nickname"]
        impression = profile["impression"]
        
        # 构建提示词附加内容
        prompt_parts = []
        if nickname:
            prompt_parts.append(f"用户昵称：{nickname}")
        if impression:
            prompt_parts.append(f"用户印象：{impression}")
        prompt_parts.append(f"关系状态：{level_description}")
        
        return "\\n".join(prompt_parts)