@echo off
setlocal enabledelayedexpansion

echo ====================================
echo Setup Infra + Selenium Environment
echo ====================================

REM ===============================
REM CHECK curl
REM ===============================
where curl >nul 2>nul
IF ERRORLEVEL 1 (
    echo curl not found. Please install curl or use Windows 10+
    pause
    exit /b 1
)

REM ===============================
REM CREATE DIRS
REM ===============================
if not exist infra\jars mkdir infra\jars
if not exist infra\minio-storage mkdir infra\minio-storage
if not exist infra\pg-metastore-data mkdir infra\pg-metastore-data

REM ===============================
REM DOWNLOAD JARS
REM ===============================
echo Downloading JAR files...

set BASE_DIR=infra\jars

curl -f -L -o %BASE_DIR%\aws-java-sdk-bundle-1.12.367.jar ^
 https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk-bundle/1.12.367/aws-java-sdk-bundle-1.12.367.jar || goto :error

curl -f -L -o %BASE_DIR%\hadoop-aws-3.3.4.jar ^
 https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-aws/3.3.4/hadoop-aws-3.3.4.jar || goto :error

curl -f -L -o %BASE_DIR%\postgresql-42.6.2.jar ^
 https://jdbc.postgresql.org/download/postgresql-42.6.2.jar || goto :error

curl -f -L -o %BASE_DIR%\iceberg-spark-runtime-3.5_2.12-1.5.2.jar ^
 https://repo1.maven.org/maven2/org/apache/iceberg/iceberg-spark-runtime-3.5_2.12/1.5.2/iceberg-spark-runtime-3.5_2.12-1.5.2.jar || goto :error

curl -f -L -o %BASE_DIR%\delta-spark_2.12-3.1.0.jar ^
 https://repo1.maven.org/maven2/io/delta/delta-spark_2.12/3.1.0/delta-spark_2.12-3.1.0.jar || goto :error

curl -f -L -o %BASE_DIR%\delta-storage-3.1.0.jar ^
 https://repo1.maven.org/maven2/io/delta/delta-storage/3.1.0/delta-storage-3.1.0.jar || goto :error

echo JAR download completed.

REM ===============================
REM PYTHON CHECK
REM ===============================
python --version || goto :error

REM ===============================
REM INSTALL PYTHON PACKAGES
REM ===============================
python -m pip install --upgrade pip || goto :error
python -m pip install selenium webdriver-manager || goto :error

echo ====================================
echo SETUP COMPLETED SUCCESSFULLY
echo ====================================
pause
exit /b 0

:error
echo.
echo ====================================
echo SETUP FAILED - PLEASE CHECK LOG
echo ====================================
pause
exit /b 1
