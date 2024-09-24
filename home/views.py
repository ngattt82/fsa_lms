import os
import pandas as pd
from django.shortcuts import render
from django.conf import settings

def get_home(request):
    
    # Define the file path to the CSV file
    file_path = os.path.join(settings.BASE_DIR, 'media/data_csv', 'Java Web Developer_data.csv')
    
    # Load the CSV file into a pandas DataFrame
    data = pd.read_csv(file_path)
    
    # Extract the course name and list of sub-courses
    course_name = data['course'].iloc[0]
    sub_course_list = data['sub_course'].dropna().unique()

    # Dictionary to store sub-courses, modules, and sub-modules
    sub_courses_data = {}
    
    # Iterate over the DataFrame rows
    for index, row in data.iterrows():
        sub_course = row['sub_course']
        module_name = row['module']
        sub_module_name = row['sub_module']
        
        # Initialize the sub-course if it's not already in the dictionary
        if sub_course not in sub_courses_data:
            sub_courses_data[sub_course] = {}

        # Initialize the module under the sub-course if not already present
        if module_name not in sub_courses_data[sub_course]:
            sub_courses_data[sub_course][module_name] = []
        
        # If there's a valid sub-module, process and append the data
        if pd.notna(sub_module_name):
            content_html_list = row['content_html_list'] if pd.notna(row['content_html_list']) else ''
            img_list = row['img_list'] if pd.notna(row['img_list']) else ''
            video_url = row['video_url'] if pd.notna(row['video_url']) else ''

            # Replace \n with <br> and \' with ' in content_html_list
            content_html_list = content_html_list.replace('\\n', '<br>').replace("\\'", "'")
            
            # Append the sub-module data to the list under the corresponding module
            sub_courses_data[sub_course][module_name].append({
                'sub_module': sub_module_name,
                'content_html_list': content_html_list,
                'img_list': img_list,
                'video_url': video_url
            })

    # Split the sub-courses into title and description
    split_sub_courses = []
    for sub_course in sub_course_list:
        if ':' in sub_course:
            title, description = sub_course.split(':', 1)
            split_sub_courses.append({
                'title': title.strip(),
                'description': description.strip(),
                'modules': sub_courses_data[sub_course] 
            })

    # Prepare the context for rendering the template
    context = {
        'course_name': course_name,
        'split_sub_courses': split_sub_courses,  
    }
    
    # Render the template with the context
    return render(request, 'course.html', context)
