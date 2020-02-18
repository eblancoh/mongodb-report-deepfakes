from dataframe import *

df, df_proba, df_path_to_video, df_streams, df_video, df_audio, df_metadata, probs, theta, theta_describe=\
    df_builder(query={"filename": "KIM KARDASHIAN SPECTRE PROJECT DEEPFAKE MANIPULATING FANS VIDEO SPECTRE PROJECT TALKS REAL.mp4"}, collector="headpose")


print(theta_describe)
# kde_distplot(theta)

