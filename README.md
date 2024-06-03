# CodeLog: A Journaling Web Application for Software Engineers

## Overview
CodeLog is a web application designed to help software engineers maintain a daily journaling habit. Users can log their daily progress, track their streaks, and interact with posts through comments and likes.

![20240603_123108](https://github.com/Chareeef/CodeLog/assets/100241289/2866077d-8a05-4af3-9cdc-610828c2ac28)

## Table of Contents
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [API Endpoints](#api-endpoints)
- [Deployment](#deployment)
- [License](#license)

## Features
- **User Authentication**: Secure user registration and login with JWT authentication.

![20240603_123139](https://github.com/Chareeef/CodeLog/assets/100241289/f7198700-0eff-45ec-8243-96658e361ccf)

- **Journaling**: Log daily entries and edit or delete past entries.

![20240603_123335](https://github.com/Chareeef/CodeLog/assets/100241289/c8f331ed-9f57-419b-a626-730a85bd87f8)

- **Streak Tracking**: Track current and longest streaks with time-based logic.

![20240603_123420](https://github.com/Chareeef/CodeLog/assets/100241289/4ecbe55a-b4c2-49ae-82a3-05e732d73ad1)

- **Comments and Likes**: Interact with posts through comments and likes.

![20240603_123516](https://github.com/Chareeef/CodeLog/assets/100241289/191d6044-514d-45ff-8f6c-836210a87190)


## Technologies Used
- **Frontend**: React.js
- **Backend**: Flask, Gunicorn
- **Database**: MongoDB, Redis
- **Deployment**: DigitalOcean, Nginx, Let's Encrypt (SSL)
- **Other**: JWT for authentication, Systemd for process management

## Installation
### Prerequisites
- Node.js and npm
- Python and pip
- MongoDB
- Redis
- DigitalOcean account (or another hosting service)

### Clone the Repository
```bash
git clone https://github.com/yourusername/code-log.git
cd code-log
```

### Backend Setup
1. **Create a virtual environment and install dependencies**:
    ```bash
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

2. **Configure environment variables**:
    Create a `.env` file in the backend directory and set the required environment variables.

3. **Run the backend server**:
    ```bash
    flask run
    ```

### Frontend Setup
1. **Navigate to the frontend directory and install dependencies**:
    ```bash
    cd frontend
    npm install
    ```

2. **Run the frontend server**:
    ```bash
    npm start
    ```

## API Endpoints
### Authentication
- `POST /register`: Create a new user.
- `POST /login`: Authenticate a user and return JWT tokens.

### User Management
- `PUT /me/update_infos`: Update user information.
- `PUT /me/update_password`: Update user password.
- `DELETE /me/delete_user`: Delete user account.

### Posts Management
- `POST /log`: Log a new entry.
- `GET /feed/get_posts`: Retrieve all public posts with optional pagination.
- `PUT /me/update_post`: Edit a specific post.
- `DELETE /me/delete_post`: Delete a specific post.

### Streak Management
- `GET /me/streaks`: Get current and longest streaks.

## Deployment
### Backend Deployment
1. **Set up Gunicorn and Systemd** for process management.
2. **Configure Nginx** as a reverse proxy.
3. **Deploy on a DigitalOcean server**.

### Frontend Deployment
1. **Build the React app**:
    ```bash
    npm run build
    ```

2. **Deployed on the same DigitalOcean server** as the backend.

### SSL Certification
- **Use Let's Encrypt and Certbot** to obtain and renew SSL certificates.

### Domain Name
- We purchased and configured ["code-log.site"](https://code-log.site) as our domain name on Namecheap.

## License
This project is licensed under the MIT License.

---

## Conclusion

Code-Log is more than just a journaling app; it's a tool designed to help software engineers stay organized, track their progress, and connect with their peers through shared experiences. From robust backend solutions to a sleek, user-friendly frontend, this project showcases the power of collaboration and modern web development technologies. We're proud of what we've built and excited to see how it can benefit the developers community!

## Contributors
- **Youssef Charif Hamidi**
  - *GitHub:* [Chareeef](https://github.com/Chareeef)
  - *LinkedIn:* [youssef-charif-hamidi](https://linkedin.com/in/youssef-charif-hamidi)
  - *Email:* [youssef.charif.h@gmail.com](mailto:youssef.charif.h@gmail.com)

- **Mohamed Lamine Boukhalfa**
  - *GitHub:* [tommy457](https://github.com/tommy457)
  - *LinkedIn:* [mohamed-lamine-boukhalfa](https://linkedin.com/in/mohamed-lamine-boukhalfa)
  - *Email:* [boukhalfaml1011@gmail.com](mailto:boukhalfaml1011@gmail.com)

- **Khadija Ghadi**
  - *GitHub:* [Gdija](https://github.com/Gdija)
  - *LinkedIn:* [khadija-ghadi](https://linkedin.com/in/khadija-ghadi-017737193)
  - *Email:* [khadijaghadi00@gmail.com](mailto:khadijaghadi00@gmail.com)

- **Harriet M Mugendi**
  - *GitHub:* [MwendeHarriet](https://github.com/MwendeHarriet)
  - *LinkedIn:* [harriet-m-mugendi](]https://www.linkedin.com/in/harriet-m-mugendi-149a006b)
  - *Email:* [mwendeharriet@gmail.com](mailto:mwendeharriet@gmail.com)
