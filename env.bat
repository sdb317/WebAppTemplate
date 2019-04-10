:: Update for your environment
set path=%path%;%ProgramFiles%\PostgreSQL\9.6\bin
set path=%path%;%ProgramFiles%\nodejs
set path=%path%;%ProgramFiles%\Heroku\bin
set APP=demo
set DATABASE=web_app_template
set DATABASE_URL=postgres://postgres:postgres@localhost:5432/%DATABASE%
set SECRET_KEY="1$6vig-^1ytye$9svhy**p=x^v$(7=!+fm749q0fy$rw#v7!0z"
start "" /D %~dp0 "C:\Program Files (x86)\Microsoft Visual Studio 14.0\Common7\IDE\devenv.exe" APP.sln
