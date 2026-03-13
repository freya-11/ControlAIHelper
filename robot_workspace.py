import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

def plot_cartesian_workspace(ax, x_range, y_range, z_range):
    x_min, x_max = x_range
    y_min, y_max = y_range
    z_min, z_max = z_range
    
    vertices = np.array([
        [x_min, y_min, z_min], [x_max, y_min, z_min],
        [x_max, y_max, z_min], [x_min, y_max, z_min],
        [x_min, y_min, z_max], [x_max, y_min, z_max],
        [x_max, y_max, z_max], [x_min, y_max, z_max]
    ])
    
    faces = [
        [vertices[0], vertices[1], vertices[5], vertices[4]],
        [vertices[2], vertices[3], vertices[7], vertices[6]],
        [vertices[0], vertices[3], vertices[7], vertices[4]],
        [vertices[1], vertices[2], vertices[6], vertices[5]],
        [vertices[0], vertices[1], vertices[2], vertices[3]],
        [vertices[4], vertices[5], vertices[6], vertices[7]]
    ]
    
    poly3d = Poly3DCollection(faces, alpha=0.6, facecolor='cyan', edgecolor='darkblue')
    ax.add_collection3d(poly3d)
    
    ax.set_xlabel('X (mm)')
    ax.set_ylabel('Y (mm)')
    ax.set_zlabel('Z (mm)')
    ax.set_title('直角坐标型机器人 (Cartesian)')

def plot_cylindrical_workspace(ax, r_range, theta_range, z_range):
    r_min, r_max = r_range
    theta_min, theta_max = theta_range
    z_min, z_max = z_range
    
    theta = np.linspace(theta_min, theta_max, 30)
    z = np.linspace(z_min, z_max, 10)
    Theta, Z = np.meshgrid(theta, z)
    R_min = np.ones_like(Theta) * r_min
    R_max = np.ones_like(Theta) * r_max
    
    X_min = R_min * np.cos(Theta)
    Y_min = R_min * np.sin(Theta)
    X_max = R_max * np.cos(Theta)
    Y_max = R_max * np.sin(Theta)
    
    ax.plot_surface(X_min, Y_min, Z, alpha=0.5, color='orange')
    ax.plot_surface(X_max, Y_max, Z, alpha=0.5, color='orange')
    
    for z_val in [z_min, z_max]:
        theta_fine = np.linspace(theta_min, theta_max, 60)
        x_outer = r_max * np.cos(theta_fine)
        y_outer = r_max * np.sin(theta_fine)
        x_inner = r_min * np.cos(theta_fine)
        y_inner = r_min * np.sin(theta_fine)
        ax.plot(x_outer, y_outer, [z_val]*len(theta_fine), 'orange', lw=1)
        ax.plot(x_inner, y_inner, [z_val]*len(theta_fine), 'orange', lw=1)
    
    ax.set_xlabel('X (mm)')
    ax.set_ylabel('Y (mm)')
    ax.set_zlabel('Z (mm)')
    ax.set_title('圆柱坐标型机器人 (Cylindrical)')

def plot_spherical_workspace(ax, r_range, theta_range, phi_range):
    r_min, r_max = r_range
    theta_min, theta_max = theta_range
    phi_min, phi_max = phi_range
    
    theta = np.linspace(theta_min, theta_max, 30)
    phi = np.linspace(phi_min, phi_max, 30)
    Theta, Phi = np.meshgrid(theta, phi)
    
    R_max = np.ones_like(Theta) * r_max
    R_min = np.ones_like(Theta) * r_min
    
    X_max = R_max * np.sin(Phi) * np.cos(Theta)
    Y_max = R_max * np.sin(Phi) * np.sin(Theta)
    Z_max = R_max * np.cos(Phi)
    
    X_min = R_min * np.sin(Phi) * np.cos(Theta)
    Y_min = R_min * np.sin(Phi) * np.sin(Theta)
    Z_min = R_min * np.cos(Phi)
    
    ax.plot_surface(X_max, Y_max, Z_max, alpha=0.6, color='green')
    ax.plot_surface(X_min, Y_min, Z_min, alpha=0.6, color='lightgreen')
    
    ax.set_xlabel('X (mm)')
    ax.set_ylabel('Y (mm)')
    ax.set_zlabel('Z (mm)')
    ax.set_title('球坐标型机器人 (Spherical)')

