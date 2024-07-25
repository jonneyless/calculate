import pymysql
from dbutils.pooled_db import PooledDB

from config import mysqlInfo


class OPMysql(object):
    __pool = None

    def __init__(self):
        self.coon = OPMysql.getmysqlconn()
        self.cur = self.coon.cursor(cursor=pymysql.cursors.DictCursor)

    # 数据库连接池连接
    # blocking 如果为 True 连接池里面的东西都取光,需要做等待
    # mincached 初始化时，链接池中至少创建的空闲的链接，0表示不创建
    # maxcached 链接池中最多闲置的链接，0和None不限制
    # blocking 连接池中如果没有可用连接后，是否阻塞等待
    # maxconnections 连接池允许最大的连接数，0和None表示不做限制
    @staticmethod
    def getmysqlconn():
        if OPMysql.__pool is None:
            __pool = PooledDB(creator=pymysql, mincached=5, maxcached=20,
                              blocking=True,
                              maxconnections=20,
                              host=mysqlInfo['host'],
                              db=mysqlInfo['db'],
                              user=mysqlInfo['user'],
                              passwd=mysqlInfo['passwd'],
                              port=mysqlInfo['port']
                              )

        return __pool.connection()

    # 插入\更新\删除
    def op_update(self, sql):
        self.cur.execute(sql)
        self.coon.commit()
        lastrowid = self.cur.lastrowid

        return lastrowid

    def op_safe_update(self, sql, fields):
        self.cur.execute(sql, fields)
        self.coon.commit()
        lastrowid = self.cur.lastrowid

        return lastrowid

    # 查询
    def op_select_one(self, sql):
        self.cur.execute(sql)
        select_res = self.cur.fetchone()
        return select_res

    # 安全搜寻方式
    def op_safe_select_one(self, sql, fields):
        self.cur.execute(sql, fields)
        select_res = self.cur.fetchone()
        return select_res

    # 查询
    def op_select_all(self, sql):
        self.cur.execute(sql)
        select_res = self.cur.fetchall()
        return select_res

    def op_safe_select_all(self, sql, fields=None):
        self.cur.execute(sql, fields)
        select_res = self.cur.fetchall()
        return select_res

    # 释放资源
    def dispose(self):
        try:
            self.cur.close()
            self.coon.close()
        except Exception as e:
            print("dispose %s" % e)
