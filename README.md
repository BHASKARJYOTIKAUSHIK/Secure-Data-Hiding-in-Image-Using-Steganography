# Image Steganography Project

## Project Overview
This project provides a Python tool for securely hiding text messages within image files using steganography techniques. The implementation uses the Least Significant Bit (LSB) method to encode messages, making the changes virtually undetectable to the human eye while allowing for message recovery with proper authentication.

## Internship Details
- **Organization**: Edunet Foundation
- **Internship Duration**: 6 weeks (January 15, 2025 - February 26, 2025)
- **Project Category**: Data Security and Privacy

## Features
- Hide text messages in image files
- Password protection for enhanced security
- Cross-platform compatibility (Windows, macOS, Linux)
- User-friendly command-line interface
- Error handling and validation
- Image capacity verification
- Message recovery with password authentication

## Requirements
- Python 3.6 or higher
- OpenCV (cv2) library
- NumPy library

## Installation

### Step 1: Clone or download the repository
```
git clone https://github.com/yourusername/image-steganography.git
cd image-steganography
```

### Step 2: Install required dependencies
```
pip install opencv-python numpy
```

## Usage Instructions

### Step 1: Run the application
```
python steganography.py
```

### Step 2: Choose from the available options
1. **Hide a message in an image**
   - Enter the path to the cover image
   - Type your secret message
   - Create a password
   - Specify the output filename
   
2. **Recover a message from an image**
   - Enter the path to the image containing the hidden message
   - Provide the password used during encoding
   - View the decoded message

3. **Exit the application**

## How It Works

### Encoding Process
1. The original image is loaded
2. The message and password are converted to binary format
3. The least significant bit of each color channel in each pixel is modified to store the binary data
4. A delimiter is added to mark the end of the message
5. The modified image is saved to the specified location

### Decoding Process
1. The image with hidden data is loaded
2. The least significant bit of each color channel in each pixel is extracted
3. The password is verified against the stored password
4. If authentication succeeds, the binary data is converted back to text
5. The message is displayed to the user

## Example

```
===== Image Steganography Tool =====

Choose an option:
1. Hide a message in an image
2. Recover a message from an image
3. Exit

Enter your choice (1/2/3): 1

Enter the path to the cover image: nature.jpg
Enter the secret message: This is a confidential message for demonstration purposes.
Enter a password: mySecretPass123

Encoding message... Please wait.
Enter the output image filename (e.g., encrypted.png): hidden_message.png

Success! Message hidden in hidden_message.png
Image dimensions: 1920x1080
Message length: 56 characters

Would you like to view the image? (y/n): y
```

## Security Considerations
- The security of this steganography implementation depends on keeping the password secret
- Larger images can hide longer messages more securely
- Avoid compressing the output image as this might destroy the hidden data
- This tool is designed for educational purposes and may not be suitable for highly sensitive information

## Project Structure
```
image-steganography/
├── steganography.py    # Main application file
├── README.md           # Project documentation
├── examples/           # Example images before and after encoding
│   ├── original.jpg    
│   └── encoded.jpg     
└── requirements.txt    # Required dependencies
```

## Future Improvements
- Graphical user interface (GUI)
- Support for hiding messages in audio and video files
- Multiple encoding algorithms
- File encryption for hiding any file type
- Improved resistance to statistical attacks

## License
This project was developed during an internship at Edunet Foundation and is available for educational purposes.

## Acknowledgments
- Edunet Foundation for providing the internship opportunity
- OpenCV library documentation and community
- Python programming community
