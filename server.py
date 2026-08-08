from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import FileResponse

from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pathlib import Path
from contextlib import asynccontextmanager
import pandas as pd
import pickle
import os
from sklearn.preprocessing import MinMaxScaler

BASE_DIR = Path(__file__).parent
DATA_STORE = {} # Словарь датасетов для сайта
FAVICON_PATH = "favicon.ico"


#####################################################################################################
#
# Создаем настроенный словарь параметров слоя полярной диаграммы
#
#####################################################################################################
@asynccontextmanager
async def lifespan( app: FastAPI ):
    # Однократная инициализация при старте сервера
    REGIONS_FILE = f"{BASE_DIR}/data/regions_for_modeling.csv"
    CLUSTERS_FILE = f"{BASE_DIR}/data/clusters.csv"
    MODEL_FILE = f"{BASE_DIR}/model/model_regions.pkl"
    
    df_regions = pd.read_csv( REGIONS_FILE )
    df_clusters = pd.read_csv( CLUSTERS_FILE )
    
    with open( MODEL_FILE, 'rb' ) as pkl_file:
        model_from_file = pickle.load( pkl_file )
        
    df_regions[ 'cluster' ] = model_from_file.predict( df_regions )
    
    # Читаем признаки
    df_features = pd.read_csv( 'data/cols_for_draw.csv' )
    cols_for_draw = df_features['cols_for_draw'].to_list()
    cols_for_draw.append( 'cluster' )    
    cols_for_geo = ['region', 'lat', 'lon', 'cluster']

    # Готовим датасеты
    DATA_STORE[ 'df_regions_draw' ] = df_regions[ cols_for_draw ].copy()  # Данные с отображаемыми признаками
    DATA_STORE[ 'df_regions_geo' ] = df_regions[ cols_for_geo ].copy()    # Широта и долгота административных центров
    DATA_STORE[ 'df_clusters' ] = df_clusters                             # Описание кластеров
    DATA_STORE[ 'df_regions_merged' ] = df_regions.merge( df_clusters, on = "cluster", how = "left" ) # Склеивает данные с признаками и координаты
    
    yield
    DATA_STORE.clear()

app = FastAPI( title = "Кластерный анализ регионов РФ", lifespan = lifespan )
app.mount( "/static", StaticFiles( directory = f"{BASE_DIR}/static" ), name = "static" )
templates = Jinja2Templates(  directory = str(f"{BASE_DIR}/templates" ) )


#####################################################################################################
#
# Создаем настроенный словарь параметров слоя полярной диаграммы
#
#####################################################################################################
@app.get( "/", response_class = HTMLResponse )
async def index( request: Request ):
    clusters = DATA_STORE[ 'df_clusters' ][["cluster", "name"]].to_dict(orient = "records")
    regions = sorted( DATA_STORE['df_regions_geo']["region"].tolist() )
    draw = DATA_STORE['df_regions_draw'].to_dict()

    return templates.TemplateResponse( request, "index.html", {
        "clusters": clusters,
        "regions": regions,
        "draw": draw
    })


#####################################################################################################
#
# Создаем настроенный словарь параметров слоя полярной диаграммы
#
#####################################################################################################
@app.get( "/api/clusters" )
async def get_clusters():
    return DATA_STORE[ 'df_clusters' ].to_dict( orient = "records" )


#####################################################################################################
#
# Создаем настроенный словарь параметров слоя полярной диаграммы
#
#####################################################################################################
@app.get( "/api/clusters/{cluster_id}" )
async def get_cluster_info( cluster_id: int ):
    cluster_row = DATA_STORE['df_clusters'][DATA_STORE['df_clusters']["cluster"] == cluster_id]
    if cluster_row.empty:
        raise HTTPException( status_code = 404, detail = "Кластер не найден" )
    
    cluster_info = cluster_row.iloc[0].to_dict()
    regions = sorted(DATA_STORE['df_regions_geo'][DATA_STORE['df_regions_geo']["cluster"] == cluster_id]["region"].tolist())

    return {
        "cluster": cluster_id,
        "name": cluster_info["name"],
        "description": cluster_info["description"],
        "regions": regions,
        "count": len(regions),
    }


#####################################################################################################
#
# Создаем настроенный словарь параметров слоя полярной диаграммы
#
#####################################################################################################
@app.get( "/api/regions" )
async def get_regions():
    return DATA_STORE['df_regions_merged'].to_dict( orient = "records" )


