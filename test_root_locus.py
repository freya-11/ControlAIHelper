import sys
sys.path.insert(0, '.')

# 模拟Streamlit的st对象
import types
st = types.SimpleNamespace()
st.error = lambda x: print(f'ERROR: {x}')
st.success = lambda x: print(f'SUCCESS: {x}')
st.warning = lambda x: print(f'WARNING: {x}')
st.info = lambda x: print(f'INFO: {x}')
st.markdown = lambda x: print(f'MARKDOWN: {x}')
st.write = lambda x: print(f'WRITE: {x}')
st.subheader = lambda x: print(f'SUBHEADER: {x}')
st.pyplot = lambda *args, **kwargs: print('PLOT: 根轨迹图绘制成功')
st.divider = lambda: print('---')
st.expander = lambda *args, **kwargs: types.SimpleNamespace(**{'__enter__': lambda self: self, '__exit__': lambda *args: None})
st.caption = lambda x: print(f'CAPTION: {x}')
st.columns = lambda n: [st for _ in range(n)]
st.latex = lambda x: print(f'LATEX: {x}')
st.empty = lambda: types.SimpleNamespace(**{'info': lambda x: None, 'success': lambda x: None})

# 导入并覆盖st
import functions
functions.st = st

from functions import plot_root_locus
import numpy as np

# 测试一个三阶系统
print('测试三阶系统根轨迹分析...')
try:
    # 测试三阶系统：G(s) = K/(s(s+1)(s+2))
    num = [1]
    den = [1, 3, 2, 0]
    K = 1.0
    
    print(f'测试传递函数：分子 {num}, 分母 {den}, K={K}')
    print('-' * 60)
    
    # 调用函数
    plot_root_locus(num, den, K)
    
    print('-' * 60)
    print('✅ 三阶系统测试通过！')
except Exception as e:
    print(f'❌ 测试失败：{str(e)}')
    import traceback
    print(traceback.format_exc())
