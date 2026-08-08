        
# Пример использования кастомного трансформера
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import MinMaxScaler
import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from sklearn.manifold import TSNE
from sklearn.cluster import SpectralClustering, AgglomerativeClustering
#from pandas.io.formats.style import Styler

################################################################################################
# 
# Оборачиваем t-SNE в класс, чтобы был совместим с pipeline:
#
################################################################################################
class PipelineTSNE( BaseEstimator, TransformerMixin ):
    def __init__(self, n_components = 2, random_state = None, perplexity = 15):
        self.n_components = n_components
        self.random_state = random_state
        self.perplexity = perplexity
        
    def fit(self, X, y = None):
        self.tsne_ = TSNE(n_components = self.n_components, perplexity = self.perplexity, random_state = self.random_state)
        self.embedded_X_ = self.tsne_.fit_transform( X )
        return self

    def transform( self, X ):
        return self.embedded_X_
    
################################################################################################
# 
# Оборачиваем SpectralClustering в класс, чтобы был совместим с pipeline:
#
################################################################################################
class PipelineSpectralClustering( BaseEstimator ):
    def __init__( self, **args):
        self.args = args
        self.labels_ = []
        
    def predict( self, X ):
        return self.labels_
        
    def fit( self, X, y = None ):
        self.SpectralClustering = SpectralClustering( **self.args )
        self.SpectralClustering.fit( X )
        self.labels_ = self.SpectralClustering.labels_
        return self
    
    def fit_predict( self, X, y = None ):
        self.fit(X )
        return self.labels_    

################################################################################################
# 
# Оборачиваем AgglomerativeClustering в класс, чтобы был совместим с pipeline:
#
################################################################################################    
class PipelineAgglomerativeClustering( BaseEstimator ):
    def __init__( self, **args):
        self.args = args
        self.labels_ = []
        
    def predict( self, X, y = None ):
        return self.labels_
        
    def fit( self, X, y = None ):
        self.AgglomerativeClustering = AgglomerativeClustering( **self.args )
        self.AgglomerativeClustering.fit_predict( X )
        self.labels_ = self.AgglomerativeClustering.labels_
        return self
    
    def fit_predict( self, X, y = None ):
        self.fit(X )
        return self.labels_       
    
    
################################################################################################
# 
# Класс для печати полярной диаграммы
#
################################################################################################
class plot_model_clusters():
    def __init__( self, X, n_clusters, col_name = 'cluster' ):
        self.X = X
        self.n_clusters = n_clusters
        self.col_name = col_name;

    # Функция для визуализации профиля всех кластеров в виде полярной диаграммы на одном рисунке
    def plot_cluster_all( self ):
        """Функция для визуализации профиля кластеров в виде полярной диаграммы.

        Args:
            grouped_data (DataFrame): таблица, сгруппированная по номерам кластеров с агрегированными характеристиками объектов.
            n_clusters (int): количество кластеров
        """
        # Нормализуем сгруппированные данные, приводя их к масштабу 0-1.
        X_medians = self.X.groupby( self.col_name ).median()
        df_grouped_data = pd.DataFrame( MinMaxScaler().fit_transform( X_medians ), columns = X_medians.columns )

        # Создаём список признаков
        features = df_grouped_data.columns

        # Создаём пустую фигуру
        fig = go.Figure()
        
        # В цикле визуализируем полярную диаграмму для каждого кластера
        for i in range( self.n_clusters ):
            # Создаём полярную диаграмму и добавляем её на общий график
            fig.add_trace( go.Scatterpolar(
                r = df_grouped_data.iloc[i].values, # радиусы
                theta = features, # название засечек
                fill = 'toself', # заливка многоугольника цветом
                name = f'Кластер {i}', # название — номер кластера
            ))
        # Обновляем параметры фигуры
        fig.update_layout(
            showlegend = True, # отображение легенды
            autosize = False, # устаналиваем свои размеры графика
            width = 800, # ширина (в пикселях)
            height = 800, # высота (в пикселях)
        )
        # Отображаем фигуру
        fig.show()
        #fig.write_html("data/plot_cluster_profile.html")   
        return df_grouped_data
            

    # Функция для визуализации профиля всех кластеров в виде полярной диаграммы, каждый на отдельном рисунке
    def plot_cluster_by_one( self ):
        # группируем по кластерам
        X_medians = self.X.groupby( self.col_name  ).median()

        # Нормализуем сгруппированные данные, приводя их к масштабу 0-1.
        df_grouped_data = pd.DataFrame( MinMaxScaler().fit_transform( X_medians ), columns = X_medians.columns )

        # Создаём список признаков
        features = df_grouped_data.columns

        # Создаём пустые n_clusters фигур
        n_clusters = self.n_clusters
        fig = make_subplots( rows = 1, cols = n_clusters, specs = [[{'type': 'polar'}] * n_clusters] * 1)
              
        # В цикле визуализируем полярную диаграмму для каждого кластера
        for i in range(n_clusters):
            # Создаём полярную диаграмму и добавляем её на общий график
            fig.add_trace( go.Scatterpolar(
                r = df_grouped_data.iloc[i].values, # радиусы
                theta = features, # название засечек
                fill = 'toself', # заливка многоугольника цветом
                name = f'Кластер {i}', # название — номер кластера
            ), 1, i + 1)
            
        # Обновляем параметры фигуры
        fig.update_layout(
            showlegend = True, # отображение легенды
            autosize = False, # устаналиваем свои размеры графика
            width = 600 * n_clusters, # ширина (в пикселях)
            height = 500, # высота (в пикселях)
        )

        # Отображаем фигуру
        fig.show()
        return df_grouped_data

################################################################################################
# 
# Класс для красивой печати таблицы в Jupyter 
#
################################################################################################
class other_services:
    def __init__( self ):
        pass
        
    def print_table( df ):
        tmp_df = df.style.set_properties( **{
            'text-align': 'center',       # Выравнивание текста по центру
            'font-size': '14px',          # Размер шрифта
            'font-family': 'Arial',       # Красивый читаемый шрифт
            'border': '1px solid #e0e0e0' # Тонкие аккуратные границы
        } ).set_table_styles( [
            # Стили для заголовков колонок
            {'selector': 'th', 'props': [
                ( 'background-color', '#4CAF50' ), # Зеленый цвет шапки
                ( 'color', 'white' ),              # Белый текст в шапке
                ( 'font-weight', 'bold' ),
                ( 'text-align', 'center' ),
                (' padding', '10px' )
            ] },
            
            # Отступы (padding) внутри ячеек данных
            {'selector': 'td', 'props': [('padding', '12px')]}
        ] ).hide( axis  = 'index' ) # Прячем стандартный индекс (0, 1, 2) слева

        # Вывод в Jupyter
        return tmp_df
        
