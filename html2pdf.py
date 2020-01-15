
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
from datetime import datetime
from dataframe import df_builder, probs_render, histogram_render, pie_render
from watcher import get_logger

env = Environment(loader=FileSystemLoader('templates'))
template = env.get_template("report.html")

logger = get_logger("html2pdf")

def render(query, collector):

    ahora = datetime.now()

    df, df_proba, df_path_to_video, df_streams, df_video, df_audio, df_metadata, probs = df_builder(query, collector)

    if df_proba["probability"].T["mean"] >= 0.6: 
        conclusion = "alta"
    elif df_proba["probability"].T["mean"] < 0.6 and df_proba["probability"].T["mean"]>=0.4:
        conclusion = "moderada"
    else:
        conclusion = "baja"
    
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
    
    # Renderizamos el pdf
    html_out = template.render(template_vars)

    HTML(string=html_out).write_pdf("reports/{}_{}_{}.pdf".format(collector, template_vars["title"], ahora))
    logger.info("{}_{}_{}.pdf successfully generated.".format(collector, template_vars["title"], ahora))
    

if __name__=="__main__":
    query = {"filename": "Taxi Driver starring Al Pacino [DeepFake].mp4"}
    collector = "faceforensics"

    render(query, collector)

        
