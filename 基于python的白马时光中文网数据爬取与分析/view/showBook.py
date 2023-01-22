import pandas as pd
from pyecharts.charts import Scatter, Pie
from pyecharts.commons.utils import JsCode
from pyecharts.globals import ThemeType
from pyecharts.options import *
from sqlalchemy import create_engine

pd.set_option('display.max_rows', None)


def create_data():
    """连接数据库"""
    engine = create_engine('mysql+pymysql://root:123456@localhost:3306/test?charset=utf8')
    sql_values = "select * from books"
    data = pd.read_sql(sql_values, engine)
    return data


def handle(data):
    """数据处理"""
    # 查看数据是否有重复、缺失
    dp1 = data.isnull().value_counts()
    dp2 = data.duplicated().value_counts()
    #  有部分类型为空 替换为 ->暂无分类
    data['type'] = data['type'].replace('None', '暂无分类')
    data.sort_values(by='words', inplace=True)
    return data


def scanner_show(data):
    """
    根据类型、点击量、字数、书名进行绘制散点图
    根据type分组
    words->x轴  click->y轴
    提示框显示 book_name
    'book_name', 'author', 'status', 'type', 'click', 'words', 'ex'
    """

    scatter = Scatter(init_opts=InitOpts(theme=ThemeType.INFOGRAPHIC))
    scatter.add_xaxis(data['words'])
    for k, v in data.groupby('type'):
        scatter.add_yaxis(k, v[['click', 'book_name']].values.tolist())

    scatter.set_global_opts(
        datazoom_opts=DataZoomOpts(is_show=True),
        legend_opts=LegendOpts(type_="scroll", pos_left='right', pos_top='9%', pos_bottom="18%", orient="vertical"),
        tooltip_opts=TooltipOpts(
            axis_pointer_type='cross',
            formatter=JsCode(
                '''
                function(params) {
                    return '书名:'+params.data[2]
                }
                '''
            )
        ),
        title_opts=TitleOpts(title='基于python的白马时光中文网数据爬取与分析'),
        xaxis_opts=AxisOpts(name='书籍的点击量'),
        yaxis_opts=AxisOpts(name='书籍的字数')
    )

    scatter.set_series_opts(
        label_opts=LabelOpts(is_show=False)
    )
    scatter.render('scanner.html')


def pie_show(data):
    """使用饼状图 展示不同类型的比重"""
    pie = Pie()
    df_pie = data.value_counts('type')
    pie.add(
        '',
        [[i, j] for i, j in zip(df_pie.index.tolist(), df_pie.values.tolist())],
        radius=["30%", "55%"],
        center=["40%", "40%"],
    )

    pie.set_global_opts(
        legend_opts=LegendOpts(type_="scroll", pos_left='left', pos_top='9%', pos_bottom="18%", orient="vertical"),
        title_opts=TitleOpts(title="各图书类型占比图")
    )
    pie.set_series_opts(
        label_opts=LabelOpts(is_show=False)
    )
    pie.render('pie.html')


if __name__ == '__main__':
    data = handle(create_data())
    # scanner_show(data)  # 散点图
    # pie_show(data)       # 饼状图
