# Parking Space Tracker

## Overview

This project provides a parking space detection system using OpenCV. It allows users to select a video file and detects available parking spots by analyzing video frames. The system automatically loads a corresponding reference image for better visualization.

## Features

- Select a video file from the `videos` folder using a file dialog.
- Automatically loads a corresponding image from the `img` folder.
- Detects free and occupied parking spaces.
- Uses adaptive thresholding with trackbar controls for fine-tuning.
- Displays real-time parking status overlayed on the video.

## Requirements

Ensure you have the following dependencies installed:

```bash
pip install opencv-python opencv-python-headless numpy cvzone
```

## Folder Structure

```
project_directory/
│-- main.py
│-- CarParkPos (parking positions file)
│-- polygons (alternative positions file)
│-- videos/   # Folder containing video files
│-- img/      # Folder containing reference images
```

## How to Use

1. Run the script:
   ```bash
   python main.py
   ```
2. Select a video file from the pop-up file dialog.
3. The script will automatically load the corresponding image from the `img` folder (if available).
4. Adjust threshold settings using the trackbars to fine-tune parking space detection.
5. The number of free and occupied spaces is displayed on the video.
6. Press `ESC` to exit the program.

## Configuration

- **Parking Positions**: Parking spaces are read from `CarParkPos` or `polygons`. These files store predefined parking space coordinates.
- **Threshold Trackbars**:
  - `Block Size`: Controls the size of the neighborhood for adaptive thresholding.
  - `Constant`: Fine-tunes the brightness threshold.
  - `Blur`: Applies a median blur to reduce noise.

## Example Output

The program displays the selected video with highlighted parking spots:

- **Green**: Available spot.
- **Red**: Occupied spot.

## License

This project is open-source and available under the MIT License.

## Contributing

Feel free to contribute by submitting issues or pull requests!

