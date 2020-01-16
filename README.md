# Herramienta de Reporte para Deep Fakes Exposer 

Distorsionar información haciendo uso de tecnologías basadas en Machine Learning para la
creación de Deep Fakes nunca ha sido más sencillo. Esta capacidad hace posible crear audio y
video de personas reales que dicen y hacen cosas que esos mismos sujetos nunca dijeron o
hicieron. Las técnicas de Machine Learning son cada vez más sofisticadas, haciendo estas
falsificaciones cada vez más realistas y cada vez más resistentes a la detección. 

Estas
tecnologías dedicadas al engaño se difuenden rápidamente entre la sociedad, poniéndola en
manos de actores sofisticados y no sofisticados. Ahí es donde reside su verdadera peligrosidad.

Actualmente, tanto las personas como las empresas se enfrentan a nuevas formas de
explotación, intimidación, sabotaje y descrédito personal. Los riesgos para nuestra democracia
y para la seguridad nacional también son profundos.

Telefónica Digital España S.A. está concienciada con los principios éticos del uso de la
Inteligencia Artificial y es consciente de los problemas y consecuencias derivadas del mal uso
de este tipo de tecnologías. Por ello, el Departamento de Ideas Locas CDCO tiene como objetivo
proporcionar un servicio modular de detección de contenido no legítimo haciendo uso del
estado del arte en referencia a las herramientas de detección de alteración de recursos
multimedia.

## Descripción del proyecto

El presente repositorio tiene como misión la automatización en la generación de un reporte en formato PDF sobre la idoneidad de un recurso
analizado tanto por los repositorios [VoightKampffWannabe-FaceWarpingArtifacts](http://172.16.0.146/eblancoh/voightkampffwannabe-facewarpingartifacts) como [VoightKampffWannabe-FaceForensics](http://172.16.0.146/eblancoh/voightkampffwannabe-faceforensics). 

Haciendo uso de la librería de Python [weasyprint](https://weasyprint.org/). Esta librería permite convertir sencillos ficheros HTML en archivos PDF.

## Instalación

Se recomienda hacer uso de un entorno virtual con Python 3.6 para la instalación de todos los paquetes necesarios.
Una vez creado el entorno virtual, sugerimos realizar:

```bash
$ conda env create -f environment.yml
```

## Uso

Tras haber realizado el anaĺisis de un determinado recurso multimedia de acuerdo con las intrucciones indicadas en [este enlace de FaceWarpingArtifacts](http://172.16.0.146/eblancoh/voightkampffwannabe-facewarpingartifacts/blob/master/README.md#uso) o [en este otro de FaceForensics++](http://172.16.0.146/eblancoh/voightkampffwannabe-faceforensics/blob/master/README.md#uso), generamos el reporte ejecutando el siguiente comando:
```bash
$ python html2pdf.py --filename <filename> --collector <collector>
```

Siendo `<filename>` el título del vídeo que se ha almacenado en base de datos tras su análisis por el correspondiente motor y `<collector>` un keyword
de los motores actualmentes soportados (` faceforensics` o `facewarpingartifacts`).

Tras ejecutar este comando, se creará un fichero pdf en la carpeta `reports/` con una nomenclatura: `<collector>_<filename>_%datetime%.pdf`. El reporte se divide en un **Informe Técnico** y en un **Informe Ejecutivo** sobre el vídeo analizado.
___________________________________________________________
La base de datos está alojada en **mongoDB Atlas**, en un **CLUSTER TIER M0 Sandbox (General) en la REGION Azure / Ireland (northeurope)**.

Se realizan las conexiones y consultas haciendo uso de `pymongo` con driver *Python versión 3.6 o superior*:
```python 
client = pymongo.MongoClient("mongodb+srv://<username>:<password>@<clustername>-<identifier>.azure.mongodb.net/test?retryWrites=true&w=majority")
db = client.test
``` 

## LICENSE
This is free and unencumbered software released into the public domain. Anyone is free to copy, modify, publish, use, compile, sell, or distribute this software, either in source code form or as a compiled binary, for any purpose, commercial or non-commercial, and by any means.

In jurisdictions that recognize copyright laws, the author or authors of this software dedicate any and all copyright interest in the software to the public domain. We make this dedication for the benefit of the public at large and to the detriment of our heirs and successors. We intend this dedication to be an overt act of relinquishment in perpetuity of all present and future rights to this software under copyright law.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
