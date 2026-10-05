# 中国象棋 - 构建 / 打包脚本（GNU Make）
#
# 用法：
#   make build       打包发布版（one-folder，输出 dist/chess-<版本>/）
#   make debug       打包调试版（单文件，输出 dist/chess-<版本>-debug.exe，并复制为 dist/chess.exe）
#   make main        以源码方式运行游戏
#   make ui          由 src/ui/*.ui 重新生成界面代码
#   make bump        版本号 +1（src/version.py）
#   make clean       清理构建产物（build、*.spec、.qt_for_python）
#
# 依赖不在 PATH 的 python 里时，用 PYTHON 指定解释器：
#   make PYTHON="C:/Users/xxx/AppData/Local/Programs/Python/Python310/python.exe" build
# 界面代码生成器默认取 PATH 里的 pyside6-uic，也可单独指定：
#   make PYTHON="..." UIC="C:/.../Python310/Scripts/pyside6-uic.exe" ui
#
# 打包前请确认 pyinstaller 已装在该环境里：
#   "$(PYTHON)" -m pip install pyinstaller

PYTHON ?= python
UIC ?= pyside6-uic
PYINSTALLER = "$(PYTHON)" -m PyInstaller
VERSION := $(shell $(PYTHON) -c "from src import version; print(version.VERSION)")

# 需要打进包的数据（qqchess 里的模型和图片也要带上，否则识别功能不可用）
DATAS = --add-data "src/images;images" \
        --add-data "src/engines;engines" \
        --add-data "src/audios;audios" \
        --add-data "src/qqchess/model.pkl;qqchess" \
        --add-data "src/qqchess/images;qqchess/images"

FLAGS += --noconfirm --name chess-$(VERSION)
# FLAGS += -F     # 单文件模式（启动慢、体积大）
# FLAGS += -w     # 隐藏控制台窗口

.PHONY: build
build: check
	$(PYINSTALLER) src/main.py -i src/images/favicon.ico $(DATAS) $(FLAGS)

.PHONY: debug
debug: check
	$(PYINSTALLER) src/main.py -i src/images/favicon.ico $(DATAS) --noconfirm -F --name chess-$(VERSION)-debug
	"$(PYTHON)" -c "import shutil; shutil.copyfile('dist/chess-$(VERSION)-debug.exe', 'dist/chess.exe')"

.PHONY: main
main: ui
	"$(PYTHON)" src/main.py

.PHONY: ui
ui: src/ui/settings.py src/ui/method.py

src/ui/%.py: src/ui/%.ui
	"$(UIC)" $< -o $@

.PHONY: bump
bump:
	"$(PYTHON)" -c "from src import version; version.increase()"

.PHONY: check
check:
	@"$(PYTHON)" -c "import sys, importlib.util; mods = ['PySide6', 'cv2', 'torch', 'numpy', 'PIL', 'matplotlib', 'pygame', 'win32gui', 'keyboard', 'PyInstaller']; missing = [m for m in mods if importlib.util.find_spec(m) is None]; print('[check] python =', sys.executable); print('[check] missing modules:', missing) if missing else print('[check] ok'); sys.exit(1) if missing else None"

.PHONY: clean
clean:
	"$(PYTHON)" -c "import glob, os, shutil; [shutil.rmtree(p, ignore_errors=True) for p in ('build', '.qt_for_python')]; [os.remove(f) for f in glob.glob('*.spec')]; print('[clean] removed build/, .qt_for_python/, *.spec (dist/ kept)')"
