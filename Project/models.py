import uuid
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from projectplace.storage_backends import PublicDocumentStorage, PublicImageStorage


class ApplicationType(models.Model):
    """Defines the type of application. Ex - Web App, Cloud App etc."""

    category = models.CharField(
                            verbose_name="Category",
                            max_length=100
                            )

    def __str__(self):
        return str(self.category)


class TechStack(models.Model):
    """Lists the tech stacks used in the application. Ex - Java, SpringBoot etc."""

    technology = models.CharField(
                            verbose_name="Technology",
                            max_length=100
                            )

    def __str__(self):
        return str(self.technology)


class Project(models.Model):
    """The parent model of the application that decribes the Project entity."""

    id = models.UUIDField(
                        verbose_name="Project ID",
                        primary_key=True,
                        editable=False,
                        default=uuid.uuid4
                        )
    name = models.CharField(
                        verbose_name="Project Name",
                        max_length=500,
                        blank=False,
                        null=False
                        )
    price = models.PositiveIntegerField(
                        verbose_name="Project Price",
                        validators=[MinValueValidator(limit_value=500),
                                    MaxValueValidator(limit_value=999999)
                                    ]
                        )
    description = models.CharField(
                        verbose_name="Project Description",
                        max_length=2000,
                        blank=True,
                        null=True
                        )
    application_type = models.ManyToManyField(
                        to=ApplicationType,
                        verbose_name="Type of Application Project"
                        )
    tech_stack = models.ManyToManyField(
                        to=TechStack,
                        verbose_name='Tech Stack'
                        )
    created_at = models.DateTimeField(
                        auto_created=True,
                        auto_now_add=True
                        )

    class Meta:
        ordering = ['created_at', 'id']

    def __str__(self):
        return str(self.name)


class ProjectsImage(models.Model):
    """The child model of Project that describes the image entity of any project."""

    project = models.ForeignKey(
                    to=Project,
                    on_delete=models.CASCADE,
                    related_name='images'
                    )
    image = models.ImageField(
                    verbose_name="Project Images",
                    storage=PublicImageStorage()
                    )

    def __str__(self):
        return str(self.project.name)


class ProjectsDocument(models.Model):
    """The child model of Project that describes the document entity of any project."""

    project = models.ForeignKey(
                    to=Project,
                    on_delete=models.CASCADE,
                    related_name='documents'
                    )
    document = models.FileField(
                    verbose_name="Project Documents",
                    storage=PublicDocumentStorage()
                    )

    def __str__(self):
        return str(self.project.name)