#####################################################################################################
#
# Создаем настроенный словарь параметров слоя полярной диаграммы
#
#####################################################################################################
@app.get( "/api/regions/{region_name}" )
async def get_region_info(region_name: str):
    region_row = DATA_STORE['df_regions_merged'][DATA_STORE['df_regions_merged']["region"] == region_name]
    if region_row.empty:
        raise HTTPException(status_code=404, detail="Регион не найден")
    
    row_data = region_row.iloc[0]
    return {
        "region": region_name,
        "cluster": int( row_data[ "cluster" ]) ,
        "cluster_name": row_data.get( "name", "" ),
        "description": row_data.get( "description", "" ),
        "lat": float( row_data.get( "lat", 0) ),
        "lon": float( row_data.get( "lon", 0) ),
    }

@app.get( "/api/map-data" )
async def get_map_data():
    return DATA_STORE[ 'df_regions_merged' ].to_dict( orient = "records" )


#####################################################################################################
#
# Создаем настроенный словарь параметров слоя полярной диаграммы
#
#####################################################################################################
def prepare_for_draw():
    # Берем данные 
    df_regions_draw = DATA_STORE[ 'df_regions_draw' ]

    # Группируем и масштабируем признаки
    X_medians = df_regions_draw.groupby( 'cluster' ).median()
    tmp_grouped_data = pd.DataFrame( MinMaxScaler().fit_transform( X_medians ), columns = X_medians.columns )   

    # На диаграмме отразим признаки в русскоязычном виде
    ru_labels = {
        'population_norm': 'Население (норм.)', 
        'disabled_total': 'Инвалидность (всего)', 
        'morbidity': 'Заболеваемость',
        'poverty_percent': 'Бедность (%)', 
        'welfare': 'Благосостояние', 
        'per_capita': 'Доход на душу', 
        'retail': 'Розница',
        'gross_regional_product': 'ВРП', 
        'regional_production': 'Производство', 
        'housing_Жилая_площадь': 'Жилая площадь',
        'housing_Комнат': 'Кол-во комнат', 
        'child_mortality_newborn': 'Рождаемость', 
        'crim_group': 'Преступность'
    }

    feature_names = [ ru_labels.get( col, col ) for col in tmp_grouped_data.columns ]
    theta_labels = feature_names + [ feature_names[0] ]

    # Используем рекомендованную дизайнером политру цветов
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']

    return tmp_grouped_data, theta_labels, colors


#####################################################################################################
#
# Создаем настроенный словарь параметров слоя полярной диаграммы
#
#####################################################################################################
def create_trace( ind_cluster, row, colors, theta_labels ):
    color = colors[ ind_cluster % len( colors ) ]

    # Используем рекомендованную дизайнером политру цветов
    fill_color = f"rgba( {int( color[1:3], 16 )}, {int( color[3:5], 16 )}, {int( color[5:], 16 )}, 0.3 )"

    # Настраиваем радиусы диаграммы
    r_values = row.to_list()
    r_values = r_values + [r_values[0]]

    # Создаем словарь параметров scatterpolar
    trace = {
        "type": 'scatterpolar',
        "mode": 'lines+markers',
        "r": r_values,
        "theta": theta_labels,
        "fill": 'toself',
        "fillcolor": fill_color,
        "line": {
            "color": color, 
            "width": 2
        },
        "marker": {
            "color": color, 
            "size": 8
        },
        "name": f'Кластер {ind_cluster}'
    }

    return trace


#####################################################################################################
#
# API: Возвращяет клиенту массив слоев-объектов полярной диаграммы
#
#####################################################################################################
@app.get( "/api/polarAll" )
async def get_polarAll():
    tmp_grouped_data, theta_labels, colors = prepare_for_draw()

    output_clusters = []

    for i, (_, row) in enumerate( tmp_grouped_data.iterrows() ):
        trace = create_trace( i, row, colors, theta_labels )
        output_clusters.append( trace )
    return output_clusters


#####################################################################################################
#
# Создаем настроенный словарь параметров слоя полярной диаграммы
#
#####################################################################################################
@app.get( "/api/polarByOne" )
async def get_polarByOne():
    tmp_grouped_data, theta_labels, colors = prepare_for_draw()
    df_regions_geo = DATA_STORE[ 'df_regions_geo' ]

    output_clusters = []

    for i, (_, row) in enumerate( tmp_grouped_data.iterrows() ):
        trace = create_trace( i, row, colors, theta_labels )
        cluster_regions = sorted( df_regions_geo[ df_regions_geo["cluster"] == i ][ "region" ].tolist() )

        output_clusters.append({
            "cluster_id": i,
            "trace": [trace],
            "regions": cluster_regions
        })

    return output_clusters


@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return FileResponse( FAVICON_PATH )

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run( "server:app", host = "0.0.0.0", port = port, reload = True)
