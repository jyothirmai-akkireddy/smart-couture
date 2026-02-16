import cv2
import numpy as np
from PIL import Image
import io

class ImageProcessor:
    """Image processing for skin tone detection and virtual try-on"""
    
    def detect_skin_tone(self, image_path):
        """
        Detect skin tone from uploaded image
        Returns: skin tone category (fair, light, medium, tan, deep)
        """
        try:
            # Read image
            img = cv2.imread(image_path)
            if img is None:
                return 'medium'  # default
            
            # Convert to RGB
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            
            # Convert to HSV for better skin detection
            img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            
            # Define skin color range in HSV
            lower_skin = np.array([0, 20, 70], dtype=np.uint8)
            upper_skin = np.array([20, 255, 255], dtype=np.uint8)
            
            # Create mask for skin pixels
            mask = cv2.inRange(img_hsv, lower_skin, upper_skin)
            
            # Get skin pixels
            skin_pixels = img_rgb[mask > 0]
            
            if len(skin_pixels) == 0:
                return 'medium'  # default
            
            # Calculate average RGB values
            avg_color = np.mean(skin_pixels, axis=0)
            
            # Calculate brightness
            brightness = np.mean(avg_color)
            
            # Categorize skin tone based on brightness
            if brightness > 200:
                return 'fair'
            elif brightness > 170:
                return 'light'
            elif brightness > 140:
                return 'medium'
            elif brightness > 110:
                return 'tan'
            else:
                return 'deep'
        
        except Exception as e:
            print(f"Error detecting skin tone: {e}")
            return 'medium'
    
    def process_for_virtual_tryon(self, user_image_path, clothing_image_path):
        """
        Simple virtual try-on using image overlay
        This is a basic implementation - production would use more advanced CV
        """
        try:
            # Read images
            user_img = cv2.imread(user_image_path)
            clothing_img = cv2.imread(clothing_image_path)
            
            if user_img is None or clothing_img is None:
                return None
            
            # Resize clothing to fit on user (simple overlay)
            h, w = user_img.shape[:2]
            clothing_resized = cv2.resize(clothing_img, (w//2, h//2))
            
            # Calculate position (center of image)
            y_offset = h // 4
            x_offset = w // 4
            
            # Create overlay
            result = user_img.copy()
            
            # Blend clothing onto user image
            y1, y2 = y_offset, y_offset + clothing_resized.shape[0]
            x1, x2 = x_offset, x_offset + clothing_resized.shape[1]
            
            if y2 <= h and x2 <= w:
                # Simple alpha blending
                alpha = 0.6
                result[y1:y2, x1:x2] = cv2.addWeighted(
                    result[y1:y2, x1:x2], 1-alpha,
                    clothing_resized, alpha, 0
                )
            
            return result
        
        except Exception as e:
            print(f"Error in virtual try-on: {e}")
            return None
    
    def save_processed_image(self, image, output_path):
        """Save processed image"""
        try:
            cv2.imwrite(output_path, image)
            return True
        except Exception as e:
            print(f"Error saving image: {e}")
            return False
    
    def compress_image(self, image_path, max_size_kb=500):
        """Compress image for faster loading"""
        try:
            img = Image.open(image_path)
            
            # Convert RGBA to RGB if necessary
            if img.mode == 'RGBA':
                img = img.convert('RGB')
            
            # Calculate quality based on file size
            quality = 85
            output = io.BytesIO()
            img.save(output, format='JPEG', quality=quality, optimize=True)
            
            # Reduce quality until size is acceptable
            while output.tell() > max_size_kb * 1024 and quality > 20:
                output = io.BytesIO()
                quality -= 5
                img.save(output, format='JPEG', quality=quality, optimize=True)
            
            # Save compressed image
            with open(image_path, 'wb') as f:
                f.write(output.getvalue())
            
            return True
        
        except Exception as e:
            print(f"Error compressing image: {e}")
            return False
