@echo off
echo Checking Node.js version...
node --version
echo.
echo Checking npm version...
npm --version
echo.
echo Attempting to install clawhub globally...
npm install -g clawhub
echo.
echo Checking if clawhub is installed...
where clawhub
echo.
echo If clawhub is installed, now installing sonoscli skill...
clawhub install sonoscli
echo.
echo Installation complete!
pause