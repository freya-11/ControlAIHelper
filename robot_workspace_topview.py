import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

def plot_cartesian_topview(ax, x_range, y_range):
    x_min, x_max = x_range
    y_min, y_max = y_range
    
    rect = plt.Rectangle((x_min, y_min), x_max - x_min, y_max - y_min, 
                          fill=True, alpha=0.5, facecolor='cyan', edgecolor='darkblue', lw=2)
    ax.add_patch(rect)
    
    ax.set_xlim(x_min - 50, x_max + 50)
    ax.set_ylim(y_min - 50, y_max + 50)
    ax.set_xlabel('X (mm)')
    ax.set_ylabel('Y (mm)')
    ax.set_title('直角坐标型 (Cartesian) - 俯视图')
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3)

def plot_cylindrical_topview(ax, r_range):
    r_min, r_max = r_range
    
    theta = np.linspace(0, 2*np.pi, 100)
    
    x_outer = r_max * np.cos(theta)
    y_outer = r_max * np.sin(theta)
    ax.fill(x_outer, y_outer, alpha=0.5, facecolor='orange', edgecolor='darkorange', lw=2)
    
    x_inner = r_min * np.cos(theta)
    y_inner = r_min * np.sin(theta)
    ax.fill(x_inner, y_inner, alpha=1, facecolor='white', edgecolor='darkorange', lw=2)
    
    ax.set_xlim(-r_max - 50, r_max + 50)
    ax.set_ylim(-r_max - 50, r_max + 50)
    ax.set_xlabel('X (mm)')
    ax.set_ylabel('Y (mm)')
    ax.set_title('圆柱坐标型 (Cylindrical) - 俯视图')
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3)

def plot_spherical_topview(ax, r_range):
    r_min, r_max = r_range
    
    circle = plt.Circle((0, 0), r_max, fill=True, alpha=0.5, facecolor='green', edgecolor='darkgreen', lw=2)
    ax.add_patch(circle)
    
    inner_circle = plt.Circle((0, 0), r_min, fill=True, facecolor='white', edgecolor='darkgreen', lw=2)
    ax.add_patch(inner_circle)
    
    ax.set_xlim(-r_max - 50, r_max + 50)
    ax.set_ylim(-r_max - 50, r_max + 50)
    ax.set_xlabel('X (mm)')
    ax.set_ylabel('Y (mm)')
    ax.set_title('球坐标型 (Spherical) - 俯视图')
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3)

def plot_scara_topview(ax, l1, l2, theta1_range, theta2_range):
    theta1_min, theta1_max = theta1_range
    theta2_min, theta2_max = theta2_range
    
    theta2 = np.linspace(theta2_min, theta2_max, 100)
    R = np.sqrt(l1**2 + l2**2 + 2*l1*l2*np.cos(theta2))
    r_min, r_max = R.min(), R.max()
    
    theta1 = np.linspace(theta1_min, theta1_max, 100)
    
    for r_val in [r_min, r_max]:
        x = r_val * np.cos(theta1)
        y = r_val * np.sin(theta1)
        ax.plot(x, y, 'r-', lw=2)
    
    for theta_val in [theta1_min, theta1_max]:
        x_edge = [r_min * np.cos(theta_val), r_max * np.cos(theta_val)]
        y_edge = [r_min * np.sin(theta_val), r_max * np.sin(theta_val)]
        ax.plot(x_edge, y_edge, 'r-', lw=2)
    
    theta_fill = np.linspace(theta1_min, theta1_max, 50)
    r_fill = np.linspace(r_min, r_max, 20)
    Theta, R_fill = np.meshgrid(theta_fill, r_fill)
    X = R_fill * np.cos(Theta)
    Y = R_fill * np.sin(Theta)
    ax.fill(X.flatten(), Y.flatten(), alpha=0.5, facecolor='red')
    
    ax.set_xlim(-r_max - 50, r_max + 50)
    ax.set_ylim(-r_max - 50, r_max + 50)
    ax.set_xlabel('X (mm)')
    ax.set_ylabel('Y (mm)')
    ax.set_title('SCARA机器人 - 俯视图')
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3)

def main():
    fig, axes = plt.subplots(2, 2, figsize=(12, 12))
    
    plot_cartesian_topview(axes[0, 0], x_range=(0, 500), y_range=(0, 500))
    
    plot_cylindrical_topview(axes[0, 1], r_range=(100, 400))
    
    plot_spherical_topview(axes[1, 0], r_range=(200, 600))
    
    plot_scara_topview(axes[1, 1], 
                       l1=300, 
                       l2=250, 
                       theta1_range=(-np.pi/3, np.pi/3),
                       theta2_range=(-np.pi/2, np.pi/2))
    
    plt.tight_layout()
    plt.savefig('robot_workspace_topview.png', dpi=150, bbox_inches='tight')
    plt.show()
    
    print("俯视图已保存为 robot_workspace_topview.png")

if __name__ == "__main__":
    main()
