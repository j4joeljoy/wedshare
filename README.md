# Wedding Gallery (WedShare)

A Django-based wedding photo sharing and gallery application.

## Features

- **User Accounts**: Photographer and User logins.
- **Gallery Management**: Upload and organize wedding photos.
- **Dashboard**: Analytics and management interface.
- **Cloud Storage**: Integration with Cloudinary for media storage.
- **Production Ready**: Configured for deployment on Railway.

## Tech Stack

- **Backend**: Django 6.0 (Python 3.12)
- **Database**: SQLite (Local), PostgreSQL (Production)
- **Static Files**: Whitenoise
- **Deployment**: Nixpacks (Railway)

## Local Development Setup

1.  **Clone the repository**:
    ```bash
    git clone <repository-url>
    cd <repository-name>
    ```

2.  **Create a virtual environment**:
    ```bash
    python -m venv venv
    # Windows
    .\venv\Scripts\activate
    # Unix/MacOS
    source venv/bin/activate
    ```

3.  **Install dependencies**:
    ```bash
    cd wedding_gallery
    pip install -r requirements.txt
    ```

4.  **Run Migrations**:
    ```bash
    python manage.py migrate
    ```

5.  **Start the server**:
    ```bash
    python manage.py runserver
    ```

## Deployment (Railway)

This project is configured for seamless deployment on [Railway.app](https://railway.app/).

1.  **Push to GitHub**.
2.  **Create a new project on Railway** from your GitHub repo.
3.  **Add a PostgreSQL Database** service.
4.  **Set Environment Variables** in Railway:

    | Variable | Description |
    | :--- | :--- |
    | `SECRET_KEY` | Your Django secret key |
    | `DEBUG` | Set to `False` in production |
    | `CLOUDINARY_CLOUD_NAME` | Cloudinary Cloud Name |
    | `CLOUDINARY_API_KEY` | Cloudinary API Key |
    | `CLOUDINARY_API_SECRET` | Cloudinary API Secret |
    | `DATABASE_URL` | Auto-set by Railway when linking Postgres |
    | `RAILWAY_STATIC_URL` | (Optional) Your Railway domain (e.g., `xxx.up.railway.app`) |

    **Note**: A `nixpacks.toml` file in the root handles the build process, pointing Railway to the `wedding_gallery` subdirectory.

## Project Structure

- `wedding_gallery/`: Main Django project directory.
- `nixpacks.toml`: Build configuration for Railway.
