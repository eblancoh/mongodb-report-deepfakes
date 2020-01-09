import pandas as pd
from pandas.io.json import json_normalize  
import json
from database import db_read
import os
import matplotlib.pyplot as plt
import seaborn as sns



def df_builder(query, collector):
    """
    query: i.e., {"link": "https://www.youtube.com/watch?v=VWrhRBb-1Ig"}
                 {"filename": "Bill Hader channels Tom Cruise [DeepFake].mp4"}
    collector: "faceartifacts" | "faceforensics"
    """
    cursor = db_read(query, collector)
    content = list(cursor)[0]
    df = json_normalize(content)

    if len(df["hash"].iloc[0]) > 40:
        df["hash"].iloc[0] = df["hash"].iloc[0][0:40] + '...'

    if collector == "faceforensics":
        df_proba = pd.DataFrame(json_normalize(content, 
                                  record_path='fake_prediction_FaceForensics')['probability'].describe())
        probs = pd.DataFrame(json_normalize(content, 
                                  record_path='fake_prediction_FaceForensics'))
    elif collector == "facewarpingartifacts":
        df_proba = pd.DataFrame(json_normalize(content, 
                                  record_path='fake_prediction_FaceWarpingArtifacts')['probability'].describe())
        probs = pd.DataFrame(json_normalize(content, 
                                  record_path='fake_prediction_FaceWarpingArtifacts'))
    
    # Extract streams info
    df_streams = df['metadata.streams'].apply(pd.Series)
    df_streams = json_normalize(df_streams.melt()['value']).T
    # Extract path to video
    df_path_to_video = df['metadata.path_to_video']
    # Extract video info
    df_video = df['metadata.video'].apply(pd.Series)
    df_video = json_normalize(df_video.melt()['value']).T
    # Extract audio info
    df_audio = df['metadata.audio'].apply(pd.Series)
    df_audio = json_normalize(df_audio.melt()['value']).T
    # Extract metadata info
    df_metadata = df[['metadata.metadata.major_brand', 
                      'metadata.metadata.minor_version',
                      'metadata.metadata.compatible_brands',
                      'metadata.metadata.creation_time',
                      'metadata.metadata.Duration',
                      'metadata.metadata.start',
                      'metadata.metadata.bitrate']].T
    # Delete unnecesary information from main dataframe
    df = df[['_id', 'hash', 'link', 'filename', 'fake']].T

    return df, df_proba, df_path_to_video, df_streams, df_video, df_audio, df_metadata, probs


def probs_render(probs):
    sns.set(color_codes=True)

    f, (a1, a2) = plt.subplots(1, 2, 
                               gridspec_kw={'width_ratios': [5, 1], 'wspace': 0.01},
                               sharey=True)

    # Lineplot 
    a1.plot(probs["frame_no"], probs["probability"], lw=1)
    a1.tick_params(axis="x", labelsize=10)
    a1.tick_params(axis="y", labelsize=10)
    a1.set_xlabel("# frame", fontsize=10)
    a1.set_ylabel("fake probability $(10²)$ [%]", fontsize=10)
    
    # Violinplot to the right
    a2.violinplot(probs["probability"], 
                  showmeans=False,
                  showmedians=True)
    # tidy up the figure
    a2.get_xaxis().set_ticks([])
    f.tight_layout()
    # save the figure
    directory = "templates"
    f.savefig(os.path.join(directory, "genuineness.jpg"), quality=95)



def histogram_render(probs):

    # Definimos el número de bins 
    n_bins = 1000
    # Cogemos las probabilidades
    x = probs["probability"]

    fig, ax = plt.subplots(figsize=(8, 5))

    # color the intervals
    ax.axvspan(xmin=0, xmax=0.4, ymin=0, ymax=1.1, facecolor='b', alpha=0.4)
    ax.axvspan(xmin=0.4, xmax=0.6, ymin=0, ymax=1.1, facecolor='orange', alpha=0.4)
    ax.axvspan(xmin=0.6, xmax=1.0, ymin=0, ymax=1.1, facecolor='r', alpha=0.4)

    # Add labels to the plot
    style = dict(size=10, color='k')

    ax.text(0.2, 0.5, "safe", ha='center', **style)
    ax.text(0.5, 0.5, "uncertain", ha='center', **style)
    ax.text(0.8, 0.5, "risky", ha='center', **style)

    # plot the cumulative histogram
    n, bins, patches = ax.hist(x, n_bins, density=True, histtype='step',
                           cumulative=True, color='k')
    patches[0].set_xy(patches[0].get_xy()[:-1])

    # tidy up the figure
    ax.grid(True)    
    ax.set_xlabel("fake probability $(10²)$ [%]", fontsize=10)
    ax.set_ylabel('cumulative fakeness dist. $(10²)$ [%]', fontsize=10)
    ax.set_xlim(left=0.0, right=1.0)
    # save the figure
    directory = "templates"
    plt.savefig(os.path.join(directory, "histogram.jpg"), quality=95)


