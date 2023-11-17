from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
import uuid


class Project(models.Model):
    id = models.UUIDField(verbose_name="Project ID", primary_key=True, editable=False, default=uuid.uuid4)
    name = models.CharField(verbose_name="Project Name", max_length=500, blank=False, null=False)
    price = models.PositiveIntegerField(verbose_name="Project Price", validators=[MinValueValidator(limit_value=500), MaxValueValidator(limit_value=999999)])
    description = models.CharField(verbose_name="Project Description", max_length=2000, blank=True, null=True)

    def __str__(self):
        return self.name


class ProjectsImage(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(verbose_name="Project Images", upload_to='project_images')

    def __str__(self):
        return self.project.name
    

class ProjectsDocument(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='documents')
    document = models.FileField(verbose_name="Project Documents", upload_to='project_docs')

    def __str__(self):
        return self.project.name
