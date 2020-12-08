from django.shortcuts import render, redirect, get_object_or_404

from ..models import Venue, Artist, Note, Show
from ..forms import VenueSearchForm, NewNoteForm, NoteSearchForm, UserRegistrationForm

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseForbidden
from django.contrib import messages

from django.core.paginator import Paginator


@login_required
def new_note(request, show_pk):

    show = get_object_or_404(Show, pk=show_pk)

    if request.method == 'POST' :
        form = NewNoteForm(request.POST, request.FILES)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.show = show
            note.save()
            return redirect('note_detail', note_pk=note.pk)

    else :
        form = NewNoteForm()

    return render(request, 'lmn/notes/new_note.html', { 'form': form, 'show': show })


def latest_notes(request):
    notes = Note.objects.all().order_by('-posted_date')
        
    paginator = Paginator(notes, 25)
    page_number = request.GET.get('page')
    page_object = paginator.get_page(page_number)
    
    return render(request, 'lmn/notes/note_list.html', { 'notes': page_object })


def notes_for_show(request, show_pk): 
    # Notes for show, most recent first
    notes = Note.objects.filter(show=show_pk).order_by('-posted_date')
    show = Show.objects.get(pk=show_pk)  
    
    paginator = Paginator(notes, 25)
    page_number = request.GET.get('page')
    page_object = paginator.get_page(page_number)
    
    return render(request, 'lmn/notes/note_list.html', { 'show': show, 'notes': page_object })

# note_detail route checks to make sure the user who owns this not is editing it
def note_detail(request, note_pk):
    note = get_object_or_404(Note, pk=note_pk)
    # at the start of view function needs to have the note.user be equal to request.user
    if note.user != request.user:
        return HttpResponseForbidden()
    if request.method == 'POST':
        form = NewNoteForm(request.POST, request.FILES, instance=note) # instance = model object to update with the form data
        if form.is_valid():
            form.save()
            messages.info(request, 'User notes updated!')
        else:
            messages.error(request, form.errors) # Temp error message - future version should improve
        return redirect('note_details', note_pk=note_pk)
    else: #GET note details
        if latest_notes:
            review_form = NewNoteForm(instance=note)
            return render(request, 'lmn/notes/note_detail.html', {'note': note, 'review_form': review_form})
        else:
            return render(request, 'lmn/notes/note_detail.html', { 'note': note })
@login_required
def modify_note(request, note_pk):
    note = get_object_or_404(Note, pk=note_pk)
    show = get_object_or_404(Show, pk=note.show_id)
    if note.user != request.user:
        return HttpResponseForbidden()
    if request.method == 'POST' :
        form = NewNoteForm(request.POST, request.FILES, instance=note)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.User
            note.show = show
            note.save()
            return redirect('note_detail', note_pk=note.pk)
        else:
            form = NewNoteForm(instance=note)
        return redirect('note_detail', note_pk=note.pk)

@login_required #check that the user requesting to delete the note is the owner of the selected note
def delete_note(request, note_pk):
    note = get_object_or_404(Note, pk=note_pk)
    if note.user == request.user:
        note.delete()
        return redirect('latest_notes')
    else:
        return HttpResponseForbidden() 

@login_required
def user_notes(request):
    form = NoteSearchForm()
    search_name = request.GET.get('search_name')
    if search_name:
        notes = Note.objects.filter(user=request.user, title__icontains=search_name).order_by('-posted_date') | \
                Note.objects.filter(user=request.user, text__icontains=search_name).order_by('-posted_date')
    else:
        notes = Note.objects.filter(user=request.user).order_by('-posted_date')
    paginator = Paginator(notes, 25)
    page_number = request.GET.get('page')
    page_object = paginator.get_page(page_number)
        
    return render(request, 'lmn/notes/note_list.html', {'notes': page_object, 'my_notes': True, 'form': form,
                                                        'search_term': search_name})

