import cloudinary
import cloudinary.uploader
from fastapi import UploadFile
import os
from dotenv import load_dotenv

load_dotenv()

class CloudinaryService:
    def __init__(self):
        cloud_name = os.getenv("CLOUDINARY_CLOUD_NAME")
        api_key = os.getenv("CLOUDINARY_API_KEY")
        api_secret = os.getenv("CLOUDINARY_API_SECRET")
        
        print(f"DEBUG: Cloudinary Config - Name: {cloud_name}, Key: {api_key}, Secret: {'*' * 5 if api_secret else 'None'}")
        
        if not all([cloud_name, api_key, api_secret]):
            print("ERROR: Missing Cloudinary environment variables")

        cloudinary.config(
            cloud_name=cloud_name,
            api_key=api_key,
            api_secret=api_secret
        )

    def upload_image(self, file: UploadFile, folder: str = "banner_evento") -> str:
        """
        Uploads an image to Cloudinary and returns the secure URL.
        """
        try:
            upload_result = cloudinary.uploader.upload(
                file.file, folder=folder, resource_type="image"
            )
            return upload_result.get("secure_url")
        except Exception as e:
            print(f"Error uploading image to Cloudinary: {e}")
            raise e
