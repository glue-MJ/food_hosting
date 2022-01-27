@echo off
goto main

:main
color 0a
cls
cd food_app
cd backend_web
echo FILES CREATED FOR THE WEBSITE
powershell ls -File -recurse -exclude *pyc" | Select Name, FullName, Length"
set FLASK_APP=app.py
flask run
goto end

:end
echo GoodBye %USERNAME%
pause