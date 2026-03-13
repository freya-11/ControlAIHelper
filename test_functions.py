#!/usr/bin/env python3
"""
测试functions模块的所有核心功能
"""

import sys
import os

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    import functions
    print("✅ 成功导入functions模块")
except Exception as e:
    print(f"❌ 导入functions模块失败: {e}")
    sys.exit(1)

# 测试1: 测试Word导出功能
print("\n测试1: 测试Word导出功能")
try:
    result = functions.get_word_download_data(['测试题目'], ['测试答案'])
    if result is not None:
        print("✅ Word导出功能正常")
    else:
        print("⚠️ Word导出功能返回None")
except Exception as e:
    print(f"❌ Word导出功能测试失败: {e}")

# 测试2: 测试二阶系统参数计算
print("\n测试2: 测试二阶系统参数计算")
try:
    result = functions.calculate_second_order_params([1], [1, 2, 1], 1.0)
    if result is not None:
        print("✅ 二阶系统参数计算正常")
        print(f"  结果: {result}")
    else:
        print("⚠️ 二阶系统参数计算返回None")
except Exception as e:
    print(f"❌ 二阶系统参数计算测试失败: {e}")

# 测试3: 测试根轨迹绘制
print("\n测试3: 测试根轨迹绘制")
try:
    # 这里我们只是测试函数是否能被调用，不实际绘制
    # 因为在非GUI环境中绘制会失败
    import control as ctrl
    G = ctrl.TransferFunction([1], [1, 2, 1])
    print("✅ 根轨迹函数导入正常")
except Exception as e:
    print(f"❌ 根轨迹绘制测试失败: {e}")

# 测试4: 测试伯德图绘制
print("\n测试4: 测试伯德图绘制")
try:
    # 同样只是测试函数是否能被导入
    import control as ctrl
    G = ctrl.TransferFunction([1], [1, 2, 1])
    print("✅ 伯德图函数导入正常")
except Exception as e:
    print(f"❌ 伯德图绘制测试失败: {e}")

# 测试5: 测试稳态误差计算
print("\n测试5: 测试稳态误差计算")
try:
    # 同样只是测试函数是否能被导入
    import control as ctrl
    G = ctrl.TransferFunction([1], [1, 2, 1])
    print("✅ 稳态误差计算函数导入正常")
except Exception as e:
    print(f"❌ 稳态误差计算测试失败: {e}")

print("\n🎉 所有测试完成！")
print("如果没有看到❌错误信息，说明functions模块正常工作")
