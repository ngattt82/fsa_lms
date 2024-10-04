from django.shortcuts import render, redirect
from .forms import ExcelImportCourseForm
from .models import Course
from module_group.models import ModuleGroup
from django.contrib import messages
import pandas as pd
import csv
import os
import re


module_groups = ModuleGroup.objects.all()


def clean_content(content):
    if isinstance(content, str):
        return re.sub(r'[^\x00-\x7F]+', '', content)  # Loại bỏ ký tự không phải ASCII
    return content

def course_list(request):
    # Lấy danh sách khóa học khác nhau (distinct)
    courses = Course.objects.values('course').distinct()  
    module_groups = ModuleGroup.objects.all()
    
    if request.method == 'POST':
        form = ExcelImportCourseForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['excel_file']
            try:
                df = pd.read_excel(uploaded_file)

                for index, row in df.iterrows():
                    course_name = row.get("course")
                    sub_course = row.get("sub_course")
                    module = row.get("module")
                    sub_module = row.get("sub_module")
                    content = row.get("content")
                    img_list = row.get("img_list")
                    video_url = row.get("video_url")

                    # Kiểm tra nếu khóa học đã tồn tại
                    if not Course.objects.filter(course=course_name).exists():
                        Course.objects.create(
                            course=course_name,
                            sub_course=sub_course,
                            module=module,
                            sub_module=sub_module,
                            content=content,
                            img_list=img_list,
                            video_url=video_url
                        )
                    else:
                        messages.warning(request, f"Course '{course_name}' already exists. Skipping.")

                messages.success(request, "Courses imported successfully!")
            except Exception as e:
                messages.error(request, f"An error occurred during import: {e}")
            return redirect('courses:course_list')  # Đảm bảo rằng bạn sử dụng đúng tên url
    else:
        form = ExcelImportCourseForm()

    return render(request, 'course_list.html', {'courses': courses, 'module_groups': module_groups, 'form': form})

def course_detail(request, pk):
    
    course = Course.objects.filter(pk=pk).first()

    # Lấy tất cả các khóa học có cùng tên khóa học
    related_courses = Course.objects.filter(course=course.course)

    # Trả về template với thông tin khóa học và danh sách khóa học liên quan
    return render(request, 'course_detail.html', {'course': course, 'related_courses': related_courses})

def import_courses(request):
    if request.method == 'POST':
        form = ExcelImportCourseForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['csv_file']
            try:
                df = pd.read_csv(uploaded_file)  
                print(df)
                print(df.columns) 

                courses_imported = 0 

                df['content_html_list'] = df['content_html_list'].apply(clean_content)

            
                for index, row in df.iterrows():
                    if row.isnull().all():
                        continue 
                    course_name = row.get("course")
                    sub_course_name = row.get("sub_course")
                    module_name = row.get("module")
                    sub_module_name = row.get("sub_module")
                    content = row.get("content_html_list")  
                    img_list = row.get("img_list")
                    video_url = row.get("video_url")

                    try:
                        Course.objects.create(
                            course=course_name,
                            sub_course=sub_course_name,
                            module=module_name,
                            sub_module=sub_module_name,
                            content=content,
                            img_list=img_list,
                            video_url=video_url
                        )
                        courses_imported += 1
                        print(f"Imported row {index} successfully.")  # Thông báo nhập thành công
                    except Exception as e:
                        print(f"Error importing row {index}: {e}")  # In ra lỗi nếu có

                messages.success(request, f"{courses_imported} courses imported successfully!")
            except Exception as e:
                messages.error(request, f"An error occurred during import: {e}")

            return redirect('courses:course_list')  # Redirect to your course list page
    else:
        form = ExcelImportCourseForm()

    return render(request, 'course_list.html', {'form': form})

def delete_courses(request):
    if request.method == 'POST':
        course_name = request.POST.get('course_name')
        
        if course_name:
            deleted_count, _ = Course.objects.filter(course=course_name).delete()
            if deleted_count > 0:
                messages.success(request, f"{deleted_count} courses deleted successfully!")
            else:
                messages.warning(request, "No courses found with that name.")
        else:
            messages.error(request, "Please provide a course name.")

    return render(request, 'course_list.html') 
