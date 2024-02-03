# Northbirds Course Downloader

This Python script automates the process of downloading course videos from the Northbirds platform using Selenium and Beautiful Soup. It is particularly designed for the Northbirds platform and requires credentials for authentication.

## Features

- **Automated Login**: The script automates the login process using provided credentials.
- **Course Information Extraction**: It extracts course information such as lesson title, duration, and URL.
- **Video Download**: Downloads course videos using the Vimeo downloader library.
- **Multithreading**: Utilizes multithreading for parallel video downloads, enhancing efficiency.

## Dependencies

- **Selenium**: For web automation.
- **Beautiful Soup (bs4)**: For HTML parsing.
- **requests**: For making HTTP requests.
- **pandas**: For data manipulation and storage.
- **termcolor**: For colorful console output.
- **vimeo_downloader**: For downloading Vimeo videos.

## Usage

1. Install the required dependencies using `pip`:

   ```bash
   pip install selenium beautifulsoup4 requests pandas termcolor vimeo_downloader
   ```

   or

   ```bash
   pip install -r requirements.txt
   ```

2. Download the script file (`northbirds_course_downloader.py`).

3. Provide your Northbirds login credentials (`username` and `password`) in the script.

4. Run the script:

   ```bash
   python main.py
   ```

5. The script will automate the process of logging in, extracting course information, and downloading videos.

## Note

- Ensure you have the Chrome WebDriver installed and its path configured properly for Selenium.
- This script is tailored for the Northbirds platform. Adjustments may be needed for other platforms.

## Disclaimer

- This script is for educational purposes only. Use it responsibly and respect the terms of service of the Northbirds platform.

## Author

- Created by Huaish