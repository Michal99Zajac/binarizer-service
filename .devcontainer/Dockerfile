FROM mcr.microsoft.com/devcontainers/base:ubuntu-22.04

# Update the system
RUN apt-get update -y && apt-get upgrade -y

# Install C++ tools
RUN apt-get install -y build-essential cmake clang libclang-dev

# Install OpenCV
RUN apt-get install -y libopencv-dev

# Install Rust
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y

# Add rust to the path (necessary to use cargo and rustc)
ENV PATH="/root/.cargo/bin:${PATH}"

# Check the installation of Rust and Cargo
RUN rustc --version
RUN cargo --version
