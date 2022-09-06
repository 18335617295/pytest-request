import os
import threading
from conf.GlobalConfig import GlobalConfig
from libs import utils
import datetime
import pymysql

from libs.Base import Base

threadLock = threading.Lock()


class MySqlHandler(Base):
    conn = None

    def __init__(self, db=None, key="DB"):
        """连接数据库"""
        try:
            db_info = utils.yaml_file(GlobalConfig.ENV, None, f"..{os.sep}conf", key)
            # 判断是需要指定数据库
            if "db" in db_info:
                self.conn = pymysql.Connection(host=db_info["host"], port=int(db_info["port"]), user=db_info["user"],
                                               passwd=db_info["passwd"], db=db_info["db"], charset=db_info["charset"],
                                               autocommit=True)
            elif db:
                self.conn = pymysql.Connection(host=db_info["host"], port=int(db_info["port"]), user=db_info["user"],
                                               passwd=db_info["passwd"], db=db, charset=db_info["charset"],
                                               autocommit=True)
            else:
                self.conn = pymysql.Connection(host=db_info["host"], port=int(db_info["port"]), user=db_info["user"],
                                               passwd=db_info["passwd"], charset=db_info["charset"],
                                               autocommit=True)
        except pymysql.Error as e:
            self.log.error("连接数据库失败，请检查...")
            self.log.error("Mysql Error %d: %s" % (e.args[0], e.args[1]))

    def update(self, table_name, params_dic, where=None, update_date=False):
        """
        :param table_name: 表名
        :param params_dic: 更新字段
        :param where: 条件
        :param update_date:
        :return:
        """
        if update_date:
            params_dic.update({'updated_at': self.get_datetime_string()})
        edit_sql = ",".join([("%s" % (str(x)) + "=%s") for x in params_dic.keys()])
        values = [x for x in params_dic.values()]
        where_sql = ''

        if where:
            if isinstance(where, str):
                where_sql = where
            elif isinstance(where, dict):
                where_sql = " AND ".join([("%s" % (str(x)) + "=%s") for x in where.keys()])
                where_values = [x for x in where.values()]
                values = list(values) + list(where_values)
            sql = "UPDATE %s SET %s WHERE %s" % (table_name, edit_sql, where_sql)
        else:
            sql = "UPDATE %s SET %s " % (table_name, edit_sql)
        return self.exeCuteCommit(sql, values)

    # 针对更新,删除,事务等操作失败时回滚
    def exeCuteCommit(self, sql='', param=None):
        """
        执行一个sql
        :param sql:
        :param param:
        :return:
        """
        try:
            cursor = self.conn.cursor()
            if param is None:
                cursor.execute(sql)
            else:
                cursor.execute(sql, param)
            self.conn.commit()
            return int(cursor.lastrowid)
        except pymysql.Error as e:
            self.conn.rollback()
            self.log.error('MySQL execute failed! ERROR (%s): %s . Mysql cmd: %s' % (e.args[0], e.args[1], sql))

    def get_datetime_string(self):
        return datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")

    def delete(self, table_name, where=None):
        """
        :param table_name: 表名
        :param where: 条件
        :return:
        """
        where_sql = ''
        if where:
            if isinstance(where, str):
                where_sql = where
            elif isinstance(where, dict):
                where_sql = " AND ".join(["%s='%s'" % (str(x[0]), str(x[1])) for x in where.items()])
            sql_prefix = "DELETE FROM %s WHERE %s "
            sql = sql_prefix % (table_name, where_sql)
        else:
            sql_prefix = "DELETE FROM %s "
            sql = sql_prefix % (table_name)
        return self.exeCuteCommit(sql)

    def select_one(self, table, cond_dict='', order=''):
        """
        查询一条数据
        :param table: 表名
        :param cond_dict:  条件
        :param order: 排序例: order by a desc
        :return:
        """
        consql = ' '
        if cond_dict != '':
            for k in cond_dict:
                consql = consql + k + '="' + cond_dict[k] + '" and'
        consql = consql + ' 1=1 '
        sql = 'select * from %s where ' % table
        sql = sql + consql + order
        data = self.exeCute(sql, one="one")
        return {key: str(value) for key, value in data.items()}

    def select_All(self, table, cond_dict='', order=''):
        """
        查询所有
        :param table: 表名
        :param cond_dict:  条件
        :param order: 排序例: order by a desc
        :return:
        """
        consql = ' '
        if cond_dict != '':
            for k, v in cond_dict:
                consql = consql + k + '=' + v + ' and'
        consql = consql + ' 1=1 '
        sql = 'select * from %s where ' % table
        sql = sql + consql + order
        return self.exeCute(sql, one="all")

    def exeCute(self, sql='', one="one"):
        """
        执行一个sql
        :param sql:
        :param one: 返回一条结果
        :return:
        """
        try:
            cur = self.conn.cursor(cursor=pymysql.cursors.DictCursor)
            self.log.debug(sql)
            threadLock.acquire()
            cur.execute(sql)
            if "one" == one:
                records = cur.fetchone()
            else:
                records = cur.fetchall()
            threadLock.release()
            self.log.debug(records)
            return records
        except pymysql.Error as e:
            threadLock.release()
            self.log.error('MySQL execute failed! ERROR (%s): %s' % (e.args[0], e.args[1]))
            raise e

    def search_database(self, sql, count="more"):  # count=more是返回多条记录；count=one是只返回第一条记录
        '''#sql: select * from'''
        data = self.exeCute(sql, count)
        return data

    # 插入单条数据,字典格式
    def insert(self, table, param):
        """
        插入单挑数据
        :param table:
        :param param:
        :return:
        """
        # values_sql = ['%s' for v in attrs]
        attrs_sql = '(' + ','.join([i for i in param.keys()]) + ')'
        values_sql = ' values(' + ','.join(["'" + str(i) + "'" for i in param.values()]) + ')'
        sql = 'insert into %s' % table
        sql = sql + attrs_sql + values_sql
        self.exeCuteCommit(sql)

    def clear_database(self, tables: list):
        """
        清除list内所有表
        :param tables:
        :return:
        """
        for table in tables:
            self.conn.cursor().execute('delete FROM %s' % table)
        self.conn.commit()

    def close_database(self):
        """关闭数据库连接"""
        self.conn.cursor().close()
        self.conn.close()

    # 插入多年条数据sql list格式
    def insert_by_sql_list(self, sql_list: list):
        """
        通过insert sql语句批量插入数据
        :param insert_sql: "insert into table1（'id', 'name', 'gender') values(1, '张三', '男');"
        :return:
        """
        try:
            cursor = self.conn.cursor()
            for insert_sql in sql_list:
                cursor.execute(insert_sql)
            self.conn.commit()
            return int(cursor.lastrowid)
        except pymysql.Error as e:
            self.conn.rollback()
            self.log.error(('MySQL execute failed! ERROR (%s): %s . Mysql cmd: ' % (e.args[0], e.args[1])),
                           sql_list)

    def search_one(self, search_sql):
        """
        查询出所有符合条件的第一条结果结果
        :param conn:
        :param cur:
        :param search_sql: "select * from table1 order by id desc;"
        :return: 一条结果
        """
        data = self.exeCute(search_sql)
        return tuple(value for key, value in data.items())

    # 插入单条数据sql
    def insert_by_sql(self, insert_sql):
        """
        通过insert sql语句插入数据
        :param conn:
        :param cur:
        :param insert_sql: "insert into table1（'id', 'name', 'gender') values(1, '张三', '男');"
        :return:
        """
        cursor = self.conn.cursor()
        cursor.execute(insert_sql)
        self.conn.commit()
        return int(cursor.lastrowid)

    def exe_cute_all(self, sql_list: list):
        """
        执行多条sql
        :param sql_list:
        :return:
        """
        try:
            threadLock.acquire()
            cur = self.conn.cursor(cursor=pymysql.cursors.DictCursor)
            for sql in sql_list:
                self.log.debug(sql)
                cur.execute(sql)
            self.conn.commit()
            threadLock.release()
            return "执行sql成功"
        except pymysql.Error as e:
            self.conn.rollback()
            threadLock.release()
            self.log.error('MySQL execute failed! ERROR (%s): %s' % (e.args[0], e.args[1]))
            raise e

    def select_in(self, table, cond_dict, field=None):
        sql = ''
        if field:
            sql += f"select {field} from {table} where "
        else:
            sql += f"select * from {table} where "
        if cond_dict != '':
            for k in cond_dict:
                sql += k + ' in ' + '('
                for i in cond_dict[k]:
                    sql += f'"{i}",'
                sql = sql.rstrip(",")
            sql += ')'
        return self.exeCute(sql, "all")


if __name__ == "__main__":
    pass
