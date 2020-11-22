from django.db import models

# Create your models here.
class Record(models.Model):
    id = models.AutoField(primary_key=True)
    okpd = models.CharField(max_length=12, unique=True, null=False)
    ktru_records_count = models.CharField(max_length=30, null=False)
    isCanceled = models.BooleanField(null=False)
    zapret = models.CharField(max_length=20, null=False)
    ogranichenia = models.CharField(max_length=20, null=False)
    preimuschestvo = models.CharField(max_length=20, null=False)
    dopusk = models.CharField(max_length=20, null=False)
    perechen = models.CharField(max_length=20, null=False)
    forma = models.CharField(max_length=20, null=False)
    tk = models.CharField(max_length=20, null=False)
    efektivnost = models.CharField(max_length=20, null=False)
    perechenTryUIS = models.CharField(max_length=20, null=False)
    nepubl = models.CharField(max_length=20, null=False)
    date_changed = models.DateTimeField(auto_now=True, null=False)

    def __repr__(self):
        return f'ОКПД - {self.okpd}'
    def __str__(self):
        return f'ОКПД - {self.okpd}'



    # id = db.Column(db.Integer, primary_key=True)
    # okpd = db.Column(db.String(20), unique=True, nullable=False)    #KOD OKPD
    # ktru_records_count = db.Column(db.String(20), nullable=False)   #zapisei v ktru
    # isCanceled = db.Column(db.Boolean, nullable=False)              #Отменён
    # zapret = db.Column(db.String(20), nullable=False)               #Запреты
    # ogranichenia = db.Column(db.String(20), nullable=False)         #Ограничения
    # preimuschestvo = db.Column(db.String(20), nullable=False)       #Преимущества
    # dopusk = db.Column(db.String(20), nullable=False)               #Условия допуска
    # perechen = db.Column(db.String(20), nullable=False)             #Аукционный перечень
    # forma = db.Column(db.String(20), nullable=False)                #Электронная форма !!!!!!223-ФЗ
    # tk = db.Column(db.String(20), nullable=False)                   #Типовой контракт
    # efektivnost = db.Column(db.String(20), nullable=False)          #Энергоэффективность
    # perechenTryUIS = db.Column(db.String(20), nullable=False)       #Перечень ТРУ, производимых УИС
    # nepubl = db.Column(db.String(20), nullable=False)               #Не размещается в ЕИС
    # date_changed = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    #
