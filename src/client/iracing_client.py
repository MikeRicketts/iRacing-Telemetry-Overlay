"""
iRacing Telemetry Client

Handles connection to iRacing and provides real-time telemetry data.
"""

import threading
import time
import json
import irsdk


class IRacingClient:
    """Client for connecting to iRacing and retrieving telemetry data."""
    
    def __init__(self):
        """Initialize the iRacing client with background telemetry updates."""
        self.ir = irsdk.IRSDK()
        self.is_connected = False
        self.lock = threading.Lock()
        self.telemetry = {}
        self.session_info = {}
        self.running = True
        self.thread = threading.Thread(target=self._update_loop, daemon=True)
        self.thread.start()

    def connect(self):
        """Attempt to connect to iRacing."""
        if not self.ir.is_initialized:
            self.ir.startup()
        self.is_connected = self.ir.is_initialized and self.ir.is_connected
        return self.is_connected

    def _update_loop(self):
        """Background thread that continuously updates telemetry data."""
        while self.running:
            if self.connect():
                with self.lock:
                    self.telemetry = self._get_telemetry()
                    self.session_info = self._get_session_info()
            time.sleep(0.05)

    def _get_telemetry(self):
        """Extract telemetry data from iRacing."""
        try:
            return {
                'speed': self.ir['Speed'],
                'rpm': self.ir['RPM'],
                'gear': self.ir['Gear'],
                'lap_time': self.ir['LapCurrentLapTime'],
                'fuel_level': self.ir['FuelLevel'],
                'steering': self.ir['SteeringWheelAngle'],
                'throttle': self.ir['Throttle'],
                'brake': self.ir['Brake'],
                'clutch': self.ir['Clutch'],
                'tire_temp_LF': self.ir['LFtempCL'],
                'tire_temp_RF': self.ir['RFtempCL'],
                'tire_temp_LR': self.ir['LRtempCL'],
                'tire_temp_RR': self.ir['RRtempCL'],
            }
        except Exception:
            return {}

    def _get_session_info(self):
        """Extract session information from iRacing."""
        try:
            # Use get_session_info_string to get JSON, then parse
            info_str = self.ir.get_session_info_string()
            if not info_str:
                return {}
            info = json.loads(info_str)
            track = info.get('WeekendInfo', {}).get('TrackName', '')
            session_num = self.ir['SessionNum'] if 'SessionNum' in self.ir.var_headers else 0
            sessions = info.get('SessionInfo', {}).get('Sessions', [])
            session_type = sessions[session_num]['SessionType'] if session_num < len(sessions) else ''
            session_time = self.ir['SessionTime'] if 'SessionTime' in self.ir.var_headers else 0
            session_laps = self.ir['SessionLapsRemain'] if 'SessionLapsRemain' in self.ir.var_headers else 0
            return {
                'track': track,
                'session_type': session_type,
                'session_time': session_time,
                'session_laps': session_laps
            }
        except Exception:
            return {}

    def get_telemetry(self):
        """Get a copy of the current telemetry data."""
        with self.lock:
            return self.telemetry.copy()

    def get_session_info(self):
        """Get a copy of the current session information."""
        with self.lock:
            return self.session_info.copy()

    def stop(self):
        """Stop the background telemetry updates."""
        self.running = False
        self.thread.join() 