FROM mcr.microsoft.com/devcontainers/python:3.11

# Update the system
RUN apt-get update -y && apt-get upgrade -y

# Install Rust
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y

# Add rust to the path (necessary to use cargo and rustc)
ENV PATH="/root/.cargo/bin:${PATH}"

# Check the installation of Rust and Cargo
RUN rustc --version
RUN cargo --version

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Add Poetry to the path (necessary to use poetry)
ENV PATH="$HOME/.local/bin:${PATH}"

# Check the installation of Poetry
RUN poetry --version

WORKDIR /app
