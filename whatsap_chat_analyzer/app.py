from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import preprocess
import re
import stats
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import numpy as np
import base64
from io import BytesIO
import os

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file selected')
        return redirect(request.url)
    
    file = request.files['file']
    if file.filename == '':
        flash('No file selected')
        return redirect(request.url)
    
    if file:
        try:
            # Read file content
            data = file.read().decode('utf-8')
            
            # Process the data
            df = preprocess.preprocess(data)
            
            # Check if dataframe is empty
            if df.empty:
                flash('Unable to process the chat file. Please ensure it\'s a valid WhatsApp export.')
                return redirect(url_for('index'))
            
            # Get unique users
            user_list = df['User'].unique().tolist()
            if 'Group Notification' in user_list:
                user_list.remove('Group Notification')
            user_list.sort()
            user_list.insert(0, "Overall")
            
            # Store dataframe in session or temporary storage
            # For simplicity, we'll store it as a CSV temporarily
            df.to_csv('temp_data.csv', index=False)
            
            return render_template('analysis.html', users=user_list)
            
        except Exception as e:
            flash(f'Error processing file: {str(e)}')
            return redirect(url_for('index'))

@app.route('/analyze', methods=['POST'])
def analyze():
    selected_user = request.form.get('user')
    
    # Load the data
    import pandas as pd
    df = pd.read_csv('temp_data.csv')
    
    # Get statistics
    num_messages, num_words, media_omitted, links = stats.fetchstats(selected_user, df)
    
    # Generate visualizations
    charts = {}
    
    # Busy users chart (only for Overall)
    if selected_user == 'Overall':
        busycount, newdf = stats.fetchbusyuser(df)
        charts['busy_users'] = create_bar_chart(busycount.index, busycount.values, 'Most Busy Users', 'red')
    
    # Word cloud
    df_img = stats.createwordcloud(selected_user, df)
    charts['wordcloud'] = create_wordcloud_image(df_img)
    
    # Most common words
    most_common_df = stats.getcommonwords(selected_user, df)
    charts['common_words'] = create_horizontal_bar_chart(most_common_df[0], most_common_df[1], 'Most Common Words')
    
    # Emoji analysis
    emoji_df = stats.getemojistats(selected_user, df)
    emoji_df.columns = ['Emoji', 'Count']
    emojicount = list(emoji_df['Count'])
    perlist = [(i/sum(emojicount))*100 for i in emojicount]
    emoji_df['Percentage use'] = np.array(perlist)
    
    # Monthly timeline
    time = stats.monthtimeline(selected_user, df)
    charts['monthly_timeline'] = create_line_chart(time['Time'], time['Message'], 'Monthly Timeline', 'green')
    
    # Activity maps
    busy_day = stats.weekactivitymap(selected_user, df)
    busy_month = stats.monthactivitymap(selected_user, df)
    charts['busy_day'] = create_bar_chart(busy_day.index, busy_day.values, 'Most Busy Day', 'purple')
    charts['busy_month'] = create_bar_chart(busy_month.index, busy_month.values, 'Most Busy Month', 'orange')
    
    return render_template('results.html', 
                         selected_user=selected_user,
                         num_messages=num_messages,
                         num_words=num_words,
                         media_omitted=media_omitted,
                         links=links,
                         emoji_df=emoji_df.to_html(classes='table table-striped'),
                         charts=charts)

def create_bar_chart(x, y, title, color='blue'):
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(x, y, color=color)
    plt.xticks(rotation=45, ha='right')
    plt.title(title)
    plt.tight_layout()
    return plot_to_base64(fig)

def create_horizontal_bar_chart(x, y, title):
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.barh(x, y)
    plt.title(title)
    plt.tight_layout()
    return plot_to_base64(fig)

def create_line_chart(x, y, title, color='blue'):
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(x, y, color=color)
    plt.xticks(rotation=45, ha='right')
    plt.title(title)
    plt.tight_layout()
    return plot_to_base64(fig)

def create_wordcloud_image(wordcloud):
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    return plot_to_base64(fig)

def plot_to_base64(fig):
    buf = BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    plot_data = base64.b64encode(buf.read()).decode('utf-8')
    plt.close(fig)
    return f"data:image/png;base64,{plot_data}"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
