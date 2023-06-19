# Binarizer Service

*Placeholder for your project description. Include details about what the project does, its goals, and any other relevant information.*

## Table of Contents

- [Binarizer Service](#binarizer-service)
  - [Table of Contents](#table-of-contents)
  - [Getting Started](#getting-started)
    - [Prerequisites](#prerequisites)
      - [Installing Rust](#installing-rust)
      - [Installing OpenCV](#installing-opencv)
    - [Setting up Pre-commit Hooks](#setting-up-pre-commit-hooks)
    - [Building](#building)
    - [Running](#running)
    - [Testing](#testing)
  - [Contact](#contact)

## Getting Started

### Prerequisites

Ensure you have Rust and OpenCV installed.

#### Installing Rust

You can install Rust by following the instructions at [rust-lang.org](https://www.rust-lang.org/tools/install).

#### Installing OpenCV

OpenCV can be installed via package managers or by building it from source.

**On Ubuntu**:

You can install OpenCV using `apt` package manager:

```sh
sudo apt update
sudo apt install libopencv-dev
```

**On MacOS**:

You can install OpenCV using `brew` package manager:

```sh
brew install opencv
brew install llvm
```

**On Windows**:

Install OpenCV by downloading the pre-built libraries from [OpenCV Release Page](https://opencv.org/releases/), and set environment variables according to the installation path.

**Building from source**:

If you prefer to build OpenCV from source, follow the instructions on the [official OpenCV documentation](https://docs.opencv.org/master/d7/d9f/tutorial_linux_install.html).

### Setting up Pre-commit Hooks

This project uses `pre-commit` hooks to ensure code quality and consistency. To set up these hooks on your local machine, navigate to the project's directory and run the following script:

```sh
./prepare.sh
```

This will install the necessary pre-commit hooks for the project.

### Building

To build the project, navigate to the project's directory and run:

```sh
cargo build
```

This will create an executable in the `target/debug/` directory.

### Running

After building the project, you can run it by executing the following command:

```sh
cargo run
```

This command builds (if necessary) and runs your project.

### Testing

To run the tests for this project, use the following command:

```sh
cargo test
```

This will run all the tests in the `tests` directory and any doc-tests.

## Contact

Michal Zajac - dev.michal.99.zajac@gmail.com

Project Link: [https://github.com/Michal99Zajac/binarizer-service](https://github.com/Michal99Zajac/binarizer-service)
