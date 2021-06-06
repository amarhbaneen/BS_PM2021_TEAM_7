@echo off
cd ..
cmd /c ".\env\Scripts\activate  & start http://localhost:8000/ & python manage.py runserver"
