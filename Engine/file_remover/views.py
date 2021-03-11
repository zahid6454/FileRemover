import os, shutil, datetime
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse


@api_view(['POST'])
def index(request):
    if request.method == 'POST':
        # Getting POSTMAN request data
        data = JSONParser().parse(request)

        # Retrieving threshold from the data
        days_threshold = data['days_threshold']

        # Setting the Temp directory path
        dir_path = 'C:/Windows/Temp/'

        # Collecting the file and folder path inside the Temp directory
        elements = os.listdir(dir_path)

        # Storing the path of file and folder as Keys inside dictionary and the date as their values
        all_file_folder = {}
        for element in elements:
            element_path = dir_path+element
            date_time = datetime.datetime.fromtimestamp(os.stat(dir_path+element).st_mtime)
            all_file_folder[element_path] = date_time

        # Getting today's date-time
        current_date = datetime.datetime.now()

        # Declaring two dictionary for display purpose
        deleted_file    = {}
        deleted_folder  = {}

        # Going through every file path and calculating the date-time difference between every file or folder with
        # today's date-time. If the difference between a file or folder's date-time is greater than days_threshold then
        # remove that file or folder.
        file_count = 0
        folder_count = 0

        # Checking if the directory exists or not
        if os.path.isdir(dir_path):

            # Looping over every file or folder for condition checking
            for file_folder_path, file_folder_date in all_file_folder.items():
                delta = current_date - file_folder_date

                # Checking if the file or folder's date-time is greater than days_threshold or not
                if delta.days > days_threshold:

                    # Checking if the file_folder_path is a directory or not
                    if os.path.isdir(file_folder_path):

                        # Try-Except to avoid deleting folder that can raise permission access error
                        try:
                            folder_count += 1
                            name = f'Folder {folder_count}'
                            shutil.rmtree(file_folder_path)
                            deleted_folder[name] = {'Path': file_folder_path,
                                                    'Date-Time': file_folder_date,
                                                    'Days Difference': delta.days}
                        except Exception as exception:
                            return JsonResponse({
                                'Status_Code': status.HTTP_200_OK,
                                'Folder Path': file_folder_path,
                                'Message': 'Folder Delete Permission Denied !!',
                                'Response': {
                                    'Deleted Files': deleted_file,
                                    'Deleted Folders': deleted_folder,
                                }
                            })

                    # Checking if the file_folder_path is a file or not
                    elif os.path.isfile(file_folder_path):

                        # Try-Except to avoid deleting file that can raise permission access error
                        try:
                            file_count += 1
                            name = f'File {file_count}'
                            os.remove(file_folder_path)
                            deleted_file[name] = {'Path': file_folder_path,
                                                  'Date-Time': file_folder_date,
                                                  'Days Difference': delta.days}
                        except Exception as exception:
                            return JsonResponse({
                                'Status_Code': status.HTTP_200_OK,
                                'File Path': file_folder_path,
                                'Message': 'File Delete Permission Denied !!',
                                'Response': {
                                    'Deleted Files': deleted_file,
                                    'Deleted Folders': deleted_folder,
                                }
                            })

                    else:
                        return JsonResponse({
                            'Status_Code': status.HTTP_200_OK,
                            'Response': {
                                'Message': 'No Such File or Folder Exceeds The Date-Time Threshold !!'
                            }
                        })

            return JsonResponse({
                'Status_Code': status.HTTP_200_OK,
                'Response': {
                    'Deleted Files': deleted_file,
                    'Deleted Folders': deleted_folder,
                }
            })

        else:
            return JsonResponse({
                'Status_Code': status.HTTP_200_OK,
                'Response': {
                    'Message': 'Directory Does Not Exist !!'
                }
            })
