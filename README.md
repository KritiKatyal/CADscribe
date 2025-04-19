# CADscribe

CADscribe is a project designed for seamless integration between Fusion 360 and a web-based platform for generating 3D models using AI-driven technologies.

## Features
- **Fusion 360 Integration**: Direct interaction with Fusion 360 to retrieve and modify models.
- **AI Model Generation**: Automatically generate 3D models from design inputs.
- **STL File Handling**: Upload, download, and manage STL files.
- **Web Interface**: User-friendly interface for interacting with the system.

## Setup

### Prerequisites
- [Python 3.11+](https://www.python.org/downloads/)
- [Node.js](https://nodejs.org/)
- [Fusion 360 Account](https://www.autodesk.com/products/fusion-360/overview)

### Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/KritiKatyal/CADscribe.git
    ```

2. Install backend dependencies:
    ```bash
    cd CADscribe/backend
    pip install -r requirements.txt
    ```

3. Install frontend dependencies:
    ```bash
    cd ../frontend
    npm install
    ```

4. Set up environment variables for both backend and frontend. Refer to the `.env.example` file for required configurations.

### Running the Application

1. Start the backend:
    ```bash
    cd backend
    python main.py
    ```

2. Start the frontend:
    ```bash
    cd ../frontend
    npm start
    ```

3. Open the web application in your browser at `http://localhost:3000`.

## Demo

Here is a demo of the CADscribe application:

<video width="100%" controls>
  <source src="https://raw.githubusercontent.com/KritiKatyal/CADscribe/main/frontend/public/demo.mp4" type="video/mp4">
  Your browser does not support the video tag.
</video>

## Contributing

We welcome contributions! Please fork the repository and submit pull requests for any changes or improvements you would like to contribute.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments
- Fusion 360 for their powerful API and 3D modeling tools.
- Open-source community for continuous contributions and innovations.
