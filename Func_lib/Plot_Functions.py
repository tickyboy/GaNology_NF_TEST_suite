import numpy as np
import matplotlib.pyplot as plt


def Plot_Smith(p1_x, p1_y, p2_x, p2_y, x_match, y_match, title, file_path):
    fig, ax = plt.subplots(figsize=(10, 10))
    # 绘制Smith图圆形和坐标轴
    circle = plt.Circle((1, 1), 1, fill=False, color='black', linestyle='solid')
    ax.add_artist(circle)
    ax.plot([0, 2], [1, 1], color='gray', linestyle='dashed')  # 实部轴
    ax.plot([1, 1], [0, 2], color='gray', linestyle='dashed')  # 虚部轴
    ax.plot([1 - np.cos(45 / 360 * 2 * np.pi), 1 + np.cos(45 / 360 * 2 * np.pi)],
            [1 - np.sin(45 / 360 * 2 * np.pi), 1 + np.sin(45 / 360 * 2 * np.pi)], color='gray', linestyle='dashed')
    ax.plot([1 - np.cos(45 / 360 * 2 * np.pi), 1 + np.cos(45 / 360 * 2 * np.pi)],
            [1 + np.sin(45 / 360 * 2 * np.pi), 1 - np.sin(45 / 360 * 2 * np.pi)], color='gray', linestyle='dashed')
    values = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
    for r_value in values:
        angle = np.linspace(0, 2 * np.pi, 100)
        x = 1 + r_value * np.cos(angle)
        y = 1 + r_value * np.sin(angle)
        text_position = (1, 1 + r_value)
        text_content = str(r_value)
        ax.text(*text_position, text_content, color='black', fontsize=16, ha='center', va='center')
        ax.plot(x, y, color='gray', linestyle='dashed')
    # 在Smith图上绘制一系列点
    ax.scatter(p1_x, p1_y, color='purple', label='Instability')
    ax.scatter(p2_x, p2_y, color='gray', label='Stability')
    ax.plot(x_match, y_match, marker='*', linestyle='', markersize=10, color='red', label='Conjugate matching point')
    #ax.scatter(x_match, y_match, color='red', label='Conjugate matching point')

    # 设置坐标轴属性
    ax.set_xlim(0, 2)
    ax.set_ylim(0, 2)
    ax.set_aspect('equal', adjustable='box')
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title(title, fontsize=20)
    ax.legend()
    plt.savefig(file_path + '.tif', format='tif')
    plt.show()

