    "In software engineering, the active record pattern is an architectural pattern found in software that stores its data in relational databases. It was named by Martin Fowler in his 2003 book Patterns of Enterprise Application Architecture[1]. The interface to such an object would include functions such as Insert, Update, and Delete, plus properties that correspond more or less directly to the columns in the underlying database table.
Active record is an approach to accessing data in a database. A database table or view is wrapped into a class. Thus, an object instance is tied to a single row in the table. After creation of an object, a new row is added to the table upon save. Any object loaded gets its information from the database. When an object is updated the corresponding row in the table is also updated. The wrapper class implements accessor methods or properties for each column in the table or view.
This pattern is commonly used by object persistence tools, and in object-relational mapping. Typically, foreign key relationships will be exposed as an object instance of the appropriate type via a property."
                                                                                    -----FROM WIKI
     ActiveRecord4J is the implementation of active record in Java.
     the simple introduction is here:
      ActiveRecord4Java 说明文档

一、ActiveRecord4J特点
A. 目前是脚本语言像php ruby这些脚本语言对数据库操作很简单，采用Active Record 模式，直接将数据库操作方法封装进实体Bean里面
B. Java ORM框架配置复杂，比如Hibernate,而且不容易上手，不利于快速开发，AR4J只需要配置数据库连接，实体属性命名遵循与数据库一直，万事OK，你就可以用你的实体操作数据库了。
C. 运行速度，目前ORM框架内置了很多功能，导致运行熟读减慢，AR4J框架精简，实现了我们最常用功能，运行速度接近JDBC运行速度。
D. 提供很多常用方法内置于实体Bean中，基本减去了我们再去写Dao的任务,如果你业务需要你可以在扩展，AR4J提供SQL语句片段，你可以组合它们实现你复杂的业务。
E. 完全采用preparedStatement，防止SQL注入攻击
二、ActiveRecord 4J实现的功能
A. Orm 是必须的，核心类Model,你的实体bean只需要继承它，就会拥有大量数据库操作方法。
B. 保证数据类型，能够安全转换，因为AR4J一直围绕PreparedStatement,不管是更新删除插入还是查询，让类型转换交给我们的数据库驱动做，因为它最了解数据库类型与java类型的映射关系。
C. 针对web开发提供常用方法，方便快速开发web应用程序，有图有真相，方法如下：

ActiveRecord4Java 说明文档
1. insert(),实现用数据库插入一条记录，返回数据库生成的id。
2. update(),实现更新在数据库存在的记录，只会更新bean里面不为空的属性,返回自己的id。
3. delete(),输出数据库一条记录,返回布尔类型。
4. save(),只是简单把insert()与update()包装一下，通过对当前Bean的id判断是insert，还是update，返回id.
5. findOne(),查找出数据库里面一条数据,返回一个封装的Bean。
6. findColumns(),根据条件查找出数据库相关列，返回List<Map<String,Object>>这样的类型，将每行的列封转在一个Map里面。
7. find(),根据条件查出数据库相关数据，封转成Bean，返回类型List<T extends Model>.
8. findSelf(),找出自己，bean里面的id属性不能小于1.返回类型为Bean.
9. findById(long id),根据参数，找出一个实体Bean,返回类型Bean.
10. count(),根据条件，查出相关记录的条数，返回类型int.
以上函数为查询函数，下面为设置条件函数，主要将SQL语句拆分，
11. asc(String column) ,输入列名，结果将以输入列名升序排序，返回类型是Model。
12. desc(String column),输入列名，结果将以输入列名降序排序，返回类型为Model。
13. select(String... columns),输入多个列名，结果将只包含这些列名，返回类型Model.
14. like(String column,Object arg),输入列名与之对应的条件值，返回类型Model.
15. and(),链接多个条件函数，返回类型Model.
16. or() ,链接多个条件，返回类型Model.
17. gt(String column,Object arg),比某个值大，返回类型Model.
18. gtOreq(String colums,Object arg),比某个大或者等于，返回类型Model.
19. lt(String column,Object arg),比某个值小，返回类型Model.
20. ltOreq(String column,Object arg),比某个值小或者相等，返回类型Model.
21. limit(int from,int offset),从from+1开始 到from+offset的记录，返回Model
22. page(int page,int size),用于分页，其实和limit差不多，返回类型Model
23. from(String...tableNames),用于多表查询，返回类型Model.
当然你如果觉得这些函数没法满足你的应用程序，你可以在你自己的Bean里面添加就行了。
三、ActiveRecord4J数据操作流程

四、使用ActiveRecord4J注意事项
A. 你的bean的命名应该和数据库表名（去掉前缀）一致，然后你需要在配置文件设置前缀名。
B. 你的bean对应数据库中的表的主键生成策略应该设置自增，我们不提供生成策略,并且主键名必须为id,你的bean也不需要再写id这个属性，因为你继承Model后，Model里面已经有了，你的bean的属性名必须与数据库表列名一一对应。
C. 现在只支持MYSQL，现在此项目只是测试阶段，所以只用测试，我会尽快更新它，使它完善，投入使用。
