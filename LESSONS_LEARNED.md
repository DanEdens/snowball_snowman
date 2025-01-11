# Lessons Learned

## Development Setup

### Python Environment
- Python 3.11 works better than 3.13 for current dependencies
- Virtual environment is essential for consistent testing
- Package installation on Mac requires additional setup:
  - `pkg-config` for pygame installation
  - Specific Python version compatibility checks

### Testing Framework
- Pygame Zero requires special handling for testing
  - Need to mock the screen object
  - Can't test actual rendering directly
  - Focus on testing game logic separately from display
- Using pytest fixtures makes screen mocking reusable
- Test files should be kept separate from game logic

### Game Architecture
- Separating game states (MENU, PLAYING, CELEBRATION) early helps organization
- Drawing functions should be modular for easier testing
- Keep game logic separate from rendering code
- Use constants for configuration values

## Best Practices Discovered

### Code Organization
- Keep main game loop clean and delegate to specific functions
- Use state pattern for different game phases
- Organize assets in clear directory structure
- Separate concerns: input handling, game logic, rendering

### Testing Strategy
1. Unit tests for game logic
2. Mock pygame objects for display tests
3. Test state transitions independently
4. Keep test files organized by functionality

### Documentation
- Update documentation as features are added
- Include setup instructions for different environments
- Document testing approach and requirements
- Keep track of lessons learned while they're fresh

## Challenges and Solutions

### Environment Setup
**Challenge:** Python 3.13 compatibility issues
**Solution:** Use Python 3.11 for now, document requirement

### Testing
**Challenge:** Testing Pygame Zero applications
**Solution:** Created mock objects for screen and drawing

### Development Workflow
**Challenge:** Managing game states and testing
**Solution:** Clear state separation and dedicated test files
