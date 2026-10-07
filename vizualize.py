import matplotlib.pyplot as plt

import numpy as np

from analyzer import df

from stats import calculate_price_by_year,range_mileage,brand_stats

plt.style.use('_mpl-gallery')

def vizualize_price_by_year(s):
    x = s.index.tolist()
    y = s['mean_price'].astype(int).tolist()
        
    fig,ax =  plt.subplots()

    ax.plot(x,y,linewidth = 1,marker = '.')

    ax.ticklabel_format(style= 'plain',axis = 'y')
        
    ax.set(xlim = (min(x),max(x)))
    ax.set_xticks(x)
    
    ax.set_xlabel('Год')
    ax.set_ylabel('Средняя цена')
    ax.set_title('Динамика изменения цены в зависимости от года')

    plt.subplots_adjust(bottom=0.04,top=0.98,left=0.04,right=0.99)

    plt.show()
    
def vizualize_mileage(s):
    s = s.loc[s > 0]
    
    interval = []
    
    for i in s.index.tolist():
        a = str(i.left // 1000)
        b = str(i.right // 1000)
        interval.append(a + '-' + b)

    x = interval
    y = s
        
    fig,ax = plt.subplots()
        
    ax.bar(x,y)

    ax.set_xlabel('Пробег, тыс. км')
    ax.set_ylabel('Количество авто')
    ax.set_title('Количество авто в зависимости от пробега')

    plt.subplots_adjust(left= 0.03, bottom=0.043, right= 0.971,top = 0.962)
        
    plt.show()

def visualize_brands(d):
    indexes = d.index.tolist()

    columns = list(d)
    columns =  [elem for elem in columns if 'price' in elem]

    x = indexes
    x_price = np.arange(len(indexes))

    y_year = d['year_mean']
    y_count = d['count']
    y_mileage = d['mileage_mean']

    fig,((ax_count,ax_year),(ax_mileage,ax_price)) = plt.subplots(nrows=2, ncols=2, figsize = (6,6))

    count_bar = ax_count.bar(x,y_count)
    ax_count.bar_label(count_bar)
    ax_count.set_title('Количество машин')
    ax_count.set_xlabel('Бренды')
    ax_count.set_ylabel('Кол-во')

    mileage_bar = ax_mileage.bar(x,y_mileage)
    ax_mileage.bar_label(mileage_bar)
    ax_mileage.set_title('Средний пробег каждого бренда')
    ax_mileage.set_xlabel('Бренды')
    ax_mileage.set_ylabel('Пробег, км')

    year_bar = ax_year.bar(x,y_year)
    ax_year.bar_label(year_bar)
    ax_year.set_title('Средний год каждого бренда')
    ax_year.set_xlabel('Бренды')
    ax_year.set_ylabel('Год')

    width = 0.15
    w = -(width *(len(columns)/2) - width/2)
    for i in columns:
        price_bar = ax_price.bar(x_price+w,d[i],width)
        ax_price.bar_label(price_bar,fmt = '%.0f',rotation = 90, label_type = 'center')
        w+=width
        
    ax_price.set_title('Статистика цен каждого бренда')
    ax_price.set_xlabel('Бренды')
    ax_price.set_ylabel('Цена, руб.')
    ax_price.legend(columns)
    ax_price.ticklabel_format(style = 'plain', axis = 'y')
    ax_price.set_xticks(x_price,indexes)

    plt.tight_layout()
    plt.subplots_adjust(right=0.97,left=0.05,top=0.962,bottom=0.043)
    plt.show()