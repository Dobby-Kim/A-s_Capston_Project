# Empty Seat? Team A's Project Repository Overview

## A-s_Capston_Project: 'Empty Seat?' Directory Structure

> - **WebHost**
>   - _app_
>     - _public_
>     - _img_
>     - _src_
>       - _data_
>       - _img_
>       - _script_
>       - _style_
>   - _nginx_
>   - _server_
>     - _routes_
>     - _util_
>     - _view_
>       - _css_
> - **module**
>   - _img_
>   - _util_
>   - _yolov5_
>     - _data_
>     - _models_
>     - _utils_

This repository contains the codebase for the A-s Capston Project. Below is an overview of the top-level directories and their respective roles:

### WebHost

The `WebHost` directory is central to the web application component of the project, encompassing both frontend and backend functionalities.

#### app

- **Purpose**: Houses the frontend of the web application.
- **Contents**: Includes user interface elements like HTML, CSS, and JavaScript files. Utilizes Node.js or a similar JavaScript runtime for its operation.
- **Functionality**: Manages the presentation layer of the web application, rendering the user interface and handling user interactions.

#### nginx

- **Purpose**: Contains configuration files for the Nginx web server.
- **Functionality**: Primarily used for serving static content and as a reverse proxy, enhancing the web application's performance and security.

#### server

- **Purpose**: Serves as the backend of the web application.
- **Contents**: Contains server-side scripts and configuration files.
- **Functionality**: Responsible for processing requests, data handling, and interactions with databases or other services, ensuring the application's business logic is executed efficiently.

### module

The `module` directory contains specialized functionalities and components integral to the project.

#### img

- **Purpose**: Stores images and media files used within the project test.
- **Functionality**: Provides visual resources for the application test.

#### util

- **Purpose**: Includes utility scripts and modules.
- **Functionality**: Offers common functions and services that are utilized across `Object detection & Database update` parts of the project, enhancing code reusability and efficiency.

#### yolov5

- **Purpose**: Implements the YOLOv5 (You Only Look Once version 5) model.
- **Functionality**: Used for object detection tasks, primarily in image processing and computer vision applications within the project, demonstrating cutting-edge AI capabilities.

---

Each directory is structured to support the project's scalability and manageability, ensuring a clear separation of concerns and efficient project organization.

---

# Running the A-s_Capston_Project

To get the A-s Capston Project up and running on your local machine, follow these steps:

## Prerequisites

Ensure you have the following installed:

- Node.js (for the `app` and `server` directories)
- Docker (optional, for containerized environments used for Deploy)
- Any other specific dependencies or environment settings required by the project.

---

### Setting up the Frontend

1. Navigate to the `app` directory:
   `cd WebHost/app`

2. Install the necessary Node.js packages:
   `npm install`

3. Build the frontend application:
   `npm run build`

### Setting up the Backend

1. Navigate to the `server` directory:
   `cd WebHost/server`

2. Install the necessary Node.js packages:
   `npm install`

### Using Docker

you can build and run the application using the provided Dockerfiles and docker-compose.yml.

1. Navigate to the `WebHost` directory:
   `cd WebHost`

2. Build and run the containers:
   `docker-compose up --build`

### Running the Modules (run Object Detection & DataBase Update)

For running modules (like `yolov5` for object detection), video sources are required (e.g. parksangjo.mp4, rtsp source ).

1. Navigate to the `module` directory:
   `cd module`

2. Run Object Detection & DataBase Update:
   `python main.py`

---

After following these steps, your application should be running and accessible.
