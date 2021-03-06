from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
from datetime import datetime
from dataframe import df_builder, probs_render, histogram_render, pie_render
from watcher import get_logger
import argparse

env = Environment(loader=FileSystemLoader('templates'))

logger = get_logger("html2pdf")

def render(query, collector):

    if collector != "headpose":
        template = env.get_template("ff++fwa.html")
    else:
        template = env.get_template("headpose.html")


    ahora = datetime.now()

    df, df_proba, df_path_to_video,\
        df_streams, df_video, df_audio,\
        df_metadata, probs, theta, theta_describe =\
        df_builder(query, collector)
    
        
    if collector != "headpose":
        if df_proba["probability"].T["mean"] >= 0.6: 
            conclusion = "alta"
        elif df_proba["probability"].T["mean"] < 0.6 and df_proba["probability"].T["mean"]>=0.4:
            conclusion = "moderada"
        else:
            conclusion = "baja"
    else:
        if df.T['fake'].values=='risky': 
            conclusion = "alta"
        elif df.T['fake'].values=='uncertain':
            conclusion = "moderada"
        else:
            conclusion = "baja"
    
    if collector != "headpose":
        # Creamos y almacenamos el pie chart de legitimidad
        sizes = pie_render(probs)

        # Definimos un diccionario con las variables a pasar al html de cara a la renderización

        template_vars = {"title" : query["filename"],
                        "main_table": df.to_html(),
                        "proba_table": df_proba.to_html(),
                        "streams_table": df_streams.to_html(),
                        "video_table": df_video.to_html(),
                        "audio_table": df_audio.to_html(),
                        "metadata_table": df_metadata.to_html(),
                        "engine": collector,
                        "is_fake": df.T["fake"].iloc[0],
                        "median": round(df_proba["probability"].T["50%"], 3),
                        "mean": round(df_proba["probability"].T["mean"], 3),
                        "std": round(df_proba["probability"].T["std"], 3),
                        "iqr": str(round(df_proba["probability"].T["25%"], 3)) + \
                            '-' + \
                            str(round(df_proba["probability"].T["75%"], 3)),
                        "num_frames": df_proba["probability"].T["count"].astype(int),
                        "date": ahora,
                        "pie_safe": round(sizes[0], 1),
                        "pie_warning": round(sizes[1], 1),
                        "pie_risky": round(sizes[2], 1), 
                        "conclusion": conclusion
                        }
        
        # Creamos y almacenamos los plots de la evolución de legitimidad
        probs_render(probs)
        histogram_render(probs)
    
    else:
        # Definimos un diccionario con las variables a pasar al html de cara a la renderización

        template_vars = {"title" : query["filename"],
                        "main_table": df.to_html(),
                        "streams_table": df_streams.to_html(),
                        "video_table": df_video.to_html(),
                        "audio_table": df_audio.to_html(),
                        "metadata_table": df_metadata.to_html(),
                        "engine": collector,
                        "is_fake": df.T["fake"].iloc[0],
                        "cos_table": theta_describe.to_html(),
                        "median": round(theta_describe.T["50%"].iloc[0], 3),
                        "mean": round(theta_describe.T["mean"].iloc[0], 3),
                        "std": round(theta_describe.T["std"].iloc[0], 3),
                        "iqr": str(round(theta_describe.T["25%"].iloc[0], 3)) + \
                            '-' + \
                            str(round(theta_describe.T["75%"].iloc[0], 3)),
                        "num_frames": theta_describe.T["count"].iloc[0].astype(int),
                        "date": ahora, 
                        "conclusion": conclusion
                        }

        
    # Renderizamos el pdf
    html_out = template.render(template_vars)

    HTML(string=html_out).write_pdf("reports/{}_{}_{}.pdf".format(collector, template_vars["title"], ahora))
    logger.info("{}_{}_{}.pdf successfully generated.".format(collector, template_vars["title"], ahora))
    

if __name__=="__main__":

    # parser = argparse.ArgumentParser(description="Report generation for DeepFake detection.")
    # parser.add_argument("--filename", type=str, help="Name of the analyzed file.")
    # parser.add_argument("--collector", type=str, help="Engine that analyzed the resource. Available values: faceforensics|facewarpingartifacts .")
    # args =parser.parse_args()

    # if not args.collector and not args.filename:
    #     parser.print_help()
    #     raise ValueError("Please, provide <filename> and <collector> to start database retrieval and report generation.")
    query = {"filename": "KIM KARDASHIAN SPECTRE PROJECT DEEPFAKE MANIPULATING FANS VIDEO SPECTRE PROJECT TALKS REAL.mp4"}
    collector = "headpose"

    # render(query=args.filename, collector=args.collector)
    render(query=query, collector=collector)
