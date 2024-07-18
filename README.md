Here's a sample `README.md` file for your Flask project:

---

# Flask Blog Application

## Overview
This is a Flask-based web application for blogging. Users can register, log in, write blog posts, comment on posts, and add friends. The application also includes user authentication, email verification, and a simple like system for posts.

## Features
- **User Registration and Authentication**: Secure user login and registration using Flask-Login.
- **Email Verification**: Users receive an OTP to verify their email address.
- **Blog Posting**: Users can write and manage their blog posts.
- **Commenting System**: Users can comment on blog posts.
- **Friend System**: Users can add other users as friends.
- **Like System**: Users can like and unlike posts.
- **User Profiles**: Users can view and edit their profile information.

## Technologies Used
- **Flask**: Web framework
- **Flask-Login**: User session management
- **Flask-SQLAlchemy**: ORM for database interactions
- **SQLite**: Database for storing user and blog data
- **Werkzeug**: Password hashing utilities
- **SMTP**: For sending email verification OTPs
- **Urwid**: Console UI library (not used in current routes but imported)

## Prerequisites
- Python 3.x
- Virtual Environment (venv)
- pip (Python package installer)

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/flask-blog.git
   cd flask-blog
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install the dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Set up the database**:
   ```bash
   python app.py
   ```

6. **Run the application**:
   ```bash
   python app.py
   ```

## Usage
- **Home Page**: Accessible at `http://127.0.0.1:5000/`. Users can log in or register.
- **Profile Page**: Users can view and edit their profile information.
- **Blog Management**: Users can add, view, and comment on blog posts.
- **Friend System**: Users can search for other users and add them as friends.
- **OTP Verification**: After registration, users will receive an OTP email for verification.

## Project Structure
- `app.py`: Main application file containing routes and application logic.
- `templates/`: Folder containing HTML templates.
- `static/`: Folder for static files like CSS and JavaScript.
- `requirements.txt`: List of dependencies required for the project.

## Routes

- `/`: Home page with login form.
- `/login`: Login page.
- `/register`: Registration page.
- `/profile`: User profile page.
- `/addblog`: Page to add a new blog post.
- `/blog_index`: Page to view all blog posts.
- `/singleblog/<int:noteid>`: Page to view a single blog post.
- `/comment/<int:noteid>`: Page to view and add comments on a blog post.
- `/addlike/<int:id>`: Endpoint to like/unlike a blog post.
- `/addbio`: Endpoint to update user bio.
- `/getprofile`: Page to search and view other user profiles.
- `/addfrnd/<username>`: Endpoint to add a friend.
- `/otpfirst`: Page to initiate OTP verification.
- `/otp`: Endpoint to verify OTP.

## Contributing
Contributions are welcome! Please fork the repository and submit pull requests.

1. **Fork the repository**.
2. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Commit your changes**:
   ```bash
   git commit -m 'Add some feature'
   ```
4. **Push to the branch**:
   ```bash
   git push origin feature/your-feature-name
   ```
5. **Open a pull request**.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements
- Thanks to the Flask community for their support and contributions.
- Special thanks to the contributors who helped make this project possible.

---

Feel free to modify this README to better fit your specific project details and requirements.
