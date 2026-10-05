'''
(C) Copyright 2021 Steven;
@author: Steven kangweibaby@163.com
(C) Copyright 2026 Zhang-ikun;
@maintainer: Zhang-ikun 2439884871@qq.com
@date: 2026-10-04
'''

import numpy as np
from PIL import Image

from PySide6 import QtCore
from PySide6 import QtGui
from PySide6 import QtWidgets

from logger import logger
from dialogs.base import BaseDialog


def to_pixmap(image, max_size=(760, 600)):
    """把 PIL 图像或 numpy 数组转换成缩放后的 QPixmap。"""
    if isinstance(image, np.ndarray):
        image = Image.fromarray(image)
    image = image.convert('RGB')

    data = image.tobytes('raw', 'RGB')
    qimage = QtGui.QImage(
        data, image.width, image.height, image.width * 3,
        QtGui.QImage.Format_RGB888)
    pixmap = QtGui.QPixmap.fromImage(qimage.copy())

    if (pixmap.width() > max_size[0]) or (pixmap.height() > max_size[1]):
        pixmap = pixmap.scaled(
            QtCore.QSize(*max_size),
            QtCore.Qt.KeepAspectRatio,
            QtCore.Qt.SmoothTransformation)
    return pixmap


class DebugDialog(BaseDialog):

    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self.setWindowTitle("调试")
        self.info = {}

        self.status = QtWidgets.QLabel()
        self.status.setAlignment(QtCore.Qt.AlignCenter)
        self.status.setWordWrap(True)

        self.raw_view = QtWidgets.QLabel()
        self.board_view = QtWidgets.QLabel()
        for view in (self.raw_view, self.board_view):
            view.setAlignment(QtCore.Qt.AlignCenter)
            view.setMinimumSize(420, 340)

        tabs = QtWidgets.QTabWidget(self)
        tabs.addTab(self.raw_view, "原始截图")
        tabs.addTab(self.board_view, "棋盘裁剪")

        self.save_button = QtWidgets.QPushButton("保存原始截图...")
        self.close_button = QtWidgets.QPushButton("关闭")

        buttons = QtWidgets.QHBoxLayout()
        buttons.addWidget(self.save_button)
        buttons.addStretch(1)
        buttons.addWidget(self.close_button)

        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.status)
        layout.addWidget(tabs, 1)
        layout.addLayout(buttons)

        self.save_button.clicked.connect(self.save_image)
        self.close_button.clicked.connect(self.close)

        self.refresh()

    def refresh(self, info=None):
        self.info = info if info is not None else {}

        error = self.info.get('error')
        pred = self.info.get('pred')
        if error:
            status = f"识别失败: {error}"
        elif pred is not None:
            status = f"识别成功: {len(pred)} 个棋子"
        else:
            status = "还没有截图，请先使用「截屏」或「连线」"
        self.status.setText(status)

        self.set_view(self.raw_view, self.info.get('window'), "暂无截图")
        self.set_view(self.board_view, self.info.get('board'), "暂无棋盘")

    @staticmethod
    def set_view(view, image, empty_text):
        if image is None:
            view.clear()
            view.setText(empty_text)
            return
        view.setPixmap(to_pixmap(image))

    def save_image(self):
        image = self.info.get('window')
        if image is None:
            self.status.setText("没有可保存的截图，请先使用「截屏」或「连线」")
            return

        filename = QtWidgets.QFileDialog.getSaveFileName(
            self, "保存原始截图", "qqchess.png", "PNG 图片 (*.png)")[0]
        if not filename:
            return

        image.save(filename)
        logger.info("save debug image %s", filename)
