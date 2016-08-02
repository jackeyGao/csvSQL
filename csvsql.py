# -*- coding: utf-8 -*-
'''
File Name: main.py
Author: JackeyGao
mail: gaojunqi@outlook.com
Created Time: 二  8/ 2 12:58:57 2016
'''

__version__ = '0.1'

import sys, signal, codecs, argparse, sqlite3, csv
from contextlib import closing
from terminaltables import AsciiTable

reload(sys)
sys.setdefaultencoding('utf-8')

def dequote(s):
    """
    对于字符串两边有引号的字符串进行解析
    取中间有效字符 仅仅对" 和 ' 两种引号生效.
    注意: 这里仅对两边包围的引号生效,
    对内部的引号不影响
    """
    if (s[0] == s[-1]) and s.startswith(("'", '"')):
        return s[1:-1]
    return s

def debom(s):
    """
    此函数是去除字符串中bom字符, 
    由于此字符出现再文件的头位置
    所以对csv 的header造成的影响, 甚至乱码
    通过此函数可以避免这种情况
    """
    boms = [ k for k in dir(codecs) if k.startswith('BOM') ]
    for bom in boms:
        s = s.replace(getattr(codecs, bom), '')
    return s


def to_normalized(string):
    """
    由于csv 列信息的不确定性， 有时
    不能直接作为数据库的字段名
    这里可以实用此函数`to_normalized`进行转换
    """
    string = string.strip().lower().replace(" ", "_")
    return dequote(debom(string))


class Row(object):
    """
    此对象可以实例化一个列信息 源列名 和 规范列名对应表

    .original   源列明
    .normalized 转换后的列明
    """
    def __init__(self, original, normalized):
        self.original = original
        self.normalized = normalized


class CSVHandler(object):

    """解析对象"""

    def __init__(self, filename, path=':memory:', 
            text_factory=str):

        self.reader = csv.DictReader(open(filename))
        self.db = sqlite3.connect(path)
        self.db.text_factory = text_factory
        self.cols = self._build_cols()

        self.create_and_insert()

    def _build_cols(self):
        """
        转换所有列名为规范列名， 并生成Row实例列表
        """
        return [
            Row(f, to_normalized(f))
            for f in self.reader.fieldnames
        ]

    def _insert_row(self):
        """
        插入解析后的数据到表
        """
        with closing(self.db.cursor()) as cur:
            for row in self.reader:
                cur.execute(
                    """INSERT INTO t VALUES ({})""".format(
                        ",".join(["?"] * len(self.cols))
                    ),
                    [row[c.original] for c in self.cols]
                )

                
    def _create_table(self):
         """
         在数据库中创建table
         """
         with closing(self.db.cursor()) as cur:
            create_columns = [ 
                "{} varchar".format(c.normalized) \
                    for c in self.cols
            ]

            cur.execute("""CREATE TABLE t (
                {create_columns}
            )""".format(create_columns=','.join(create_columns)))

    def create_and_insert(self):
        self._create_table()
        self._insert_row()

        with closing(self.db.cursor()) as cur:
            cur.execute("select count(*) from t;")
            number_rows = cur.fetchall()[0][0]
            sys.stdout.write("Loaded {} rows into t({})\n".format(
                number_rows, 
                ", ".join(c.normalized for c in self.cols))
            )

    def interactive(self):
        """
        开始SQL交互式模式
        """
        cur = self.db.cursor()
        while True:
            sys.stdout.write("> ")
            try:
                cur.execute(sys.stdin.readline())
                header = [ c[0] for c in cur.description]
            except sqlite3.OperationalError as e:
                sys.stderr.write(str(e) + '\n')
                continue
            except TypeError as e:
                sys.stderr.write(str(e) + '\n')
                continue

            table = AsciiTable(
                [header] + [r for r in cur.fetchall()]
            )
            sys.stdout.write(table.table + '\n')


def handle_command_line(argv):
    """
    命令入口方法
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--filename", type=str,
            help="The csv file path.", required=True)
    args = parser.parse_args()
    p = CSVHandler(args.filename)
    p.interactive()


def signal_handler(signal, frame):
    sys.stdout.write('You pressed Ctrl+C!\n')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

if __name__ == '__main__':
    handle_command_line(sys.argv)
