import os

UPLOAD_FOLDER = os.path.join(os.getcwd(), "uploads")

if os.path.exists(UPLOAD_FOLDER):
    if not os.path.isdir(UPLOAD_FOLDER):
        raise Exception(
            "'uploads' exists but it is a FILE. Delete it and create a folder named uploads."
        )
else:
    os.mkdir(UPLOAD_FOLDER)


def save_uploaded_file(uploaded_file):

    file_path = os.path.join(
        UPLOAD_FOLDER,
        uploaded_file.name
    )

    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    return file_path