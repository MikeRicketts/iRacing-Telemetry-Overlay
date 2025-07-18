"""
Text Overlay Component

Displays real-time telemetry data in a text format with customizable positioning and sizing.
"""

from PyQt5 import QtWidgets, QtCore, QtGui
import math


class TextOverlay(QtWidgets.QWidget):
    """Text overlay for displaying telemetry data in a readable format."""
    
    RESIZE_MARGIN = 10

    def __init__(self, ir_client):
        """Initialize the text overlay with the iRacing client."""
        super().__init__()
        self.ir_client = ir_client
        self.setWindowFlags(
            QtCore.Qt.WindowStaysOnTopHint |
            QtCore.Qt.FramelessWindowHint |
            QtCore.Qt.Tool
        )
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setAttribute(QtCore.Qt.WA_ShowWithoutActivating)
        self.setWindowTitle('iRacing Text Overlay')
        self.setGeometry(100, 100, 800, 400)
        
        # Timer for updates
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(50)
        
        # Mouse interaction state
        self._drag_active = False
        self._drag_position = None
        self._resize_active = False
        self._resize_dir = None
        self._resize_start_rect = None
        self._resize_start_pos = None

    def mousePressEvent(self, event):
        """Handle mouse press events for dragging and resizing."""
        if event.button() == QtCore.Qt.LeftButton:
            pos = event.pos()
            margin = self.RESIZE_MARGIN
            rect = self.rect()
            
            # Determine if near edge for resizing
            resizing = False
            if pos.x() < margin:
                self._resize_dir = 'left'
                resizing = True
            elif pos.x() > rect.width() - margin:
                self._resize_dir = 'right'
                resizing = True
            elif pos.y() < margin:
                self._resize_dir = 'top'
                resizing = True
            elif pos.y() > rect.height() - margin:
                self._resize_dir = 'bottom'
                resizing = True
            
            # Corners
            if pos.x() < margin and pos.y() < margin:
                self._resize_dir = 'topleft'
                resizing = True
            elif pos.x() > rect.width() - margin and pos.y() < margin:
                self._resize_dir = 'topright'
                resizing = True
            elif pos.x() < margin and pos.y() > rect.height() - margin:
                self._resize_dir = 'bottomleft'
                resizing = True
            elif pos.x() > rect.width() - margin and pos.y() > rect.height() - margin:
                self._resize_dir = 'bottomright'
                resizing = True
            
            if resizing:
                self._resize_active = True
                self._resize_start_rect = self.geometry()
                self._resize_start_pos = event.globalPos()
                event.accept()
                return
            
            # Otherwise, drag
            self._drag_active = True
            self._drag_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        """Handle mouse move events for dragging and resizing."""
        if self._resize_active and self._resize_dir:
            if self._resize_start_rect is None:
                return
            diff = event.globalPos() - self._resize_start_pos
            rect = self._resize_start_rect
            min_w, min_h = 150, 100
            x, y, w, h = rect.x(), rect.y(), rect.width(), rect.height()
            dir = self._resize_dir
            
            if dir == 'right':
                w = max(min_w, w + diff.x())
            elif dir == 'left':
                x = x + diff.x()
                w = max(min_w, w - diff.x())
            elif dir == 'bottom':
                h = max(min_h, h + diff.y())
            elif dir == 'top':
                y = y + diff.y()
                h = max(min_h, h - diff.y())
            elif dir == 'topleft':
                x = x + diff.x()
                w = max(min_w, w - diff.x())
                y = y + diff.y()
                h = max(min_h, h - diff.y())
            elif dir == 'topright':
                w = max(min_w, w + diff.x())
                y = y + diff.y()
                h = max(min_h, h - diff.y())
            elif dir == 'bottomleft':
                x = x + diff.x()
                w = max(min_w, w - diff.x())
                h = max(min_h, h + diff.y())
            elif dir == 'bottomright':
                w = max(min_w, w + diff.x())
                h = max(min_h, h + diff.y())
            
            self.setGeometry(x, y, w, h)
            event.accept()
            return
        
        if self._drag_active and event.buttons() & QtCore.Qt.LeftButton:
            self.move(event.globalPos() - self._drag_position)
            event.accept()

    def mouseReleaseEvent(self, event):
        """Handle mouse release events."""
        if event.button() == QtCore.Qt.LeftButton:
            self._drag_active = False
            self._resize_active = False
            self._resize_dir = None
            event.accept()

    def paintEvent(self, event):
        """Paint the overlay with telemetry data."""
        telemetry = self.ir_client.get_telemetry()
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        rect = self.rect()
        
        # Draw semi-transparent background
        painter.setBrush(QtGui.QColor(20, 20, 20, 100))
        painter.setPen(QtCore.Qt.NoPen)
        painter.drawRoundedRect(rect, 20, 20)
        
        margin = 20
        available_height = rect.height() - 2 * margin
        available_width = rect.width() - 2 * margin
        
        # Calculate layout
        steering_wheel_size = min(available_width * 0.6, available_height * 0.6)
        text_width = available_width - steering_wheel_size - 20  # 20px gap
        
        # Draw steering wheel
        wheel_rect = QtCore.QRect(
            int(rect.left() + margin),
            int(rect.top() + margin + (available_height - steering_wheel_size) // 2),
            int(steering_wheel_size),
            int(steering_wheel_size)
        )
        steering = telemetry.get('steering', 0)
        # Display the real steering angle in degrees, inverted
        steering_angle_deg = -math.degrees(steering)
        self._draw_steering_wheel(painter, wheel_rect, steering_angle_deg)
        
        # Draw text section
        text_rect = QtCore.QRect(
            int(rect.left() + margin + steering_wheel_size + 20),
            int(rect.top() + margin),
            int(text_width),
            int(available_height)
        )
        
        lines = [
            f"MPH: {telemetry.get('speed_mph', 0):.1f}",
            f"RPM: {telemetry.get('rpm', 0):.0f}",
            f"Gear: {telemetry.get('gear', 0)}"
        ]
        self._draw_text_section(painter, text_rect, lines)

    def _draw_steering_wheel(self, painter, rect, steering_angle):
        """Draw a visual steering wheel representation."""
        center_x = rect.center().x()
        center_y = rect.center().y()
        radius = min(rect.width(), rect.height()) // 2 - 10

        # steering_angle is now the real angle in degrees

        # Draw single wheel circle (white and thicker)
        painter.setPen(QtGui.QPen(QtGui.QColor(255, 255, 255), 8))
        painter.setBrush(QtCore.Qt.NoBrush)
        painter.drawEllipse(int(center_x - radius), int(center_y - radius), int(radius * 2), int(radius * 2))

        # Draw the 'center hub' as a bright cyan circle that rotates with the steering angle
        hub_radius = radius * 0.15
        hub_angle = math.radians(steering_angle - 90)  # -90 so 0 deg is top
        hub_x = center_x + radius * 0.85 * math.cos(hub_angle)
        hub_y = center_y + radius * 0.85 * math.sin(hub_angle)
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 255, 255), 2))
        painter.setBrush(QtGui.QColor(0, 255, 255))
        painter.drawEllipse(int(hub_x - hub_radius), int(hub_y - hub_radius), int(hub_radius * 2), int(hub_radius * 2))

        # Draw a line from the center to the hub (optional, for clarity)
        # painter.setPen(QtGui.QPen(QtGui.QColor(180, 180, 180), 2))
        # painter.drawLine(int(center_x), int(center_y), int(hub_x), int(hub_y))

        # Draw steering angle text at the bottom of the wheel
        font = QtGui.QFont('Segoe UI', max(8, radius // 15), QtGui.QFont.Bold)
        painter.setFont(font)
        painter.setPen(QtGui.QPen(QtGui.QColor(255, 255, 255), 1))
        angle_text = f"{steering_angle:.0f}°"
        fm = QtGui.QFontMetrics(font)
        text_width = fm.width(angle_text)
        text_x = center_x - text_width // 2
        text_y = center_y + radius + fm.height() + 5
        painter.drawText(text_x, text_y, angle_text)

    def _draw_text_section(self, painter, rect, lines):
        """Draw the text section with responsive font sizing."""
        n_lines = len(lines)
        
        # Dynamically find max font size to fit all lines
        font_size = 1
        test_font = QtGui.QFont('Segoe UI', font_size, QtGui.QFont.Bold)
        fm = QtGui.QFontMetrics(test_font)
        
        while True:
            test_font.setPointSize(font_size + 1)
            fm = QtGui.QFontMetrics(test_font)
            if fm.height() * n_lines > rect.height():
                break
            font_size += 1
        
        font = QtGui.QFont('Segoe UI', font_size, QtGui.QFont.Bold)
        painter.setFont(font)
        painter.setPen(QtGui.QPen(QtGui.QColor(255, 255, 255), 2))
        
        fm = QtGui.QFontMetrics(font)
        total_text_height = fm.height() * n_lines
        y = rect.top() + (rect.height() - total_text_height) // 2 + fm.ascent()
        
        for line in lines:
            text_width = fm.width(line)
            x = rect.left() + (rect.width() - text_width) // 2
            painter.drawText(x, y, line)
            y += fm.height() 