"""
iRacing Telemetry Overlay

Main application entry point for the iRacing telemetry overlay system.
"""

import sys

# PyQt5 imports
try:
    from PyQt5 import QtWidgets
except ImportError:
    print('PyQt5 is not installed. Please run: pip install PyQt5')
    sys.exit(1)

# Local imports
from src.client.iracing_client import IRacingClient
from src.ui.dashboard import DashboardWindow
from src.ui.text_overlay import TextOverlay
from src.ui.graph_overlay import GraphOverlay


def main():
    """Main application entry point."""
    app = QtWidgets.QApplication(sys.argv)
    
    # Initialize iRacing client
    ir_client = IRacingClient()
    
    # Overlay instances
    text_overlay = None
    graph_overlay = None

    def show_text_overlay():
        """Show or activate the text overlay."""
        nonlocal text_overlay
        if text_overlay is None or not text_overlay.isVisible():
            text_overlay = TextOverlay(ir_client)
            text_overlay.show()
        else:
            text_overlay.activateWindow()
            text_overlay.raise_()

    def show_graph_overlay():
        """Show or activate the graph overlay."""
        nonlocal graph_overlay
        if graph_overlay is None or not graph_overlay.isVisible():
            graph_overlay = GraphOverlay(ir_client)
            graph_overlay.show()
        else:
            graph_overlay.activateWindow()
            graph_overlay.raise_()

    # Create and show dashboard
    dashboard = DashboardWindow(ir_client, show_text_overlay, show_graph_overlay)
    dashboard.show()
    
    # Run application
    exit_code = app.exec_()
    
    # Cleanup
    ir_client.stop()
    sys.exit(exit_code)


if __name__ == '__main__':
    main()