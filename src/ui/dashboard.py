"""
Dashboard Component

Main dashboard window that provides controls for opening overlays and displaying telemetry data.
"""

from PyQt5 import QtWidgets, QtCore, QtGui


class DashboardWindow(QtWidgets.QWidget):
    """Main dashboard window for controlling overlays and displaying telemetry."""
    
    def __init__(self, ir_client, show_text_overlay_callback, show_graph_overlay_callback):
        """Initialize the dashboard with the iRacing client and overlay callbacks."""
        super().__init__()
        self.ir_client = ir_client
        self.setWindowTitle('iRacing Dashboard')
        self.setGeometry(200, 200, 400, 400)
        
        # Layout
        layout = QtWidgets.QVBoxLayout(self)
        
        # Info labels
        self.labels = {}
        for key in ['Track', 'Session', 'Speed', 'RPM', 'Gear', 'Lap Time', 'Fuel', 'LF Temp', 'RF Temp', 'LR Temp', 'RR Temp']:
            lbl = QtWidgets.QLabel(f"{key}: ...")
            lbl.setFont(QtGui.QFont('Segoe UI', 14))
            layout.addWidget(lbl)
            self.labels[key] = lbl
        
        # Pop out overlay buttons
        self.text_overlay_btn = QtWidgets.QPushButton('Pop Out Text Overlay')
        self.text_overlay_btn.clicked.connect(show_text_overlay_callback)
        layout.addWidget(self.text_overlay_btn)
        
        self.graph_overlay_btn = QtWidgets.QPushButton('Pop Out Graph Overlay')
        self.graph_overlay_btn.clicked.connect(show_graph_overlay_callback)
        layout.addWidget(self.graph_overlay_btn)
        
        # Timer for updates
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_dashboard)
        self.timer.start(100)

    def update_dashboard(self):
        """Update the dashboard with current telemetry data."""
        telemetry = self.ir_client.get_telemetry()
        session = self.ir_client.get_session_info()
        
        self.labels['Track'].setText(f"Track: {session.get('track', '...')}")
        self.labels['Session'].setText(f"Session: {session.get('session_type', '...')}")
        self.labels['Speed'].setText(f"Speed: {telemetry.get('speed', 0):.1f} mph")
        self.labels['RPM'].setText(f"RPM: {telemetry.get('rpm', 0):.0f}")
        self.labels['Gear'].setText(f"Gear: {telemetry.get('gear', 0)}")
        self.labels['Lap Time'].setText(f"Lap Time: {telemetry.get('lap_time', 0):.2f}")
        self.labels['Fuel'].setText(f"Fuel: {telemetry.get('fuel_level', 0):.1f}")
        self.labels['LF Temp'].setText(f"LF Temp: {telemetry.get('tire_temp_LF', 0):.1f}")
        self.labels['RF Temp'].setText(f"RF Temp: {telemetry.get('tire_temp_RF', 0):.1f}")
        self.labels['LR Temp'].setText(f"LR Temp: {telemetry.get('tire_temp_LR', 0):.1f}")
        self.labels['RR Temp'].setText(f"RR Temp: {telemetry.get('tire_temp_RR', 0):.1f}") 