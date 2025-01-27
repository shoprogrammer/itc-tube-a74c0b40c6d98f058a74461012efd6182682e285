from django.http.response import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404,redirect
from django.views.generic import ListView, DetailView, FormView #インポート
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import NippoModel
from .forms import  NippoModelForm, NippoFormClass
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.contrib import messages

class OwnerOnly(UserPassesTestMixin):
    def test_func(self):
        nippo_instance = self.get_object()
        return nippo_instance.user == self.request.user
    
    def handle_no_permission(self):
        messages.error(self.request,"ご自身の日報でのみ編集、削除が可能です")
        return redirect("nippo-detail",pk=self.kwargs["pk"])
        




class NippoListView(ListView): #クラス作成
    template_name = "nippo/nippo-list.html" #変数
    model = NippoModel #変数
    
    def get_queryset(self):
        qs = NippoModel.objects.all()
        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        return ctx

class NippoDetailView(DetailView):
    template_name = "nippo/nippo-detail.html"
    model = NippoModel
    
    def get_object(self):
        return super().get_object()
    
class NippoCreateModelFormView(LoginRequiredMixin, CreateView):
    template_name = "nippo/nippo-form.html"
    form_class = NippoModelForm
    success_url = reverse_lazy("nippo-list")

    
    def get_form_kwargs(self,*args,**kwargs):
        kwargs = super().get_form_kwargs(*args,**kwargs)
        kwargs["user"] = self.request.user
        return kwargs




    
class NippoUpdateModelFormView(OwnerOnly,UpdateView):
    template_name = "nippo/nippo-form.html"
    model = NippoModel
    form_class = NippoModelForm
    success_url = reverse_lazy("nippo-list")
    
class NippoDeleteView(OwnerOnly,DeleteView):
    template_name = "nippo/nippo-delete.html"
    model = NippoModel
    success_url = reverse_lazy("nippo-list")
    
#以下未使用
    
class NippoCreateFormView(FormView):
    template_name = "nippo/nippo-form.html"
    form_class = NippoFormClass
    success_url = reverse_lazy("nippo-list")
    
    def form_valid(self, form):
        data = form.cleaned_data
        obj = NippoModel(**data)
        obj.save()
        return super().form_valid(form)

def nippoListView(request):
    template_name = "nippo/nippo-list.html"
    ctx = {}
    qs = NippoModel.objects.all()
    ctx["object_list"] = qs
    ctx["something"] = "1"
    return render(request, template_name, ctx)

def nippoDetailView(request, pk):
    template_name = "nippo/nippo-detail.html"
    ctx = {}
    q =  get_object_or_404(NippoModel, pk=pk)
    ctx["object"] = q
    return render(request, template_name, ctx)

def nippoCreateView(request):
    template_name = "nippo/nippo-form.html"
    form = NippoFormClass(request.POST or None)
    ctx = {}
    ctx["form"] = form
    if form.is_valid():
        title = form.cleaned_data["title"]
        content = form.cleaned_data["content"]
        obj = NippoModel(title=title, content=content)
        obj.save()
        return redirect("nippo-list")
    return render(request, template_name, ctx)

def nippoUpdateFormView(request, pk):
    template_name = "nippo/nippo-form.html"
    obj =  get_object_or_404(NippoModel, pk=pk)
    initial_values = {"title": obj.title, "content":obj.content}
    form = NippoFormClass(request.POST or initial_values)
    ctx = {"form": form}
    ctx["object"] = obj
    if form.is_valid():
        title = form.cleaned_data["title"]
        content = form.cleaned_data["content"]
        obj.title = title
        obj.content = content
        obj.save()
        if request.POST:
            return redirect("nippo-list")
    return render(request, template_name, ctx)

def nippoDeleteView(request,pk):
    template_name = "nippo/nippo-delete.html"
    obj = get_object_or_404(NippoModel, pk=pk)
    ctx = {"object": obj}
    if request.POST:
        obj.delete()
        return redirect("nippo-list")
    return render(request, template_name, ctx)
