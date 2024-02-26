import pandas as pd
import time
from django.shortcuts import render, redirect
from django.http import JsonResponse,HttpResponse #for login
from django.conf import settings
from django.http import FileResponse
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import os
import json

# Index page calling function
def index(request):
    return render(request, 'voting_web/index.html')


def panel(request):
    return render(request, 'voting_web/panel_po.html')

def register_user(request):
    # Your view logic goes here
    return render(request, 'voting_web/register_user.html')

def home_view(request):
    return render(request, 'voting_web/index.html') 

# login page password checker and calling function
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        excel_path = os.path.join(settings.BASE_DIR,'voting_web', 'data', 'pollingOfficerLogin.xlsx')
        
        # Load the Excel file
        df = pd.read_excel(excel_path)
        
        # Check if any row matches the username and password
        if any((df['username'] == username) & (df['password'] == password)):
            # Redirect to the next page (replace 'next-page' with your desired URL)
            return redirect('panel')
        else:
            # If no match is found
            return JsonResponse({'success': False, 'message': 'Password wrong'})
    
    return render(request, 'voting_web/login_po.html')  # Replace 'voting_web' with your app's name


def add_user(request):
    if request.method == 'POST':
        username = request.POST.get('userid')
        password = request.POST.get('Password')

        excel_path = os.path.join(settings.BASE_DIR, 'voting_web', 'data', 'pollingOfficerLogin.xlsx')

        # Load the Excel file
        df = pd.read_excel(excel_path)

        # Create a new DataFrame for the new user
        new_user = pd.DataFrame({'username': [username], 'password': [password]})

        # Concatenate the new user DataFrame with the original DataFrame
        df = pd.concat([df, new_user], ignore_index=True)

        # Save the updated DataFrame back to the Excel file
        df.to_excel(excel_path, index=False)

        # Return a JSON response indicating success
        return JsonResponse({'success': True, 'message': 'User added successfully'})

    # If it's not a POST request, return an error response
    return JsonResponse({'success': False, 'message': 'Invalid request'})

def show_results(request):
    excel_path = os.path.join(settings.BASE_DIR, 'voting_web', 'data', 'Votes.xlsx')
    df = pd.read_excel(excel_path)

    # Check if the DataFrame is empty
    if df.empty:
        return JsonResponse({'success': False, 'message': 'No votes have been recorded yet.'})

    # Calculate the winner
    winner = df[df['Votes_Count'] == df['Votes_Count'].max()]['Party_Name'].values[0]

    # Sort the DataFrame by Votes_Count in ascending order
    df_sorted = df.sort_values(by='Votes_Count')

    # Generate a message with the results
    result_message = f"Winner: {winner}\n\nResults:\n"
    
    for index, row in df_sorted.iterrows():
        result_message += f"{row['Party_Name']}: {row['Votes_Count']}\n"

    # Display the message in a single alert box
    return JsonResponse({'success': True, 'message': result_message})

def reset_votes(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        entered_password = data.get('password')
        
        # Check if the entered password is correct
        expected_password = "Admin123"  # Set your expected password here
        if entered_password == expected_password:
            # Password is correct, reset the Votes Excel file
            excel_path = os.path.join(settings.BASE_DIR, 'voting_web', 'data', 'Votes.xlsx')
            
            # Load the Excel file
            df = pd.read_excel(excel_path)
            
            # Reset all vote counts to 0
            df['Votes_Count'] = 0
            
            # Save the updated Excel file
            df.to_excel(excel_path, index=False)
            
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False})
    
    # return HttpResponseNotAllowed(['POST'])



