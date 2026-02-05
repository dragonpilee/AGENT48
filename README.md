# AGENT48 🤖
> **AI Coding Agent with Terminal Interface**

![Status](https://img.shields.io/badge/Status-Production-success?style=for-the-badge) ![Docker](https://img.shields.io/badge/Deployment-Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white) ![Python](https://img.shields.io/badge/Backend-Python-3776AB?style=for-the-badge&logo=python&logoColor=white) ![React](https://img.shields.io/badge/Frontend-React-61DAFB?style=for-the-badge&logo=react&logoColor=black)

**AGENT48** is a full-stack AI coding agent featuring a **Terminal** interface. Built for autonomous code generation and execution, it combines retro-futuristic aesthetics with modern local LLM capabilities powered by Docker Model Runner and Granite-4.0-Nano.

---

## ✨ Features

- **🧠 Local Intelligence**: Privacy-focused architecture using Docker's native Model Runner with Granite-4.0-Nano (1.46B parameters)
- **🛠️ ReAct Agent Loop**: Autonomous tool execution with `write_file`, `read_file`, and `run_command` capabilities
- **⚡ Real-Time Streaming**: Live agent thoughts and tool outputs displayed in the terminal
- **🎨 Pure Black Theme**: Minimalist design with JetBrains Mono typography and CRT effects
- **🔌 Zero-Config Deployment**: Single Docker Compose command - no manual model downloads required
- **🦾 GPU Accelerated**: Optimized for NVIDIA GPUs (tested on RTX )
- **🛡️ Isolated Workspace**: All file operations and commands execute in a containerized environment

---

## 🚀 Quick Start

### Prerequisites

1.  **Docker Desktop** (v4.30+): Ensure Docker is running with WSL2 and NVIDIA Container Toolkit.
2.  **Git**: To clone the repository.
3.  **NVIDIA GPU** (Optional): For accelerated inference.

### Installation & Run

1.  Clone the repository:
    ```bash
    git clone https://github.com/yourusername/AGENT48.git
    cd AGENT
    ```

2.  Build and launch the stack:
    ```bash
    docker-compose up -d --build
    ```

3.  Open your browser and visit:
    **[http://localhost:5173](http://localhost:5173)**

### Docker Commands

```bash
# Restart containers
docker-compose restart

# Stop containers
docker-compose down

# View logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Rebuild after code changes
docker-compose up -d --build
```

---

## 🛠️ Technology Stack

| Component | Technology |
|----------|------------|
| **Frontend Framework** | React + Vite |
| **Backend Framework** | FastAPI (Python) |
| **Language** | JavaScript + Python |
| **Styling** | Vanilla CSS (Terminal Theme) |
| **LLM Engine** | Docker Model Runner + Granite-4.0-Nano |
| **Infrastructure** | Docker Compose (Multi-container) |

---

## 🎯 How It Works

1.  **Input**: Type a command or request in the terminal prompt.
2.  **Process**: The FastAPI backend sends the request to Granite-4.0-Nano via Docker Model Runner.
3.  **Execute**: The agent autonomously decides which tools to use (`write_file`, `run_command`, etc.).
4.  **Stream**: Real-time agent thoughts and tool outputs are displayed in the terminal.
5.  **Complete**: The final result is shown with a summary.

---

## 🎨 Design Philosophy

- **Digital Authenticity**: Scanline effects, monospaced typography, and CRT-style cursor blinking
- **Terminal-First**: Zero GUI clutter - just you and the command prompt
- **Typography**: Uses **JetBrains Mono** for maximum legibility and retro aesthetic
- **Pure Black**: True #000000 background for OLED displays and classic terminal feel
- **Responsive**: Fluid layout that adapts from mobile to ultrawide monitors

---

## 🧪 Example Usage

Try these commands in the AGENT48 terminal:

```
Create a Python script named hello.py that prints "Hello from AGENT48"
```

```
Write a simple web server in Python using Flask
```

```
Read the contents of README.md and summarize it
```

---

## 🤝 Contributing

**Important:** We prioritize features that enhance agent autonomy and terminal immersion.

1.  **Fork & Branch**: Create a feature branch.
2.  **Develop**: Test with Docker or local development.
3.  **Commit**: Push changes and open a PR.

---

## 📝 License

This project is open source and available under the MIT License.

---

<div align="center">
  <sub>Developed with ❤️ for autonomous coding</sub><br>
  <sub>Terminal Interface • Docker Native • GPU Accelerated</sub>
</div>



