from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import Subject, Chapter, Note

# Customize Admin Site Branding
admin.site.site_header = "StudyMate Administration"
admin.site.site_title = "StudyMate Admin Portal"
admin.site.index_title = "Study Materials & Notes Management"


class NoteInline(admin.TabularInline):
    """Allows uploading/managing notes directly inside Chapter admin"""
    model = Note
    extra = 1
    fields = ('title', 'file', 'uploaded_by', 'upload_date')
    readonly_fields = ('upload_date',)
    show_change_link = True

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "uploaded_by":
            kwargs["initial"] = request.user.id
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class ChapterInline(admin.TabularInline):
    """Allows adding/managing chapters directly inside Subject admin"""
    model = Chapter
    extra = 1
    fields = ('name', 'image', 'notes_count_badge')
    readonly_fields = ('notes_count_badge',)
    show_change_link = True

    @admin.display(description="Notes Count")
    def notes_count_badge(self, obj):
        if obj.pk:
            count = obj.notes.count()
            color = "#10b981" if count > 0 else "#94a3b8"
            return format_html(
                '<span style="background-color: {}; color: white; padding: 2px 8px; border-radius: 9999px; font-weight: 600; font-size: 11px;">{} Notes</span>',
                color, count
            )
        return "-"


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'year_badge', 'quantum_badge', 'get_chapters_count', 'get_notes_count', 'quick_actions')
    list_filter = ('year', 'is_quantum')
    search_fields = ('name',)
    inlines = [ChapterInline]
    ordering = ('year', 'name')
    list_per_page = 25

    @admin.display(description="Year", ordering="year")
    def year_badge(self, obj):
        colors = {
            1: "#059669",  # Emerald
            2: "#2563eb",  # Blue
            3: "#7c3aed",  # Purple
            4: "#ea580c",  # Orange
        }
        color = colors.get(obj.year, "#475569")
        suffix = "st" if obj.year == 1 else "nd" if obj.year == 2 else "rd" if obj.year == 3 else "th"
        return format_html(
            '<span style="background-color: {}; color: #fff; padding: 3px 10px; border-radius: 9999px; font-weight: 600; font-size: 12px;">{} Year</span>',
            color, f"{obj.year}{suffix}"
        )

    @admin.display(description="Type", ordering="is_quantum")
    def quantum_badge(self, obj):
        if obj.is_quantum:
            return format_html(
                '<span style="background-color: #dc2626; color: white; padding: 3px 8px; border-radius: 6px; font-weight: 600; font-size: 11px;">⚛️ Quantum</span>'
            )
        return format_html(
            '<span style="background-color: #e2e8f0; color: #475569; padding: 3px 8px; border-radius: 6px; font-weight: 500; font-size: 11px;">Regular</span>'
        )

    @admin.display(description="Chapters")
    def get_chapters_count(self, obj):
        count = obj.chapters.count()
        return format_html('<strong>{}</strong>', count)

    @admin.display(description="Total Notes")
    def get_notes_count(self, obj):
        count = Note.objects.filter(chapter__subject=obj).count()
        color = "#2563eb" if count > 0 else "#94a3b8"
        return format_html(
            '<span style="color: {}; font-weight: 600;">{} notes</span>',
            color, count
        )

    @admin.display(description="Quick View")
    def quick_actions(self, obj):
        url = reverse('subject_notes', args=[obj.id])
        return format_html(
            '<a href="{}" target="_blank" style="padding: 3px 8px; font-size: 12px; background: #f1f5f9; border: 1px solid #cbd5e1; border-radius: 4px; text-decoration: none; color: #1e293b;">View Page ↗</a>',
            url
        )


@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display = ('name', 'subject_link', 'get_year_badge', 'get_notes_count')
    list_filter = ('subject__year', 'subject__is_quantum', 'subject')
    search_fields = ('name', 'subject__name')
    autocomplete_fields = ()
    inlines = [NoteInline]
    ordering = ('subject__year', 'subject__name', 'name')
    list_per_page = 25

    @admin.display(description="Subject", ordering="subject__name")
    def subject_link(self, obj):
        link = reverse("admin:notes_subject_change", args=[obj.subject.id])
        tag = " <span style='color: #dc2626; font-size: 11px;'>(Quantum)</span>" if obj.subject.is_quantum else ""
        return format_html('<a href="{}" style="font-weight: 600; text-decoration: none; color: #2563eb;">{}{}</a>', link, obj.subject.name, format_html(tag))

    @admin.display(description="Year", ordering="subject__year")
    def get_year_badge(self, obj):
        colors = {1: "#059669", 2: "#2563eb", 3: "#7c3aed", 4: "#ea580c"}
        color = colors.get(obj.subject.year, "#475569")
        return format_html(
            '<span style="background-color: {}; color: white; padding: 2px 8px; border-radius: 9999px; font-weight: 600; font-size: 11px;">Year {}</span>',
            color, obj.subject.year
        )

    @admin.display(description="Notes")
    def get_notes_count(self, obj):
        count = obj.notes.count()
        return format_html('<span style="font-weight: 600;">{}</span>', count)


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'chapter_info', 'subject_name', 'year_info', 'uploaded_by', 'upload_date', 'file_action')
    list_filter = ('chapter__subject__year', 'chapter__subject__is_quantum', 'chapter__subject', 'upload_date')
    search_fields = ('title', 'chapter__name', 'chapter__subject__name', 'uploaded_by__username')
    date_hierarchy = 'upload_date'
    ordering = ('-upload_date',)
    list_per_page = 25

    fieldsets = (
        ("Note Information", {
            "fields": ("title", "file")
        }),
        ("Placement (Subject / Chapter)", {
            "fields": ("chapter",),
            "description": "Select the chapter/unit this note belongs to. Format: <em>Chapter Name • Subject Name (Year)</em>"
        }),
        ("Upload Metadata", {
            "fields": ("uploaded_by",),
            "classes": ("collapse",),
            "description": "Leave as is to automatically assign to yourself."
        })
    )

    def save_model(self, request, obj, form, change):
        """Auto-assign current user if uploaded_by is not explicitly provided"""
        if not obj.uploaded_by_id:
            obj.uploaded_by = request.user
        super().save_model(request, obj, form, change)

    def get_changeform_initial_data(self, request):
        """Pre-populate uploaded_by with current user"""
        initial = super().get_changeform_initial_data(request)
        initial['uploaded_by'] = request.user.id
        return initial

    @admin.display(description="Chapter", ordering="chapter__name")
    def chapter_info(self, obj):
        return obj.chapter.name

    @admin.display(description="Subject", ordering="chapter__subject__name")
    def subject_name(self, obj):
        return obj.chapter.subject.name

    @admin.display(description="Year", ordering="chapter__subject__year")
    def year_info(self, obj):
        colors = {1: "#059669", 2: "#2563eb", 3: "#7c3aed", 4: "#ea580c"}
        color = colors.get(obj.chapter.subject.year, "#475569")
        return format_html(
            '<span style="background-color: {}; color: white; padding: 2px 7px; border-radius: 9999px; font-weight: 600; font-size: 11px;">Year {}</span>',
            color, obj.chapter.subject.year
        )

    @admin.display(description="File")
    def file_action(self, obj):
        if obj.file:
            return format_html(
                '<a href="{}" target="_blank" download style="display: inline-flex; align-items: center; gap: 4px; padding: 3px 8px; font-size: 11px; background-color: #ecfdf5; border: 1px solid #6ee7b7; color: #047857; border-radius: 4px; text-decoration: none; font-weight: 600;">📥 Download</a>',
                obj.file.url
            )
        return "-"
 