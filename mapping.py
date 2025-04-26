import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.patches as patches

COLOR_PALETTE = ['#4f81bd', '#c0504d', '#9bbb59', '#8064a2', '#4bacc6', '#f79646']
TEXT_COLORS = ['#1f497d', '#eeece1', 'black', 'white']

def load_data(file_path='database.csv', sep=';'):
    """
    Load the CSV data into a Pandas DataFrame
    
    Parameters:
    -----------
    file_path : str
        Path to the CSV file
    sep : str
        Separator used in the CSV file
        
    Returns:
    --------
    pandas.DataFrame
        Loaded data
    """
    return pd.read_csv(file_path, sep=sep)

def categorize_publisher(publisher):
    """
    Categorize publishers into groups
    
    Parameters:
    -----------
    publisher : str
        Publisher name
        
    Returns:
    --------
    str
        Publisher category
    """
    if 'IEEE' in publisher:
        return 'IEEE'
    elif 'Springer' in publisher:
        return 'Springer'
    elif 'Nature' in publisher:
        return 'Nature'
    else:
        return 'Other'

def plot_type_distribution(data, figsize=(10, 6), save_path=None, title_fontsize=16, label_fontsize=12, tick_fontsize=10):
    """
    Create a column chart displaying data grouped by type
    
    Parameters:
    -----------
    data : pandas.DataFrame
        Data to plot
    figsize : tuple
        Figure size
    save_path : str, optional
        Path to save the figure
    title_fontsize : int
        Font size for the title
    label_fontsize : int
        Font size for axis labels
    tick_fontsize : int
        Font size for tick labels
    """
    type_counts = data['type'].value_counts()
    plt.figure(figsize=figsize)
    ax = type_counts.plot(kind='bar', color=COLOR_PALETTE[0])
    plt.title('Distribution of Types', fontsize=title_fontsize, color=TEXT_COLORS[0])
    plt.xlabel('Type', fontsize=label_fontsize, color=TEXT_COLORS[0])
    plt.ylabel('Count', fontsize=label_fontsize, color=TEXT_COLORS[0])
    
    # Adjust tick label font size
    plt.xticks(fontsize=tick_fontsize, color=TEXT_COLORS[0])
    plt.yticks(fontsize=tick_fontsize, color=TEXT_COLORS[0])
    
    # Add value labels on top of bars
    for i, v in enumerate(type_counts):
        ax.text(i, v + 0.1, str(v), ha='center', fontsize=tick_fontsize, color=TEXT_COLORS[0])
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight', pad_inches=0)
    plt.show()

def plot_types_per_year(data, figsize=(16, 9), save_path=None, title_fontsize=16, label_fontsize=14, tick_fontsize=12, legend_fontsize=10):
    """
    Create a chart of types per year
    """
    year_type_counts = data.groupby(['year', 'type']).size().unstack('type', fill_value=0)
    
    # Use the first two colors from the palette
    colors = COLOR_PALETTE[:2]
    
    plt.figure(figsize=figsize)
    ax = year_type_counts.plot(kind='bar', color=colors)
    
    # No title - will be added in the poster
    
    # Adjust axis labels with larger font and black color
    plt.xlabel('Year', fontsize=label_fontsize, color='black')
    plt.ylabel('Number of Publications', fontsize=label_fontsize, color='black')
    
    # Adjust legend with black text and box
    plt.legend(title='Type', fontsize=legend_fontsize, title_fontsize=legend_fontsize, 
              labelcolor='black', edgecolor='black', frameon=True, 
              framealpha=1.0, facecolor='white')
    
    # Make x-axis labels horizontal with larger font and black color
    plt.xticks(rotation=0, fontsize=tick_fontsize, color='black')
    plt.yticks(fontsize=tick_fontsize, color='black')
    
    if save_path:
        # Adjust subplot parameters to give specified padding
        plt.subplots_adjust(left=0, right=1, bottom=0, top=1)
        plt.savefig(save_path, dpi=300, bbox_inches='tight', pad_inches=0)
    plt.show()

