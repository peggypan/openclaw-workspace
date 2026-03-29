#!/usr/bin/env python3
"""
写作风格指南 - 风格检查清单
验证文章是否符合选定的写作风格
"""

import argparse

CHECKLISTS = {
    "呼吸感": [
        "句子有长短变化吗？",
        "有适当的留白/停顿吗？",
        "读起来像说话一样自然吗？",
        "读出来是否顺口？",
        "有没有让人喘不过气的大长句？",
        "情感转折点是否有停顿？"
    ],
    "毛边感": [
        "有真实的瑕疵细节吗？",
        "有狼狈/不完美的描写吗？",
        "读完觉得\"太精致反而不真实\"吗？",
        "有没有过于精致的形容词？",
        "是否回避了狼狈、尴尬、丑陋的细节？"
    ],
    "颗粒感": [
        "有具体的细节描写吗？",
        "能唤起感官记忆吗？",
        "有时间的厚重感吗？"
    ],
    "凛冽感": [
        "用词精准、无冗余吗？",
        "情感克制、冷峻吗？",
        "像手术刀一样利落吗？",
        "有废话可以删减吗？"
    ],
    "矿物感": [
        "逻辑严密、层层递进吗？",
        "去情感化、客观陈述吗？",
        "有数据/事实支撑吗？",
        "避免了主观感受词吗？"
    ],
    "粘稠感": [
        "有浓郁的意象吗？",
        "情绪层层堆叠吗？",
        "有沉浸感吗？",
        "避免了过早给出结论吗？"
    ],
    "少年感": [
        "语气是向上的吗？",
        "有新鲜感和好奇心吗？",
        "避免了老气横秋的表达吗？"
    ],
    "灰尘味": [
        "有时间沉淀的感觉吗？",
        "温情而不煽情吗？",
        "有旧物/老场景的描写吗？"
    ],
    "摩擦力": [
        "有真实的困难描写吗？",
        "避免了\"鸡汤\"式结尾吗？",
        "有受力的质感吗？"
    ],
    "架构感": [
        "结构清晰吗？",
        "层次分明吗？",
        "模块化组织吗？",
        "有清晰的框架吗？"
    ],
    "透明感": [
        "表达极简吗？",
        "去除一切修饰了吗？",
        "有透明/空灵感吗？",
        "留白充足吗？"
    ],
    "金属感": [
        "有冷色调意象吗？",
        "有机械/科技隐喻吗？",
        "有未来感吗？",
        "冷冽而非温暖吗？"
    ]
}

def show_checklist(style_name):
    """显示风格的检查清单"""
    if style_name not in CHECKLISTS:
        print(f"❌ 未知风格：{style_name}")
        print(f"可用风格：{', '.join(CHECKLISTS.keys())}")
        return
    
    items = CHECKLISTS[style_name]
    print(f"\n✅ 【{style_name}】检查清单\n")
    for i, item in enumerate(items, 1):
        print(f"  {i}. [ ] {item}")
    print(f"\n共 {len(items)} 项检查")

def show_all_checklists():
    """显示所有风格的检查清单"""
    for style_name in CHECKLISTS:
        show_checklist(style_name)
        print("\n" + "="*50 + "\n")

def interactive_check():
    """交互式检查"""
    print("\n🎯 写作风格检查工具\n")
    print("请选择要检查的风格：")
    
    styles = list(CHECKLISTS.keys())
    for i, style in enumerate(styles, 1):
        print(f"  {i}. {style}")
    print(f"  {len(styles)+1}. 全部")
    
    try:
        choice = int(input("\n输入编号: "))
        if 1 <= choice <= len(styles):
            show_checklist(styles[choice-1])
        elif choice == len(styles) + 1:
            show_all_checklists()
        else:
            print("❌ 无效选择")
    except ValueError:
        print("❌ 请输入数字")

def main():
    parser = argparse.ArgumentParser(description="写作风格检查清单")
    parser.add_argument("--style", help="显示特定风格的检查清单")
    parser.add_argument("--all", action="store_true", help="显示所有检查清单")
    parser.add_argument("--interactive", action="store_true", help="交互式检查")
    
    args = parser.parse_args()
    
    if args.style:
        show_checklist(args.style)
    elif args.all:
        show_all_checklists()
    elif args.interactive:
        interactive_check()
    else:
        parser.print_help()
        print("\n💡 示例：")
        print("  python style_checker.py --style 呼吸感")
        print("  python style_checker.py --all")
        print("  python style_checker.py --interactive")

if __name__ == "__main__":
    main()
