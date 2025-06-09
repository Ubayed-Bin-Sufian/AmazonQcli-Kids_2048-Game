FROM mcr.microsoft.com/devcontainers/python:3.11

# Install system dependencies for pygame
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends \
    libsdl2-dev \
    libsdl2-image-dev \
    libsdl2-mixer-dev \
    libsdl2-ttf-dev \
    && apt-get clean -y && rm -rf /var/lib/apt/lists/*

# Set up a non-root user
ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=$USER_UID

# Create the user if it doesn't exist
RUN if [ ! $(getent passwd $USERNAME) ]; then \
    groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
    && apt-get update \
    && apt-get install -y sudo \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME; \
    fi

# Set the default user
USER $USERNAME

# Set working directory
WORKDIR /workspaces/kids_2048

# Install Python dependencies
COPY requirements.txt .
RUN pip install --user -r requirements.txt

# Create necessary directories
RUN mkdir -p assets/fonts assets/images assets/sounds

# Set the entrypoint
CMD ["python", "main.py"]
