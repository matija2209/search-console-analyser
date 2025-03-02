# Google Search Console Data Analysis

This tool analyzes Google Search Console data across multiple domains to provide insights, summary statistics, and visualizations, helping you understand your website's search performance.

## Features

-   Analyzes multiple domains from Google Search Console data.
-   Provides time series analysis of clicks and impressions.
-   Analyzes traffic by country, device, pages, and search queries.
-   Generates detailed statistical analysis including percentiles and outlier detection.
-   Creates beautiful HTML reports with Tailwind CSS styling.

## Data Structure

The tool expects the data to be organized in the following structure within the `data/` directory:

-   `data/`
    -   `domain1-com-Performance-on-Search-YYYY-MM-DD/`
        -   `Countries.csv`
        -   `Dates.csv`
        -   `Devices.csv`
        -   `Filters.csv`  (If applicable/available)
        -   `Pages.csv`
        -   `Search appearance.csv` (If applicable/available)
        -   `Queries.csv`
    -   `domain2-net-Performance-on-Search-YYYY-MM-DD/`
        -   `Countries.csv`
        -   `Dates.csv`
        -   `Devices.csv`
        -   `Filters.csv` (If applicable/available)
        -   `Pages.csv`
        -   `Search appearance.csv` (If applicable/available)
        -   `Queries.csv`
    -   ... (and so on for each domain)

**Explanation:**

1.  **`data/` directory:**  All Google Search Console data should be placed within this directory.
2.  **Domain Folders:** Each domain's data should be in its own separate folder.  The folder name should follow the pattern: `domain-name.com-Performance-on-Search-YYYY-MM-DD`.  Replace `domain-name.com` with the actual domain (e.g., `example-com`) and `YYYY-MM-DD` with the date of the data export.  Use hyphens instead of periods in the domain name portion.
3.  **CSV Files:**  Within each domain folder, place the CSV files exported from Google Search Console.  Ensure they are named exactly as listed above (case-sensitive).  `Filters.csv` and `Search appearance.csv` are optional and the script should handle their absence gracefully.

## Installation

1.  **Clone the repository:**

    ```bash
    git clone <repository_url>  # Replace <repository_url> with the actual URL
    cd <repository_name>     # Replace <repository_name> with the cloned directory name
    ```

2.  **Create a virtual environment:**

    ```bash
    python3 -m venv venv
    ```

3.  **Activate the virtual environment:**

    -   **macOS/Linux:**
        ```bash
        source venv/bin/activate
        ```
    -   **Windows:**
        ```bash
        venv\Scripts\activate
        ```

4.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

## Usage

1.  **Place Data:**  Place your exported Google Search Console data in the `data/` directory, following the structure described above.

2.  **Run Analysis:**  Execute the main analysis script:

    ```bash
    python main.py
    ```

3.  **View Report:**  The generated HTML report will be saved in the `reports/` directory.  Open the HTML file in your web browser to view the analysis and visualizations.

## Output

The tool provides the following outputs:

-   **Console Output:** Summary statistics and progress information are printed to the console during script execution.
-   **HTML Report:**  A detailed HTML report is generated in the `reports/` directory, containing:
    -   Aggregated statistics across all domains.
    -   Domain-specific analysis, including time series charts, tables, and outlier detection.
    -   Visualizations for clicks, impressions, country, device, page, and query data.

## Requirements

-   Python 3.8+
-   pandas
-   matplotlib
-   numpy
-   (Other dependencies listed in `requirements.txt`)

## License

This project is licensed under the MIT License 