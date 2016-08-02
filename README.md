csvSQL
---------

csvSQL 可以让你通过SQL来查看csv文件数据

```bash
$ csvsql -f test.csv
Loaded 57 rows into t(name, position, office, age, start_date, salary)
> select * from t limit 5;
+----------------+-------------------------------+---------------+------+------------+------------+
| name           | position                      | office        | age  | start_date | salary     |
+----------------+-------------------------------+---------------+------+------------+------------+
| Airi Satou     | Accountant                    | Tokyo         | 33.0 | 2008/11/28 | $162,700   |
| Angelica Ramos | Chief Executive Officer (CEO) | London        | 47.0 | 2009/10/09 | $1,200,000 |
| Ashton Cox     | Junior Technical Author       | San Francisco | 66.0 | 2009/01/12 | $86,000    |
| Bradley Greer  | Software Engineer             | London        | 41.0 | 2012/10/13 | $132,000   |
| Brenden Wagner | Software Engineer             | San Francisco | 28.0 | 2011/06/07 | $206,850   |
+----------------+-------------------------------+---------------+------+------------+------------+
> select count(*) from t;
+----------+
| count(*) |
+----------+
| 57       |
+----------+
> 
```

## 特别说明

衍生于: [csv-sql](https://github.com/alex/csv-sql)

感谢: [alex](https://github.com/alex)


**衍生功能:**

* 优化bom带来的第一列列名不显示bug
* 支持UTF-8 
* 优化命令形式及传参方式


## 安装使用

```shell
$ git clone https://github.com/jackeyGao/csvSQL
$ cd csvSQL
$ python setup.py install
$ csvsql -f test.csv
```

