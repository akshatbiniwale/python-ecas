#Save uploaded csv locally on server
import os
import logging

def saveCsv(file=None):
    """Handle file upload.

    Expects a file to be uploaded in a POST request. 
    Saves the uploaded file to the 'uploads' directory and logs the action.

    Returns:
        JSON response with a success message or an error message.
    """
    if file is None:
        raise Exception("Error! No file uploaded", 400)
    
    uploaded_csv_path = os.path.join(os.getcwd() ,'uploads', file.filename)
    file.save(uploaded_csv_path)
    logging.info(f'Uploaded file saved at: {uploaded_csv_path}')
    return file