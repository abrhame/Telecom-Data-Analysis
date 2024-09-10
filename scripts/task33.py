import pandas as pd
from scipy import stats

def handle_missing_outliers(df):


    # Detect outliers using Z-score for specific columns
    columns_to_check = ['TCP', 'RTT', 'Throughput']
    if all(col in df.columns for col in columns_to_check):
        z_scores = np.abs(stats.zscore(df[columns_to_check].dropna()))
        outliers = (z_scores > 3).any(axis=1)
        df.loc[outliers, columns_to_check] = df[columns_to_check].median()

    return df

def aggregate_customer_data(df):
    # Aggregate data by customer ID
    customer_aggregated = df.groupby('CustomerID').agg(
        avg_TCP_retransmission=('TCP', 'mean'),
        avg_RTT=('RTT', 'mean'),
        handset_type=('Handset', 'mode'),
        avg_throughput=('Throughput', 'mean')
    ).reset_index()
    
    return customer_aggregated


def compute_statistics(df, column):
    top_values = df[column].nlargest(10)
    bottom_values = df[column].nsmallest(10)
    most_frequent = df[column].mode().head(10)  # mode() returns a series of modes
    
    return top_values, bottom_values, most_frequent


def throughput_distribution(df):
    # Compute average throughput per handset type
    throughput_per_handset = df.groupby('Handset')['Throughput'].mean()
    
    return throughput_per_handset


# Distribution of average TCP retransmission per handset type
def tcp_retransmission_per_handset(df):
    # Compute average TCP retransmission per handset type
    tcp_retransmission_per_handset = df.groupby('Handset')['TCP'].mean()
    
    return tcp_retransmission_per_handset


def perform_kmeans_clustering(df, n_clusters=3):
    for column in ['TCP', 'RTT', 'Throughput']:
        df[column] = pd.to_numeric(df[column], errors='coerce')

    # Prepare data for clustering
    clustering_data = df[['avg_TCP_retransmission', 'avg_RTT', 'avg_throughput']]
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(clustering_data)
    
    # Apply K-Means clustering
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    df['Cluster'] = kmeans.fit_predict(scaled_data)