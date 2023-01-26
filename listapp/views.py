from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from .forms import UserRegisterForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import List, Object
from django.contrib import messages

def registrera(request):
    if request.method=='POST':
        form=UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            anvandarnamn = form.cleaned_data.get('username')
            messages.success(request, f'Konto skapades för {anvandarnamn}')
            return redirect('loggain')
    else:
        form=UserRegisterForm()

    return render(request, 'listapp/registrera.html',{'form':form})

class AllaListor(LoginRequiredMixin,ListView):
    model=List
    template_name = 'listapp/hem.html'
    context_object_name = 'listor'
    ordering = ['-cdate']

class EnLista(LoginRequiredMixin,ListView):
    model=Object
    template_name = 'listapp/lista.html'
    context_object_name = 'objects'

    def get_queryset(self):
        return Object.objects.filter(list=self.kwargs['pk'])

    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        context['listan'] = List.objects.filter(id=self.kwargs['pk'])
        return context

class SkapaLista(LoginRequiredMixin,CreateView):
    model=List
    fields=['listname']

    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        context['status'] = {"status":"Ny"}
        return context

    def form_valid(self,form):
        form.instance.cuser=self.request.user
        return super().form_valid(form)

class UppdateraLista(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model=List
    fields=['listname']

    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        context['status'] = {"status":"Uppdatera"}
        return context

    def test_func(self):
        lista=self.get_object()
        if self.request.user == lista.cuser:
            return True
        return False

class RaderaLista(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model=List
    success_url='/'

    def test_func(self):
        lista=self.get_object()
        if self.request.user == lista.cuser:
            return True
        return False

class SkapaObject(LoginRequiredMixin,CreateView):
    model=Object
    fields=['objectname', 'amount']

    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        lista=get_object_or_404(List,id=self.kwargs.get('l_pk'))
        context['status'] = {"status":"Ny",'listID':lista.id}
        return context

    def form_valid(self,form):
        form.instance.list=get_object_or_404(List,id=self.kwargs.get('l_pk'))
        return super().form_valid(form)

class UppdateraObject(LoginRequiredMixin,UpdateView):
    model=Object
    fields=['objectname', 'amount']

    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        context['status'] = {"status":"Uppdatera"}
        return context

class RaderaObject(LoginRequiredMixin,DeleteView):
    model=Object

    def get_success_url(self):
        lista = self.object.list
        return reverse_lazy('lista-sida', kwargs={'pk':lista.id})
