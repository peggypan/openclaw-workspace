#!/usr/bin/env python3
"""
写作风格指南 - 风格选择助手
帮助用户根据文章类型选择合适的写作风格
"""

import argparse

STYLES = {
    "呼吸感": {
        "dimension": "第一象限（生命/自然）",
        "traits": "节奏与留白",
        "keywords": "起伏、通透、生命流动",
        "scenes": ["随笔", "感悟", "情绪叙事"],
        "combo": ["毛边感", "粘稠感"]
    },
    "毛边感": {
        "dimension": "第一象限（生命/自然）",
        "traits": "真实与瑕疵",
        "keywords": "手感、诚恳、未经修饰",
        "scenes": ["个人独白", "内心剖析", "真实生活"],
        "combo": ["呼吸感", "颗粒感"]
    },
    "少年感": {
        "dimension": "第一象限（生命/自然）",
        "traits": "轻盈与好奇",
        "keywords": "朝气、干净、向上生长",
        "scenes": ["旅行游记", "成长感悟", "激励文"],
        "combo": ["颗粒感", "呼吸感"]
    },
    "颗粒感": {
        "dimension": "第二象限（现实/物理）",
        "traits": "细节与质感",
        "keywords": "写实、厚重、岁月痕迹",
        "scenes": ["回忆录", "纪实文学", "职场复盘"],
        "combo": ["灰尘味", "摩擦力"]
    },
    "灰尘味": {
        "dimension": "第二象限（现实/物理）",
        "traits": "时间沉淀",
        "keywords": "旧时光、温暖、沉淀",
        "scenes": ["怀旧散文", "老同事故事", "童年回忆"],
        "combo": ["颗粒感", "摩擦力"]
    },
    "摩擦力": {
        "dimension": "第二象限（现实/物理）",
        "traits": "冲突与挣扎",
        "keywords": "阻力、真实痛感",
        "scenes": ["创业艰辛", "奋斗记录", "真实困难"],
        "combo": ["颗粒感", "灰尘味"]
    },
    "矿物感": {
        "dimension": "第三象限（理性/逻辑）",
        "traits": "逻辑与坚硬",
        "keywords": "物理、客观、去情感化",
        "scenes": ["硬核科普", "哲学推演", "技术分析"],
        "combo": ["凛冽感", "架构感"]
    },
    "凛冽感": {
        "dimension": "第三象限（理性/逻辑）",
        "traits": "精准与极简",
        "keywords": "冷峻、利落、手术刀",
        "scenes": ["深度评论", "前沿洞察", "先锋文学"],
        "combo": ["矿物感", "金属感"]
    },
    "架构感": {
        "dimension": "第三象限（理性/逻辑）",
        "traits": "层次与秩序",
        "keywords": "结构化、模块化、清晰",
        "scenes": ["系统设计", "方法论", "概念梳理"],
        "combo": ["矿物感"]
    },
    "粘稠感": {
        "dimension": "第四象限（意境/抽象）",
        "traits": "浓烈与沉浸",
        "keywords": "氛围、隐喻、情感溺水",
        "scenes": ["意识流", "梦境记录", "情感宣泄"],
        "combo": ["呼吸感", "透明感"]
    },
    "透明感": {
        "dimension": "第四象限（意境/抽象）",
        "traits": "极简与纯粹",
        "keywords": "空灵、无杂质",
        "scenes": ["禅意", "冥想记录", "纯粹状态"],
        "combo": ["粘稠感"]
    },
    "金属感": {
        "dimension": "第四象限（意境/抽象）",
        "traits": "现代与冷冽",
        "keywords": "未来感、机械美学",
        "scenes": ["赛博朋克", "前卫设计", "未来畅想"],
        "combo": ["凛冽感"]
    }
}

SCENE_RECOMMENDATIONS = {
    "随笔": ["呼吸感", "毛边感"],
    "感悟": ["呼吸感", "粘稠感"],
    "技术评论": ["凛冽感", "矿物感"],
    "回忆录": ["颗粒感", "灰尘味"],
    "游记": ["少年感", "颗粒感"],
    "科普": ["矿物感", "架构感"],
    "职场": ["颗粒感", "摩擦力"],
    "创业": ["摩擦力", "颗粒感"],
    "深夜emo": ["呼吸感", "粘稠感"],
    "评论": ["凛冽感", "矿物感"],
    "小说": ["粘稠感", "呼吸感"],
    "诗歌": ["透明感", "粘稠感"]
}

def list_styles():
    """列出所有风格"""
    print("\n📚 12种写作风格：\n")
    print(f"{'风格':<10} {'象限':<20} {'核心特质':<15} {'适用场景'}")
    print("-" * 70)
    for name, info in STYLES.items():
        scenes = ", ".join(info["scenes"][:2])
        print(f"{name:<10} {info['dimension']:<20} {info['traits']:<15} {scenes}")

def recommend_style(scene):
    """根据场景推荐风格"""
    scene = scene.lower()
    matched = None
    
    for key, styles in SCENE_RECOMMENDATIONS.items():
        if key in scene or scene in key:
            matched = styles
            break
    
    if matched:
        print(f"\n🎯 针对「{scene}」推荐风格：")
        for style in matched:
            info = STYLES[style]
            print(f"\n  【{style}】")
            print(f"   特质：{info['traits']}")
            print(f"   关键词：{info['keywords']}")
            print(f"   场景：{", ".join(info['scenes'])}")
            print(f"   推荐组合：{', '.join(info['combo'][:2])}")
    else:
        print(f"\n⚠️ 未找到「{scene}」的推荐，试试这些场景：")
        print(", ".join(SCENE_RECOMMENDATIONS.keys()))

def show_style_detail(style_name):
    """显示风格详情"""
    if style_name not in STYLES:
        print(f"❌ 未知风格：{style_name}")
        print(f"可用风格：{', '.join(STYLES.keys())}")
        return
    
    info = STYLES[style_name]
    print(f"\n📖 【{style_name}】\n")
    print(f"象限：{info['dimension']}")
    print(f"核心特质：{info['traits']}")
    print(f"关键词：{info['keywords']}")
    print(f"\n适用场景：")
    for scene in info["scenes"]:
        print(f"  • {scene}")
    print(f"\n推荐组合：{', '.join(info['combo'])}")

def main():
    parser = argparse.ArgumentParser(description="写作风格选择助手")
    parser.add_argument("--list", action="store_true", help="列出所有风格")
    parser.add_argument("--scene", help="根据场景推荐风格")
    parser.add_argument("--detail", help="查看风格详情")
    
    args = parser.parse_args()
    
    if args.list:
        list_styles()
    elif args.scene:
        recommend_style(args.scene)
    elif args.detail:
        show_style_detail(args.detail)
    else:
        parser.print_help()
        print("\n💡 示例：")
        print("  python style_selector.py --list")
        print("  python style_selector.py --scene 随笔")
        print("  python style_selector.py --detail 呼吸感")

if __name__ == "__main__":
    main()
