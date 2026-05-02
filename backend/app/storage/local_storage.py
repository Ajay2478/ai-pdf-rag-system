import os
from uuid import uuid4

# Base directory for storing uploaded files
BASE_UPLOAD_DIR = "storage/uploads"


def save_file(file) -> str:
    """
    Save uploaded file to local storage.

    Returns:
        file_path (str): Path where file is stored
    """

    # Ensure directory exists
    os.makedirs(BASE_UPLOAD_DIR, exist_ok=True)

    # Generate unique filename
    file_id = str(uuid4())
    file_extension = file.filename.split(".")[-1]
    filename = f"{file_id}.{file_extension}"

    file_path = os.path.join(BASE_UPLOAD_DIR, filename)
    
    # Normalize path (important for portability)
    file_path = file_path.replace("\\", "/")
    
    # Save file to disk
    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())

    return file_path