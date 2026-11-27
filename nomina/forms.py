from django import forms
from django.utils import timezone
from .models import TbProvincia, TbCanton, TbEstudiantes, TbUniversidades


class AccessibleModelForm(forms.ModelForm):
    """Shared Bootstrap classes and accessible autocomplete defaults."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            widget = field.widget
            if isinstance(widget, forms.Select):
                widget.attrs.setdefault("class", "form-select")
            elif isinstance(widget, forms.Textarea):
                widget.attrs.setdefault("class", "form-control")
                widget.attrs.setdefault("rows", 3)
            else:
                widget.attrs.setdefault("class", "form-control")
            widget.attrs.setdefault("autocomplete", "off")
            if field.errors:
                widget.attrs["class"] = "{} is-invalid".format(widget.attrs.get("class", "")).strip()
            if name == "fecha_nacimiento_est":
                widget.attrs.setdefault("max", timezone.localdate().isoformat())


class ProvinciaForm(AccessibleModelForm):
    id_provincia = forms.IntegerField(
        min_value=1, label="Código de provincia",
        widget=forms.NumberInput(attrs={"min": "1", "step": "1", "inputmode": "numeric"}),
    )
    nombre_provincia = forms.CharField(
        required=True, min_length=2, max_length=100,
        label="Nombre de la provincia",
        widget=forms.TextInput(attrs={"minlength": "2", "maxlength": "100", "autocomplete": "address-level1"}),
    )

    class Meta:
        model = TbProvincia
        fields = ("id_provincia", "nombre_provincia")

    def clean_id_provincia(self):
        value = self.cleaned_data["id_provincia"]
        duplicate = TbProvincia.objects.filter(id_provincia=value)
        if self.instance.pk:
            duplicate = duplicate.exclude(pk=self.instance.pk)
        if duplicate.exists():
            raise forms.ValidationError("Ya existe una provincia con este código.")
        return value

    def clean_nombre_provincia(self):
        value = self.cleaned_data["nombre_provincia"].strip()
        duplicate = TbProvincia.objects.filter(nombre_provincia__iexact=value)
        if self.instance.pk:
            duplicate = duplicate.exclude(pk=self.instance.pk)
        if duplicate.exists():
            raise forms.ValidationError("Ya existe una provincia con este nombre.")
        return value


class CantonForm(AccessibleModelForm):
    nombre_canton = forms.CharField(
        required=True, min_length=2, max_length=100, label="Nombre del cantón",
        widget=forms.TextInput(attrs={"minlength": "2", "maxlength": "100"}),
    )

    class Meta:
        model = TbCanton
        fields = ("nombre_canton", "id_provincia")
        labels = {"id_provincia": "Provincia"}
        widgets = {"id_provincia": forms.Select(attrs={"required": True})}

    def clean_nombre_canton(self):
        value = self.cleaned_data["nombre_canton"].strip()
        provincia = self.cleaned_data.get("id_provincia")
        duplicate = TbCanton.objects.filter(nombre_canton__iexact=value, id_provincia=provincia)
        if self.instance.pk:
            duplicate = duplicate.exclude(pk=self.instance.pk)
        if duplicate.exists():
            raise forms.ValidationError("Ya existe un cantón con ese nombre en la provincia seleccionada.")
        return value


class EstudianteForm(AccessibleModelForm):
    apellido_est = forms.CharField(
        required=True, min_length=2, max_length=50, label="Apellidos",
        widget=forms.TextInput(attrs={"minlength": "2", "maxlength": "50", "autocomplete": "family-name"}),
    )
    nombre_est = forms.CharField(
        required=True, min_length=2, max_length=50, label="Nombres",
        widget=forms.TextInput(attrs={"minlength": "2", "maxlength": "50", "autocomplete": "given-name"}),
    )
    cedula_est = forms.RegexField(
        regex=r"^[0-9]{10}$", min_length=10, max_length=10,
        error_messages={"invalid": "Ingresa los 10 dígitos de la cédula."},
        label="Cédula",
        widget=forms.TextInput(attrs={"pattern": "[0-9]{10}", "inputmode": "numeric", "maxlength": "10", "minlength": "10", "autocomplete": "off"}),
    )
    direccion_est = forms.CharField(
        required=True, max_length=500, label="Dirección",
        widget=forms.Textarea(attrs={"maxlength": "500", "autocomplete": "street-address"}),
    )
    fecha_nacimiento_est = forms.DateField(
        label="Fecha de nacimiento",
        widget=forms.DateInput(attrs={"type": "date", "autocomplete": "bday"}),
    )
    estado_est = forms.ChoiceField(
        choices=(("ACTIVO", "Activo"), ("INACTIVO", "Inactivo")),
        label="Estado",
    )

    class Meta:
        model = TbEstudiantes
        fields = ("apellido_est", "nombre_est", "cedula_est", "id_canton", "direccion_est", "fecha_nacimiento_est", "estado_est")
        labels = {"id_canton": "Cantón"}
        widgets = {"id_canton": forms.Select(attrs={"required": True})}

    def clean_cedula_est(self):
        value = self.cleaned_data["cedula_est"]
        duplicate = TbEstudiantes.objects.filter(cedula_est=value)
        if self.instance.pk:
            duplicate = duplicate.exclude(pk=self.instance.pk)
        if duplicate.exists():
            raise forms.ValidationError("Ya existe un estudiante con esta cédula.")
        return value

    def clean_fecha_nacimiento_est(self):
        value = self.cleaned_data["fecha_nacimiento_est"]
        if value > timezone.localdate():
            raise forms.ValidationError("La fecha de nacimiento no puede ser futura.")
        return value


class UniversidadForm(AccessibleModelForm):
    nombre_uni = forms.CharField(
        required=True, min_length=2, max_length=200, label="Nombre de la universidad",
        widget=forms.TextInput(attrs={"minlength": "2", "maxlength": "200"}),
    )
    rector_uni = forms.CharField(
        required=True, min_length=2, max_length=200, label="Rector o rectora",
        widget=forms.TextInput(attrs={"minlength": "2", "maxlength": "200", "autocomplete": "name"}),
    )
    estado_uni = forms.CharField(
        required=True, min_length=2, max_length=25, label="Estado",
        widget=forms.TextInput(attrs={"minlength": "2", "maxlength": "25", "placeholder": "Ej. ACTIVA"}),
    )

    class Meta:
        model = TbUniversidades
        fields = ("nombre_uni", "rector_uni", "estado_uni")

    def clean(self):
        cleaned = super().clean()
        name = cleaned.get("nombre_uni")
        if name:
            duplicate = TbUniversidades.objects.filter(nombre_uni__iexact=name.strip())
            if self.instance.pk:
                duplicate = duplicate.exclude(pk=self.instance.pk)
            if duplicate.exists():
                self.add_error("nombre_uni", "Ya existe una universidad con este nombre.")
            cleaned["nombre_uni"] = name.strip()
        return cleaned
