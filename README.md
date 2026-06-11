# KinzyProject

A versatile collection of automation scripts, utility tools, and problem-solving hacks written primarily in PowerShell and Python. This repository serves as a personal Swiss Army knife for system administration, media processing, and workflow automation.

## 🛠️ Main Features & Scripts

### ⚙️ System Administration & Shortcuts (PowerShell)
*   **CopyToStartup.ps1:** Automates copying critical scripts or apps to the Windows Startup folder.
*   **Schedule Tasks.ps1:** Streamlines creating and managing Windows Scheduled Tasks.
*   **ShortcutWithAdmin.ps1:** Generates application shortcuts that automatically launch with Administrator privileges.
*   **Get-ShortcutIconInfo.ps1 / NewReplaceIcon.ps1:** Utilities to read, extract, and customize Windows shortcut icons.

### 🖼️ Media & Image Processing (Python)
*   **Cartoonize Image (cv2 / kmeans).py:** Converts standard images into stylized cartoon artwork using OpenCV and K-Means clustering.
*   **RemBG.py:** Automatically removes image backgrounds using machine learning.
*   **Gray Scale.py:** Quick utility for converting images to grayscale.
*   **Convert Media.py:** Batch converts audio/video files between formats.

### 🔍 File Management & Search (Python / PowerShell)
*   **Find Files.py / SearchFiles.ps1:** Fast, pattern-based file searching tools.
*   **List files.ps1:** Recursively extracts structured lists of directory contents.
*   **Pdfs.py:** Automates merging, splitting, or manipulating PDF files.

### 🌐 Automation & Networking (Python / Google Apps Script)
*   **Batch send gmails.gs:** Google Apps Script to automate mass personalized email delivery via Sheets.
*   **Battery lifesaver.py:** Monitors battery status and sends notifications to optimize battery longevity.
*   **Key Generator.py / RsaKeyGen.py:** Generates secure strings, random cryptographic keys, and RSA key pairs.

## 💻 How to Use

### Prerequisites
1.  **For Python scripts:** Install Python 3.x and required dependencies:
    ```bash
    pip install opencv-python rembg numpy pillow
    ```
2.  **For PowerShell scripts:** Ensure your execution policy allows local scripts to run:
    ```powershell
    Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
    ```

### Execution
Run any script directly from your terminal or console depending on the file type:
```bash
python "Cartoonize Image - cv2.py"
```
```powershell
.\SearchFiles.ps1
```

## 📝 License

This project is for personal utility and custom problem-solving. Feel free to use and adapt these scripts for your own automation needs.
