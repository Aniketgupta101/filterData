from django.db.models import Q
from django.shortcuts import render
from .models import User
from django.db.models import Count, Case, When
import pandas as pd
import urllib, base64
import matplotlib.pyplot as plt
import io

# Create your views here.
def Home_Page(request):
    # Load entire data
    qs = User.objects.all()

    # Filter inputs
    input_username = request.GET.get('input_userName')
    input_city = request.GET.getlist('input_city')  # Get list of cities
    input_phone = request.GET.get('input_phoneNumber')

    # List of distinct cities for the dropdown, sorted alphabetically
    cities = User.objects.values_list('city', flat=True).distinct().order_by('city')

    # Apply filtering
    if input_username:
        qs = qs.filter(username__icontains=input_username)  # Filter by username (case-insensitive)

    if input_city:  # Check if any cities were selected
        qs = qs.filter(city__in=input_city)  # Filter by selected cities
        qs = qs.order_by('city')

    if input_phone:
        qs = qs.filter(contact_number__icontains = input_phone)

    # Sort the filtered queryset by city alphabetically
   

    # Prepare the context for rendering
    context = {
        'queryset': qs,
        'cities': list(cities)
    }

    return render(request, 'index.html', context)




def categorize_age(age):
    age = int(age)
    if age < 20:
        return '<20'
    elif 20 <= age <= 30:
        return '20-30'
    elif 31 <= age <= 40:
        return '31-40'
    elif 41 <= age <= 50:
        return '41-50'
    else:
        return '>50'

def Graph_Page(request):
    qs = User.objects.all().values('username', 'contact_number', 'city', 'age')
    df = pd.DataFrame(list(qs))

    df['age_category'] = df['age'].apply(categorize_age)
    
    age_order = ['<20', '20-30', '31-40', '41-50', '>50']
    df['age_category'] = pd.Categorical(df['age_category'], categories=age_order, ordered=True)

    age_category_freq = df['age_category'].value_counts().reindex(age_order).reset_index()
    age_category_freq.columns = ['age_category', 'frequency']
    
    df_dict = age_category_freq.to_dict(orient='records')


    # Create the plot
    fig, ax = plt.subplots()
    ax.bar(age_category_freq['age_category'], age_category_freq['frequency'], color='skyblue')
    
    # Set labels and title
    ax.set_xlabel('Age Category')
    ax.set_ylabel('Frequency')
    ax.set_title('Age Category Frequency Distribution')
    
    # Save the plot to a bytes buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    
    # Encode the image to base64 to embed in HTML
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)

    #return render(request, 'graph.html', {'age_category_data': df_dict})
    #return render(request, 'graph.html', {'data_uri': uri})

    return render(request, 'graph.html', {'age_category_data': df_dict, 'data_uri': uri})