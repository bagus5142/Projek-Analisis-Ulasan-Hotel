# Contributing to Hotel Review Analysis Project

Thank you for your interest in contributing to this project! This document provides guidelines for contributing.

## 🎯 How to Contribute

### Reporting Issues

If you find a bug or have a suggestion:

1. Check if the issue already exists in the [Issues](https://github.com/bagus5142/Projek-Analisis-Ulasan-Hotel/issues) page
2. If not, create a new issue with:
   - Clear, descriptive title
   - Steps to reproduce (for bugs)
   - Expected vs actual behavior
   - Screenshots if applicable
   - Your environment (Python version, OS, etc.)

### Submitting Changes

1. **Fork the repository**
   ```bash
   git clone https://github.com/bagus5142/Projek-Analisis-Ulasan-Hotel.git
   cd Projek-Analisis-Ulasan-Hotel
   ```

2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/your-bug-fix
   ```

3. **Make your changes**
   - Follow the code style guide below
   - Add tests if applicable
   - Update documentation

4. **Test your changes**
   ```bash
   # Run the dashboard
   cd src
   streamlit run visual.py
   
   # If you added tests
   pytest tests/
   ```

5. **Commit with clear messages**
   ```bash
   git add .
   git commit -m "feat: add new feature X"
   # or
   git commit -m "fix: resolve issue with Y"
   ```

6. **Push and create Pull Request**
   ```bash
   git push origin feature/your-feature-name
   ```
   Then open a PR on GitHub with:
   - Description of changes
   - Related issue numbers
   - Screenshots/examples if applicable

## 📝 Code Style Guide

### Python Code

- Follow [PEP 8](https://pep8.org/) style guide
- Use meaningful variable names
- Add docstrings to functions:
  ```python
  def my_function(param1: str, param2: int) -> bool:
      """
      Brief description of function
      
      Args:
          param1: Description of param1
          param2: Description of param2
      
      Returns:
          Description of return value
      """
      pass
  ```
- Maximum line length: 100 characters
- Use type hints where appropriate

### File Organization

When adding new features, follow this structure:

```
src/
├── config.py           # Configuration settings
├── utils.py            # Utility functions
├── visual.py           # Main dashboard (to be refactored)
└── modules/            # Future: modular components
    ├── data_loader.py
    ├── analytics.py
    └── visualizations.py
```

### Commit Message Convention

Use conventional commits format:

- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `style:` - Code style changes (formatting)
- `refactor:` - Code refactoring
- `test:` - Adding or updating tests
- `chore:` - Maintenance tasks

Examples:
```
feat: add hotel comparison chart
fix: resolve BUMN categorization bug
docs: update README with installation steps
refactor: extract CSS to separate file
```

## 🧪 Testing Guidelines

### Manual Testing Checklist

Before submitting, test:

- [ ] Dashboard loads without errors
- [ ] All 8 tabs render correctly
- [ ] Filters work as expected
- [ ] Data export functions properly
- [ ] No console errors in browser
- [ ] Responsive on different screen sizes

### Adding Unit Tests

If adding new utility functions:

```python
# tests/test_utils.py
import pytest
from src.utils import categorize_hotel

def test_categorize_hotel_exact_match():
    category, confidence = categorize_hotel("Hotel Patra Jasa")
    assert category == "BUMN"
    assert confidence >= 0.9

def test_categorize_hotel_unknown():
    category, confidence = categorize_hotel("Unknown Hotel XYZ")
    assert category in ["BUMN", "Non-BUMN", "Unknown"]
    assert 0 <= confidence <= 1
```

## 🎨 UI/UX Guidelines

- Maintain consistent color scheme (see `src/config.py`)
- Use Streamlit components appropriately
- Ensure accessibility (colorblind-safe palettes, alt text)
- Add loading indicators for slow operations
- Provide clear error messages

## 📚 Documentation

When adding features:

1. Update README.md if user-facing
2. Add docstrings to new functions
3. Update CODE_ANALYSIS.md if architecture changes
4. Consider adding examples in docstrings

## 🐛 Priority Areas for Contribution

We especially welcome contributions in these areas:

### High Priority

1. **Modularization** - Break down visual.py into smaller modules
2. **Unit Tests** - Add comprehensive test coverage
3. **Error Handling** - Improve error handling throughout
4. **Performance** - Optimize for large datasets (pagination, caching)

### Medium Priority

5. **Logging** - Add proper logging infrastructure
6. **Data Validation** - Strengthen input validation
7. **Documentation** - More examples and tutorials
8. **Accessibility** - Improve colorblind support, keyboard navigation

### Nice to Have

9. **REST API** - Create API for programmatic access
10. **Predictive Analytics** - Add trend forecasting
11. **Authentication** - User management system
12. **Internationalization** - Multi-language support

## 💡 Getting Help

- Check the [CODE_ANALYSIS.md](CODE_ANALYSIS.md) for architecture overview
- Review existing code before making changes
- Ask questions in Issues or Discussions
- Join our community [if applicable]

## 📋 Code Review Process

1. All PRs require review before merging
2. Address review comments promptly
3. Keep PRs focused and reasonably sized
4. Ensure CI checks pass (when available)

## 🔐 Security

- Never commit sensitive data (API keys, credentials)
- Use `.gitignore` for sensitive files
- Report security issues privately
- Follow secure coding practices

## 📄 License

By contributing, you agree that your contributions will be licensed under the same license as the project.

---

Thank you for contributing! 🙏

For questions, open an issue or contact the maintainers.
