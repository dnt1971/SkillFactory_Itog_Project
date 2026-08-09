# Определение уязвимых групп населения

## Оглавление  
[1. Постановка задачи](#постановка-задачи)<br>
[2. Описание данных](#описание-данных)<br>
[3. Основные этапы решения задачи](#основные-этапы-решения-задачи)<br>
[4. Использованные инструменты](#использованные-инструменты)<br>
[5. Результаты работы и их интерпретация](#результаты-работы-и-их-интерпретация)<br>
[6. Развертывание модели](Развертывание-модели)<br>

### Постановка задачи 
Задачу, описанную в брифе, поставила молодая НКО, которая хочет помогать малообеспеченным людям. Чтобы делать это эффективно, НКО нужно понять, где живут такие люди, и открыть там свои филиалы.
Кроме того, в НКО хотят выяснить, с какими факторами связана бедность и как эти факторы связаны между собой.

Цель:
* кластеризовать регионы России и определить, какие из них наиболее
остро нуждаются в помощи малообеспеченным/неблагополучным
слоям населения;
* описать группы населения, сталкивающиеся с бедностью;
* определить:
    * факторы, влияющие на уровень бедности;
    * влияет ли число детей, пенсионеров и других социально уязвимых
групп на уровень бедности в регионе;
    * связаны ли уровень бедности/социального неблагополучия с
производством и потреблением в регионе;
    * какие ещё зависимости можно наблюдать относительно
социально незащищённых слоёв населения.

:arrow_up:[к оглавлению](#оглавление)

### Описание данных
Данные о доходах, заболеваемости, социально незащищённых слоях населения России и другие экономические и демографические данные [здесь](https://drive.google.com/file/d/1WLGnZY7XpD1cO8a-U1Jncb9oysC3fTg8/view?usp=drive_link) или [Здесь](https://github.com/dnt1971/SkillFactory_Itog_Project/blob/master/arh/social_russia_data.7z). 

➔ [child_mortality_rural_1990_2021.xls](https://docs.google.com/spreadsheets/d/13idFZetR43Ceh0YGxz4e7ZBgltflTzqz/edit?usp=drive_link&ouid=103632009178932960617&rtpof=true&sd=true) — число умерших на первом году жизни детей за год, по всем регионам, в сельской местности.

➔ [child_mortality_urban_1990_2021.xls](https://docs.google.com/spreadsheets/d/1KOJ8rvuAXJnBCiJ5o5LAmppZrYE0UO_k/edit?usp=drive_link&ouid=103632009178932960617&rtpof=true&sd=true) — число умерших на первом году жизни детей за год, по всем регионам, в городской местности.

➔ [disabled_total_by_age_2017_2022.csv](https://drive.google.com/file/d/1y7wsCoj9mobpZcQ49vriH_9_esI2h2Sn/view?usp=drive_link) — число людей с инвалидностью по регионам, по месяцам, по возрастным группам.

➔ [morbidity_2005_2020_age_disease.xls](https://docs.google.com/spreadsheets/d/1fjvvhwCsCqTjuCTNV1XM8-unRbkvi-4n/edit?usp=drive_link&ouid=103632009178932960617&rtpof=true&sd=true) — заболеваемость на 100 тыс. человек населения, по возрастным группам и группам заболеваний.

➔ [poverty_percent_by_regions_1992_2020.csv](https://drive.google.com/file/d/1_4xzpP5RZKw-BeTwDqy4Dn3y1jGnjxrL/view?usp=drive_link) — процент людей, живущих за чертой бедности (с денежными доходами ниже величины прожиточного минимума), оценка за год по регионам.

➔ [welfare_expense_share_2015_2020.xlsx](https://docs.google.com/spreadsheets/d/1Rc6XhfcNQn6WGJXAWKWXoKrNJtGJSjsq/edit?usp=drive_link&ouid=103632009178932960617&rtpof=true&sd=true) — расходы на социальную политику от общих расходов бюджета региона, % в год.

➔ [cash_real_income_wages_2015_2020.xlsx](https://docs.google.com/spreadsheets/d/1XSn4k8dYErMOBWszA3R-Eu-AcnSEN5vR/edit?usp=drive_link&ouid=103632009178932960617&rtpof=true&sd=true) — среднедушевые и реальные денежные доходы населения, номинальная и реальная начисленная зарплата, по регионам.

➔ [poverty_socdem_2017.xls](https://docs.google.com/spreadsheets/d/1GI5RKOzV2hhtJbn5iDg3tG3QxRW8D9s6/edit?usp=drive_link&ouid=103632009178932960617&rtpof=true&sd=true), [poverty_socdem_2018.xls](https://docs.google.com/spreadsheets/d/1os1hcoLVpu3IV3WoHj41gt6eh_gt-7xl/edit?usp=drive_link&ouid=103632009178932960617&rtpof=true&sd=true), [poverty_socdem_2019.xls](https://docs.google.com/spreadsheets/d/1rrVbiTHNGVPAttUH8wsJc8brVl_pKfJe/edit?usp=drive_link&ouid=103632009178932960617&rtpof=true&sd=true), [poverty_socdem_2020.xls](https://docs.google.com/spreadsheets/d/1Eb_Mt0MnfwbZ-aPQIL64qqdOOISwtRQc/edit?usp=drive_link&ouid=103632009178932960617&rtpof=true&sd=true) — распределение малоимущего населения по социально-демографическим группам (дети, трудящиеся, пенсионеры) за 2017–2020 гг., по регионам.

➔ [housing_2020.xlsx](https://docs.google.com/spreadsheets/d/1jJQBj0Xw9ZYUCPi1keCSmr2_kboODS2s/edit?usp=drive_link&ouid=103632009178932960617&rtpof=true&sd=true) — характеристика жилищных условий домохозяйств. Оценка домохозяйствами состояния занимаемого ими жилого помещения, обследование 2020 года.

➔ [population.xlsx](https://docs.google.com/spreadsheets/d/1J9zfqU6Khd1oCdHtJBzsAU4FcIv2uyU6/edit?usp=drive_link&ouid=103632009178932960617&rtpof=true&sd=true) — численность населения по регионам и федеральным округам на 1 января каждого года за 1999–2022 гг.

➔ [gross_regional_product_1996_2020.xls](https://docs.google.com/spreadsheets/d/1i4Nce_wpXOhczy-j1qN_Wn1Svb6HpsXe/edit?usp=drive_link&ouid=103632009178932960617&rtpof=true&sd=true) — валовой региональный продукт на душу населения, в рублях.

➔ [regional_production_2005_2016.csv](https://drive.google.com/file/d/1L9NbMgjvIK51S_jN76861BZAogQ8w4Rf/view?usp=drive_link), [regional_production_2017_2020.csv](https://drive.google.com/file/d/1OcEkhJfZVMwWDtpSwWUGuCOzRJmbTk3N/view?usp=drive_link), — объём отгруженных товаров собственного производства или работ/услуг, выполненных

собственными силами, по видам деятельности за 2005–2016 гг., 2017–2020 гг. (в тысячах рублей, значение показателя за год, полный круг).

➔ [retail_turnover_per_capita_2000_2021.xls](https://docs.google.com/spreadsheets/d/16ohHkXdoCWznehzAgxmppk6LEGB1JMc3/edit?usp=drive_link&ouid=103632009178932960617&rtpof=true&sd=true) — оборот розничной торговли на душу населения, в рублях.

➔ папка [crimes](https://drive.google.com/drive/folders/1jpIqA64vATPGVPbPtd9sm7Vth-ACRNS0?usp=drive_link) — сведения о преступлениях, совершённых отдельными категориями лиц за 2016–2022 гг., по месяцам, регионам, категориям лиц, категориям преступлений.

➔ [drug_alco.xlsx](https://docs.google.com/spreadsheets/d/1kCdekXQcw7QodIcfFfhKo5m3yUrF8eBh/edit?usp=drive_link&ouid=103632009178932960617&rtpof=true&sd=true) — сведения о заболеваемости алкоголизмом и наркоманией, на 100 тыс. населения (2005–2018).

➔ [newborn_2006_2022_monthly.csv](https://drive.google.com/file/d/1xTqFRn9xia11hdJevdEii07PSHf7TrfH/view?usp=drive_link) — рождённые в этом месяце, по регионам, без учёта мертворождённых.

➔ [child_count_2020.xlsx](https://docs.google.com/spreadsheets/d/1_p7L649uUZB6g2PKf-LNehrNisCtRCog/edit?usp=drive_link&ouid=103632009178932960617&rtpof=true&sd=true) — Количество детей (на конец 2020 год).

➔ [retired_count_2016_2021.xls](https://docs.google.com/spreadsheets/d/1zmLau2xesw6kw-Z-eqwmjyCUd54WXbfD/edit?usp=drive_link&ouid=103632009178932960617&rtpof=true&sd=true) — Количество пенсионеров (на конец года).

➔ [regions_geo.csv](https://drive.google.com/file/d/1J3nro4cyoTOtzvptHPsOmLrCwmYzIPec/view?usp=drive_link) — Координаты административных центров регионов.

:arrow_up:[к оглавлению](#оглавление)

### Основные этапы решения задачи  
1. Загрузка и первичная обработка данных
2. Разведывательный анализ данных (EDA)
3. Моделирование 
4. Интерпритация результатов моделирования
5. Создание web-сервера для визуализации результатов моделирования и развертываение в формате докер-контейнера
6. Документирование проекта
7. Выгрузка в [GitHub](https://github.com/dnt1971/SkillFactory_Itog_Project) и [DockerHub](https://hub.docker.com/repository/docker/dnt1971/project_cluster_container/general)

:arrow_up:[к оглавлению](#оглавление)

### Использованные инструменты  
1. Использованы методы PCA и TSNE для понижения размерности. 
2. Применены модели GaussianMixture, SpectralClustering, KMeans, AgglomerativeClustering для кластеризации регионов.
3. Классы-обертки над моделями кластеризации для pipeline.
4. Метрики Силуэта, Калински-Харабаса, Дэвиса-Болдина для оценки метрик моделей.
5. FastAPI для организации web-сервера
6. pickle для сериализации и десериализации моделей
7. Scatterpolar для визуализации данных
8. DockerHub для экспорта докер-контейнеров

:arrow_up:[к оглавлению](#оглавление)

### Результаты работы и их интерпретация  
Выделено 3 кластера регионов.
* 0 - Регионы со средними хараетеристиками.
* 1 - Лидеры промышленности и инфраструктуры.
* 2 - Дотационные регионы.

Также создан web-сайт, размещенный в докер-контейнере для получения инфорации о регионе о результатах кластеризации.

:arrow_up:[к оглавлению](#оглавление)


### Развертывание модели 

**Ручной запуск**
1. Создайте виртуальное окружение
*python3 -m venv venv*

2. Активируйте среду окружения
*source venv/bin/activate*

3. Проверьте среду окружения, выполнив любую команду, например
*print( "Здравствуй МетаВселенная" )*

4. Установите зависимости
*pip install -r requirements.txt*

5. Пошагово
5.1. Выполните *01_preprocessing.ipynb*
5.2. Выполните *02_eda.ipynb*
5.3. Выполните *03_model.ipynb*
5.4. Выполните *04_model_from_file.ipynb*
5.5. Запустите сервер *uvicorn server:app --reload*

**Запуск сайта из образа**
Для скачивания образа выполните команду:
*$ docker pull dnt1971/project_cluster_container*

Для запуска образа выполните команду:
*$ docker run -d -p 8000:8000 --name=prod_test dnt1971/project_cluster_container*

Резервная копия docker-файла [тут](https://drive.google.com/file/d/1DRo2ng4De04yVPxEvlccC58_RSE3Ijz9/view?usp=drive_link)

:arrow_up:[к оглавлению](#оглавление)
