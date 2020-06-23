from django.shortcuts import render, redirect
from .models import *
from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView, ListView, CreateView
from django.contrib.auth.models import User
from .forms import ContactoForm
from django.core.mail import send_mail
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse
from random import shuffle




class Inicio(SuccessMessageMixin, FormView):
    form_class = ContactoForm
    template_name = 'index.html'
    success_url = reverse_lazy('inicio')
    success_message = "Tu mensaje ha sido enviado exitosamente. Gracias por contactarnos."
    

    def form_valid(self, form):
        contact_name = form.cleaned_data['contact_name']
        contact_email = form.cleaned_data['contact_email']
        subject = form.cleaned_data['subject']
        message = "{0} tienes un nuevo mensaje:\n\n{1}".format(contact_name, form.cleaned_data['message'])
        send_mail(subject, message, contact_email, ['karen_t195@hotmail.com'], fail_silently = False)
        return super(Inicio, self).form_valid(form)

   
    def get_context_data(self, **kwargs):
        context = super(Inicio, self).get_context_data(**kwargs)
        context['nos'] = Nosotros.objects.all()
        context['proyectos'] = Proyecto.objects.all()
        context['prensa'] = Noticia.objects.all()
        return context



class AboutUs(TemplateView):
    model = Nosotros
    template_name = 'aplicacion/nosotros.html'   
    context_object_name = 'nos'
    queryset = Nosotros.objects.all() 

   
    def get_context_data(self, **kwargs):
        context = super(Nosotros, self).get_context_data(**kwargs)
        context['proyectos'] = Proyecto.objects.all()
        return context


    
class Programa(ListView):
    model = Proyecto
    template_name = 'aplicacion/proyecto.html'
    context_object_name = 'proyectos'
    queryset = Proyecto.objects.all()

                
    def get_context_data(self, **kwargs):
        context=super(Programa, self).get_context_data(**kwargs)
        parametro = self.kwargs.get('id', None)
        context['programaId']=Proyecto.objects.filter(id=parametro)
        return context


class Resources(ListView):
    paginate_by = 8
    model = Recurso
    template_name = 'aplicacion/recursos.html'
    context_object_name= 'res' 
    queryset = Recurso.objects.all()

    def get_context_data(self, **kwargs):
        context = super(Resources, self).get_context_data(**kwargs)
        context['proyectos'] = Proyecto.objects.all()
        return context

    def year_archive(request, nombreRecurso):
        a_list = Recurso.objects.filter(pub_date__year=nombreRecurso)
        context = {'year': nombreRecurso, 'article_list': a_list}
        return render(request, 'aplicacion/recursos.html', context)
    
    """def Buscar(request):
                                if request.GET["dow"]:
                                    nombreRecurso = request.GET["dow"]
                                    articulo = Recurso.objects.filter(nombre_icontains=nombreRecurso)
                                    return render(request, "aplicacion/recursos.html",{"articulo": articulo, "query":nombreRecurso})
                                else: 
                                    mensaje = "No has introducido nada"
                                return HttpResponse(mensaje)
            """

    

class Partners(ListView):
    model = Colaborador
    template_name = 'aplicacion/colaboradores.html'

    def get_context_data(self, **kwargs):
        context = super(Partners, self).get_context_data(**kwargs)
        context['proyectos'] = Proyecto.objects.all()
        lista = list(Colaborador.objects.all())
        shuffle(lista)
        context['colaboradores'] = lista
        return context



class Prensa(ListView):
    paginate_by = 3
    model = Noticia
    template_name = 'aplicacion/noticias.html'
    context_object_name = 'prensa'
    queryset = Noticia.objects.all()

    def get_context_data(self, **kwargs):
        context = super(Prensa, self).get_context_data(**kwargs)
        context['proyectos'] = Proyecto.objects.all()
        return context

    
        

class Contacto(SuccessMessageMixin, FormView):
    form_class = ContactoForm
    success_url = reverse_lazy('aplicacion:contacto')
    template_name = 'aplicacion/contacto.html'
    success_message = "Tu mensaje fue enviado exitosamente. Gracias por contactarnos."
    
    def form_valid(self, form):
        contact_name = form.cleaned_data['contact_name']
        contact_email = form.cleaned_data['contact_email']
        subject = form.cleaned_data['subject']
        message = "{0} tienes un nuevo mensaje:\n\n{1}".format(contact_name, form.cleaned_data['message'])
        send_mail(subject, message, contact_email, ['karen_t195@hotmail.com'], fail_silently = False)
        return super(Contacto, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(Contacto, self).get_context_data(**kwargs)
        context['proyectos'] = Proyecto.objects.all()
        return context



     
    