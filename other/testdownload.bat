@echo off
set place="C:\*\Desktop"
echo Enter website
set /p web=
:notok
youtube-dl "%web%" --get-title
echo.
youtube-dl.exe -R infinite -F %web%
IF ERRORLEVEL 1 goto notok
:reenter
echo videotype       normal press 1       Live press 2
set /p type=
echo.
if not "%type%"=="1" if not "%type%"=="2"  echo Wrong type please enter again && echo. && goto reenter
if "%type%"=="1" goto normal
if "%type%"=="2" goto live
:normal
echo Enter video number if you don't want press "n"
set /p vid=
echo Enter audio number if you don't want press "n"
set /p aud=
:normal1
if "%aud%"=="n" goto aud
if "%vid%"=="n" goto vid
if not "%aud%"=="n" if not "%vid%"=="n" goto both
:vid
set vidandaud="%vid%"
goto finish
:aud
set vidandaud="%aud%"
goto finish
:both
set vidandaud="%vid%+%aud%"
goto finish
:finish
youtube-dl -o "%place%\%%(title)s.%%(ext)s" -R infinite  -f %vidandaud% %web% 
echo.
IF ERRORLEVEL 1 goto normal1
goto end
:live
echo Enter live number
set /p live=
echo.
youtube-dl --hls-use-mpegts -o "%place%\%%(title)s.%%(ext)s" -R infinite  -f %live% %web%
echo.
IF ERRORLEVEL 1 goto live
goto end
:end
pause