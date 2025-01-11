# Contributing to Snowball Snowman

Thank you for your interest in contributing to Snowball Snowman! This document provides guidelines and instructions for contributing to the project.

## For AI Agents
When running tests or debugging the game, use the `--agent` flag to enable agent mode:
```bash
python src/main.py --agent  # Game will auto-close after 5 seconds
```

This mode is specifically designed for automated testing and AI-assisted development. It will:
- Auto-close the game after 5 seconds
- Print agent-specific debug messages
- Take screenshots automatically
- Help maintain consistent test environments

### AI Development Tips
- Always use `--agent` flag when running the game during development
- Check test_screenshots directory for visual verification
- Use pytest for automated testing
- Monitor agent-specific debug messages in console output

## Development Environment Setup

### Prerequisites
- Python 3.11 (recommended) or compatible version
- pip (Python package manager)
- pkg-config (for Mac users)
- Git

### Virtual Environment Tips
- When using pgzero, make sure to install both pygame and pgzero:
  ```bash
  pip install pygame pgzero
  ```
- If you get "ModuleNotFoundError: No module named 'pgzrun'", try:
  ```bash
  pip uninstall pgzero
  pip install pgzero --no-cache-dir
  ```
- Always activate the virtual environment before running:
  ```bash
  source venv/bin/activate  # On Unix/MacOS
  venv\Scripts\activate     # On Windows
  ```
- If modules still aren't found, try setting PYTHONPATH:
  ```bash
  PYTHONPATH=$PYTHONPATH:./src python src/main.py
  ```

### Setting Up Your Development Environment
1. Clone the repository:
   ```bash
   git clone https://github.com/DanEdens/snowball_snowman.git
   cd snowball_snowman
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run tests to verify setup:
   ```bash
   python -m pytest
   ```

## Project Structure
```
snowball_snowman/
├── src/               # Source code
│   ├── game/         # Game logic
│   ├── graphics/     # Visual elements
│   └── utils/        # Utility functions
├── assets/           # Game resources
│   ├── images/       # Graphics and sprites
│   ├── sounds/       # Sound effects
│   └── music/        # Background music
├── tests/            # Test files
└── docs/            # Documentation
```

## Development Workflow

### Creating a New Feature
1. Create a new branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Write tests first:
   ```bash
   # Create a new test file in tests/
   # Run tests to ensure they fail initially
   python -m pytest
   ```

3. Implement the feature
4. Run tests and ensure they pass
5. Update documentation if needed
6. Submit a pull request

### Testing Guidelines
- Write tests for all new features
- Use pytest fixtures for common setup
- Mock Pygame Zero objects when testing display
- Keep tests focused and well-documented
- Run the full test suite before committing

### Code Style
- Follow PEP 8 guidelines
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions focused and small
- Comment complex logic

### Commit Messages
- Use clear, descriptive commit messages
- Start with a verb (Add, Fix, Update, etc.)
- Reference issues if applicable
- Keep commits focused and atomic

## Pull Request Process
1. Update documentation for new features
2. Ensure all tests pass
3. Update CHANGELOG.md
4. Request review from maintainers
5. Address review feedback

## Adding Game Assets
1. Place assets in appropriate directories:
   - Images: `assets/images/`
   - Sounds: `assets/sounds/`
   - Music: `assets/music/`

2. Use appropriate formats:
   - Images: PNG (for transparency)
   - Sounds: WAV or OGG
   - Music: OGG

3. Update asset documentation

## Documentation
- Update README.md for user-facing changes
- Add docstrings for new functions/classes
- Update CHANGELOG.md for all changes
- Keep LESSONS_LEARNED.md updated
- Update ROADMAP.md for new features

## Getting Help
- Check existing issues
- Review documentation
- Ask questions in pull requests
- Contact maintainers

## License
By contributing, you agree that your contributions will be licensed under the project's MIT License.
