# Website Template Scraper

This project provides a tool to scrape website templates for learning or development purposes. The scraper allows developers to extract HTML, CSS, and JavaScript files from public websites to understand their structure and use them as inspiration for personal projects.

## Features

- Extracts complete HTML, CSS, and JavaScript files from websites.
- Supports dynamic content handling using Selenium for JavaScript-heavy websites.
- Saves assets like images, fonts, and scripts locally.
- User-friendly and customizable for specific scraping needs.
- Outputs files in a structured folder format for easy reuse.

## Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.8 or above
- Google Chrome (or any compatible browser)
- ChromeDriver (for Selenium, if needed for dynamic websites)

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/website-template-scraper.git
   cd website-template-scraper
   ```

2. Install the required Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. (Optional) Set up a virtual environment for the project:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

## Usage

### Basic Scraping

1. Update the `config.json` file with the target website URL and other settings:
   ```json
   {
       "url": "https://example.com",
       "output_dir": "output",
       "include_assets": true
   }
   ```

2. Run the scraper:
   ```bash
   python scraper.py
   ```

### Dynamic Content Handling

For websites with heavy JavaScript rendering, enable Selenium:

1. Install Selenium:
   ```bash
   pip install selenium
   ```

2. Update the `config.json` file:
   ```json
   {
       "use_selenium": true,
       "browser": "chrome"
   }
   ```

3. Ensure `chromedriver` is installed and in your PATH.

## Output

The scraped website files will be saved in the `output` directory (or the directory specified in the configuration). The directory structure will look like this:

```
output/
├── index.html
├── assets/
│   ├── css/
│   ├── js/
│   ├── images/
```

## Legal Disclaimer

This tool is intended for educational purposes and personal use only. Scraping websites without permission may violate their terms of service or applicable laws. Always seek permission before scraping content from any website.

## Contributions

Contributions are welcome! If you'd like to contribute:

1. Fork the repository.
2. Create a new branch:
   ```bash
   git checkout -b feature-name
   ```
3. Commit your changes and push the branch:
   ```bash
   git push origin feature-name
   ```
4. Open a pull request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Contact

For any questions or issues, feel free to contact:

- Email: jaivishwa.dev@gmail.com
- GitHub: [jaivishwaj](https://github.com/jaivishwaj)

---
Happy coding! 🎉
