#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
公众号 AI 写作工具 - 首次配置向导
引导用户填写公众号 API 信息，保存到配置文件
"""

import os
import sys
import json

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    print()
    print("=" * 50)
    print("    公众号 AI 写作工具 - 首次配置向导")
    print("=" * 50)
    print()
    print("欢迎！只需要填写几个信息，以后就不用再配了。")
    print()
    print("【如何获取这些信息？】")
    print("1. 打开 https://mp.weixin.qq.com/ 登录你的公众号")
    print("2. 左边菜单 → 设置与开发 → 基本配置")
    print("3. 复制「开发者ID(AppID)」和「开发者密码(AppSecret)」")
    print()
    print("提示：AppSecret 只显示一次，复制后请妥善保存。")
    print("-" * 50)
    print()

def get_input(prompt, required=True):
    while True:
        value = input(prompt).strip()
        if value or not required:
            return value
        print("  ⚠️  这个不能为空，请重新输入")

def main():
    clear_screen()
    print_header()
    
    # 获取用户输入
    print("【填写公众号信息】")
    print()
    
    app_id = get_input("  开发者ID (AppID): ")
    app_secret = get_input("  开发者密码 (AppSecret): ")
    author = get_input("  作者名（显示在文章里）: ", required=False)
    
    if not author:
        author = "公众号作者"
    
    # 确认信息
    print()
    print("-" * 50)
    print("请确认以下信息：")
    print(f"  AppID:    {app_id}")
    print(f"  AppSecret: {'*' * (len(app_secret) - 4)}{app_secret[-4:]}")
    print(f"  作者名:   {author}")
    print()
    
    confirm = input("确认保存？(y/n): ").strip().lower()
    if confirm != 'y':
        print("已取消，重新运行脚本再试。")
        return
    
    # 保存配置
    config_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # 保存到通用配置
    config = {
        "app_id": app_id,
        "app_secret": app_secret,
        "author": author
    }
    
    config_path = os.path.join(config_dir, "user_config.json")
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)
    
    # 同时更新 wechat-publisher 的配置
    wp_config_path = os.path.join(config_dir, "工具", "wechat-publisher", "wechat-publisher.yaml")
    if os.path.exists(os.path.dirname(wp_config_path)):
        yaml_content = f"""default: main
accounts:
  main:
    name: "我的公众号"
    app_id: "{app_id}"
    app_secret: "{app_secret}"
    author: "{author}"
"""
        with open(wp_config_path, 'w', encoding='utf-8') as f:
            f.write(yaml_content)
        print(f"  ✓ 已更新 wechat-publisher 配置")
    
    print()
    print("=" * 50)
    print("  ✅ 配置完成！")
    print("=" * 50)
    print()
    print("现在你可以使用所有工具了。")
    print("配置文件保存在: user_config.json")
    print()
    print("提示：如果以后需要修改，重新运行这个脚本就行。")
    print()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n已取消配置。")
        sys.exit(0)
    except Exception as e:
        print(f"\n出错了: {e}")
        print("请检查输入是否正确，然后重试。")
        input("\n按回车退出...")
