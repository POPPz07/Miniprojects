# Contributing to Customer Support AI

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## 🤝 How to Contribute

### Reporting Bugs

If you find a bug, please create an issue with:
- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Environment details (OS, Python version, etc.)

### Suggesting Enhancements

For feature requests:
- Describe the feature and its benefits
- Provide use cases
- Consider implementation complexity

### Pull Requests

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Test thoroughly
5. Commit with clear messages (`git commit -m 'Add amazing feature'`)
6. Push to your fork (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## 📋 Development Setup

```bash
# Clone your fork
git clone https://github.com/yourusername/customer-support-ai.git
cd customer-support-ai

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Download NLTK data
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet')"
```

## 🧪 Testing

Before submitting:
- Test your changes locally
- Ensure the Streamlit app runs without errors
- Verify model training still works
- Check for any breaking changes

## 📝 Code Style

- Follow PEP 8 guidelines
- Use meaningful variable names
- Add comments for complex logic
- Keep functions focused and small

## 🎯 Areas for Contribution

### High Priority
- Improve duplicate detection algorithms
- Add more visualization options
- Optimize batch processing speed
- Enhance error handling

### Medium Priority
- Add unit tests
- Improve documentation
- Add more preprocessing options
- Support additional languages

### Low Priority
- UI/UX improvements
- Additional export formats
- Integration with ticketing systems

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

## 💬 Questions?

Feel free to open an issue for any questions or clarifications.

Thank you for contributing! 🎉
