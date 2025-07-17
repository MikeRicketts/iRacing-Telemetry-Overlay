# iRacing Telemetry Overlay

A real-time telemetry overlay system for iRacing that provides customizable, movable, and resizable overlays for monitoring vehicle and driver data.

## Features

- **Real-time Telemetry**: Live data from iRacing including speed, RPM, gear, throttle, brake, steering, and tire temperatures
- **Dual Overlay System**: 
  - **Text Overlay**: Displays current values in a clean, readable format
  - **Graph Overlay**: Real-time scrolling graph showing throttle (green) and brake (red) inputs over time
- **Fully Customizable**: 
  - Move overlays anywhere on screen
  - Resize overlays by dragging edges/corners
  - Transparent backgrounds
  - Responsive text scaling
- **Independent Overlays**: Each overlay operates independently and can be positioned separately

## Screenshots

*Add screenshots here when available*

## Installation

### Prerequisites

- Python 3.7 or higher
- iRacing installed and running
- PyQt5

### Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/iracing-telemetry-overlay.git
cd iracing-telemetry-overlay
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python main.py
```

## Usage

1. **Start iRacing** and join a session
2. **Launch the overlay application** by running `python main.py`
3. **Open overlays** using the dashboard buttons:
   - "Pop Out Text Overlay" - Shows current telemetry values
   - "Pop Out Graph Overlay" - Shows real-time throttle/brake graph
4. **Position and resize** overlays by dragging and resizing as needed
5. **Close overlays** independently - closing one doesn't affect the other

### Controls

- **Move Overlay**: Click and drag anywhere on the overlay
- **Resize Overlay**: Drag the edges or corners of the overlay
- **Close Overlay**: Use the window close button or Alt+F4

## Project Structure

```
iracing-telemetry-overlay/
├── src/
│   ├── __init__.py
│   ├── client/
│   │   ├── __init__.py
│   │   └── iracing_client.py
│   ├── ui/
│   │   ├── __init__.py
│   │   ├── dashboard.py
│   │   ├── text_overlay.py
│   │   └── graph_overlay.py
│   └── utils/
│       ├── __init__.py
│       └── telemetry_utils.py
├── main.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Configuration

The overlays can be customized by modifying the following parameters:

- **Default Sizes**: Change initial overlay dimensions in the respective overlay classes
- **Update Frequency**: Modify timer intervals for different update rates
- **Graph History**: Adjust `max_history_points` for longer/shorter graph history
- **Colors**: Customize overlay colors and transparency levels

## Dependencies

- `PyQt5`: GUI framework
- `irsdk`: iRacing SDK for telemetry data
- `threading`: For background telemetry updates
- `json`: For session information parsing

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [irsdk](https://github.com/kutu/pyirsdk) - Python iRacing SDK
- [PyQt5](https://www.riverbankcomputing.com/software/pyqt/) - GUI framework

## Troubleshooting

### Common Issues

1. **"PyQt5 is not installed"**
   - Run: `pip install PyQt5`

2. **No telemetry data showing**
   - Ensure iRacing is running and you're in a session
   - Check that the iRacing SDK is properly installed

3. **Overlays not appearing**
   - Check that the application has permission to create windows
   - Try running as administrator if on Windows

### Support

If you encounter any issues, please:
1. Check the troubleshooting section above
2. Search existing issues on GitHub
3. Create a new issue with detailed information about your problem

## Roadmap

- [ ] Add more telemetry data (lap times, fuel consumption, etc.)
- [ ] Customizable overlay themes
- [ ] Save/load overlay positions
- [ ] Multiple graph types (speed, RPM, etc.)
- [ ] Export telemetry data
- [ ] Web-based dashboard option 