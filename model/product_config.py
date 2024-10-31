from peewee import Model, CharField, IntegerField, DateTimeField, MySQLDatabase

db = MySQLDatabase('fishsale',
                   user='root',
                   password='xcc86977@@',
                   host='8.137.14.45',
                   charset='utf8mb4',
                   port=3306
                   )


class ProductConfig(Model):
    id = IntegerField(primary_key=True)
    product_id = IntegerField(null=True)
    pdd_search_name = CharField(max_length=100, null=True)
    fish_config = CharField(max_length=50, null=True)
    pdd_search_config = CharField(max_length=50, null=True)
    create_time = DateTimeField()
    update_time = DateTimeField()

    class Meta:
        database = db
        table_name = 'product_config'

    @classmethod
    def create_product_config(cls, product_id, product_name, fish_config, pdd_search_config):
        return cls.create(product_id=product_id,
                          product_name=product_name,
                          fish_config=fish_config,
                          pdd_search_config=pdd_search_config
                          )

    @classmethod
    def get_product_config_list_by_product_id(cls, product_id):
        return cls.select().where(cls.product_id == product_id)

    def update_product_config(self, product_name=None, fish_config=None, pdd_search_config=None):
        if product_name:
            self.product_name = product_name
        if fish_config:
            self.fish_config = fish_config
        if pdd_search_config:
            self.pdd_search_config = pdd_search_config
        self.save()

    def delete_product_config(self):
        self.delete_instance()