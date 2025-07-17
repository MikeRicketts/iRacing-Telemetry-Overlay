"""
Graph Overlay Component

Displays real-time throttle and brake inputs as a scrolling line graph.
"""

from PyQt5 import QtWidgets, QtCore, QtGui


class GraphOverlay(QtWidgets.QWidget):
    """Graph overlay for displaying throttle and brake inputs over time."""
    
    RESIZE_MARGIN = 10

    def __init__(self, ir_client):
        """Initialize the graph overlay with the iRacing client."""
        super().__init__()
        self.ir_client = ir_client
        self.setWindowFlags(
            QtCore.Qt.WindowStaysOnTopHint |
            QtCore.Qt.FramelessWindowHint |
            QtCore.Qt.Tool
        )
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setAttribute(QtCore.Qt.WA_ShowWithoutActivating)
        self.setWindowTitle('iRacing Graph Overlay')
        self.setGeometry(600, 500, 900, 300)
        
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
        
        # Telemetry history for graphs
        self.throttle_history = []
        self.brake_history = []
        self.max_history_points = 100  # ~5 seconds at 20fps

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
        """Paint the overlay with the input graph."""
        telemetry = self.ir_client.get_telemetry()
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        rect = self.rect()
        
        # Draw semi-transparent background
        painter.setBrush(QtGui.QColor(20, 20, 20, 100))
        painter.setPen(QtCore.Qt.NoPen)
        painter.drawRoundedRect(rect, 20, 20)
        
        # Update telemetry history
        throttle = telemetry.get('throttle', 0)
        brake = telemetry.get('brake', 0)
        self.throttle_history.append(throttle)
        self.brake_history.append(brake)
        
        if len(self.throttle_history) > self.max_history_points:
            self.throttle_history.pop(0)
            self.brake_history.pop(0)
        
        # Draw graph
        graph_rect = QtCore.QRect(rect.left() + 10, rect.top() + 10,
                                 rect.width() - 20, rect.height() - 20)
        self._draw_input_graph(painter, graph_rect)

    def _draw_input_graph(self, painter, rect):
        """Draw the input graph with throttle and brake lines."""
        if len(self.throttle_history) < 2:
            return
        
        # Draw graph background
        painter.setBrush(QtGui.QColor(0, 0, 0, 50))
        painter.setPen(QtCore.Qt.NoPen)
        painter.drawRoundedRect(rect, 10, 10)
        
        # Draw grid lines
        painter.setPen(QtGui.QPen(QtGui.QColor(100, 100, 100), 1))
        for i in range(5):
            y = rect.top() + (rect.height() * i) // 4
            painter.drawLine(rect.left(), y, rect.right(), y)
        
        # Draw input lines
        graph_width = rect.width() - 20
        graph_height = rect.height() - 20
        graph_left = rect.left() + 10
        graph_top = rect.top() + 10
        
        # Throttle line (green)
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 255, 0), 2))
        points = []
        for i, throttle in enumerate(self.throttle_history):
            x = int(graph_left + (i * graph_width) // (len(self.throttle_history) - 1))
            y = int(graph_top + graph_height - (throttle * graph_height))
            points.append(QtCore.QPoint(x, y))
        
        if len(points) > 1:
            painter.drawPolyline(points)
        
        # Brake line (red)
        painter.setPen(QtGui.QPen(QtGui.QColor(255, 0, 0), 2))
        points = []
        for i, brake in enumerate(self.brake_history):
            x = int(graph_left + (i * graph_width) // (len(self.brake_history) - 1))
            y = int(graph_top + graph_height - (brake * graph_height))
            points.append(QtCore.QPoint(x, y))
        
        if len(points) > 1:
            painter.drawPolyline(points)
        
        # Draw labels
        font = QtGui.QFont('Segoe UI', 10, QtGui.QFont.Bold)
        painter.setFont(font)
        painter.setPen(QtGui.QPen(QtGui.QColor(255, 255, 255)))
        painter.drawText(rect.left() + 5, rect.top() + 15, "Throttle (Green) / Brake (Red)") 