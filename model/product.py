from peewee import Model, CharField, IntegerField, DateTimeField, MySQLDatabase

db = MySQLDatabase('fishsale',
                   user='root',
                   password='xcc86977@@',
                   host='8.137.14.45',
                   charset='utf8mb4',
                   port=3306
                   )

class Product(Model):
    id = IntegerField(primary_key=True)
    name = CharField(max_length=100, null=True)
    pdd_search_name = CharField(max_length=50, null=True)
    is_no_size = IntegerField(null=True)
    create_time = DateTimeField()
    update_time = DateTimeField()

    class Meta:
        database = db
        table_name = 'product'

    @classmethod
    def create_product(cls, name, pdd_search_name, is_no_size):
        return cls.create(name=name, pdd_search_name=pdd_search_name, is_no_size=is_no_size)

    @classmethod
    def get_product_by_id(cls, product_id):
        return cls.get_or_none(id=product_id)

    @classmethod
    def get_all_product(cls):
        return cls.select(Product.id, Product.name, Product.pdd_search_name)

    @classmethod
    def get_product_list_by_no_size(cls, is_no_size):
        product_list = cls.select().where(cls.is_no_size == is_no_size)
        return product_list

    def update_product(self, name=None, pdd_search_name=None, is_no_size=None):
        if name:
            self.name = name
        if pdd_search_name:
            self.pdd_search_name = pdd_search_name
        if is_no_size is not None:
            self.is_no_size = is_no_size
        self.save()

    def delete_product(self):
        self.delete_instance()