def plot_publications_by_publisher(data, figsize=(16, 9), save_path=None, title_fontsize=16, label_fontsize=14, tick_fontsize=12, legend_fontsize=10):
    """
    Create a stacked bar chart of publications by type and publisher
    """
    # Add publisher group column if it doesn't exist
    if 'publisher_group' not in data.columns:
        data['publisher_group'] = data['Publisher'].apply(categorize_publisher)
    
    grouped = data.groupby(['type', 'publisher_group']).size().unstack(fill_value=0)
    
    # Use the first four colors from the palette
    colors = COLOR_PALETTE[:4]
    
    plt.figure(figsize=figsize)
    ax = grouped.plot(kind='bar', stacked=True, color=colors)
    
    # No title - will be added in the poster
    
    # Remove x-axis label
    plt.xlabel('')
    
    # Adjust y-axis label with larger font and black color
    plt.ylabel('Number of Publications', fontsize=label_fontsize, color='black')
    
    # Make x-axis labels horizontal with larger font and black color
    plt.xticks(rotation=0, fontsize=tick_fontsize, color='black')
    plt.yticks(fontsize=tick_fontsize, color='black')
    
    # Improve legend with black text and box
    plt.legend(title='Publisher', bbox_to_anchor=(1.05, 1), loc='upper left', 
              fontsize=legend_fontsize, title_fontsize=legend_fontsize,
              labelcolor='black', edgecolor='black', frameon=True, 
              framealpha=1.0, facecolor='white')
    
    if save_path:
        # Adjust subplot parameters to give specified padding
        plt.subplots_adjust(left=0, right=1, bottom=0, top=1)
        plt.savefig(save_path, dpi=300, bbox_inches='tight', pad_inches=0)
    plt.show()

def plot_keyword_distribution(data, top_n=15, figsize=(16, 9), save_path=None, 
                              title_fontsize=16, label_fontsize=14, tick_fontsize=12):
    """
    Create a bar chart showing the distribution of the most frequent keywords
    
    Parameters:
    -----------
    data : pandas.DataFrame
        Data to plot containing a 'keywords' column
    top_n : int
        Number of top keywords to display
    figsize : tuple
        Figure size
    save_path : str, optional
        Path to save the figure
    title_fontsize : int
        Font size for the title
    label_fontsize : int
        Font size for axis labels
    tick_fontsize : int
        Font size for tick labels
    """
    # Extract keywords and create a list of individual keywords
    all_keywords = []
    for keywords in data['keywords']:
        if pd.notnull(keywords):
            for keyword in keywords.split(';'):
                # Clean and normalize the keyword
                keyword = keyword.strip().lower()
                if keyword:  # Only add non-empty keywords
                    all_keywords.append(keyword)
    
    # Convert the list of keywords to a Pandas Series
    keyword_series = pd.Series(all_keywords)
    
    # Create a DataFrame with keyword counts and sort by count
    keyword_counts = keyword_series.value_counts().reset_index()
    keyword_counts.columns = ['Keyword', 'Count']
    
    # Get the top N keywords
    top_keywords = keyword_counts.head(top_n)
    
    # Create the plot
    plt.figure(figsize=figsize)
    ax = sns.barplot(
        data=top_keywords, 
        y='Keyword', 
        x='Count',
        color=COLOR_PALETTE[3],  # Use purple from your palette
        orient='h'  # Horizontal bars
    )
    
    # No title - will be added in the poster
    
    # Adjust axis labels with larger font and black color
    plt.xlabel('Frequency', fontsize=label_fontsize, color='black')
    plt.ylabel('Keywords', fontsize=label_fontsize, color='black')
    
    # Adjust tick labels with black color
    plt.xticks(fontsize=tick_fontsize, color='black')
    plt.yticks(fontsize=tick_fontsize, color='black')
    
    # Add value labels at the end of each bar
    for i, v in enumerate(top_keywords['Count']):
        ax.text(v + 0.1, i, str(v), va='center', fontsize=tick_fontsize, color='black')
    
    # Adjust layout
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight', pad_inches=0)
    plt.show()