def increase_vote(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        selected_color = data.get('color')

        excel_path = os.path.join(settings.BASE_DIR, 'voting_web', 'data', 'Votes.xlsx')

        # Load the Excel file
        df = pd.read_excel(excel_path)

        # Increase the vote count for the selected color
        df.loc[df['Party_Name'] == selected_color, 'Votes_Count'] += 1

        # Save the updated Excel file
        df.to_excel(excel_path, index=False)

        # Return a JSON response indicating success
        return JsonResponse({'success': True})  # Return a valid JSON response

    return JsonResponse({'success': False})  # Return a valid JSON response



def vote_panel(request):
    return render(request, 'voting_web/vote_panel.html')


import os
import base64
from django.shortcuts import render, redirect
from django.contrib import messages  # Import the messages module
from django.conf import settings
from django.core.files.storage import FileSystemStorage

# Define the path to the user_data directory
user_data_dir = os.path.join(settings.BASE_DIR, 'voting_web','data', 'user_data')

# def register_user(request):
#     if request.method == 'POST':
#         voter_id = request.POST.get('voterID')
#         captured_image_data = request.POST.get('capturedImageData')  # Get the captured image data

#         # Create a folder with the same name as the Voter ID
#         user_folder = os.path.join(user_data_dir, voter_id)

#         try:
#             # Create the folder if it doesn't exist
#             os.makedirs(user_folder)
#         except FileExistsError:
#             pass  # Folder already exists

#         if captured_image_data:
#             # Decode the base64 image data
#             image_data = base64.b64decode(captured_image_data)

#             # Save the decoded image data to a file
#             with open(os.path.join(user_folder, 'profile_image.jpg'), 'wb') as image_file:
#                 image_file.write(image_data)

#             # Use Django messages to send a success message to the next page
#             messages.success(request, 'Registration successful!')

#             # Redirect to the vote_panel page or any other page as needed
#             return redirect('index')

#     return render(request, 'voting_web/register_user.html')


# Define the path to the Excel file
excel_file_path = os.path.join(settings.BASE_DIR, 'voting_web', 'data', 'user_data', 'user_database.xlsx')

def register_user(request):
    if request.method == 'POST':
        voter_id = request.POST.get('voterID')
        digital_id = request.POST.get('digitalID')
        captured_image_data = request.POST.get('capturedImageData')  # Get the data URL
        
        if captured_image_data:
            # Decode the data URL to binary data
            image_data = captured_image_data.split(",")[-1].encode()
            
            # Create a folder with the same name as the Voter ID
            user_folder = os.path.join(user_data_dir, voter_id)
            
            try:
                # Create the folder if it doesn't exist
                os.makedirs(user_folder)
            except FileExistsError:
                pass  # Folder already exists
            
            # Save the image data as a file in the folder
            with open(os.path.join(user_folder, 'profile_image.jpg'), 'wb') as image_file:
                image_file.write(base64.b64decode(image_data))
            
            # Store the voter_id and digital_id in the Excel file
            data = {'Digital_ID': [digital_id], 'Voter_ID': [voter_id]}
            df = pd.DataFrame(data)
            
            # Check if the Excel file exists, if not create it
            if not os.path.exists(excel_file_path):
                df.to_excel(excel_file_path, index=False)
            else:
                existing_df = pd.read_excel(excel_file_path)
                updated_df = pd.concat([existing_df, df], ignore_index=True)
                updated_df.to_excel(excel_file_path, index=False)
            
            # Use Django messages to send a success message to the next page
            messages.success(request, 'Registration successful!')
            time.sleep(0.70)
            # Redirect to the vote_panel page or any other page as needed
            return redirect('index')
    reg_messages = messages.get_messages(request)
    # return render(request, 'voting_web/register_user.html')
    return render(request, 'voting_web/register_user.html', {'reg_messages': reg_messages})

from deepface import DeepFace
import face_recognition

def user_login(request):
    excel_file_path = os.path.join(settings.BASE_DIR, 'voting_web', 'data', 'user_data', 'user_database.xlsx')
    users_temp_check = os.path.join(settings.BASE_DIR, 'voting_web', 'data', 'temp_check')

    if request.method == 'POST':
        voter_id = request.POST.get('voterID')
        digital_id = request.POST.get('digitalID')
        
        # Get the captured image data
        captured_image_data = request.POST.get('capturedImageData')  # Get the data URL
        
        if captured_image_data:
            # Decode the data URL to binary data
            image_data = captured_image_data.split(",")[-1].encode()
            
            # Save the captured image temporarily
            temp_image_path = os.path.join(users_temp_check, 'captured_image.jpg')
            with open(temp_image_path, 'wb') as image_file:
                image_file.write(base64.b64decode(image_data))

            # Construct the path to the folder containing user data (profile image)
            user_folder = os.path.join(settings.BASE_DIR, 'voting_web', 'data', 'user_data', voter_id)
            # Construct the path to the profile image within the user folder
            profile_image_path = os.path.join(user_folder, 'profile_image.jpg')
                
            # Check if the Excel file exists
            if os.path.exists(excel_file_path):
                # Read the Excel file into a DataFrame
                df = pd.read_excel(excel_file_path)

                # Check if the entered Voter ID and Digital ID exist in the DataFrame
                if (df['Voter_ID'] == voter_id).any() and (df['Digital_ID'] == digital_id).any():
                    # Check if the profile image exists
                    if os.path.exists(profile_image_path):
                        # Perform face comparison
                        result = perform_face_comparison(profile_image_path, temp_image_path)
                        if result:
                            # Redirect to the vote_panel page if face verification is successful
                            return redirect('vote_panel')
                        else:
                            messages.error(request, 'Face verification failed. Please try again.')
                    else:
                        messages.error(request, 'Profile image not found. Please try again.')
                else: 
                    # Display an error message if credentials are incorrect
                    messages.error(request, 'Wrong credentials. Please try again.')
            else:
                # Display an error message if the Excel file doesn't exist
                messages.error(request, 'User database not found. Please contact the administrator.')

    login_messages = messages.get_messages(request)
    return render(request, 'voting_web/user_login.html', {'login_messages': login_messages})

def perform_face_comparison(profile_image_path, compare_pic, threshold=0.5):
    # Load the images
    profile_image = face_recognition.load_image_file(profile_image_path)
    compare_image = face_recognition.load_image_file(compare_pic)

    # Find face encodings
    profile_face_encoding = face_recognition.face_encodings(profile_image)
    compare_face_encoding = face_recognition.face_encodings(compare_image)

    if not profile_face_encoding or not compare_face_encoding:
        return False  # No face encoding found in one or both images

    # Compare face encodings with custom threshold
    results = face_recognition.compare_faces([profile_face_encoding[0]], compare_face_encoding[0], tolerance=threshold)

    # Return True if the faces match, False otherwise
    return results[0] if results else False





