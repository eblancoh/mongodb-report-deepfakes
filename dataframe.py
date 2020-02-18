import pandas as pd
from pandas.io.json import json_normalize
import json
from database import db_read
import os
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


def df_builder(query, collector):
    """
    query: i.e., {"link": "https://www.youtube.com/watch?v=VWrhRBb-1Ig"}
                 {"filename": "Bill Hader channels Tom Cruise [DeepFake].mp4"}
    collector: "facewarpingartifacts" | "faceforensics" | "headpose"
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
        theta = None
        theta_describe = None
    elif collector == "facewarpingartifacts":
        df_proba = pd.DataFrame(json_normalize(content, 
                                  record_path='fake_prediction_FaceWarpingArtifacts')['probability'].describe())
        probs = pd.DataFrame(json_normalize(content, 
                                  record_path='fake_prediction_FaceWarpingArtifacts'))
        theta = None
        theta_describe = None
    elif collector == "headpose":
        df_proba = None
        probs = None
        cos_dist = df['head_poses.cosine_distance'].iloc[0]

        theta = list()
        for item in cos_dist:
            theta.append(item['theta'])
        
        theta_describe = pd.DataFrame(theta).describe()
        
    try:
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
    except KeyError:
        df_streams = None
        df_path_to_video = None
        df_video = None
        df_audio = None
        df_metadata = None
    # Delete unnecesary information from main dataframe
    df = df[['_id', 'hash', 'link', 'filename', 'fake']].T

    return df, df_proba, df_path_to_video, df_streams, df_video, df_audio, df_metadata, probs, theta, theta_describe


def probs_render(probs):
    sns.set(color_codes=True)

    f, (a1, a2) = plt.subplots(1, 2, 
                               gridspec_kw={'width_ratios': [5, 2], 'wspace': 0.03},
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
    f.savefig(os.path.join(directory, "linearplot.jpg"), quality=95)



def histogram_render(probs):

    # Definimos el número de bins 
    n_bins = 50
    # Cogemos las probabilidades
    x = probs["probability"]

    fig, ax = plt.subplots(figsize=(8, 5))

   
    # Add labels to the plot
    style = dict(size=10, color='k')

    # ax.text(0.2, 0.5, "safe", ha='center', **style)
    # ax.text(0.5, 0.5, "uncertain", ha='center', **style)
    # ax.text(0.8, 0.5, "risky", ha='center', **style)

    # plot the cumulative histogram
    n, bins, patches = ax.hist(x, n_bins, density=True, histtype='step',
                           cumulative=True)
    patches[0].set_xy(patches[0].get_xy()[:-1])

    # color the intervals
    ax.axvspan(xmin=0, xmax=0.4, ymin=0, ymax=1.1, facecolor='b', alpha=0.2)
    ax.axvspan(xmin=0.4, xmax=0.6, ymin=0, ymax=1.1, facecolor='orange', alpha=0.2)
    ax.axvspan(xmin=0.6, xmax=1.0, ymin=0, ymax=1.1, facecolor='r', alpha=0.2)


    # tidy up the figure
    ax.grid(True)    
    ax.set_xlabel("fake probability $(10²)$ [%]", fontsize=10)
    ax.set_ylabel('cumulative fakeness dist. $(10²)$ [%]', fontsize=10)
    ax.set_xlim(left=0.0, right=1.0)
    # save the figure
    directory = "templates"
    plt.savefig(os.path.join(directory, "histogram.jpg"), quality=95)

def pie_render(probs):

    # Pie chart
    labels = ['safe', 'uncertain', 'risky']
    no_safe = np.where(probs["probability"] < 0.4)[0].__len__()
    no_uncertain = np.where((probs["probability"] >= 0.4) &  (probs["probability" ]< 0.6))[0].__len__()
    no_risky = np.where(probs["probability"] >= 0.6)[0].__len__()

    frames = no_safe + no_uncertain + no_risky
    
    sizes = [no_safe*100/frames, no_uncertain*100/frames, no_risky*100/frames]
    
    # only "explode" the 3rd slice (i.e. 'risky')
    explode = (0, 0, 0.1)

    colors = ["#22bb33", "#f0ad4e", "#bb2124"]

    fig, ax = plt.subplots()
    ax.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%',
        shadow=True, startangle=90)
    
    # Equal aspect ratio ensures that pie is drawn as a circle
    ax.axis('equal')
    plt.tight_layout()
    # save the figure
    directory = "templates"
    plt.savefig(os.path.join(directory, "pie.jpg"), quality=95)

    return sizes

def kde_distplot(theta):
    sns.distplot(theta, hist = False, kde = True,
                 kde_kws = {'shade': True, 'linewidth': 2})
    # color the intervals
    plt.axvspan(xmin=-0.02, xmax=0.02, ymin=0, ymax=1.1, facecolor='b', alpha=0.2)
    plt.axvspan(xmin=0.02, xmax=0.04, ymin=0, ymax=1.1, facecolor='orange', alpha=0.2)
    plt.axvspan(xmin=0.04, xmax=0.5, ymin=0, ymax=1.1, facecolor='r', alpha=0.2)

    plt.xlabel("cosine distance")
    plt.ylabel("number of frames")

    # save the figure
    directory = "templates"
    plt.savefig(os.path.join(directory, "kde_distplot.jpg"), quality=95)

