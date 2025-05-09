from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QPushButton, QLabel, QTextEdit, QComboBox)
from PyQt5.QtCore import Qt
import sys
from analyzer_engine import StockAnalyzerGUI  # Add this import at the top

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("妖股分析系统")
        self.setGeometry(100, 100, 800, 600)
        self.init_ui()
        
    def init_ui(self):
        # 主控件
        main_widget = QWidget()
        layout = QVBoxLayout()
        
        # 条件选择区域
        condition_layout = QHBoxLayout()
        self.market_cap_combo = QComboBox()
        self.market_cap_combo.addItems(["小市值(<50亿)", "中市值(50-200亿)", "大市值(>200亿)"])
        
        self.holder_combo = QComboBox()
        self.holder_combo.addItems(["机构持股>30%", "游资主导", "散户集中"])
        
        condition_layout.addWidget(QLabel("市值条件:"))
        condition_layout.addWidget(self.market_cap_combo)
        condition_layout.addWidget(QLabel("股东结构:"))
        condition_layout.addWidget(self.holder_combo)
        
        # 分析按钮
        self.analyze_btn = QPushButton("开始分析")
        self.analyze_btn.clicked.connect(self.analyze_stocks)
        
        # 结果显示区域
        self.result_display = QTextEdit()
        self.result_display.setReadOnly(True)
        
        # 布局组装
        layout.addLayout(condition_layout)
        layout.addWidget(self.analyze_btn)
        layout.addWidget(QLabel("分析结果:"))
        layout.addWidget(self.result_display)
        
        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)
    
    def analyze_stocks(self):
        """执行分析逻辑"""
        # 获取用户选择的条件
        market_cap = self.market_cap_combo.currentText()
        holder_type = self.holder_combo.currentText()
        
        # 调用分析引擎
        analyzer = StockAnalyzerGUI()
        results = analyzer.analyze(market_cap, holder_type)
        
        # 显示结果
        self.result_display.clear()
        self.result_display.append("分析完成！\n")
        self.result_display.append(results)