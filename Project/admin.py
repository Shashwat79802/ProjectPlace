from django.contrib import admin, sites
from .models import Project, ProjectsDocument, ProjectsImage, TechStack, ApplicationType


class ProjectsImageInline(admin.StackedInline):
    model = ProjectsImage
    extra = 1


class ProjectsDocumentInline(admin.StackedInline):
    model = ProjectsDocument
    extra = 1


class ProjectInline(admin.StackedInline):
    model = Project
    extra = 1


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'price', 'description']
    list_filter = ['price',]
    inlines = [ProjectsImageInline, ProjectsDocumentInline]
    filter_horizontal = ("application_type", "tech_stack")


@admin.register(ProjectsImage)
class ProjectsImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'image']


@admin.register(ProjectsDocument)
class ProjectsDocumentAdmin(admin.ModelAdmin):
    list_display = ['id', 'document']


@admin.register(TechStack)
class TechStackAdmin(admin.ModelAdmin):
    list_display = ['id', 'technology']


@admin.register(ApplicationType)
class ApplicationTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'category']
