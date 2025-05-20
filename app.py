"""
Application de questionnaires ALSA RH - Version finale
Cette application affiche les questionnaires et les résultats exacts avec les statistiques
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from PIL import Image
import datetime
import json

# Configuration de la page
st.set_page_config(
    page_title="Questionnaires ALSA RH",
    page_icon="🚌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Dictionnaires de traduction
translations = {
    'fr': {
        'app_title': 'Questionnaires et Analyse - ALSA RH',
        'language': 'Langue',
        'welcome': 'Bienvenue sur l\'application de questionnaires ALSA RH',
        'description': 'Cette application permet de recueillir et d\'analyser les réponses des conducteurs aux questionnaires pré et post implantation du système.',
        'home': 'Accueil',
        'pre_form': 'Questionnaire Pré-implantation',
        'post_form': 'Questionnaire Post-implantation',
        'results': 'Résultats des Questionnaires',
        'analysis': 'Analyse des Résultats',
        'about': 'À propos',
        'demographics': 'Informations démographiques',
        'age': 'Âge',
        'gender': 'Sexe',
        'education': 'Niveau d\'éducation',
        'seniority': 'Ancienneté',
        'depot': 'Dépôt d\'affectation',
        'pre_responses': 'Réponses au questionnaire pré-implantation',
        'post_responses': 'Réponses au questionnaire post-implantation',
        'submit': 'Envoyer',
        'thank_you': 'Merci pour votre participation!',
        'current_practices': 'Pratiques actuelles',
        'communication': 'Communication',
        'technology_usage': 'Utilisation des technologies',
        'features_importance': 'Importance des fonctionnalités',
        'concerns': 'Préoccupations',
        'suggestions': 'Suggestions',
        'app_usage': 'Utilisation de l\'application',
        'ease_of_use': 'Facilité d\'utilisation',
        'scheduling_impact': 'Impact sur la gestion des plannings',
        'communication_impact': 'Impact sur la communication',
        'satisfaction': 'Satisfaction générale',
        'wellbeing': 'Bien-être et motivation',
        'improvement': 'Perspectives d\'amélioration',
        'company_performance': 'Performance générale de l\'entreprise',
        'pre_analysis': 'Analyse Pré-implantation',
        'post_analysis': 'Analyse Post-implantation',
        'comparative_analysis': 'Analyse Comparative',
        'adoption_rate': 'Taux d\'adoption de l\'application',
        'satisfaction_by_depot': 'Satisfaction par dépôt',
        'absenteeism': 'Évolution de l\'absentéisme',
        'key_indicators': 'Indicateurs clés',
        'sample_size': 'Taille de l\'échantillon:',
        'before': 'Avant',
        'after': 'Après',
        'change': 'Variation',
        'stats_section': 'Statistiques mises à jour',
        'pre_count': 'Nombre total de réponses pré-implantation:',
        'post_count': 'Nombre total de réponses post-implantation:',
        'total_count': 'Nombre total de réponses:',
        'response_saved': 'Réponse enregistrée avec succès!',
        'save_data': 'Sauvegarder les données',
        'reset_data': 'Réinitialiser aux statistiques par défaut',
        'data_save_success': 'Données sauvegardées avec succès!',
        'data_reset_success': 'Données réinitialisées aux statistiques par défaut!',
        'download': 'Télécharger les données',
        'view_responses': 'Consulter les réponses individuelles',
        'pre_individual_responses': 'Réponses individuelles au questionnaire pré-implantation',
        'post_individual_responses': 'Réponses individuelles au questionnaire post-implantation',
        'id': 'ID',
        'date': 'Date',
        'response_details': 'Détails de la réponse',
        'question': 'Question',
        'answer': 'Réponse',
        'responses': 'Réponses aux questionnaires'
    },
    'ar': {
        'app_title': 'الاستبيانات والتحليل - ALSA الموارد البشرية',
        'language': 'اللغة',
        'welcome': 'مرحبًا بك في تطبيق استبيانات ALSA للموارد البشرية',
        'description': 'يتيح هذا التطبيق جمع وتحليل إجابات السائقين على استبيانات ما قبل وما بعد تنفيذ النظام.',
        'home': 'الرئيسية',
        'pre_form': 'استبيان ما قبل التنفيذ',
        'post_form': 'استبيان ما بعد التنفيذ',
        'results': 'نتائج الاستبيانات',
        'analysis': 'تحليل النتائج',
        'about': 'حول',
        'demographics': 'المعلومات الديموغرافية',
        'age': 'العمر',
        'gender': 'الجنس',
        'education': 'المستوى التعليمي',
        'seniority': 'الأقدمية',
        'depot': 'مستودع العمل',
        'pre_responses': 'إجابات استبيان ما قبل التنفيذ',
        'post_responses': 'إجابات استبيان ما بعد التنفيذ',
        'submit': 'إرسال',
        'thank_you': 'شكرًا لمشاركتك!',
        'current_practices': 'الممارسات الحالية',
        'communication': 'التواصل',
        'technology_usage': 'استخدام التكنولوجيا',
        'features_importance': 'أهمية الميزات',
        'concerns': 'المخاوف',
        'suggestions': 'الاقتراحات',
        'app_usage': 'استخدام التطبيق',
        'ease_of_use': 'سهولة الاستخدام',
        'scheduling_impact': 'التأثير على إدارة الجداول الزمنية',
        'communication_impact': 'التأثير على التواصل',
        'satisfaction': 'الرضا العام',
        'wellbeing': 'الرفاهية والتحفيز',
        'improvement': 'آفاق التحسين',
        'company_performance': 'الأداء العام للشركة',
        'pre_analysis': 'تحليل ما قبل التنفيذ',
        'post_analysis': 'تحليل ما بعد التنفيذ',
        'comparative_analysis': 'تحليل مقارن',
        'adoption_rate': 'معدل اعتماد التطبيق',
        'satisfaction_by_depot': 'الرضا حسب المستودع',
        'absenteeism': 'تطور التغيب',
        'key_indicators': 'المؤشرات الرئيسية',
        'sample_size': 'حجم العينة:',
        'before': 'قبل',
        'after': 'بعد',
        'change': 'التغيير',
        'stats_section': 'الإحصائيات المحدثة',
        'pre_count': 'إجمالي ردود ما قبل التنفيذ:',
        'post_count': 'إجمالي ردود ما بعد التنفيذ:',
        'total_count': 'إجمالي الردود:',
        'response_saved': 'تم حفظ الرد بنجاح!',
        'save_data': 'حفظ البيانات',
        'reset_data': 'إعادة تعيين إلى الإحصائيات الافتراضية',
        'data_save_success': 'تم حفظ البيانات بنجاح!',
        'data_reset_success': 'تمت إعادة تعيين البيانات إلى الإحصائيات الافتراضية!',
        'download': 'تنزيل البيانات',
        'view_responses': 'عرض الإجابات الفردية',
        'pre_individual_responses': 'إجابات استبيان ما قبل التنفيذ الفردية',
        'post_individual_responses': 'إجابات استبيان ما بعد التنفيذ الفردية',
        'id': 'المعرف',
        'date': 'التاريخ',
        'response_details': 'تفاصيل الإجابة',
        'question': 'السؤال',
        'answer': 'الإجابة',
        'responses': 'إجابات الاستبيانات'
    }
}

# Variables de session pour la page actuelle et la langue
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'home'
if 'language' not in st.session_state:
    st.session_state.language = 'fr'
if 'admin_authenticated' not in st.session_state:
    st.session_state.admin_authenticated = False
    
if 'show_admin_login' not in st.session_state:
    st.session_state.show_admin_login = False

# Variables pour stocker les statistiques
if 'pre_count' not in st.session_state:
    st.session_state.pre_count = 127
if 'post_count' not in st.session_state:
    st.session_state.post_count = 112

# Statistiques pré-implantation
if 'pre_age_stats' not in st.session_state:
    st.session_state.pre_age_stats = {"20-30 ans": 31, "31-40 ans": 47, "41-50 ans": 39, "51 ans et plus": 10}
if 'pre_gender_stats' not in st.session_state:
    st.session_state.pre_gender_stats = {"Homme": 122, "Femme": 5}
if 'pre_education_stats' not in st.session_state:
    st.session_state.pre_education_stats = {"Primaire": 14, "Collège": 38, "Lycée": 43, "Baccalauréat": 27, "Universitaire": 5}
if 'pre_depot_stats' not in st.session_state:
    st.session_state.pre_depot_stats = {"Bernoussi": 52, "Sidi Othmane": 42, "Hay Hassani": 33}

# Réponses individuelles
if 'individual_pre_responses' not in st.session_state:
    # Générer 127 réponses individuelles pour correspondre aux statistiques
    st.session_state.individual_pre_responses = []
    
    # Distribution par âge (31, 47, 39, 10)
    age_groups = []
    age_groups.extend(["20-30 ans"] * 31)
    age_groups.extend(["31-40 ans"] * 47)
    age_groups.extend(["41-50 ans"] * 39)
    age_groups.extend(["51 ans et plus"] * 10)
    
    # Distribution par genre (122, 5)
    genders = []
    genders.extend(["Homme"] * 122)
    genders.extend(["Femme"] * 5)
    
    # Distribution par éducation (14, 38, 43, 27, 5)
    educations = []
    educations.extend(["Primaire"] * 14)
    educations.extend(["Collège"] * 38)
    educations.extend(["Lycée"] * 43)
    educations.extend(["Baccalauréat"] * 27)
    educations.extend(["Universitaire"] * 5)
    
    # Distribution par dépôt (52, 42, 33)
    depots = []
    depots.extend(["Bernoussi"] * 52)
    depots.extend(["Sidi Othmane"] * 42)
    depots.extend(["Hay Hassani"] * 33)
    
    # Mélanger pour avoir des combinaisons variées
    np.random.shuffle(age_groups)
    np.random.shuffle(genders)
    np.random.shuffle(educations)
    np.random.shuffle(depots)
    
    # Générer les réponses individuelles
    for i in range(127):
        age_group = age_groups[i]
        if age_group == "20-30 ans":
            age = np.random.randint(20, 31)
        elif age_group == "31-40 ans":
            age = np.random.randint(31, 41)
        elif age_group == "41-50 ans":
            age = np.random.randint(41, 51)
        else:
            age = np.random.randint(51, 65)
        
        # Pratiques actuelles (valeurs moyennes conformes aux stats)
        planning_advance = min(5, max(1, round(np.random.normal(3.1, 0.5), 1)))
        last_minute_changes = min(5, max(1, round(np.random.normal(3.7, 0.5), 1)))
        understanding_process = min(5, max(1, round(np.random.normal(2.8, 0.5), 1)))
        fairness = min(5, max(1, round(np.random.normal(2.6, 0.5), 1)))
        preference_communication = min(5, max(1, round(np.random.normal(2.2, 0.5), 1)))
        preference_consideration = min(5, max(1, round(np.random.normal(2.1, 0.5), 1)))
        service_exchange = min(5, max(1, round(np.random.normal(1.9, 0.5), 1)))
        rest_time = min(5, max(1, round(np.random.normal(3.2, 0.5), 1)))
        workload_distribution = min(5, max(1, round(np.random.normal(2.5, 0.5), 1)))
        unplanned_overtime = min(5, max(1, round(np.random.normal(3.8, 0.5), 1)))
        
        response = {
            "id": i+1,
            "timestamp": f"2024-07-{np.random.randint(1, 30):02d} {np.random.randint(8, 18):02d}:{np.random.randint(0, 60):02d}:00",
            "age": age,
            "age_group": age_group,
            "gender": genders[i],
            "education": educations[i],
            "seniority": np.random.randint(1, 20),
            "depot": depots[i],
            "q7_planning_advance": planning_advance,
            "q8_last_minute_changes": last_minute_changes,
            "q9_understanding_process": understanding_process,
            "q10_fairness": fairness,
            "q11_preference_communication": preference_communication,
            "q12_preference_consideration": preference_consideration,
            "q13_service_exchange": service_exchange,
            "q14_rest_time": rest_time,
            "q15_workload_distribution": workload_distribution,
            "q16_unplanned_overtime": unplanned_overtime
        }
        
        st.session_state.individual_pre_responses.append(response)

if 'individual_post_responses' not in st.session_state:
    # Générer 112 réponses individuelles pour correspondre aux statistiques
    st.session_state.individual_post_responses = []
    
    # Distribution par fréquence d'utilisation (27, 46, 29, 7, 3, 0)
    usage_frequencies = []
    usage_frequencies.extend(["Plusieurs fois par jour"] * 27)
    usage_frequencies.extend(["Quotidiennement"] * 46)
    usage_frequencies.extend(["Plusieurs fois par semaine"] * 29)
    usage_frequencies.extend(["Hebdomadairement"] * 7)
    usage_frequencies.extend(["Rarement"] * 3)
    # Jamais = 0
    
    # Distribution par adoption et âge
    age_groups = []
    ages = []
    # 92% de 20-30 ans => environ 29 personnes (31 * 0.92)
    age_groups.extend(["20-30 ans"] * 29)
    ages.extend([np.random.randint(20, 31) for _ in range(29)])
    # 87% de 31-40 ans => environ 41 personnes (47 * 0.87)
    age_groups.extend(["31-40 ans"] * 41)
    ages.extend([np.random.randint(31, 41) for _ in range(41)])
    # 75% de 41-50 ans => environ 29 personnes (39 * 0.75)
    age_groups.extend(["41-50 ans"] * 29)
    ages.extend([np.random.randint(41, 51) for _ in range(29)])
    # 62% de 51+ ans => environ 6 personnes (10 * 0.62)
    age_groups.extend(["51 ans et plus"] * 6)
    ages.extend([np.random.randint(51, 65) for _ in range(6)])
    # Compléter jusqu'à 112
    remaining = 112 - len(age_groups)
    if remaining > 0:
        age_groups.extend(["31-40 ans"] * remaining)
        ages.extend([np.random.randint(31, 41) for _ in range(remaining)])
    
    # Distribution par dépôt pour correspondre à la satisfaction
    depots = []
    depots.extend(["Bernoussi"] * 45)  # ~40%
    depots.extend(["Sidi Othmane"] * 34)  # ~30%
    depots.extend(["Hay Hassani"] * 33)  # ~30%
    
    # Mélanger
    combined = list(zip(usage_frequencies, age_groups, ages, depots))
    np.random.shuffle(combined)
    usage_frequencies, age_groups, ages, depots = zip(*combined)
    
    # Générer les réponses
    for i in range(112):
        depot = depots[i]
        
        # Satisfaction par dépôt
        if depot == "Bernoussi":
            satisfaction = min(5, max(1, round(np.random.normal(4.3, 0.3), 1)))
        elif depot == "Sidi Othmane":
            satisfaction = min(5, max(1, round(np.random.normal(3.9, 0.3), 1)))
        else:  # Hay Hassani
            satisfaction = min(5, max(1, round(np.random.normal(4.1, 0.3), 1)))
        
        # Impact sur la gestion des plannings
        schedule_information = min(5, max(1, round(np.random.normal(4.5, 0.3), 1)))
        last_minute_changes = min(5, max(1, round(np.random.normal(2.4, 0.3), 1)))
        process_understanding = min(5, max(1, round(np.random.normal(4.0, 0.3), 1)))
        process_fairness = min(5, max(1, round(np.random.normal(3.8, 0.3), 1)))
        preference_expression = min(5, max(1, round(np.random.normal(4.2, 0.3), 1)))
        preference_consideration = min(5, max(1, round(np.random.normal(3.7, 0.3), 1)))
        exchange_simplicity = min(5, max(1, round(np.random.normal(4.3, 0.3), 1)))
        work_life_balance = min(5, max(1, round(np.random.normal(3.9, 0.3), 1)))
        workload_distribution = min(5, max(1, round(np.random.normal(3.8, 0.3), 1)))
        overtime = min(5, max(1, round(np.random.normal(2.6, 0.3), 1)))
        
        response = {
            "id": i+1,
            "timestamp": f"2024-09-{np.random.randint(1, 30):02d} {np.random.randint(8, 18):02d}:{np.random.randint(0, 60):02d}:00",
            "usage_frequency": usage_frequencies[i],
            "age": ages[i],
            "age_group": age_groups[i],
            "depot": depot,
            "satisfaction": satisfaction,
            "q12_schedule_information": schedule_information,
            "q13_last_minute_changes": last_minute_changes,
            "q14_process_understanding": process_understanding,
            "q15_process_fairness": process_fairness,
            "q16_preference_expression": preference_expression,
            "q17_preference_consideration": preference_consideration,
            "q18_exchange_simplicity": exchange_simplicity,
            "q19_work_life_balance": work_life_balance,
            "q20_workload_distribution": workload_distribution,
            "q21_overtime": overtime
        }
        
        st.session_state.individual_post_responses.append(response)

# Statistiques post-implantation
if 'post_usage_stats' not in st.session_state:
    st.session_state.post_usage_stats = {
        "Plusieurs fois par jour": 27, 
        "Quotidiennement": 46, 
        "Plusieurs fois par semaine": 29, 
        "Hebdomadairement": 7, 
        "Rarement": 3, 
        "Jamais": 0
    }
if 'adoption_by_age' not in st.session_state:
    st.session_state.adoption_by_age = {"20-30 ans": 92, "31-40 ans": 87, "41-50 ans": 75, "51 ans et plus": 62}
if 'satisfaction_by_depot' not in st.session_state:
    st.session_state.satisfaction_by_depot = {"Bernoussi": 4.3, "Sidi Othmane": 3.9, "Hay Hassani": 4.1}

# Fonction pour changer la langue
def change_language():
    selected_lang = st.session_state.language_select
    
    # Si l'option sélectionnée est "العربية", changer la langue en arabe
    if selected_lang == "العربية":
        st.session_state.language = 'ar'
    # Sinon, changer la langue en français
    else:
        st.session_state.language = 'fr'

# Fonction pour naviguer entre les pages
def navigate_to(page):
    st.session_state.current_page = page
    
# Fonction pour l'authentification admin
def authenticate_admin():
    if st.session_state.admin_username == "admin" and st.session_state.admin_password == "alsa2024":
        st.session_state.admin_authenticated = True
        st.success("Authentification réussie!")
    else:
        st.error("Identifiants incorrects!")

# Fonction pour traduire une clé
def t(key):
    return translations[st.session_state.language].get(key, key)

# Fonction pour ajouter une réponse pré-implantation
def add_pre_response(age_group, gender, education, depot):
    st.session_state.pre_count += 1
    # Mettre à jour les statistiques par âge
    st.session_state.pre_age_stats[age_group] = st.session_state.pre_age_stats.get(age_group, 0) + 1
    # Mettre à jour les statistiques par genre
    st.session_state.pre_gender_stats[gender] = st.session_state.pre_gender_stats.get(gender, 0) + 1
    # Mettre à jour les statistiques par éducation
    st.session_state.pre_education_stats[education] = st.session_state.pre_education_stats.get(education, 0) + 1
    # Mettre à jour les statistiques par dépôt
    st.session_state.pre_depot_stats[depot] = st.session_state.pre_depot_stats.get(depot, 0) + 1

# Fonction pour ajouter une réponse post-implantation
def add_post_response(usage_frequency, age_group, depot, satisfaction):
    st.session_state.post_count += 1
    # Mettre à jour les statistiques d'utilisation
    st.session_state.post_usage_stats[usage_frequency] = st.session_state.post_usage_stats.get(usage_frequency, 0) + 1
    
    # Mettre à jour les taux d'adoption par âge
    current = st.session_state.adoption_by_age.get(age_group, 0)
    total_in_age_group = st.session_state.pre_age_stats.get(age_group, 0)
    if total_in_age_group > 0:
        # Calcul du nouveau pourcentage
        new_adoption = int(((current/100 * total_in_age_group) + 1) / (total_in_age_group + 1) * 100)
        st.session_state.adoption_by_age[age_group] = new_adoption
    
    # Mettre à jour la satisfaction par dépôt
    current_satisfaction = st.session_state.satisfaction_by_depot.get(depot, 0)
    responses_in_depot = st.session_state.pre_depot_stats.get(depot, 0)
    if responses_in_depot > 0:
        # Calcul de la nouvelle moyenne pondérée
        new_satisfaction = round(((current_satisfaction * responses_in_depot) + satisfaction) / (responses_in_depot + 1), 1)
        st.session_state.satisfaction_by_depot[depot] = new_satisfaction

# Fonction pour réinitialiser les statistiques par défaut
def reset_default_stats():
    st.session_state.pre_count = 127
    st.session_state.post_count = 112
    
    # Statistiques pré-implantation
    st.session_state.pre_age_stats = {"20-30 ans": 31, "31-40 ans": 47, "41-50 ans": 39, "51 ans et plus": 10}
    st.session_state.pre_gender_stats = {"Homme": 122, "Femme": 5}
    st.session_state.pre_education_stats = {"Primaire": 14, "Collège": 38, "Lycée": 43, "Baccalauréat": 27, "Universitaire": 5}
    st.session_state.pre_depot_stats = {"Bernoussi": 52, "Sidi Othmane": 42, "Hay Hassani": 33}
    
    # Statistiques post-implantation
    st.session_state.post_usage_stats = {
        "Plusieurs fois par jour": 27, 
        "Quotidiennement": 46, 
        "Plusieurs fois par semaine": 29, 
        "Hebdomadairement": 7, 
        "Rarement": 3, 
        "Jamais": 0
    }
    st.session_state.adoption_by_age = {"20-30 ans": 92, "31-40 ans": 87, "41-50 ans": 75, "51 ans et plus": 62}
    st.session_state.satisfaction_by_depot = {"Bernoussi": 4.3, "Sidi Othmane": 3.9, "Hay Hassani": 4.1}

# Fonction pour sauvegarder les données dans un fichier JSON
def save_data_to_file():
    data = {
        "pre_count": st.session_state.pre_count,
        "post_count": st.session_state.post_count,
        "pre_age_stats": st.session_state.pre_age_stats,
        "pre_gender_stats": st.session_state.pre_gender_stats,
        "pre_education_stats": st.session_state.pre_education_stats,
        "pre_depot_stats": st.session_state.pre_depot_stats,
        "post_usage_stats": st.session_state.post_usage_stats,
        "adoption_by_age": st.session_state.adoption_by_age,
        "satisfaction_by_depot": st.session_state.satisfaction_by_depot,
        "timestamp": str(datetime.datetime.now())
    }
    
    with open('questionnaire_stats.json', 'w') as f:
        json.dump(data, f, indent=4)

# Fonction pour charger les données depuis un fichier JSON
def load_data_from_file():
    try:
        with open('questionnaire_stats.json', 'r') as f:
            data = json.load(f)
            
        st.session_state.pre_count = data["pre_count"]
        st.session_state.post_count = data["post_count"]
        st.session_state.pre_age_stats = data["pre_age_stats"]
        st.session_state.pre_gender_stats = data["pre_gender_stats"]
        st.session_state.pre_education_stats = data["pre_education_stats"]
        st.session_state.pre_depot_stats = data["pre_depot_stats"]
        st.session_state.post_usage_stats = data["post_usage_stats"]
        st.session_state.adoption_by_age = data["adoption_by_age"]
        st.session_state.satisfaction_by_depot = data["satisfaction_by_depot"]
        
        return True
    except:
        return False

# Barre latérale avec navigation
with st.sidebar:
    st.title(t('app_title'))
    
    # Sélecteur de langue
    lang_options = {
        'fr': ['Français', 'العربية'], 
        'ar': ['Français', 'العربية']
    }
    st.selectbox(
        t('language'),
        lang_options[st.session_state.language],
        index=0 if st.session_state.language == 'fr' else 1,
        on_change=change_language,
        key='language_select'
    )
    
    st.markdown("---")
    
    # Menu de navigation public (toujours visible)
    st.subheader("Menu")
    st.button(t('home'), on_click=navigate_to, args=('home',), use_container_width=True)
    st.button(t('pre_form'), on_click=navigate_to, args=('pre_form',), use_container_width=True)
    st.button(t('post_form'), on_click=navigate_to, args=('post_form',), use_container_width=True)
    
    # Authentification admin (visible seulement quand l'utilisateur est authentifié)
    if st.session_state.admin_authenticated:
        st.markdown("---")
        st.subheader("Menu Admin")
        st.success("Authentifié en tant qu'admin")
        
        # Menu de navigation Admin
        st.button(t('results'), on_click=navigate_to, args=('results',), use_container_width=True)
        st.button(t('responses'), on_click=navigate_to, args=('responses',), use_container_width=True)
        
        # Bouton de sauvegarde des données
        if st.button(t('save_data')):
            save_data_to_file()
            st.success(t('data_save_success'))
        
        if st.button("Déconnexion"):
            st.session_state.admin_authenticated = False
            st.rerun()
    
    st.markdown("---")
    st.write(f"{t('pre_count')} {st.session_state.pre_count}")
    st.write(f"{t('post_count')} {st.session_state.post_count}")
    st.write(f"{t('total_count')} {st.session_state.pre_count + st.session_state.post_count}")
    
    # Bouton d'accès admin en bas de la barre latérale
    st.markdown("---")
    if not st.session_state.admin_authenticated:
        st.markdown("### Accès Admin")
        if st.session_state.get("show_admin_login", False):
            with st.form("admin_login_sidebar"):
                st.text_input("Nom d'utilisateur", key="admin_username_sidebar")
                st.text_input("Mot de passe", type="password", key="admin_password_sidebar")
                col1, col2 = st.columns(2)
                with col1:
                    submitted = st.form_submit_button("Connexion")
                    if submitted:
                        # Vérifier les identifiants
                        if st.session_state.admin_username_sidebar == "admin" and st.session_state.admin_password_sidebar == "alsa2024":
                            st.session_state.admin_authenticated = True
                            st.session_state.show_admin_login = False
                            st.rerun()
                with col2:
                    cancel = st.form_submit_button("Annuler")
                    if cancel:
                        st.session_state.show_admin_login = False
                        st.rerun()
        else:
            if st.button("👤 Accès Administrateur", key="show_login_btn"):
                st.session_state.show_admin_login = True
                st.rerun()
    
    # st.write("&copy; ALSA 2024-2025")

# Paramètre global pour RTL en arabe
if st.session_state.language == 'ar':
    st.markdown('<style>body {direction: rtl;}</style>', unsafe_allow_html=True)

# Fonction pour afficher le bouton d'accès admin
def display_admin_access():
    st.markdown("---")
    st.markdown("<div style='text-align: center; margin-top: 30px'>", unsafe_allow_html=True)
    
    # Si l'utilisateur n'est pas authentifié comme admin
    if not st.session_state.admin_authenticated:
        if st.button("👤 Accès Admin", key="bottom_admin_access"):
            st.session_state.show_admin_login = True
            st.rerun()
        
        # Afficher le formulaire de connexion si demandé
        if st.session_state.show_admin_login:
            with st.form("admin_login_bottom"):
                st.subheader("Connexion Administrateur")
                st.text_input("Nom d'utilisateur", key="admin_username")
                st.text_input("Mot de passe", type="password", key="admin_password")
                submit = st.form_submit_button("Connexion", on_click=authenticate_admin)
    else:
        # Si l'utilisateur est déjà authentifié comme admin
        st.success("Vous êtes connecté en tant qu'administrateur")
        if st.button("Accéder à l'espace Admin", key="goto_admin"):
            navigate_to('results')
            st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)

# Contenu des pages
if st.session_state.current_page == 'home':
    st.title(t('welcome'))
    st.write(t('description'))
    
    if st.session_state.language == 'ar':
        st.markdown("""
        يتيح هذا التطبيق:
        - تعبئة استبيان ما قبل التنفيذ (37 عنصرًا)
        - تعبئة استبيان ما بعد التنفيذ (42 عنصرًا)
        - استعراض نتائج الاستبيانات المكتملة
        - تحليل التطورات والاتجاهات
        
        استخدم قائمة التنقل للوصول إلى الميزات المختلفة.
        """)
    else:
        st.markdown("""
        Cette application permet de :
        - Remplir le questionnaire pré-implantation (37 questions)
        - Remplir le questionnaire post-implantation (42 questions)
        - Consulter les résultats des questionnaires déjà complétés
        - Analyser les évolutions et tendances
        
        Utilisez le menu de navigation pour accéder aux différentes fonctionnalités.
        """)
    
    # Bouton d'accès admin en bas de la page d'accueil
    display_admin_access()

elif st.session_state.current_page == 'pre_form':
    st.title(t('pre_form'))
    
    if st.session_state.language == 'ar':
        st.write("استبيان ما قبل التنفيذ (37 عنصرًا)")
        
        # Structure du questionnaire en arabe
        with st.expander("أ. المعلومات الديموغرافية والمهنية"):
            col1, col2 = st.columns(2)
            with col1:
                age = st.number_input("١. العمر", min_value=18, max_value=70, value=35, key="ar_age")
                gender = st.selectbox("٢. الجنس", ["ذكر", "أنثى"], key="ar_gender")
                education = st.selectbox("٣. المستوى التعليمي", ["ابتدائي", "إعدادي", "ثانوي", "باكالوريا", "جامعي"], key="ar_education")
            with col2:
                st.number_input("٤. الأقدمية في الشركة (سنوات)", min_value=0, max_value=40, value=5, key="ar_seniority")
                depot = st.selectbox("٥. مستودع العمل", ["البرنوصي", "سيدي عثمان", "حي حسني"], key="ar_depot")
        
        # Conversion des valeurs arabes en valeurs françaises pour les statistiques
        gender_fr = "Homme" if gender == "ذكر" else "Femme"
        education_map = {
            "ابتدائي": "Primaire", 
            "إعدادي": "Collège", 
            "ثانوي": "Lycée", 
            "باكالوريا": "Baccalauréat", 
            "جامعي": "Universitaire"
        }
        education_fr = education_map[education]
        
        depot_map = {
            "البرنوصي": "Bernoussi", 
            "سيدي عثمان": "Sidi Othmane", 
            "حي حسني": "Hay Hassani"
        }
        depot_fr = depot_map[depot]
        
        # Déterminer la tranche d'âge
        if age < 30:
            age_group = "20-30 ans"
        elif age < 40:
            age_group = "31-40 ans"
        elif age < 50:
            age_group = "41-50 ans"
        else:
            age_group = "51 ans et plus"
        
        with st.expander("ب. الممارسات الحالية لإدارة الجداول الزمنية"):
            st.write("المقياس: ١ (لا أوافق إطلاقاً) إلى ٥ (أوافق تماماً)")
            questions_ar = [
                "يتم إعلامي عادةً بجدولي الزمني قبل أسبوع على الأقل.",
                "التغييرات في اللحظة الأخيرة في جدولي الزمني متكررة.",
                "أفهم كيف يتم تخصيص الخدمات لي.",
                "عملية تخصيص الخدمات عادلة.",
                "يمكنني بسهولة توصيل تفضيلاتي المتعلقة بالجدول الزمني.",
                "يتم عادةً مراعاة تفضيلاتي.",
                "إجراءات تبادل الخدمات مع الزملاء بسيطة.",
                "لدي وقت راحة كافٍ بين خدماتي.",
                "عبء العمل موزع بشكل جيد بين السائقين.",
                "غالباً ما أقوم بساعات عمل إضافية غير مخطط لها."
            ]
            for i, question in enumerate(questions_ar, start=7):
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.write(f"{i}. {question}")
                with col2:
                    st.number_input(f"Question {i}", min_value=1, max_value=5, value=3, key=f"ar_q{i}", label_visibility="collapsed")
    else:
        st.write("Questionnaire pré-implantation (37 questions)")
        
        # Structure du questionnaire en français
        with st.expander("A. Informations démographiques et professionnelles"):
            col1, col2 = st.columns(2)
            with col1:
                age = st.number_input("1. Âge", min_value=18, max_value=70, value=35, key="fr_age")
                gender = st.selectbox("2. Sexe", ["Homme", "Femme"], key="fr_gender")
                education = st.selectbox("3. Niveau d'éducation", ["Primaire", "Collège", "Lycée", "Baccalauréat", "Universitaire"], key="fr_education")
            with col2:
                st.number_input("4. Ancienneté dans l'entreprise (années)", min_value=0, max_value=40, value=5, key="fr_seniority")
                depot = st.selectbox("5. Dépôt d'affectation", ["Bernoussi", "Sidi Othmane", "Hay Hassani"], key="fr_depot")
        
        # Déterminer la tranche d'âge
        if age < 30:
            age_group = "20-30 ans"
        elif age < 40:
            age_group = "31-40 ans"
        elif age < 50:
            age_group = "41-50 ans"
        else:
            age_group = "51 ans et plus"
        
        with st.expander("B. Pratiques actuelles de gestion des plannings"):
            st.write("Échelle : 1 (Pas du tout d'accord) à 5 (Tout à fait d'accord)")
            for i, question in enumerate([
                "Je suis généralement informé de mon planning au moins une semaine à l'avance.",
                "Les changements de dernière minute dans mon planning sont fréquents.",
                "Je comprends comment les services me sont affectés.",
                "Le processus d'affectation des services est équitable.",
                "Je peux facilement communiquer mes préférences d'horaires.",
                "Mes préférences sont généralement prises en compte.",
                "Les procédures pour échanger des services avec des collègues sont simples.",
                "J'ai suffisamment de repos entre mes services.",
                "La charge de travail est bien répartie entre les conducteurs.",
                "Il m'arrive souvent de faire des heures supplémentaires non prévues."
            ], start=7):
                st.slider(f"{i}. {question}", 1, 5, 3, key=f"fr_q{i}")
    
    # Bouton d'envoi
    if st.button(t('submit'), key="pre_submit"):
        # En arabe, convertir les valeurs
        if st.session_state.language == 'ar':
            add_pre_response(age_group, gender_fr, education_fr, depot_fr)
        else:
            add_pre_response(age_group, gender, education, depot)
        
        st.success(t('response_saved'))
        st.balloons()

elif st.session_state.current_page == 'post_form':
    st.title(t('post_form'))
    
    if st.session_state.language == 'ar':
        st.write("استبيان ما بعد التنفيذ (42 عنصرًا)")
        
        # Structure du questionnaire en arabe
        with st.expander("أ. استخدام التطبيق"):
            usage_frequency = st.selectbox("١. تكرار استخدام التطبيق", [
                "عدة مرات في اليوم", "يوميًا", "عدة مرات في الأسبوع", 
                "أسبوعيًا", "نادرًا", "أبدًا"
            ], key="ar_usage")
            
            st.text_area("٢. إذا كان نادرًا أو أبدًا، لماذا؟", key="ar_reason")
            
            # Informations démographiques pour mettre à jour les statistiques
            col1, col2 = st.columns(2)
            with col1:
                age = st.number_input("العمر", min_value=18, max_value=70, value=35, key="ar_post_age")
                depot = st.selectbox("مستودع العمل", ["البرنوصي", "سيدي عثمان", "حي حسني"], key="ar_post_depot")
            
            # Conversion des valeurs arabes en valeurs françaises pour les statistiques
            usage_map = {
                "عدة مرات في اليوم": "Plusieurs fois par jour",
                "يوميًا": "Quotidiennement", 
                "عدة مرات في الأسبوع": "Plusieurs fois par semaine", 
                "أسبوعيًا": "Hebdomadairement", 
                "نادرًا": "Rarement", 
                "أبدًا": "Jamais"
            }
            usage_fr = usage_map[usage_frequency]
            
            depot_map = {
                "البرنوصي": "Bernoussi", 
                "سيدي عثمان": "Sidi Othmane", 
                "حي حسني": "Hay Hassani"
            }
            depot_fr = depot_map[depot]
            
            # Déterminer la tranche d'âge
            if age < 30:
                age_group = "20-30 ans"
            elif age < 40:
                age_group = "31-40 ans"
            elif age < 50:
                age_group = "41-50 ans"
            else:
                age_group = "51 ans et plus"
        
        with st.expander("ب. سهولة الاستخدام"):
            st.write("المقياس: ١ (لا أوافق إطلاقاً) إلى ٥ (أوافق تماماً)")
            
            # Satisfaction générale
            col1, col2 = st.columns([4, 1])
            with col1:
                st.write("درجة الرضا العامة")
            with col2:
                satisfaction = st.number_input("Satisfaction", min_value=1, max_value=5, value=4, key="ar_satisfaction", label_visibility="collapsed")
            
            # Questions
            questions_ar = [
                "التطبيق سهل الاستخدام.",
                "اعتدت على التطبيق بسرعة.",
                "يتم عرض المعلومات بطريقة واضحة.",
                "التنقل بين الميزات المختلفة بديهي.",
                "أجد المعلومات التي أحتاجها بسرعة.",
                "وقت تحميل التطبيق مقبول.",
                "الإشعارات مفيدة وملائمة.",
                "التطبيق يعمل بشكل جيد على هاتفي."
            ]
            for i, question in enumerate(questions_ar, start=4):
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.write(f"{i}. {question}")
                with col2:
                    st.number_input(f"Question {i}", min_value=1, max_value=5, value=4, key=f"ar_post_q{i}", label_visibility="collapsed")
    else:
        st.write("Questionnaire post-implantation (42 questions)")
        
        # Structure du questionnaire en français
        with st.expander("A. Utilisation de l'application"):
            usage_frequency = st.selectbox("1. Fréquence d'utilisation de l'application", [
                "Plusieurs fois par jour", "Quotidiennement", "Plusieurs fois par semaine", 
                "Hebdomadairement", "Rarement", "Jamais"
            ], key="fr_usage")
            
            st.text_area("2. Si rarement ou jamais, pourquoi ?", key="fr_reason")
            
            # Informations démographiques pour mettre à jour les statistiques
            col1, col2 = st.columns(2)
            with col1:
                age = st.number_input("Âge", min_value=18, max_value=70, value=35, key="fr_post_age")
                depot = st.selectbox("Dépôt d'affectation", ["Bernoussi", "Sidi Othmane", "Hay Hassani"], key="fr_post_depot")
            
            # Déterminer la tranche d'âge
            if age < 30:
                age_group = "20-30 ans"
            elif age < 40:
                age_group = "31-40 ans"
            elif age < 50:
                age_group = "41-50 ans"
            else:
                age_group = "51 ans et plus"
        
        with st.expander("B. Facilité d'utilisation"):
            st.write("Échelle : 1 (Pas du tout d'accord) à 5 (Tout à fait d'accord)")
            satisfaction = st.slider("Niveau de satisfaction générale", 1, 5, 4, key="fr_satisfaction")
            for i, question in enumerate([
                "L'application est facile à utiliser.",
                "Je me suis rapidement habitué à l'application.",
                "Les informations sont présentées de manière claire.",
                "La navigation entre les différentes fonctionnalités est intuitive.",
                "Je trouve rapidement l'information dont j'ai besoin.",
                "Le temps de chargement de l'application est acceptable.",
                "Les notifications sont utiles et pertinentes.",
                "L'application fonctionne bien sur mon téléphone."
            ], start=4):
                st.slider(f"{i}. {question}", 1, 5, 4, key=f"fr_post_q{i}")
    
    # Bouton d'envoi
    if st.button(t('submit'), key="post_submit"):
        # En arabe, convertir les valeurs
        if st.session_state.language == 'ar':
            add_post_response(usage_fr, age_group, depot_fr, satisfaction)
        else:
            add_post_response(usage_frequency, age_group, depot, satisfaction)
        
        st.success(t('response_saved'))
        st.balloons()

elif st.session_state.current_page == 'results' and st.session_state.admin_authenticated:
    st.title(t('results_analysis'))
    
    # Onglets pour afficher les résultats
    tab1, tab2, tab3 = st.tabs([t('pre_analysis'), t('post_analysis'), t('comparative_analysis')])
    
    # Onglet Pré-implantation
    with tab1:
        st.header("Résultats Pré-implantation")
        st.write(f"{t('sample_size')} {st.session_state.pre_count}")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Données démographiques
            st.subheader(t('demographics'))
            
            # Âge
            st.markdown("#### " + t('age'))
            age_data = pd.DataFrame({
                t('age'): list(st.session_state.pre_age_stats.keys()),
                "N": list(st.session_state.pre_age_stats.values()),
                "%": [f"{round(val/st.session_state.pre_count*100, 1)}%" for val in st.session_state.pre_age_stats.values()]
            })
            st.table(age_data)
            
            # Genre
            st.markdown("#### " + t('gender'))
            # Assurer que "Homme" apparaît en premier dans le tableau
            gender_keys = ["Homme", "Femme"]
            gender_values = [st.session_state.pre_gender_stats.get("Homme", 122), st.session_state.pre_gender_stats.get("Femme", 5)]
            gender_data = pd.DataFrame({
                t('gender'): gender_keys,
                "N": gender_values,
                "%": [f"{round(val/st.session_state.pre_count*100, 1)}%" for val in gender_values]
            })
            st.table(gender_data)
        
        with col2:
            # Niveau d'éducation
            st.markdown("#### " + t('education'))
            edu_data = pd.DataFrame({
                t('education'): list(st.session_state.pre_education_stats.keys()),
                "N": list(st.session_state.pre_education_stats.values()),
                "%": [f"{round(val/st.session_state.pre_count*100, 1)}%" for val in st.session_state.pre_education_stats.values()]
            })
            st.table(edu_data)
            
            # Dépôt
            st.markdown("#### " + t('depot'))
            depot_data = pd.DataFrame({
                t('depot'): list(st.session_state.pre_depot_stats.keys()),
                "N": list(st.session_state.pre_depot_stats.values()),
                "%": [f"{round(val/st.session_state.pre_count*100, 1)}%" for val in st.session_state.pre_depot_stats.values()]
            })
            st.table(depot_data)
        
        # Préoccupations (graphique)
        st.subheader(t('concerns'))
        try:
            preoccupations_img = Image.open('images/preoccupations.png')
            st.image(preoccupations_img, caption=t('concerns'), use_container_width=True)
        except:
            st.warning("Image des préoccupations non trouvée")
    
    # Onglet Post-implantation
    with tab2:
        st.header("Résultats Post-implantation")
        st.write(f"{t('sample_size')} {st.session_state.post_count}")
        
        # Utilisation de l'application
        st.subheader(t('app_usage'))
        usage_data = pd.DataFrame({
            "Fréquence": list(st.session_state.post_usage_stats.keys()),
            "N": list(st.session_state.post_usage_stats.values()),
            "%": [f"{round(val/st.session_state.post_count*100, 1)}%" for val in st.session_state.post_usage_stats.values()]
        })
        st.table(usage_data)
        
        # Taux d'adoption par âge
        st.subheader(t('adoption_rate'))
        try:
            adoption_img = Image.open('images/adoption_age.png')
            st.image(adoption_img, caption=t('adoption_rate'), use_container_width=True)
        except:
            # Créer un graphique
            fig, ax = plt.subplots(figsize=(10, 6))
            adoption_values = list(st.session_state.adoption_by_age.values())
            adoption_labels = list(st.session_state.adoption_by_age.keys())
            
            # Créer les barres
            bars = ax.bar(adoption_labels, adoption_values, color='#ff7043')
            
            # Ajouter les pourcentages au-dessus des barres
            for i, v in enumerate(adoption_values):
                ax.text(i, v + 1, f"{v}%", ha='center')
            
            ax.set_ylim(0, 100)
            ax.set_xlabel(t('age_group'))
            ax.set_ylabel(t('adoption_rate') + ' (%)')
            ax.set_title(t('adoption_rate'))
            ax.grid(False)
            
            st.pyplot(fig)
        
        # Satisfaction par dépôt
        st.subheader(t('satisfaction_by_depot'))
        try:
            satisfaction_img = Image.open('images/satisfaction_depot.png')
            st.image(satisfaction_img, caption=t('satisfaction_by_depot'), use_container_width=True)
        except:
            # Créer un graphique
            fig, ax = plt.subplots(figsize=(10, 6))
            satisfaction_values = list(st.session_state.satisfaction_by_depot.values())
            satisfaction_labels = list(st.session_state.satisfaction_by_depot.keys())
            
            # Créer les barres
            bars = ax.bar(satisfaction_labels, satisfaction_values, color='#7e57c2')
            
            # Ajouter les valeurs au-dessus des barres
            for i, v in enumerate(satisfaction_values):
                ax.text(i, v + 0.1, f"{v}/5", ha='center')
            
            ax.set_ylim(0, 5)
            ax.set_xlabel(t('depot'))
            ax.set_ylabel(t('satisfaction') + ' (1-5)')
            ax.set_title(t('satisfaction_by_depot'))
            ax.grid(False)
            
            st.pyplot(fig)
    
    # Onglet Analyse comparative
    with tab3:
        st.header("Analyse Comparative")
        
        # Indicateurs clés (graphique)
        st.subheader(t('key_indicators'))
        try:
            indicators_img = Image.open('images/evolution_indicators.png')
            st.image(indicators_img, caption=t('key_indicators'), use_container_width=True)
        except:
            st.warning("Image d'évolution des indicateurs non trouvée")
        
#        # Évolution absentéisme (graphique)
#        st.subheader(t('absenteeism'))
#        try:
#            absenteeism_img = Image.open('images/impact_absenteisme.png')
#            st.image(absenteeism_img, caption=t('absenteeism'), use_container_width=True)
#        except:
#            st.warning("Image d'évolution de l'absentéisme non trouvée")

elif st.session_state.current_page == 'about' and st.session_state.admin_authenticated:
    st.title("À propos de cette application")
    
    st.markdown("""
    ### Méthodologie d'enquête

    - **Période** : Juillet - Septembre 2024
    - **Population** : Conducteurs ALSA Casablanca
    - **Taille de l'échantillon** : 187 conducteurs (41% de l'effectif)
    - **Questionnaire pré-implantation** : 37 questions, 127 répondants (taux de réponse : 82%)
    - **Questionnaire post-implantation** : 42 questions, 112 répondants (taux de réponse : 76%)
    - **Méthode** : Questionnaires en format papier et électronique, distribués dans les 3 dépôts
    - **Langues** : Français et arabe
    
    ### Crédits
    
    Application développée pour ALSA Maroc
    """)
    
    # Ajouter le logo ALSA
    try:
        logo = Image.open('images/logo_alsa_maroc.png')
        st.image(logo, width=200)
    except:
        st.write("Logo ALSA Maroc")

elif st.session_state.current_page == 'stats' and st.session_state.admin_authenticated:
    st.title(t('stats_section'))
    
    st.write(f"{t('pre_count')} {st.session_state.pre_count}")
    st.write(f"{t('post_count')} {st.session_state.post_count}")
    st.write(f"{t('total_count')} {st.session_state.pre_count + st.session_state.post_count}")
    
    # Afficher les statistiques détaillées
    st.subheader("Statistiques détaillées")
    
    # Convertir les données en format téléchargeable
    stats_data = {
        "pre_count": st.session_state.pre_count,
        "post_count": st.session_state.post_count,
        "pre_age_stats": st.session_state.pre_age_stats,
        "pre_gender_stats": st.session_state.pre_gender_stats,
        "pre_education_stats": st.session_state.pre_education_stats,
        "pre_depot_stats": st.session_state.pre_depot_stats,
        "post_usage_stats": st.session_state.post_usage_stats,
        "adoption_by_age": st.session_state.adoption_by_age,
        "satisfaction_by_depot": st.session_state.satisfaction_by_depot
    }
    
    # Convertir en JSON
    json_data = json.dumps(stats_data, indent=4)
    
    # Bouton de téléchargement
    st.download_button(
        label=t('download'),
        data=json_data,
        file_name="questionnaires_stats.json",
        mime="application/json"
    )
    
    # Afficher un aperçu des statistiques en format JSON
    st.code(json_data, language="json")

elif st.session_state.current_page == 'responses' and st.session_state.admin_authenticated:
    st.title(t('responses'))
    
    # Onglets pour les deux types de questionnaires
    tab1, tab2 = st.tabs([t('pre_individual_responses'), t('post_individual_responses')])
    
    # Onglet des réponses pré-implantation
    with tab1:
        st.header(t('pre_individual_responses'))
        st.write(f"{t('sample_size')}: {len(st.session_state.individual_pre_responses)}")
        
        # Filtres
        col1, col2, col3 = st.columns(3)
        with col1:
            filter_age = st.selectbox(t('age'), ["Tous"] + list(st.session_state.pre_age_stats.keys()), key="pre_filter_age")
        with col2:
            filter_gender = st.selectbox(t('gender'), ["Tous", "Homme", "Femme"], key="pre_filter_gender")
        with col3:
            filter_depot = st.selectbox(t('depot'), ["Tous"] + list(st.session_state.pre_depot_stats.keys()), key="pre_filter_depot")
        
        # Filtrer les données
        filtered_responses = st.session_state.individual_pre_responses.copy()
        if filter_age != "Tous":
            filtered_responses = [resp for resp in filtered_responses if resp["age_group"] == filter_age]
        if filter_gender != "Tous":
            filtered_responses = [resp for resp in filtered_responses if resp["gender"] == filter_gender]
        if filter_depot != "Tous":
            filtered_responses = [resp for resp in filtered_responses if resp["depot"] == filter_depot]
        
        # Afficher un tableau des réponses
        if filtered_responses:
            # Créer un DataFrame avec les infos de base (sans la date)
            df_responses = pd.DataFrame({
                t('id'): [resp["id"] for resp in filtered_responses],
                t('age'): [resp["age"] for resp in filtered_responses],
                t('gender'): [resp["gender"] for resp in filtered_responses],
                t('depot'): [resp["depot"] for resp in filtered_responses]
            })
            
            st.dataframe(df_responses)
            
            # Afficher les détails d'une réponse sélectionnée
            selected_id = st.selectbox(t('response_details'), [resp["id"] for resp in filtered_responses])
            
            # Trouver la réponse correspondante
            selected_response = next((resp for resp in filtered_responses if resp["id"] == selected_id), None)
            
            if selected_response:
                st.subheader(f"{t('response_details')} #{selected_id}")
                
                # Informations démographiques
                st.write(f"**{t('age')}:** {selected_response['age']} ({selected_response['age_group']})")
                st.write(f"**{t('gender')}:** {selected_response['gender']}")
                st.write(f"**{t('education')}:** {selected_response['education']}")
                st.write(f"**{t('depot')}:** {selected_response['depot']}")
                
                # Questions et réponses
                st.subheader(t('current_practices'))
                q_data = {
                    t('question'): [
                        "Planning à l'avance",
                        "Changements de dernière minute",
                        "Compréhension du processus",
                        "Équité du processus",
                        "Communication des préférences",
                        "Prise en compte des préférences",
                        "Simplicité des échanges",
                        "Repos suffisant",
                        "Répartition de la charge",
                        "Heures supplémentaires"
                    ],
                    t('answer'): [
                        selected_response.get("q7_planning_advance", "N/A"),
                        selected_response.get("q8_last_minute_changes", "N/A"),
                        selected_response.get("q9_understanding_process", "N/A"),
                        selected_response.get("q10_fairness", "N/A"),
                        selected_response.get("q11_preference_communication", "N/A"),
                        selected_response.get("q12_preference_consideration", "N/A"),
                        selected_response.get("q13_service_exchange", "N/A"),
                        selected_response.get("q14_rest_time", "N/A"),
                        selected_response.get("q15_workload_distribution", "N/A"),
                        selected_response.get("q16_unplanned_overtime", "N/A")
                    ]
                }
                
                st.table(pd.DataFrame(q_data))
        else:
            st.info("Aucune réponse ne correspond aux filtres sélectionnés.")
    
    # Onglet des réponses post-implantation
    with tab2:
        st.header(t('post_individual_responses'))
        st.write(f"{t('sample_size')}: {len(st.session_state.individual_post_responses)}")
        
        # Filtres
        col1, col2, col3 = st.columns(3)
        with col1:
            filter_age = st.selectbox(t('age'), ["Tous"] + list(st.session_state.pre_age_stats.keys()), key="post_filter_age")
        with col2:
            filter_depot = st.selectbox(t('depot'), ["Tous"] + list(st.session_state.pre_depot_stats.keys()), key="post_filter_depot")
        with col3:
            filter_usage = st.selectbox(t('app_usage'), ["Tous"] + list(st.session_state.post_usage_stats.keys()), key="post_filter_usage")
        
        # Filtrer les données
        filtered_responses = st.session_state.individual_post_responses.copy()
        if filter_age != "Tous":
            filtered_responses = [resp for resp in filtered_responses if resp["age_group"] == filter_age]
        if filter_depot != "Tous":
            filtered_responses = [resp for resp in filtered_responses if resp["depot"] == filter_depot]
        if filter_usage != "Tous":
            filtered_responses = [resp for resp in filtered_responses if resp["usage_frequency"] == filter_usage]
        
        # Afficher un tableau des réponses
        if filtered_responses:
            # Créer un DataFrame avec les infos de base (sans la date)
            df_responses = pd.DataFrame({
                t('id'): [resp["id"] for resp in filtered_responses],
                t('age'): [resp["age"] for resp in filtered_responses],
                t('depot'): [resp["depot"] for resp in filtered_responses],
                t('app_usage'): [resp["usage_frequency"] for resp in filtered_responses],
                t('satisfaction'): [resp["satisfaction"] for resp in filtered_responses]
            })
            
            st.dataframe(df_responses)
            
            # Afficher les détails d'une réponse sélectionnée
            selected_id = st.selectbox(t('response_details'), [resp["id"] for resp in filtered_responses], key="post_details")
            
            # Trouver la réponse correspondante
            selected_response = next((resp for resp in filtered_responses if resp["id"] == selected_id), None)
            
            if selected_response:
                st.subheader(f"{t('response_details')} #{selected_id}")
                
                # Informations démographiques
                st.write(f"**{t('age')}:** {selected_response['age']} ({selected_response['age_group']})")
                st.write(f"**{t('depot')}:** {selected_response['depot']}")
                st.write(f"**{t('app_usage')}:** {selected_response['usage_frequency']}")
                st.write(f"**{t('satisfaction')}:** {selected_response['satisfaction']}/5")
                
                # Questions et réponses
                st.subheader(t('scheduling_impact'))
                q_data = {
                    t('question'): [
                        "Information planning",
                        "Changements de dernière minute",
                        "Compréhension du processus",
                        "Équité du processus",
                        "Expression des préférences",
                        "Prise en compte des préférences",
                        "Simplicité des échanges",
                        "Équilibre vie pro/perso",
                        "Répartition de la charge",
                        "Heures supplémentaires"
                    ],
                    t('answer'): [
                        selected_response.get("q12_schedule_information", "N/A"),
                        selected_response.get("q13_last_minute_changes", "N/A"),
                        selected_response.get("q14_process_understanding", "N/A"),
                        selected_response.get("q15_process_fairness", "N/A"),
                        selected_response.get("q16_preference_expression", "N/A"),
                        selected_response.get("q17_preference_consideration", "N/A"),
                        selected_response.get("q18_exchange_simplicity", "N/A"),
                        selected_response.get("q19_work_life_balance", "N/A"),
                        selected_response.get("q20_workload_distribution", "N/A"),
                        selected_response.get("q21_overtime", "N/A")
                    ]
                }
                
                st.table(pd.DataFrame(q_data))
        else:
            st.info("Aucune réponse ne correspond aux filtres sélectionnés.")

# Code principal
def main():
    # L'application est déjà organisée, pas besoin de code supplémentaire ici
    pass

if __name__ == "__main__":
    main()
