# 📸 Face Recognition Attendance System

A Streamlit web application designed to manage attendance using facial recognition technology. The system allows for enrolling new individuals by capturing their face images and subsequently marking their attendance by recognizing their faces through a live camera feed.

## ✨ Features

* **Enrollment:** Capture and store face images for new students/individuals.
* **Attendance Marking:** Detect and recognize faces from a live camera feed to mark attendance automatically.
* **Attendance Logging:** Records attendance with timestamps in daily CSV files.
* **Web Interface:** User-friendly interface built with Streamlit.

## 🛠️ Tech Stack

* **Backend:** Python
* **Web Framework:** Streamlit
* **Face Recognition:** `face_recognition` (built on top of `dlib`)
* **Image Processing:** OpenCV (`opencv-python`)
* **Numerical Operations:** NumPy
* **System Dependencies:** CMake

## 📋 Prerequisites

* **Python:** Version 3.7+ recommended.
* **CMake:** Required by `dlib`. The project includes a script to install it on Debian-based systems (like Ubuntu).
* **C++ Compiler:** Required by `dlib` (usually comes with build-essential tools on Linux).
* **pip:** Python package installer.
* **Web Camera:** A functional webcam connected to the system.

## ⚙️ Installation

Follow these steps to set up the project environment:

1.  **Clone the Repository (Optional):**
    If you haven't already, clone the repository to your local machine:
    ```bash
    git clone <your-repository-url>
    cd <repository-directory>
    ```

2.  **Install System Dependencies (CMake):**
    The `dlib` library, a core dependency for `face_recognition`, requires CMake. A script is provided to install it on Debian/Ubuntu systems. Run it with root privileges:
    ```bash
    sudo bash install_cmake.sh
    ```
    *Note: If you are on a different OS (macOS, Windows), you'll need to install CMake using the appropriate method for your system (e.g., `brew install cmake` on macOS, download installer from [cmake.org](https://cmake.org/download/) for Windows).*

3.  **Create a Virtual Environment (Recommended):**
    It's best practice to create a virtual environment to manage project dependencies.
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

4.  **Install Python Dependencies:**
    Install all the required Python packages listed in `requirements.txt`. This step might take some time, especially for `dlib`.
    ```bash
    pip install --no-cache-dir -r requirements.txt
    ```
    *Note: The `--no-cache-dir` flag is included as in `deploy.sh`, which can sometimes help avoid issues with cached packages.*

## ▶️ Usage

1.  **Run the Application:**
    You can start the Streamlit application using the `deploy.sh` script (which also handles dependency installation if needed) or directly using the `streamlit` command:

    * **Using the deploy script:**
        ```bash
        bash deploy.sh
        ```
        *(Note: `deploy.sh` internally runs `install_cmake.sh` and `pip install`, then starts the app. You might need `sudo` if `install_cmake.sh` hasn't been run successfully before).*

    * **Directly with Streamlit (after installation):**
        Make sure your virtual environment is activated.
        ```bash
        streamlit run app.py
        ```

2.  **Access the Application:**
    Open your web browser and navigate to the local URL provided by Streamlit (usually `http://localhost:8501`).

3.  **Enroll New Students:**
    * Navigate to the "Enroll" page using the sidebar.
    * Enter the student's name in the text input field.
    * The camera feed will start. Position the student's face clearly in the frame.
    * Click the "📸 Capture Image" button. The application will save the image.
    * Click "❌ Stop Camera" when done.
    * Enrollment images are saved under the `enrollment_images/<Student Name>/` directory.

4.  **Mark Attendance:**
    * Navigate to the "Mark Attendance" page using the sidebar.
    * Click the "▶️ Start Camera" button.
    * The application will load known faces from the `enrollment_images` directory.
    * The camera feed will start. The system will attempt to recognize faces in the frame.
    * Recognized individuals who haven't been marked present yet for the day will be logged. A success message will appear in the app.
    * Detected faces are highlighted with bounding boxes (Green for known, Red for unknown).
    * Click the "❌ Stop Camera" button to stop the attendance process.
    * Attendance logs are saved in the `attendance_logs/` directory as `attendance_YYYY-MM-DD.csv`.

## 📁 Project Structure

```
.
├── enrollment_images/      # Directory to store captured face images for enrollment
│   └── <Student Name>/
│       └── <image_files>.png
├── attendance_logs/        # Directory to store daily attendance CSV files
│   └── attendance_YYYY-MM-DD.csv
├── app.py                  # Main Streamlit application script
├── attendance.py           # Handles loading known faces and marking attendance logic
├── enroll.py               # Handles the student enrollment image capture logic
├── deploy.sh               # Deployment script (installs dependencies, runs app)
├── install_cmake.sh        # Script to install CMake on Debian-based systems
├── packages.txt            # Lists system packages (CMake) - informational
├── requirements.txt        # Python package dependencies
└── README.md               # This file
```

## ⚙️ Configuration

Some parameters can be adjusted directly in the Python scripts:

* **`app.py`:**
    * `CAPTURE_COUNT`: Number of images to capture per enrollment (currently 1).
    * `RESIZE_FACTOR`: Factor to resize frames for faster processing during attendance (currently 0.25).
    * `MODEL`: Face detection model ("hog" - faster, less accurate; "cnn" - slower, more accurate, requires GPU support for speed).
    * `TOLERANCE`: How strict the face comparison is (lower means stricter). Default is 0.55.
* **`attendance.py`:**
    * `ENROLLMENT_FOLDER`: Name of the folder storing enrollment images.
    * `ATTENDANCE_LOG_FOLDER`: Name of the folder storing attendance logs.
    * `TOLERANCE`, `MODEL`: Consistent settings used when loading faces.
* **`enroll.py`:**
    * `ENROLLMENT_FOLDER`: Consistent folder name.
    * `ENROLL_IMG_FORMAT`: Image format for saved enrollment pictures (e.g., ".png").

## ❓ Troubleshooting

* **CMake Installation Failed:** Ensure `install_cmake.sh` is run with `sudo`. If using a different OS, install CMake manually. Make sure you have build tools (`sudo apt-get install build-essential` on Debian/Ubuntu).
* **`dlib` Installation Failed:** This is often related to missing CMake or a C++ compiler. Verify prerequisites. Installation can take a long time.
* **Camera Not Found/Working:**
    * Ensure your webcam is properly connected and drivers are installed.
    * Check if another application is using the camera.
    * Verify the camera index in `cv2.VideoCapture(0)`. If you have multiple cameras, you might need to change `0` to `1`, `2`, etc.
* **Low Recognition Accuracy:**
    * Ensure good lighting conditions during enrollment and attendance.
    * Enroll faces with neutral expressions and facing the camera directly.
    * Adjust the `TOLERANCE` value in `app.py` and `attendance.py` (try values between 0.5 and 0.6).
    * Consider using the `cnn` model if accuracy is critical and your hardware supports it (will be much slower without a GPU).

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs, feature requests, or improvements.

1.  Fork the repository.
2.  Create a new branch (`git checkout -b feature/YourFeature`).
3.  Make your changes.
4.  Commit your changes (`git commit -m 'Add some feature'`).
5.  Push to the branch (`git push origin feature/YourFeature`).
6.  Open a Pull Request.

## 📜 License

MIT License

