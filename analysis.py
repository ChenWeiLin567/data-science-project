# -*- coding: utf-8 -*-
"""
Palmer Penguins 数据分析
研究问题：不同种类企鹅的体型特征（鳍长、体重等）有何差异？
          能否仅凭体型测量值区分企鹅种类？

数据来源：Palmer Penguins 数据集（CC0 公共领域协议）
         Gorman, Williams & Fraser (2014), Palmer Station LTER
"""
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns

# 中文显示（Windows 常见中文字体回退）
matplotlib.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "Arial Unicode MS", "DejaVu Sans"]
matplotlib.rcParams["axes.unicode_minus"] = False

DATA_PATH = "data/penguins.csv"
FIG_DIR = "figures"


def load_clean(path: str) -> pd.DataFrame:
    """读取数据并做基础清洗：删除关键字段缺失的行。"""
    df = pd.read_csv(path)
    print(f"原始记录数：{len(df)}")
    df = df.dropna(subset=["bill_length_mm", "bill_depth_mm",
                           "flipper_length_mm", "body_mass_g", "sex"])
    df = df.reset_index(drop=True)
    print(f"清洗后记录数：{len(df)}")
    return df


def describe(df: pd.DataFrame) -> None:
    """按种类输出核心体型指标的描述性统计。"""
    stats = df.groupby("species")[["bill_length_mm", "bill_depth_mm",
                                   "flipper_length_mm", "body_mass_g"]].mean().round(1)
    print("\n各种类体型指标均值：")
    print(stats)


def viz_scatter(df: pd.DataFrame) -> None:
    """图1：鳍长 vs 体重散点图，按种类着色 —— 展示种类的体型分离度。"""
    plt.figure(figsize=(8, 6))
    sns.scatterplot(data=df, x="flipper_length_mm", y="body_mass_g",
                    hue="species", style="species", s=70, alpha=0.85)
    plt.title("图1  企鹅鳍长与体重的关系（按种类）")
    plt.xlabel("鳍长 (mm)")
    plt.ylabel("体重 (g)")
    plt.legend(title="种类")
    plt.tight_layout()
    plt.savefig(f"{FIG_DIR}/viz1_scatter.png", dpi=150)
    plt.close()


def viz_boxplot(df: pd.DataFrame) -> None:
    """图2：各种类体重箱线图（按性别分组）—— 展示种类与性别的体重差异。"""
    plt.figure(figsize=(8, 6))
    sns.boxplot(data=df, x="species", y="body_mass_g", hue="sex")
    plt.title("图2  不同种类与性别的企鹅体重分布")
    plt.xlabel("种类")
    plt.ylabel("体重 (g)")
    plt.legend(title="性别")
    plt.tight_layout()
    plt.savefig(f"{FIG_DIR}/viz2_boxplot.png", dpi=150)
    plt.close()


def viz_island(df: pd.DataFrame) -> None:
    """图3：各岛屿上不同种类企鹅的数量 —— 展示种类的地理分布。"""
    counts = df.groupby(["island", "species"]).size().unstack(fill_value=0)
    counts.plot(kind="bar", figsize=(8, 6))
    plt.title("图3  各岛屿企鹅种类数量分布")
    plt.xlabel("岛屿")
    plt.ylabel("数量 (只)")
    plt.xticks(rotation=0)
    plt.legend(title="种类")
    plt.tight_layout()
    plt.savefig(f"{FIG_DIR}/viz3_island.png", dpi=150)
    plt.close()


def main() -> None:
    df = load_clean(DATA_PATH)
    describe(df)
    viz_scatter(df)
    viz_boxplot(df)
    viz_island(df)
    print(f"\n已生成 3 张可视化图表，保存在 {FIG_DIR}/ 目录下。")


if __name__ == "__main__":
    main()
