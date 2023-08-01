from beanie import Document
from pydantic import BaseModel
import os
import hashlib
import motor


async def upload(db, file_path):
    fs = motor.motor_asyncio.AsyncIOMotorGridFSBucket(database=db)

    # Read file to binary
    file_name = os.path.basename(file_path)

    with open(file_path, "rb") as f:
        file_data = f.read()

    md5_hash = hashlib.md5(file_data).hexdigest()
    # file_type, encoding = mimetypes.guess_type(file_data[:1024])

    grid_in = fs.open_upload_stream(
        file_name,
        metadata={
            "contentType": "text/plain",
            "md5": md5_hash,
            # "contentType": file_type,
        },
    )

    await grid_in.write(file_data)
    await grid_in.close()  # uploaded on close
    print(f"The MD5 hash of the file is: {md5_hash}")
    return grid_in._id