def plot_scara_workspace(ax, l1, l2, z_range, theta1_range, theta2_range):
    theta1_min, theta1_max = theta1_range
    theta2_min, theta2_max = theta2_range
    z_min, z_max = z_range
    
    theta2 = np.linspace(theta2_min, theta2_max, 30)
    R = np.sqrt(l1**2 + l2**2 + 2*l1*l2*np.cos(theta2))
    
    theta1 = np.linspace(theta1_min, theta1_max, 60)
    
    for r_val in [R.min(), R.max()]:
        X = r_val * np.cos(theta1)
        Y = r_val * np.sin(theta1)
        ax.plot(X, Y, [z_min]*len(theta1), 'red', lw=2)
        ax.plot(X, Y, [z_max]*len(theta1), 'red', lw=2)
    
    for theta_val in [theta1_min, theta1_max]:
        x_min_edge = R.min() * np.cos(theta_val)
        y_min_edge = R.min() * np.sin(theta_val)
        x_max_edge = R.max() * np.cos(theta_val)
        y_max_edge = R.max() * np.sin(theta_val)
        ax.plot([x_min_edge, x_max_edge], [y_min_edge, y_max_edge], [z_min, z_min], 'red', lw=2)
        ax.plot([x_min_edge, x_max_edge], [y_min_edge, y_max_edge], [z_max, z_max], 'red', lw=2)
        ax.plot([x_min_edge, x_max_edge], [y_min_edge, y_max_edge], [z_min, z_max], 'red', lw=1, alpha=0.5)
    
    theta_grid = np.linspace(theta1_min, theta1_max, 30)
    r_grid = np.linspace(R.min(), R.max(), 10)
    Theta, R_grid = np.meshgrid(theta_grid, r_grid)
    X = R_grid * np.cos(Theta)
    Y = R_grid * np.sin(Theta)
    
    Z_surf = np.ones_like(X) * ((z_min + z_max) / 2)
    ax.plot_surface(X, Y, Z_surf, alpha=0.5, color='red')
    
    ax.set_xlabel('X (mm)')
    ax.set_ylabel('Y (mm)')
    ax.set_zlabel('Z (mm)')
    ax.set_title('SCARA机器人 (SCARA)')

def main():
    fig = plt.figure(figsize=(16, 14))
    
    ax1 = fig.add_subplot(2, 2, 1, projection='3d')
    plot_cartesian_workspace(ax1, 
                           x_range=(0, 500),
                           y_range=(0, 500),
                           z_range=(0, 300))
    
    ax2 = fig.add_subplot(2, 2, 2, projection='3d')
    plot_cylindrical_workspace(ax2,
                              r_range=(100, 400),
                              theta_range=(0, 2*np.pi),
                              z_range=(0, 500))
    
    ax3 = fig.add_subplot(2, 2, 3, projection='3d')
    plot_spherical_workspace(ax3,
                           r_range=(200, 600),
                           theta_range=(0, 2*np.pi),
                           phi_range=(0, np.pi/2))
    
    ax4 = fig.add_subplot(2, 2, 4, projection='3d')
    plot_scara_workspace(ax4,
                        l1=300,
                        l2=250,
                        z_range=(0, 200),
                        theta1_range=(-np.pi/3, np.pi/3),
                        theta2_range=(-np.pi/2, np.pi/2))
    
    plt.tight_layout()
    plt.savefig('robot_workspace.png', dpi=150, bbox_inches='tight')
    plt.show()
    
    print("工作空间图已保存为 robot_workspace.png")

if __name__ == "__main__":
    main()