def plot_systematic_mapping_process(figsize=(12, 5), save_path=None, label_fontsize=14, tick_fontsize=12):
    """
    Create a horizontal flowchart of the systematic mapping review process with blue boxes on top
    and green/red boxes on the second line
    """
    # Create figure and axis with minimal margins
    fig = plt.figure(figsize=figsize, constrained_layout=False)
    ax = fig.add_axes([0, 0, 1, 1])  # Use the entire figure space
    
    # Set background color to white
    ax.set_facecolor('white')
    fig.patch.set_facecolor('white')
    
    # Define box dimensions
    box_width = 2.0
    box_height = 1.0  # Reduced height
    
    # Define positions for each box (x, y) in a two-row layout
    # Blue boxes on top, green and red boxes below
    positions = {
        'databases': (-5, 1),
        'initial_results': (-2, 1),
        'screening': (1, 1),
        'selected': (4, 1),
        'analysis': (1, -1),
        'findings': (4, -1),
        'research_questions': (-2, -1)  # Research questions to the left of analysis
    }
    
    # Define colors for different sections using our palette
    colors = {
        'search': COLOR_PALETTE[0],     # Light blue for search process
        'analysis': COLOR_PALETTE[2],   # Light green for analysis
        'results': COLOR_PALETTE[5]     # Orange for results
    }
    
    # Map boxes to their color groups
    box_colors = {
        'databases': colors['search'],
        'initial_results': colors['search'],
        'screening': colors['search'],
        'selected': colors['search'],
        'research_questions': colors['analysis'],
        'analysis': colors['analysis'],
        'findings': colors['results']
    }
    
    # Draw boxes with colors
    boxes = {}
    for name, pos in positions.items():
        # Create box with a light version of the color (alpha=0.15 for subtle fill)
        boxes[name] = patches.Rectangle(
            (pos[0] - box_width/2, pos[1] - box_height/2),
            box_width, box_height,
            linewidth=1,
            edgecolor=box_colors[name],
            facecolor=box_colors[name],
            alpha=0.15
        )
        ax.add_patch(boxes[name])
    
    # Add text to boxes with updated reduced content
    box_texts = {
        'databases': 'Databases:\n\nWoS\nScopus',
        'initial_results': '559 Papers',
        'screening': 'Two-phase\nscreening\nprocess',
        'selected': '16 Articles',
        'research_questions': 'Research\nQuestions',
        'analysis': 'Detailed\nanalysis',
        'findings': 'Findings'
    }
    
    for name, text in box_texts.items():
        pos = positions[name]
        ax.text(pos[0], pos[1], text, ha='center', va='center', 
                fontsize=label_fontsize, color='black')
    
    # Draw horizontal arrows between the search flow boxes (top row)
    search_flow = ['databases', 'initial_results', 'screening', 'selected']
    for i in range(len(search_flow) - 1):
        start = positions[search_flow[i]]
        end = positions[search_flow[i + 1]]
        # Calculate connection points at box borders
        start_x = start[0] + box_width/2  # Right side of the start box
        end_x = end[0] - box_width/2      # Left side of the end box
        ax.annotate('', 
                   xy=(end_x, end[1]),           # End point at left of target box
                   xytext=(start_x, start[1]),   # Start point at right of source box
                   arrowprops=dict(arrowstyle='->', color='black', linewidth=2))
    
    # Draw horizontal arrow between analysis and findings (bottom row)
    start = positions['analysis']
    end = positions['findings']
    start_x = start[0] + box_width/2  # Right side of the analysis box
    end_x = end[0] - box_width/2      # Left side of the findings box
    ax.annotate('', 
               xy=(end_x, end[1]),           # End point at left of findings box
               xytext=(start_x, start[1]),   # Start point at right of analysis box
               arrowprops=dict(arrowstyle='->', color='black', linewidth=2))
    
    # Draw vertical arrow from selected to analysis
    start = positions['selected']
    end = positions['analysis']
    start_y = start[1] - box_height/2  # Bottom of selected box
    end_y = end[1] + box_height/2      # Top of analysis box
    ax.annotate('', 
               xy=(end[0], end_y),           # End at top of analysis box
               xytext=(start[0], start_y),   # Start at bottom of selected box
               arrowprops=dict(arrowstyle='->', color='black', linewidth=2))
    
    # Draw horizontal arrow from research questions to analysis
    start = positions['research_questions']
    end = positions['analysis']
    start_x = start[0] + box_width/2  # Right side of research questions box
    end_x = end[0] - box_width/2      # Left side of analysis box
    ax.annotate('', 
               xy=(end_x, end[1]),           # End at left of analysis box
               xytext=(start_x, start[1]),   # Start at right of research questions box
               arrowprops=dict(arrowstyle='->', color='black', linewidth=2))
    
    # Set axis limits with minimal padding
    ax.set_xlim(-7, 6)
    ax.set_ylim(-1.8, 2)  # Reduced vertical space
    
    # Remove axis
    ax.axis('off')
    
    if save_path:
        # Remove all padding when saving the figure
        plt.savefig(save_path, dpi=300, bbox_inches='tight', pad_inches=0, 
                   facecolor='white', edgecolor='none', transparent=True)
    plt.show()

def main():
    data = load_data()
    
    plot_types_per_year(data, save_path='poster/by_year.png', 
                       title_fontsize=16, label_fontsize=14, tick_fontsize=12, legend_fontsize=10)
    
    plot_publications_by_publisher(data, save_path='poster/conf_by_editor.png', 
                                 title_fontsize=16, label_fontsize=14, tick_fontsize=12, legend_fontsize=10)

    
    plot_systematic_mapping_process(save_path='poster/systematic_mapping_process.png',
                                  label_fontsize=14, tick_fontsize=12)
    
    plot_keyword_distribution(data, top_n=15, save_path='poster/keyword_distribution.png',
                            title_fontsize=16, label_fontsize=14, tick_fontsize=12)
    
    plot_type_distribution(data, save_path='poster/type_distribution.png', 
                          title_fontsize=16, label_fontsize=12, tick_fontsize=10)

if __name__ == "__main__":
    main()
