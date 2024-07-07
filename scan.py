import cv2
import numpy as np
import webbrowser

def initialize_camera(width=640, height=480):
    """Initialize and configure the webcam."""
    cam = cv2.VideoCapture(0)  # Open default camera (index 0)
    if not cam.isOpened():
        raise IOError("Cannot open webcam")  # Throw error if camera fails to open
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, width)  # Set camera width
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, height)  # Set camera height
    return cam

def decode_qr_code(frame, qr_code_detector):
    """Decode QR code from the camera frame."""
    decoded_text, points, _ = qr_code_detector.detectAndDecode(frame)
    return decoded_text, points

def draw_bounding_box(frame, points, decoded_text):
    """Draw bounding box around QR code and optionally display decoded text."""
    if points is not None:
        points = np.int32(points).reshape(-1, 2)
        for i in range(len(points)):
            pt1 = tuple(points[i])
            pt2 = tuple(points[(i + 1) % len(points)])
            cv2.line(frame, pt1, pt2, color=(0, 255, 0), thickness=2)
        
        if decoded_text:
            x, y = points[0]
            cv2.putText(frame, decoded_text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            # Check if the decoded text is a URL and open it in a web browser
            if decoded_text.startswith('http://') or decoded_text.startswith('https://'):
                try:
                    webbrowser.open(decoded_text)  # Attempt to open URL in default web browser
                except Exception as e:
                    print(f"Failed to open URL: {e}")  # Print error if URL opening fails

def qr_code_scanner():
    """Main function to capture frames, detect QR codes, and display results."""
    cam = initialize_camera()
    qr_code_detector = cv2.QRCodeDetector()

    while True:
        try:
            success, frame = cam.read()  # Read frame from camera
            if not success:
                print("Failed to capture image")
                break

            decoded_text, points = decode_qr_code(frame, qr_code_detector)  # Decode QR code from frame
            if decoded_text:
                print(f"Decoded Text: {decoded_text}")  # Print decoded text to console

            draw_bounding_box(frame, points, decoded_text)  # Draw bounding box around QR code and display text
            cv2.imshow("QR Code Scanner", frame)  # Display frame with bounding box

            # Exit if 'q' is pressed
            key = cv2.waitKey(1)  # Wait for a key press for 1 millisecond
            if key & 0xFF == ord('q'):  # Check if 'q' key is pressed
                break

        except KeyboardInterrupt:
            break  # Exit loop if Ctrl+C is pressed
        except Exception as e:
            print(f"Error occurred: {e}")  # Print any unexpected errors

    cam.release()  # Release the camera
    cv2.destroyAllWindows()  # Close all OpenCV windows

if __name__ == "__main__":
    qr_code_scanner()  # Run the QR code scanner
