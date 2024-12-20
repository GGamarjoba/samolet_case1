import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt

# Открываем .csv

df=pd.read_csv("file.csv")
df.info()


# Анализ данных

sb.heatmap(df.isnull())


# Убираем колонки, не особо влияющие на цену, а так же дубликаты

useless_columns=["author", "author_type", "url", "deal_type", "accommodation_type", "object_type", "house_material_type", "finish_type", "phone",
"heating_type", "street", "house_number", "residential_complex"]
df=df.drop(columns=useless_columns).drop_duplicates()


# Заполняем/Удаляем пропуски

df.dropna(subset=["location", "price"], inplace=True)
df.loc[df["district"].isna(), "district"]=df["location"]
df.loc[df["underground"].isna(), "underground"]=df["location"]
df.loc[df["living_meters"]=="-1", "living_meters"]=df["total_meters"]
df.loc[df["living_meters"].isna(), "living_meters"]=df["total_meters"]
df.loc[df["kitchen_meters"]=="-1", "kitchen_meters"]=0
df.loc[df["kitchen_meters"].isna(), "kitchen_meters"]=0
df.replace(["-1", -1, "-1.0", -1.0], df['year_of_construction'].median(), inplace=True)
df=df[df['rooms_count']!=2006.0]


# Цена за метр

df['meter_price']=round(df['price']/df['total_meters'].astype(float), 2)


# Форматируем столбцы: жилые м2 и кухонные м2

df["living_meters"]=df["living_meters"].str.replace("\xa0м²","").str.replace(",",".").astype(float)
df["kitchen_meters"]=df["kitchen_meters"].str.replace("\xa0м²","").str.replace(",",".").astype(float)


# Создаем графики

fig,axs=plt.subplots(2,2,figsize=(15, 15))

axs[0, 0].scatter(y=df["meter_price"],x=df["floor"], alpha=0.05,color="seagreen")
axs[0, 0].grid(True,alpha=0.5)
axs[0, 0].set_title("По этажу")

axs[1, 1].scatter(y=df["meter_price"],x=df["year_of_construction"], alpha=0.1,color="seagreen")
axs[1, 1].grid(True,alpha=0.5)
axs[1, 1].set_title("По году постройки")

axs[0, 1].scatter(y=df["meter_price"],x=df["district"], alpha=0.05,color="seagreen")
axs[0, 1].grid(True,alpha=0.5)
axs[0, 1].set_title("По району")

axs[1, 0].scatter(y=df["price"],x=df["location"], alpha=0.9,color="seagreen")
axs[1, 0].grid(True,alpha=0.5)
axs[1, 0].set_xticklabels(labels=df["location"].value_counts().index, rotation=90)
axs[1, 0].set_title('По автору')
plt.show()


# Цена по городу

plt.figure(figsize=(10,10))
plt.scatter(x=df['location'], y=df['price'],color="seagreen")
plt.xticks(rotation = 90)
plt.show()


# Создаем матрицу корелляций 

sb.heatmap(df.select_dtypes(include=["number"]).corr(), annot=True, cmap="summer_r", fmt=".2f", linewidths=0.5)
plt.show()


df.to_csv("ready_file.csv")