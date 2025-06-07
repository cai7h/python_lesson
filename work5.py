"""
Flask + Flasgger 实验系统：
提供根据年份查询豆瓣电影标题的接口，并生成 Swagger API 文档。
"""

from flask import Flask, request, jsonify
from flasgger import Swagger
from peewee import MySQLDatabase, Model, CharField, IntegerField

# ========= 数据库连接配置 =========
db = MySQLDatabase(
    database='python_lesson',
    host='localhost',
    port=3306,
    user='root',
    password='Cqh051213',  # 改为你自己的数据库密码
    charset='utf8mb4'
)


# ========= 数据模型 =========
# pylint: disable=too-few-public-methods
class DoubanMovie(Model):
    """豆瓣电影模型（仅标题和年份）"""
    title = CharField()
    year = IntegerField()

    class Meta:
        database = db
        table_name = 'douban_movie'


# ========= 初始化应用 =========
app = Flask(__name__)
swagger = Swagger(app)


# ========= 首页路由 =========
@app.route('/')
def index():
    """首页：展示 API 文档入口"""
    return '<h3>欢迎使用豆瓣电影搜索系统。点击进入 <a href="/apidocs">接口文档</a></h3>'


# ========= 查询接口 =========
@app.route('/search_api', methods=['GET'])
def search_api():
    """
    查询某一年上映的电影
    ---
    parameters:
      - name: year
        in: query
        type: integer
        required: true
        description: 上映年份
    responses:
      200:
        description: 返回该年份的电影标题列表
        schema:
          type: object
          properties:
            year:
              type: integer
            movies:
              type: array
              items:
                type: string
    """
    year_param = request.args.get('year', '').strip()
    if not year_param.isdigit():
        return jsonify({"error": "请输入合法的年份参数"}), 400

    year = int(year_param)
    query_result = DoubanMovie.select().where(DoubanMovie.year == year)
    titles = [movie.title for movie in query_result]

    return jsonify({
        "year": year,
        "movies": titles
    })


# ========= 运行主程序 =========
if __name__ == '__main__':
    db.connect()
    app.run(debug=True)