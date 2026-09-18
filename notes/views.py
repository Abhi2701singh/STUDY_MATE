from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.http import JsonResponse
from django.contrib import messages
from django.db.models import Count, Q
from .models import Note, Subject, Chapter

def home(request):
    """Modern home page with statistics, quick year access, and recent notes"""
    search_query = request.GET.get('q', '').strip()
    
    total_notes = Note.objects.count()
    total_subjects = Subject.objects.count()
    total_chapters = Chapter.objects.count()
    
    # Counts per year for year cards
    year_stats = {}
    for y in [1, 2, 3, 4]:
        year_stats[y] = {
            'subjects_count': Subject.objects.filter(year=y, is_quantum=False).count(),
            'notes_count': Note.objects.filter(chapter__subject__year=y, chapter__subject__is_quantum=False).count()
        }
    
    quantum_stats = {
        'subjects_count': Subject.objects.filter(is_quantum=True).count(),
        'notes_count': Note.objects.filter(chapter__subject__is_quantum=True).count()
    }
    
    # If search query provided on home page
    search_results = None
    if search_query:
        search_results = Note.objects.filter(
            Q(title__icontains=search_query) |
            Q(chapter__name__icontains=search_query) |
            Q(chapter__subject__name__icontains=search_query)
        ).select_related('chapter', 'chapter__subject', 'uploaded_by').order_by('-upload_date')
    
    recent_notes = Note.objects.select_related('chapter', 'chapter__subject', 'uploaded_by').order_by('-upload_date')[:6]
    
    return render(request, 'home.html', {
        'recent_notes': recent_notes,
        'total_notes': total_notes,
        'total_subjects': total_subjects,
        'total_chapters': total_chapters,
        'year_stats': year_stats,
        'quantum_stats': quantum_stats,
        'search_query': search_query,
        'search_results': search_results,
    })

def year_notes(request, year):
    """Display notes for a specific year (excluding quantum) with search support"""
    query = request.GET.get('q', '').strip()
    subjects = Subject.objects.filter(year=year, is_quantum=False).order_by('name')
    subjects_data = []
    
    total_year_notes = 0
    for subject in subjects:
        notes_qs = Note.objects.filter(chapter__subject=subject).select_related('chapter', 'uploaded_by').order_by('-upload_date')
        if query:
            notes_qs = notes_qs.filter(
                Q(title__icontains=query) |
                Q(chapter__name__icontains=query)
            )
        notes = list(notes_qs)
        total_year_notes += len(notes)
        if notes or not query:  # Don't hide empty subjects if not searching
            subjects_data.append({
                'subject': subject,
                'notes': notes,
                'count': len(notes)
            })
    
    suffix = "st" if year == 1 else "nd" if year == 2 else "rd" if year == 3 else "th"
    return render(request, 'year_view.html', {
        'year_num': year,
        'year': f'{year}{suffix} Year',
        'subjects': subjects_data,
        'total_notes': total_year_notes,
        'query': query,
    })

def quantum(request):
    """Display quantum notes grouped by year with search support"""
    query = request.GET.get('q', '').strip()
    years = (
        Subject.objects.filter(is_quantum=True)
        .values_list('year', flat=True)
        .distinct()
        .order_by('year')
    )

    years_data = []
    total_quantum_notes = 0
    for year in years:
        year_subjects = Subject.objects.filter(is_quantum=True, year=year)
        notes_qs = Note.objects.filter(chapter__subject__in=year_subjects).select_related('chapter', 'chapter__subject', 'uploaded_by').order_by('-upload_date')
        if query:
            notes_qs = notes_qs.filter(
                Q(title__icontains=query) |
                Q(chapter__name__icontains=query) |
                Q(chapter__subject__name__icontains=query)
            )
        notes = list(notes_qs)
        total_quantum_notes += len(notes)
        if notes or not query:
            years_data.append({
                'year': year,
                'notes': notes,
                'count': len(notes)
            })

    return render(request, 'quantum.html', {
        'years': years_data,
        'total_notes': total_quantum_notes,
        'query': query,
    })

def staff_required(view_func):
    """Decorator to restrict access to staff only"""
    def wrapper(request, *args, **kwargs):
        if not request.user.is_staff:
            messages.error(request, 'Only administrators can perform this action!')
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return wrapper

