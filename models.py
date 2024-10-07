from django.db import models # type: ignore

class Contas_Receber_Fgi(models.Model):
    id_financeiro = models.IntegerField(db_column='Id_Financeiro', primary_key=True)
    matricula = models.BigIntegerField(db_column='MATRICULA')
    nome_aluno = models.CharField(db_column='Nome_Aluno', max_length=240)
    cpf = models.CharField(db_column='CFP', max_length=22)
    telefone = models.CharField(db_column='Telefone', max_length=60)
    email = models.CharField(db_column='EMAIL', max_length=200)
    cnpj_unidade = models.CharField(db_column='CNPJ_Unidade', max_length=14)
    razao_social = models.CharField(db_column='Razao_Social', max_length=100)
    formato = models.CharField(db_column='Formato', max_length=28)
    curso = models.CharField(db_column='Curso', max_length=100)
    periodo = models.CharField(db_column='Periodo', max_length=100)
    valor_mensalidade = models.FloatField(db_column='Valor_Mensalidade')
    data_vencimento = models.DateTimeField(db_column='Data_Vencimento')
    valor_pago = models.FloatField(db_column='Valor_Pago')
    data_pagamento = models.DateTimeField(db_column='Data_Pagamento', null=True, blank=True)
    tipo_parcela = models.CharField(db_column='Tipo_Parcela', max_length=510)
    tipo = models.CharField(db_column='Tipo', max_length=11)
    numero_parcela = models.IntegerField(db_column='Numero_Parcela')
    situacao_contrato = models.CharField(db_column='Situacao_Contrato', max_length=510)

    class Meta:
        db_table = 'Contas_Receber_Fgi'
        managed = False

class MetaAdsData(models.Model):
    campaign_name = models.CharField(max_length=255, verbose_name="Campanha")
    adset_name = models.CharField(max_length=255, verbose_name="Conjunto de Anúncios")
    spend = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor Gasto")
    date_start = models.DateField(verbose_name="Data de Início")
    date_stop = models.DateField(verbose_name="Data de Fim")

    class Meta:
        db_table = 'meta_ads_data'
        verbose_name = "Dados do Meta Ads"
        verbose_name_plural = "Dados do Meta Ads"
    
    def __str__(self):
        return f'{self.campaign_name} - {self.adset_name}'