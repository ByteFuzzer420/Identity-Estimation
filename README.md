![Identity-Estimation](https://img.shields.io/github/license/kathuluman/Identity-Estimation?color=blue&style=for-the-badge) ![Version](https://img.shields.io/github/v/tag/kathuluman/Identity-Estimation?color=blue&style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python&logoColor=white)
![Version](https://img.shields.io/badge/version-3.0.0-green?style=for-the-badge)

# Identify-Estimation
A Python Project inspired by smahesh29 refined to give more accurate results

## Overview

Identity-Estimation is a Python tool designed to take an picture of someone and give as accurate of an estimation of their age as possible. Can be utilized for Age verification for services, applications, and Discord Servers.

## Features

- **Age Estimation**: Efficiently Estimate Users Age
- **Records**: Store records into csv file

## Installation

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/kathuluman/Identity-Estimation.git
    cd Identity-Estimation
    ```

2. **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Download Pre-Trained Modles**:
    ```bash
    Since Github has a set upload file size I had uploaded the pre-trained modles to this mega.nz archive you can find below.
    There you will get the modles.zip, from there extract the files into the same directory as the python program.
    https://mega.nz/file/6vYkzArR#IFVD61aWDJGJTswegk8xjr2_1OEwNBg21QK2eVEAFbk
    ```

## Usage

1. **Prepare the Image**:
    Get a clear image of someone and put it in the same directory as the project.

2. **Run the Tool**:
    ```bash
    python3 main.py
    ```
    You will be prompted for a file to save the results into, you can enter a file name for example `users` and for your next face scan you can specify the same file and it will append results alongside username / alias.

### Usage for windows

1. **Create a Virtual Enviorment**:
    ```bash
    python3 -m venv venv
    #OR specify the install path of your python installation.
    C:\Users\USER\AppData\Local\Programs\PythonX\python.exe -m venv venv
    ```

2. **Activate The Virtual Enviorment**:
    ```bash
    .\venv\Scripts\activate
    ```

3. **Install requirements**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Run the Program**:
    ```bash
    python main.py --image image.jpg
    ## For easier use put the image into the same directory as the python program
    ```

## Example

```bash
$ python3 main.py --image image.jpg
Do you want to save results to a CSV file? (yes/no): yes
Enter the CSV file name: users
Enter an alias for the image (optional): myself
Gender: Male
Age: 18-20 years
```

## Configuration

- **Confidence**: You can edit the `self.model_mean_values` values to be able to refine your Age/Gender Estimation results.
- **Age Range**: In the `self.age_list` list you can refine the age values to give bigger gaps between or smaller.
