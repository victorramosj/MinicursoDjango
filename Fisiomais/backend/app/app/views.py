from django.shortcuts import render
import datetime

def home(request):
    # Obtenha o ano atual
    current_year = datetime.datetime.now().year
    
    # Passe o ano atual no contexto
    context = {
        'current_year': current_year,
    }
    return render(request, 'home.html', context)

def sobrenos(request):
    
    return render(request, 'sobrenos.html')

def especialidades_view (request):
    especialidades = [
        {
            "title": "Pilates",
            "description": "O Pilates é uma prática que promove a consciência corporal, melhora a postura e fortalece os músculos através de exercícios personalizados que combinam respiração e movimentos precisos.",
        },
        {
            "title": "Reabilitação Física",
            "description": "Programas focados na recuperação funcional pós-lesões, cirurgias e problemas ortopédicos. Trabalhamos para restaurar a mobilidade, reduzir dores e melhorar sua qualidade de vida.",
        },
        {
            "title": "Massoterapia",
            "description": "Massagens terapêuticas que aliviam dores musculares, reduzem o estresse e proporcionam relaxamento profundo para um melhor bem-estar físico e mental.",
        },
        {
            "title": "Acupuntura",
            "description": "Terapia milenar que utiliza estímulos em pontos específicos do corpo para aliviar dores, equilibrar o fluxo energético e promover o bem-estar geral.",
        },
        {
            "title": "Reeducação Postural Global",
            "description": "Método focado na correção postural através de técnicas globais para aliviar dores crônicas, melhorar a mobilidade e prevenir lesões.",
        },
        {
            "title": "Hidroterapia",
            "description": "Terapias aquáticas realizadas em piscina, ideais para recuperação de mobilidade, fortalecimento muscular e alívio de dores.",
        },
    ]
    return render(request, 'especialidades.html', {"especialidades": especialidades})
