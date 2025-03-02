import os
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np
import base64
from io import BytesIO

def load_csv_data(folder_path, filename):
    """Load CSV data from the specified folder and filename."""
    file_path = os.path.join(folder_path, filename)
    try:
        return pd.read_csv(file_path)
    except Exception as e:
        print(f"Error loading {filename}: {e}")
        return None

def generate_html_report(domain_summaries, domain_details):
    """Generate an HTML report with Tailwind CSS styling."""
    
    # Create HTML header with Tailwind CSS
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Google Search Console Analysis Report</title>
        <script src="https://unpkg.com/@tailwindcss/browser@4"></script>
        <style>
            body {
                font-family: 'Inter', sans-serif;
                background-color: #f9fafb;
            }
            .chart-container {
                width: 100%;
                max-width: 800px;
                margin: 0 auto;
            }
        </style>
    </head>
    <body class="p-6">
        <div class="max-w-7xl mx-auto">
            <h1 class="text-3xl font-bold text-gray-900 mb-8">Google Search Console Analysis Report</h1>
            <p class="text-gray-600 mb-8">Generated on: """ + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + """</p>
            
            <div class="bg-white rounded-lg shadow-md p-6 mb-8">
                <h2 class="text-xl font-semibold text-gray-800 mb-4">Overall Summary</h2>
    """
    
    # Create summary table
    if domain_summaries:
        summary_df = pd.DataFrame(domain_summaries)
        
        # Calculate aggregate statistics
        total_clicks = summary_df['total_clicks'].sum()
        total_impressions = summary_df['total_impressions'].sum()
        avg_ctr = summary_df['avg_ctr'].mean()
        avg_position = summary_df['avg_position'].mean()
        best_domain_clicks = summary_df.loc[summary_df['total_clicks'].idxmax()]['domain']
        best_domain_ctr = summary_df.loc[summary_df['avg_ctr'].idxmax()]['domain']
        
        # Add aggregate statistics to HTML
        html += f"""
                <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
                    <div class="bg-blue-50 p-4 rounded-lg">
                        <p class="text-sm text-blue-600 font-medium">Total Clicks</p>
                        <p class="text-2xl font-bold text-blue-800">{int(total_clicks)}</p>
                    </div>
                    <div class="bg-green-50 p-4 rounded-lg">
                        <p class="text-sm text-green-600 font-medium">Total Impressions</p>
                        <p class="text-2xl font-bold text-green-800">{int(total_impressions)}</p>
                    </div>
                    <div class="bg-purple-50 p-4 rounded-lg">
                        <p class="text-sm text-purple-600 font-medium">Average CTR</p>
                        <p class="text-2xl font-bold text-purple-800">{avg_ctr:.2f}%</p>
                    </div>
                </div>
                
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
                    <div class="bg-yellow-50 p-4 rounded-lg">
                        <p class="text-sm text-yellow-600 font-medium">Average Position</p>
                        <p class="text-2xl font-bold text-yellow-800">{avg_position:.2f}</p>
                    </div>
                    <div class="bg-indigo-50 p-4 rounded-lg">
                        <p class="text-sm text-indigo-600 font-medium">Best Performing Domain</p>
                        <p class="text-xl font-bold text-indigo-800">{best_domain_clicks}</p>
                        <p class="text-xs text-indigo-600">(by clicks)</p>
                    </div>
                </div>
        """
        
        # Add new section for Aggregated Averages
        html += """
            </div>
            
            <div class="bg-white rounded-lg shadow-md p-6 mb-8">
                <h2 class="text-xl font-semibold text-gray-800 mb-4">Aggregated Averages</h2>
                
                <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
        """
        
        # Calculate additional aggregated statistics
        max_clicks = summary_df['total_clicks'].max()
        min_clicks = summary_df['total_clicks'].min()
        median_clicks = summary_df['total_clicks'].median()
        
        max_impressions = summary_df['total_impressions'].max()
        min_impressions = summary_df['total_impressions'].min()
        median_impressions = summary_df['total_impressions'].median()
        
        max_ctr = summary_df['avg_ctr'].max()
        min_ctr = summary_df['avg_ctr'].min()
        
        max_position = summary_df['avg_position'].max()
        min_position = summary_df['avg_position'].min()
        
        # Calculate percentiles and standard deviation for clicks
        p25_clicks = summary_df['total_clicks'].quantile(0.25)
        p75_clicks = summary_df['total_clicks'].quantile(0.75)
        p90_clicks = summary_df['total_clicks'].quantile(0.90)
        std_clicks = summary_df['total_clicks'].std()
        iqr_clicks = p75_clicks - p25_clicks
        
        # Calculate percentiles and standard deviation for impressions
        p25_impressions = summary_df['total_impressions'].quantile(0.25)
        p75_impressions = summary_df['total_impressions'].quantile(0.75)
        p90_impressions = summary_df['total_impressions'].quantile(0.90)
        std_impressions = summary_df['total_impressions'].std()
        iqr_impressions = p75_impressions - p25_impressions
        
        # Calculate percentiles and standard deviation for CTR
        p25_ctr = summary_df['avg_ctr'].quantile(0.25)
        p75_ctr = summary_df['avg_ctr'].quantile(0.75)
        p90_ctr = summary_df['avg_ctr'].quantile(0.90)
        std_ctr = summary_df['avg_ctr'].std()
        iqr_ctr = p75_ctr - p25_ctr
        
        # Calculate percentiles and standard deviation for position
        p25_position = summary_df['avg_position'].quantile(0.25)
        p75_position = summary_df['avg_position'].quantile(0.75)
        p90_position = summary_df['avg_position'].quantile(0.90)
        std_position = summary_df['avg_position'].std()
        iqr_position = p75_position - p25_position
        
        # Update Clicks statistics with more detailed metrics
        html += f"""
                    <div class="bg-white border border-gray-200 rounded-lg p-4">
                        <h3 class="text-lg font-medium text-gray-800 mb-3">Clicks</h3>
                        <div class="space-y-2">
                            <div class="flex justify-between">
                                <span class="text-sm text-gray-600">Average:</span>
                                <span class="text-sm font-medium text-gray-900">{summary_df['total_clicks'].mean():.1f}</span>
                            </div>
                            <div class="flex justify-between">
                                <span class="text-sm text-gray-600">Median:</span>
                                <span class="text-sm font-medium text-gray-900">{median_clicks:.1f}</span>
                            </div>
                            <div class="flex justify-between">
                                <span class="text-sm text-gray-600">Standard Deviation:</span>
                                <span class="text-sm font-medium text-gray-900">{std_clicks:.1f}</span>
                            </div>
                            <div class="flex justify-between">
                                <span class="text-sm text-gray-600">25th Percentile:</span>
                                <span class="text-sm font-medium text-gray-900">{p25_clicks:.1f}</span>
                            </div>
                            <div class="flex justify-between">
                                <span class="text-sm text-gray-600">75th Percentile:</span>
                                <span class="text-sm font-medium text-gray-900">{p75_clicks:.1f}</span>
                            </div>
                            <div class="flex justify-between">
                                <span class="text-sm text-gray-600">90th Percentile:</span>
                                <span class="text-sm font-medium text-gray-900">{p90_clicks:.1f}</span>
                            </div>
                            <div class="flex justify-between">
                                <span class="text-sm text-gray-600">IQR:</span>
                                <span class="text-sm font-medium text-gray-900">{iqr_clicks:.1f}</span>
                            </div>
                            <div class="flex justify-between">
                                <span class="text-sm text-gray-600">Maximum:</span>
                                <span class="text-sm font-medium text-gray-900">{max_clicks:.0f} ({summary_df.loc[summary_df['total_clicks'].idxmax()]['domain']})</span>
                            </div>
                            <div class="flex justify-between">
                                <span class="text-sm text-gray-600">Minimum:</span>
                                <span class="text-sm font-medium text-gray-900">{min_clicks:.0f} ({summary_df.loc[summary_df['total_clicks'].idxmin()]['domain']})</span>
                            </div>
                            <div class="flex justify-between">
                                <span class="text-sm text-gray-600">Total:</span>
                                <span class="text-sm font-medium text-gray-900">{total_clicks:.0f}</span>
                            </div>
                        </div>
                    </div>
        """
        
        # Update Impressions statistics with more detailed metrics
        html += f"""
                    <div class="bg-white border border-gray-200 rounded-lg p-4">
                        <h3 class="text-lg font-medium text-gray-800 mb-3">Impressions</h3>
                        <div class="space-y-2">
                            <div class="flex justify-between">
                                <span class="text-sm text-gray-600">Average:</span>
                                <span class="text-sm font-medium text-gray-900">{summary_df['total_impressions'].mean():.1f}</span>
                            </div>
                            <div class="flex justify-between">
                                <span class="text-sm text-gray-600">Median:</span>
                                <span class="text-sm font-medium text-gray-900">{median_impressions:.1f}</span>
                            </div>
                            <div class="flex justify-between">
                                <span class="text-sm text-gray-600">Standard Deviation:</span>
                                <span class="text-sm font-medium text-gray-900">{std_impressions:.1f}</span>
                            </div>
                            <div class="flex justify-between">
                                <span class="text-sm text-gray-600">25th Percentile:</span>
                                <span class="text-sm font-medium text-gray-900">{p25_impressions:.1f}</span>
                            </div>
                            <div class="flex justify-between">
                                <span class="text-sm text-gray-600">75th Percentile:</span>
                                <span class="text-sm font-medium text-gray-900">{p75_impressions:.1f}</span>
                            </div>
                            <div class="flex justify-between">
                                <span class="text-sm text-gray-600">90th Percentile:</span>
                                <span class="text-sm font-medium text-gray-900">{p90_impressions:.1f}</span>
                            </div>
                            <div class="flex justify-between">
                                <span class="text-sm text-gray-600">IQR:</span>
                                <span class="text-sm font-medium text-gray-900">{iqr_impressions:.1f}</span>
                            </div>
                            <div class="flex justify-between">
                                <span class="text-sm text-gray-600">Maximum:</span>
                                <span class="text-sm font-medium text-gray-900">{max_impressions:.0f} ({summary_df.loc[summary_df['total_impressions'].idxmax()]['domain']})</span>
                            </div>
                            <div class="flex justify-between">
                                <span class="text-sm text-gray-600">Minimum:</span>
                                <span class="text-sm font-medium text-gray-900">{min_impressions:.0f} ({summary_df.loc[summary_df['total_impressions'].idxmin()]['domain']})</span>
                            </div>
                            <div class="flex justify-between">
                                <span class="text-sm text-gray-600">Total:</span>
                                <span class="text-sm font-medium text-gray-900">{total_impressions:.0f}</span>
                            </div>
                        </div>
                    </div>
        """
        
        # Update CTR statistics with more detailed metrics
        html += f"""
                    <div class="bg-white border border-gray-200 rounded-lg p-4">
                        <h3 class="text-lg font-medium text-gray-800 mb-3">CTR</h3>
                        <div class="space-y-2">
                            <div class="flex justify-between">
                                <span class="text-sm text-gray-600">Average:</span>
                                <span class="text-sm font-medium text-gray-900">{avg_ctr:.2f}%</span>
                            </div>
                            <div class="flex justify-between">
                                <span class="text-sm text-gray-600">Median:</span>
                                <span class="text-sm font-medium text-gray-900">{summary_df['avg_ctr'].median():.2f}%</span>
                            </div>
                            <div class="flex justify-between">
                                <span class="text-sm text-gray-600">Standard Deviation:</span>
                                <span class="text-sm font-medium text-gray-900">{std_ctr:.2f}%</span>
                            </div>
                            <div class="flex justify-between">
                                <span class="text-sm text-gray-600">25th Percentile:</span>
                                <span class="text-sm font-medium text-gray-900">{p25_ctr:.2f}%</span>
                            </div>
                            <div class="flex justify-between">
                                <span class="text-sm text-gray-600">75th Percentile:</span>
                                <span class="text-sm font-medium text-gray-900">{p75_ctr:.2f}%</span>
                            </div>
                            <div class="flex justify-between">
                                <span class="text-sm text-gray-600">90th Percentile:</span>
                                <span class="text-sm font-medium text-gray-900">{p90_ctr:.2f}%</span>
                            </div>
                            <div class="flex justify-between">
                                <span class="text-sm text-gray-600">Maximum:</span>
                                <span class="text-sm font-medium text-gray-900">{max_ctr:.2f}% ({summary_df.loc[summary_df['avg_ctr'].idxmax()]['domain']})</span>
                            </div>
                            <div class="flex justify-between">
                                <span class="text-sm text-gray-600">Minimum:</span>
                                <span class="text-sm font-medium text-gray-900">{min_ctr:.2f}% ({summary_df.loc[summary_df['avg_ctr'].idxmin()]['domain']})</span>
                            </div>
                            <div class="flex justify-between">
                                <span class="text-sm text-gray-600">Overall CTR:</span>
                                <span class="text-sm font-medium text-gray-900">{(total_clicks / total_impressions) * 100:.2f}%</span>
                            </div>
                        </div>
                    </div>
        """
        
        # Update Position statistics with more detailed metrics
        html += f"""
                    <div class="bg-white border border-gray-200 rounded-lg p-4">
                        <h3 class="text-lg font-medium text-gray-800 mb-3">Position</h3>
                        <div class="space-y-2">
                            <div class="flex justify-between">
                                <span class="text-sm text-gray-600">Average:</span>
                                <span class="text-sm font-medium text-gray-900">{avg_position:.2f}</span>
                            </div>
                            <div class="flex justify-between">
                                <span class="text-sm text-gray-600">Median:</span>
                                <span class="text-sm font-medium text-gray-900">{summary_df['avg_position'].median():.2f}</span>
                            </div>
                            <div class="flex justify-between">
                                <span class="text-sm text-gray-600">Standard Deviation:</span>
                                <span class="text-sm font-medium text-gray-900">{std_position:.2f}</span>
                            </div>
                            <div class="flex justify-between">
                                <span class="text-sm text-gray-600">25th Percentile:</span>
                                <span class="text-sm font-medium text-gray-900">{p25_position:.2f}</span>
                            </div>
                            <div class="flex justify-between">
                                <span class="text-sm text-gray-600">75th Percentile:</span>
                                <span class="text-sm font-medium text-gray-900">{p75_position:.2f}</span>
                            </div>
                            <div class="flex justify-between">
                                <span class="text-sm text-gray-600">90th Percentile:</span>
                                <span class="text-sm font-medium text-gray-900">{p90_position:.2f}</span>
                            </div>
                            <div class="flex justify-between">
                                <span class="text-sm text-gray-600">IQR:</span>
                                <span class="text-sm font-medium text-gray-900">{iqr_position:.2f}</span>
                            </div>
                            <div class="flex justify-between">
                                <span class="text-sm text-gray-600">Best (Lowest):</span>
                                <span class="text-sm font-medium text-gray-900">{min_position:.2f} ({summary_df.loc[summary_df['avg_position'].idxmin()]['domain']})</span>
                            </div>
                            <div class="flex justify-between">
                                <span class="text-sm text-gray-600">Worst (Highest):</span>
                                <span class="text-sm font-medium text-gray-900">{max_position:.2f} ({summary_df.loc[summary_df['avg_position'].idxmax()]['domain']})</span>
                            </div>
                        </div>
                    </div>
        """
        
        # Update Key Insights section with more nuanced analysis
        html += """
                </div>
                
                <div class="bg-gray-50 p-4 rounded-lg">
                    <h3 class="text-md font-medium text-gray-800 mb-2">Key Insights</h3>
                    <ul class="list-disc pl-5 space-y-1 text-sm text-gray-700">
        """
        
        # Add insights based on the data
        if max_clicks > summary_df['total_clicks'].mean() * 2:
            html += f"""
                        <li>The top-performing domain ({summary_df.loc[summary_df['total_clicks'].idxmax()]['domain']}) has {max_clicks / summary_df['total_clicks'].mean():.1f}x more clicks than the average.</li>
            """
        
        # Add insight about median vs mean for clicks (indicates skew)
        if median_clicks < summary_df['total_clicks'].mean() * 0.8:
            html += f"""
                        <li>The median clicks ({median_clicks:.1f}) is significantly lower than the mean ({summary_df['total_clicks'].mean():.1f}), indicating that a few high-performing domains are skewing the average upward.</li>
            """
        
        # Add insight about standard deviation for clicks
        if std_clicks > summary_df['total_clicks'].mean():
            html += f"""
                        <li>The high standard deviation in clicks ({std_clicks:.1f}) indicates substantial variation in performance across domains.</li>
            """
        
        # Add insight about IQR for CTR
        if iqr_ctr > avg_ctr * 0.5:
            html += f"""
                        <li>The wide interquartile range for CTR ({iqr_ctr:.2f}%) suggests significant differences in engagement rates across domains.</li>
            """
        
        # Add insight about position distribution
        if p25_position < avg_position * 0.7:
            html += f"""
                        <li>25% of domains have an average position better than {p25_position:.2f}, significantly outperforming the overall average of {avg_position:.2f}.</li>
            """
        
        # Add general insights
        html += f"""
                        <li>Overall, the domains receive an average of {summary_df['total_clicks'].mean():.1f} clicks from {summary_df['total_impressions'].mean():.1f} impressions.</li>
                        <li>The average CTR across all domains is {avg_ctr:.2f}%, with positions averaging {avg_position:.2f}.</li>
                    </ul>
                </div>
            </div>
        """
        
        # Add domain comparison table
        html += """
                <h3 class="text-lg font-medium text-gray-800 mb-2">Domain Comparison</h3>
                <div class="overflow-x-auto">
                    <table class="min-w-full divide-y divide-gray-200">
                        <thead class="bg-gray-50">
                            <tr>
                                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Domain</th>
                                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Clicks</th>
                                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Impressions</th>
                                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">CTR</th>
                                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Position</th>
                            </tr>
                        </thead>
                        <tbody class="bg-white divide-y divide-gray-200">
        """
        
        # Sort the dataframe by impressions in descending order
        sorted_summary_df = summary_df.sort_values('total_impressions', ascending=False)
        
        # Add rows for each domain
        for _, row in sorted_summary_df.iterrows():
            html += f"""
                            <tr>
                                <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{row['domain']}</td>
                                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{int(row['total_clicks'])}</td>
                                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{int(row['total_impressions'])}</td>
                                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{row['avg_ctr']:.2f}%</td>
                                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{row['avg_position']:.2f}</td>
                            </tr>
            """
        
        html += """
                        </tbody>
                    </table>
                </div>
            </div>
        """
    
    # Add detailed domain sections
    for domain_name, domain_data in domain_details.items():
        html += f"""
            <div class="bg-white rounded-lg shadow-md p-6 mb-8">
                <h2 class="text-xl font-semibold text-gray-800 mb-4">{domain_name}</h2>
                
                <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        """
        
        # Add device distribution if available
        if 'devices' in domain_data and domain_data['devices'] is not None:
            devices_df = domain_data['devices']
            
            # Create device distribution HTML
            html += """
                    <div>
                        <h3 class="text-lg font-medium text-gray-800 mb-2">Device Distribution</h3>
                        <div class="overflow-x-auto">
                            <table class="min-w-full divide-y divide-gray-200">
                                <thead class="bg-gray-50">
                                    <tr>
                                        <th class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Device</th>
                                        <th class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Clicks</th>
                                        <th class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Click %</th>
                                    </tr>
                                </thead>
                                <tbody class="bg-white divide-y divide-gray-200">
            """
            
            for _, row in devices_df.iterrows():
                html += f"""
                                    <tr>
                                        <td class="px-4 py-2 whitespace-nowrap text-sm font-medium text-gray-900">{row['Device']}</td>
                                        <td class="px-4 py-2 whitespace-nowrap text-sm text-gray-500">{int(row['Clicks'])}</td>
                                        <td class="px-4 py-2 whitespace-nowrap text-sm text-gray-500">{row['Click %']:.1f}%</td>
                                    </tr>
                """
            
            html += """
                                </tbody>
                            </table>
                        </div>
                    </div>
            """
        
        # Add top queries if available
        if 'queries' in domain_data and domain_data['queries'] is not None:
            queries_df = domain_data['queries'].head(10)
            
            # Create top queries HTML
            html += """
                    <div>
                        <h3 class="text-lg font-medium text-gray-800 mb-2">Top Queries</h3>
                        <div class="overflow-x-auto">
                            <table class="min-w-full divide-y divide-gray-200">
                                <thead class="bg-gray-50">
                                    <tr>
                                        <th class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Query</th>
                                        <th class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Clicks</th>
                                        <th class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Impressions</th>
                                    </tr>
                                </thead>
                                <tbody class="bg-white divide-y divide-gray-200">
            """
            
            for _, row in queries_df.iterrows():
                query_col = queries_df.columns[0]  # Get the name of the first column (query column)
                html += f"""
                                    <tr>
                                        <td class="px-4 py-2 whitespace-nowrap text-sm font-medium text-gray-900">{row[query_col]}</td>
                                        <td class="px-4 py-2 whitespace-nowrap text-sm text-gray-500">{int(row['Clicks'])}</td>
                                        <td class="px-4 py-2 whitespace-nowrap text-sm text-gray-500">{int(row['Impressions'])}</td>
                                    </tr>
                """
            
            html += """
                                </tbody>
                            </table>
                        </div>
                    </div>
            """
        
        # Add top pages if available
        if 'pages' in domain_data and domain_data['pages'] is not None:
            pages_df = domain_data['pages'].head(10)
            
            # Create top pages HTML
            html += """
                    <div class="col-span-1 md:col-span-2">
                        <h3 class="text-lg font-medium text-gray-800 mb-2">Top Pages</h3>
                        <div class="overflow-x-auto">
                            <table class="min-w-full divide-y divide-gray-200">
                                <thead class="bg-gray-50">
                                    <tr>
                                        <th class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Page</th>
                                        <th class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Clicks</th>
                                        <th class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Impressions</th>
                                        <th class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">CTR</th>
                                        <th class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Position</th>
                                    </tr>
                                </thead>
                                <tbody class="bg-white divide-y divide-gray-200">
            """
            
            for _, row in pages_df.iterrows():
                page_col = pages_df.columns[0]  # Get the name of the first column (page column)
                html += f"""
                                    <tr>
                                        <td class="px-4 py-2 whitespace-nowrap text-sm font-medium text-gray-900">{row[page_col]}</td>
                                        <td class="px-4 py-2 whitespace-nowrap text-sm text-gray-500">{int(row['Clicks'])}</td>
                                        <td class="px-4 py-2 whitespace-nowrap text-sm text-gray-500">{int(row['Impressions'])}</td>
                                        <td class="px-4 py-2 whitespace-nowrap text-sm text-gray-500">{float(row['CTR']):.2f}%</td>
                                        <td class="px-4 py-2 whitespace-nowrap text-sm text-gray-500">{float(row['Position']):.2f}</td>
                                    </tr>
                """
            
            html += """
                                </tbody>
                            </table>
                        </div>
                    </div>
            """
        
        html += """
                </div>
            </div>
        """
    
    # Close HTML
    html += """
        </div>
    </body>
    </html>
    """
    
    return html

def analyze_domain(domain_folder):
    """Analyze data for a specific domain."""
    print(f"\n{'='*80}\nAnalyzing domain: {os.path.basename(domain_folder)}\n{'='*80}")
    
    # Load all CSV files
    countries_df = load_csv_data(domain_folder, "Countries.csv")
    dates_df = load_csv_data(domain_folder, "Dates.csv")
    devices_df = load_csv_data(domain_folder, "Devices.csv")
    filters_df = load_csv_data(domain_folder, "Filters.csv")
    pages_df = load_csv_data(domain_folder, "Pages.csv")
    search_appearance_df = load_csv_data(domain_folder, "Search appearance.csv")
    queries_df = load_csv_data(domain_folder, "Queries.csv")
    
    # Analyze dates data (time series)
    if dates_df is not None:
        print("\n--- Time Series Analysis ---")
        # Convert Date to datetime
        dates_df['Date'] = pd.to_datetime(dates_df['Date'])
        
        # Sort by date
        dates_df = dates_df.sort_values('Date')
        
        # Clean CTR column - remove % and convert to float
        if 'CTR' in dates_df.columns:
            dates_df['CTR'] = dates_df['CTR'].astype(str).str.replace('%', '').str.replace(',', '.').astype(float)
        
        # Calculate summary statistics
        total_clicks = dates_df['Clicks'].sum()
        total_impressions = dates_df['Impressions'].sum()
        avg_ctr = (dates_df['Clicks'].sum() / dates_df['Impressions'].sum()) * 100
        avg_position = dates_df['Position'].mean()
        
        print(f"Total Clicks: {total_clicks}")
        print(f"Total Impressions: {total_impressions}")
        print(f"Average CTR: {avg_ctr:.2f}%")
        print(f"Average Position: {avg_position:.2f}")
        
        # Calculate monthly aggregates
        dates_df['Month'] = dates_df['Date'].dt.to_period('M')
        
        try:
            monthly_data = dates_df.groupby('Month').agg({
                'Clicks': 'sum',
                'Impressions': 'sum',
                'CTR': 'mean',
                'Position': 'mean'
            })
            
            print("\nMonthly Performance:")
            print(monthly_data)
        except Exception as e:
            print(f"\nError calculating monthly aggregates: {e}")
            print("Attempting to calculate with numeric columns only...")
            
            # Try with just the numeric columns
            monthly_data = dates_df.groupby('Month').agg({
                'Clicks': 'sum',
                'Impressions': 'sum',
                'Position': 'mean'
            })
            
            # Calculate CTR from the aggregated data
            monthly_data['CTR'] = (monthly_data['Clicks'] / monthly_data['Impressions']) * 100
            
            print("\nMonthly Performance:")
            print(monthly_data)
    
    # Clean CTR column in other dataframes
    for df in [countries_df, devices_df, pages_df, search_appearance_df, queries_df]:
        if df is not None and 'CTR' in df.columns:
            df['CTR'] = df['CTR'].astype(str).str.replace('%', '').str.replace(',', '.').astype(float)
    
    # Analyze countries data
    if countries_df is not None:
        print("\n--- Countries Analysis ---")
        # Sort by clicks in descending order
        countries_sorted = countries_df.sort_values('Clicks', ascending=False)
        
        print("Top 5 Countries by Clicks:")
        print(countries_sorted.head(5))
        
        # Calculate percentage of total clicks and impressions
        total_clicks = countries_df['Clicks'].sum()
        total_impressions = countries_df['Impressions'].sum()
        
        countries_df['Click %'] = (countries_df['Clicks'] / total_clicks) * 100
        countries_df['Impression %'] = (countries_df['Impressions'] / total_impressions) * 100
        
        print("\nCountry Distribution:")
        print(countries_df[['Country', 'Clicks', 'Click %', 'Impressions', 'Impression %']].head(10))
    
    # Analyze devices data
    if devices_df is not None:
        print("\n--- Devices Analysis ---")
        print(devices_df)
        
        # Calculate percentage of total for each device
        total_clicks = devices_df['Clicks'].sum()
        total_impressions = devices_df['Impressions'].sum()
        
        devices_df['Click %'] = (devices_df['Clicks'] / total_clicks) * 100
        devices_df['Impression %'] = (devices_df['Impressions'] / total_impressions) * 100
        
        print("\nDevice Distribution:")
        print(devices_df[['Device', 'Clicks', 'Click %', 'Impressions', 'Impression %']])
    
    # Analyze top pages
    if pages_df is not None:
        print("\n--- Top Pages Analysis ---")
        # Sort by clicks in descending order
        pages_sorted = pages_df.sort_values('Clicks', ascending=False)
        
        print("Top 10 Pages by Clicks:")
        print(pages_sorted.head(10))
        
        # Calculate what percentage of total traffic goes to top 10 pages
        total_clicks = pages_df['Clicks'].sum()
        top10_clicks = pages_sorted.head(10)['Clicks'].sum()
        
        print(f"\nTop 10 pages account for {(top10_clicks/total_clicks)*100:.2f}% of all clicks")
    
    # Analyze top queries
    if queries_df is not None:
        print("\n--- Top Queries Analysis ---")
        # Sort by clicks in descending order
        queries_sorted = queries_df.sort_values('Clicks', ascending=False)
        
        print("Top 10 Queries by Clicks:")
        print(queries_sorted.head(10))
        
        # Calculate what percentage of total traffic comes from top 10 queries
        total_clicks = queries_df['Clicks'].sum()
        top10_clicks = queries_sorted.head(10)['Clicks'].sum()
        
        print(f"\nTop 10 queries account for {(top10_clicks/total_clicks)*100:.2f}% of all clicks")
    
    # Store domain details for HTML report
    domain_details = {
        'dates': dates_df,
        'countries': countries_df,
        'devices': devices_df,
        'pages': pages_df.sort_values('Clicks', ascending=False) if pages_df is not None else None,
        'queries': queries_df.sort_values('Clicks', ascending=False) if queries_df is not None else None
    }
    
    return {
        'domain': os.path.basename(domain_folder),
        'total_clicks': dates_df['Clicks'].sum() if dates_df is not None else 0,
        'total_impressions': dates_df['Impressions'].sum() if dates_df is not None else 0,
        'avg_ctr': avg_ctr if dates_df is not None else 0,
        'avg_position': avg_position if dates_df is not None else 0
    }, domain_details

def main():
    # Find all domain folders in the data directory
    data_dir = "data"
    domain_folders = [os.path.join(data_dir, folder) for folder in os.listdir(data_dir) 
                     if os.path.isdir(os.path.join(data_dir, folder))]
    
    # Analyze each domain
    domain_summaries = []
    all_domain_details = {}
    
    for folder in domain_folders:
        domain_name = os.path.basename(folder)
        summary, details = analyze_domain(folder)
        domain_summaries.append(summary)
        all_domain_details[domain_name] = details
    
    # Create a summary dataframe for all domains
    if domain_summaries:
        summary_df = pd.DataFrame(domain_summaries)
        print("\n--- Overall Summary for All Domains ---")
        print(summary_df)
        
        # Calculate aggregate statistics
        print("\nAggregate Statistics:")
        print(f"Total Clicks Across All Domains: {summary_df['total_clicks'].sum()}")
        print(f"Total Impressions Across All Domains: {summary_df['total_impressions'].sum()}")
        print(f"Average CTR Across All Domains: {summary_df['avg_ctr'].mean():.2f}%")
        print(f"Average Position Across All Domains: {summary_df['avg_position'].mean():.2f}")
        print(f"Best Performing Domain (by clicks): {summary_df.loc[summary_df['total_clicks'].idxmax()]['domain']}")
        print(f"Best Performing Domain (by CTR): {summary_df.loc[summary_df['avg_ctr'].idxmax()]['domain']}")
    
    # Generate HTML report
    html_report = generate_html_report(domain_summaries, all_domain_details)
    
    # Save HTML report to file
    report_dir = "reports"
    os.makedirs(report_dir, exist_ok=True)
    report_path = os.path.join(report_dir, f"search_console_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html")
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(html_report)
    
    print(f"\nHTML report generated: {report_path}")

if __name__ == "__main__":
    main()
