"""
Telemetry Utilities

Helper functions for processing and formatting telemetry data.
"""


def format_speed(speed_mph):
    """Format speed value for display."""
    return f"{speed_mph:.1f} mph"


def format_rpm(rpm):
    """Format RPM value for display."""
    return f"{rpm:.0f}"


def format_lap_time(lap_time):
    """Format lap time value for display."""
    return f"{lap_time:.2f}"


def format_fuel_level(fuel_level):
    """Format fuel level value for display."""
    return f"{fuel_level:.1f}"


def format_tire_temp(temp):
    """Format tire temperature value for display."""
    return f"{temp:.1f}"


def format_percentage(value):
    """Format percentage value for display."""
    return f"{value * 100:.0f}%"


def format_steering_angle(steering):
    """Format steering angle value for display."""
    return f"{steering * 180:.0f}°"


def get_telemetry_display_data(telemetry):
    """Get formatted telemetry data for display."""
    return {
        'speed': format_speed(telemetry.get('speed', 0)),
        'rpm': format_rpm(telemetry.get('rpm', 0)),
        'gear': telemetry.get('gear', 0),
        'lap_time': format_lap_time(telemetry.get('lap_time', 0)),
        'fuel_level': format_fuel_level(telemetry.get('fuel_level', 0)),
        'steering': format_steering_angle(telemetry.get('steering', 0)),
        'throttle': format_percentage(telemetry.get('throttle', 0)),
        'brake': format_percentage(telemetry.get('brake', 0)),
        'tire_temp_LF': format_tire_temp(telemetry.get('tire_temp_LF', 0)),
        'tire_temp_RF': format_tire_temp(telemetry.get('tire_temp_RF', 0)),
        'tire_temp_LR': format_tire_temp(telemetry.get('tire_temp_LR', 0)),
        'tire_temp_RR': format_tire_temp(telemetry.get('tire_temp_RR', 0)),
    } 