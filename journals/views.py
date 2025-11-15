from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Q
from .models import Journal
from .forms import JournalForm
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User

def home(request):
    """Homepage showing latest approved journals."""
    # ✅ Case-insensitive filter for status
    journals = Journal.objects.filter(status__iexact='approved').order_by('-upload_date')[:6]
    return render(request, 'journals/index.html', {'journals': journals})


def search_journals(request):
    """Search only approved journals by title, author, department, or keywords."""
    query = request.GET.get('q', '').strip()
    results = []

    if query:
        results = Journal.objects.filter(
            Q(title__icontains=query) |
            Q(author__username__icontains=query) |
            Q(department__icontains=query) |
            Q(keywords__icontains=query)
        ).filter(status__iexact='approved').order_by('-upload_date')

    return render(request, 'journals/search_results.html', {
        'query': query,
        'results': results
    })

@login_required
def upload_journal(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        department = request.POST.get('department')
        supervisor = request.POST.get('supervisor')
        year = request.POST.get('year')
        keywords = request.POST.get('keywords')
        abstract = request.POST.get('abstract')
        pdf_file = request.FILES.get('pdf_file')

        if pdf_file and pdf_file.name.endswith('.pdf'):
            Journal.objects.create(
                user=request.user,
                author=request.user,
                title=title,
                department=department,
                supervisor=supervisor,
                year=year if year else None,
                keywords=keywords,
                abstract=abstract,
                pdf_file=pdf_file,
            )
            messages.success(request, '✅ Journal uploaded successfully and is now pending review.')
            return redirect('user_dashboard')
        else:
            messages.error(request, 'Please upload a valid PDF file.')

    return render(request, 'journals/upload_journal.html')


from django.contrib.admin.views.decorators import staff_member_required
from django.utils import timezone

@staff_member_required

@login_required
def admin_dashboard(request):
    pending_list = Journal.objects.filter(status="Pending").order_by('-upload_date')
    approved_list = Journal.objects.filter(status="Approved").order_by('-upload_date')
    rejected_list = Journal.objects.filter(status="Rejected").order_by('-upload_date')

    # Set uploaders (unique authors)
    total_uploaders = Journal.objects.values('author').distinct().count()

    return render(request, "journals/admin_dashboard.html", {
        "pending_list": pending_list,
        "approved_list": approved_list,
        "rejected_list": rejected_list,
        "total_uploaders": total_uploaders,
        "now": timezone.now(),
    })

from django.shortcuts import render
from .models import Journal


# ✅ Restrict admin-only access
def admin_required(view_func):
    return user_passes_test(lambda u: u.is_staff or u.is_superuser)(view_func)


# ======== JOURNAL STATUS PAGES ========

@admin_required
@login_required
def pending_journals(request):
    pending_journals = Journal.objects.filter(status='Pending').order_by('-upload_date')
    return render(request, 'journals/pending_journals.html', {'pending_journals': pending_journals})


@login_required
@admin_required
def approved_journals(request):
    """Display all approved journals"""
    approved_journals = Journal.objects.filter(status='approved').order_by('-upload_date')
    return render(request, 'journals/approved_journals.html', {'approved_journals': approved_journals})


@login_required
@admin_required
def rejected_journals(request):
    """Display all rejected journals"""
    rejected_journals = Journal.objects.filter(status='rejected').order_by('-upload_date')
    return render(request, 'journals/rejected_journals.html', {'rejected_journals': rejected_journals})


# ======== APPROVE / REJECT JOURNALS ========

@login_required
@admin_required
def approve_journal(request, journal_id):
    """Approve a journal upload"""
    journal = get_object_or_404(Journal, id=journal_id)
    journal.status = 'approved'
    journal.save()
    messages.success(request, f"✅ '{journal.title}' has been approved.")
    return redirect('pending_journals')


@login_required
@admin_required
def reject_journal(request, journal_id):
    """Reject a journal upload"""
    journal = get_object_or_404(Journal, id=journal_id)
    journal.status = 'rejected'
    journal.save()
    messages.warning(request, f"❌ '{journal.title}' has been rejected.")
    return redirect('pending_journals')

@login_required
def user_dashboard(request):
    """User dashboard showing personal journal stats"""
    user = request.user

    # Only journals uploaded by the logged-in user
    user_journals = Journal.objects.filter(user=user)

    # Dashboard counts
    uploaded_count = user_journals.count()
    pending_count = user_journals.filter(status='Pending').count()
    approved_count = user_journals.filter(status='Approved').count()
    rejected_count = user_journals.filter(status='Rejected').count()

    context = {
        'uploaded_count': uploaded_count,
        'pending_count': pending_count,
        'approved_count': approved_count,
        'rejected_count': rejected_count,
        'user_journals': user_journals,  # optional, in case you list them below
    }

    return render(request, 'journals/user_dashboard.html', context)

@login_required
def my_journals(request):
    """
    Display all journals uploaded by the logged-in user,
    along with dashboard stats.
    """
    user = request.user

    # Fetch user-specific journals
    user_journals = Journal.objects.filter(user=user).order_by('-upload_date')

    # Dashboard counts
    uploaded_count = user_journals.count()
    pending_count = user_journals.filter(status='Pending').count()
    approved_count = user_journals.filter(status='Approved').count()
    rejected_count = user_journals.filter(status='Rejected').count()

    context = {
        'user_journals': user_journals,
        'uploaded_count': uploaded_count,
        'pending_count': pending_count,
        'approved_count': approved_count,
        'rejected_count': rejected_count,
    }

    return render(request, 'journals/my_journals.html', context)