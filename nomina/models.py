# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class TbCanton(models.Model):
    id_canton = models.AutoField(primary_key=True)
    nombre_canton = models.CharField(max_length=100, blank=True, null=True)
    id_provincia = models.ForeignKey('TbProvincia', models.DO_NOTHING, db_column='id_provincia', blank=True, null=True)

    def __str__(self):
        return self.nombre_canton or f"Cantón {self.id_canton}"

    class Meta:
        managed = False
        db_table = 'tb_canton'


class TbEstudiantes(models.Model):
    id_est = models.AutoField(primary_key=True)
    apellido_est = models.CharField(max_length=50)
    nombre_est = models.CharField(max_length=50)
    cedula_est = models.CharField(max_length=10)
    id_canton = models.ForeignKey(TbCanton, models.DO_NOTHING, db_column='id_canton', blank=True, null=True)
    direccion_est = models.TextField()
    fecha_nacimiento_est = models.DateField()
    fecha_creacion_est = models.DateTimeField(blank=True, null=True)
    fecha_actualizacion_est = models.DateTimeField(blank=True, null=True)
    estado_est = models.CharField(max_length=25, blank=True, null=True)

    def __str__(self):
        return f"{self.apellido_est}, {self.nombre_est}"

    class Meta:
        managed = False
        db_table = 'tb_estudiantes'


class TbProvincia(models.Model):
    id_provincia = models.IntegerField(primary_key=True)
    nombre_provincia = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.nombre_provincia or f"Provincia {self.id_provincia}"

    class Meta:
        managed = False
        db_table = 'tb_provincia'


class TbUniversidades(models.Model):
    id_uni = models.AutoField(primary_key=True)
    nombre_uni = models.CharField(max_length=200, blank=True, null=True)
    rector_uni = models.CharField(max_length=200, blank=True, null=True)
    creacion_uni = models.DateTimeField(blank=True, null=True)
    actualizacion_uni = models.DateTimeField(blank=True, null=True)
    estado_uni = models.CharField(max_length=25, blank=True, null=True)

    def __str__(self):
        return self.nombre_uni or f"Universidad {self.id_uni}"

    class Meta:
        managed = False
        db_table = 'tb_universidades'