def _handle_note_form(request, is_quantum=False):
    """Streamlined handler for regular and quantum note uploads supporting existing or new Subject/Chapter"""
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        uploaded_file = request.FILES.get('file')
        subject_mode = request.POST.get('subject_mode', 'existing')  # 'existing' or 'new'
        chapter_mode = request.POST.get('chapter_mode', 'existing')  # 'existing' or 'new'
        
        subject_image = request.FILES.get('subject_image')
        chapter_image = request.FILES.get('chapter_image')
        
        if not title:
            messages.error(request, 'Please provide a title for the note.')
            return redirect(request.path)
            
        if not uploaded_file:
            messages.error(request, 'Please select a file to upload.')
            return redirect(request.path)

        # 1. Resolve Subject
        subject = None
        if subject_mode == 'existing':
            subject_id = request.POST.get('subject_id')
            if subject_id:
                try:
                    subject = Subject.objects.get(id=subject_id)
                except Subject.DoesNotExist:
                    subject = None

        if not subject:
            # Create new subject or use existing with same name and year
            subject_name = request.POST.get('new_subject_name', '').strip() or request.POST.get('subject', '').strip()
            year_val = request.POST.get('year')
            if not subject_name or not year_val:
                messages.error(request, 'Please select or enter a subject and year.')
                return redirect(request.path)
                
            subject, _ = Subject.objects.get_or_create(
                name=subject_name,
                year=int(year_val),
                defaults={'is_quantum': is_quantum}
            )
            # Ensure is_quantum matches
            if subject.is_quantum != is_quantum:
                subject.is_quantum = is_quantum
                subject.save()

        if subject_image:
            subject.image = subject_image
            subject.save()

        # 2. Resolve Chapter
        chapter = None
        if chapter_mode == 'existing':
            chapter_id = request.POST.get('chapter_id')
            if chapter_id:
                try:
                    chapter = Chapter.objects.get(id=chapter_id, subject=subject)
                except Chapter.DoesNotExist:
                    chapter = None

        if not chapter:
            chapter_name = request.POST.get('new_chapter_name', '').strip() or request.POST.get('chapter', '').strip()
            if not chapter_name:
                chapter_name = "General / Unit 1"
            chapter, _ = Chapter.objects.get_or_create(
                subject=subject,
                name=chapter_name
            )

        if chapter_image:
            chapter.image = chapter_image
            chapter.save()

        # 3. Create Note
        note = Note.objects.create(
            title=title,
            chapter=chapter,
            file=uploaded_file,
            uploaded_by=request.user
        )

        messages.success(request, f'🎉 Note "{note.title}" uploaded successfully to {subject.name}!')
        if is_quantum:
            return redirect('quantum')
        return redirect('year_notes', year=subject.year)

    # GET Request: Fetch subjects for easy dropdown selection
    existing_subjects = Subject.objects.filter(is_quantum=is_quantum).order_by('year', 'name')
    all_subjects = Subject.objects.all().order_by('year', 'name')

    return render(request, 'add_note.html', {
        'is_quantum': is_quantum,
        'existing_subjects': existing_subjects,
        'all_subjects': all_subjects,
    })

@login_required
@staff_required
def add_note(request):
    return _handle_note_form(request, is_quantum=False)

@login_required
@staff_required
def add_quantum_note(request):
    return _handle_note_form(request, is_quantum=True)

def api_get_chapters(request, subject_id):
    """API endpoint to get chapters of a subject dynamically"""
    chapters = Chapter.objects.filter(subject_id=subject_id).values('id', 'name')
    return JsonResponse({'chapters': list(chapters)})

@login_required
@staff_required
def delete_note(request, note_id):
    """Delete a note (staff only)"""
    note = get_object_or_404(Note, id=note_id)
    is_quantum = note.chapter.subject.is_quantum
    year = note.chapter.subject.year
    title = note.title
    
    # Delete file from storage and remove record
    if note.file:
        note.file.delete(save=False)
    note.delete()
    
    messages.success(request, f'Note "{title}" deleted successfully.')
    
    if is_quantum:
        return redirect('quantum')
    return redirect('year_notes', year=year)

def signup(request):
    """Handle user registration with automatic login"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome to StudyMate, {user.username}! Your account has been created.')
            return redirect('home')
    else:
        form = UserCreationForm()
    
    return render(request, 'signup.html', {'form': form})

def subject_notes(request, subject_id):
    """Display all notes for a specific subject"""
    subject = get_object_or_404(Subject, id=subject_id)
    notes = Note.objects.filter(chapter__subject=subject).select_related('chapter', 'uploaded_by').order_by('-upload_date')
    return render(request, 'subject_notes.html', {
        'subject': subject,
        'notes': notes
    })