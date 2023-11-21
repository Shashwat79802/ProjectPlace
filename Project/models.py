from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
import uuid


class ApplicationType(models.Model):
    category = models.CharField(verbose_name="Category", max_length=100)

    def __str__(self):
        return self.category


class TechStack(models.Model):
    technology = models.CharField(verbose_name="Technology", max_length=100)

    def __str__(self):
        return self.technology


class Project(models.Model):
    id = models.UUIDField(verbose_name="Project ID", primary_key=True, editable=False, default=uuid.uuid4)
    name = models.CharField(verbose_name="Project Name", max_length=500, blank=False, null=False)
    price = models.PositiveIntegerField(verbose_name="Project Price", validators=[MinValueValidator(limit_value=500), MaxValueValidator(limit_value=999999)])
    description = models.CharField(verbose_name="Project Description", max_length=2000, blank=True, null=True)
    application_type = models.ManyToManyField(to=ApplicationType, verbose_name="Type of Application Project")
    tech_stack = models.ManyToManyField(to=TechStack, verbose_name='Tech Stack')
    created_at = models.DateTimeField(auto_created=True, auto_now_add=True)

    class Meta:
        ordering = ['created_at', 'id']

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
