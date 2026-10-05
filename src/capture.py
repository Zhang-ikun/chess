import ctypes

import win32gui
import win32ui
from PIL import Image
from PIL import ImageGrab


def _is_black(image: Image.Image) -> bool:
    """判断截图是否整幅全黑。"""
    extrema = image.getextrema()
    if isinstance(extrema[0], tuple):
        return all(channel[1] == 0 for channel in extrema)
    return extrema[1] == 0


def _print_window(hwnd, width, height):
    # https://timgolden.me.uk/pywin32-docs/win32gui.html
    # returns the device context (DC) for the entire window,
    # including title bar, menus, and scroll bars.
    hwndDC = win32gui.GetWindowDC(hwnd)
    try:
        # Creates a PyCDC object from an integer handle.
        mfcDC = win32ui.CreateDCFromHandle(hwndDC)
        # Creates a memory DC compatible with this DC.
        saveDC = mfcDC.CreateCompatibleDC()
        # Create a bitmap object.
        saveBitMap = win32ui.CreateBitmap()
        restore = None
        try:
            # Creates a bitmap compatible with the specified device context.
            saveBitMap.CreateCompatibleBitmap(mfcDC, width, height)
            # Selects an object into the DC.
            restore = saveDC.SelectObject(saveBitMap)
            # PW_CLIENTONLY | PW_RENDERFULLCONTENT
            ctypes.windll.user32.PrintWindow(
                hwnd, saveDC.GetSafeHdc(), 3)
            bmpinfo = saveBitMap.GetInfo()
            bmpstr = saveBitMap.GetBitmapBits(True)
            return Image.frombuffer(
                'RGB',
                (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
                bmpstr, 'raw', 'BGRX', 0, 1)
        finally:
            # release object
            if restore is not None:
                saveDC.SelectObject(restore)
            handle = saveBitMap.GetHandle()
            if handle:
                win32gui.DeleteObject(handle)
            saveDC.DeleteDC()
            mfcDC.DeleteDC()
    finally:
        win32gui.ReleaseDC(hwnd, hwndDC)


def _grab_screen(left, top, right, bottom):
    """直接截取窗口在屏幕上占据的区域（适用于 GPU 渲染的窗口）。"""
    try:
        return ImageGrab.grab(
            bbox=(left, top, right, bottom), all_screens=True)
    except Exception:
        return None


def capture(window_name):

    # https://learn.microsoft.com/en-us/windows/win32/api/shellscalingapi/nf-shellscalingapi-setprocessdpiawareness
    # 按物理像素抓图，避免高 DPI 缩放下坐标错位
    PROCESS_PER_MONITOR_DPI_AWARE = 2
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(
            PROCESS_PER_MONITOR_DPI_AWARE)
    except OSError:
        pass

    hwnd = win32gui.FindWindow(None, window_name)
    if not hwnd:
        return None
    if win32gui.IsIconic(hwnd):
        return None

    left, top, right, bot = win32gui.GetWindowRect(hwnd)
    width = right - left
    height = bot - top
    if width <= 0 or height <= 0:
        return None

    # 老客户端是 GDI 渲染，PrintWindow 可直接抓取；
    # 新版客户端是 GPU 合成渲染，PrintWindow 只能得到全黑图像，
    # 此时回退为直接截取窗口在屏幕上的区域。
    try:
        image = _print_window(hwnd, width, height)
    except Exception:
        image = None
    if image is None or _is_black(image):
        image = _grab_screen(left, top, right, bot)
    return image
