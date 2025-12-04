import cloudinary
import cloudinary.uploader
from fastapi import UploadFile
import os
from dotenv import load_dotenv

load_dotenv()

class CloudinaryService:
    def __init__(self):
        cloudinary.config(
            cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
            api_key=os.getenv("CLOUDINARY_API_KEY"),
            api_secret=os.getenv("CLOUDINARY_API_SECRET")
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
