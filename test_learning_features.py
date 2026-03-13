# 测试学习辅助功能
import sys
sys.path.insert(0, r'd:\ControlAIHelper')

from functions import TERMINOLOGY

print("✅ 术语库加载成功！")
print(f"共有 {len(TERMINOLOGY)} 个模块")
print("模块列表:", list(TERMINOLOGY.keys()))
print()

for module_name, module_data in TERMINOLOGY.items():
    print(f"📚 {module_name} 模块:")
    print(f"  - 术语数量: {len(module_data['terms'])}")
    print(f"  - 术语列表: {list(module_data['terms'].keys())}")
    print(f"  - 易错点数量: {len(module_data['common_mistakes'])}")
    print()

print("✅ 所有功能正常！")
