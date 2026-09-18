from django.db import models
from django.contrib.auth.models import User

class Subject(models.Model):
    name = models.CharField(max_length=100)
    year = models.IntegerField()  # 1 for 1st year, 2 for 2nd year, etc.
    image = models.ImageField(upload_to='subject_images/', null=True, blank=True)
    is_quantum = models.BooleanField(default=False)

    def __str__(self):
        tag = " [Quantum]" if self.is_quantum else ""
        return f"{self.name} (Year {self.year}){tag}"

    class Meta:
        ordering = ['year', 'name']
        verbose_name = "Subject"
        verbose_name_plural = "Subjects"

class Chapter(models.Model):
    name = models.CharField(max_length=255)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='chapters')
    image = models.ImageField(upload_to='chapter_images/', null=True, blank=True)
    
    def __str__(self):
        return f"{self.name} • {self.subject.name} (Yr {self.subject.year})"

    class Meta:
        ordering = ['subject', 'name']
        verbose_name = "Chapter / Unit"
        verbose_name_plural = "Chapters / Units"

class Note(models.Model):
    title = models.CharField(max_length=200)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name='notes')
    file = models.FileField(upload_to='notes/')
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploaded_notes')
    upload_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.chapter.name})"

    class Meta:
        ordering = ['-upload_date']
        verbose_name = "Note"
        verbose_name_plural = "Notes"
 