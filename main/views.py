from django.shortcuts import render
from .models import User
from django.core.paginator import Paginator
import pandas as pd
import urllib, base64
import matplotlib.pyplot as plt
import io

# Home Page view
def Home_Page(request):
    # Load entire user data
    qs = User.objects.all()

    # Get filter inputs from request
    input_username = request.GET.get('input_userName')
    input_city = request.GET.getlist('input_city')  # List of selected cities
    input_phone = request.GET.get('input_phoneNumber')
    select_all_cities = request.GET.get('select_all_cities')  # Checkbox for "All Cities"

    # Get distinct cities for dropdown in alphabetical order
    cities = User.objects.values_list('city', flat=True).distinct().order_by('city')

    # Apply filtering
    if input_username:
        qs = qs.filter(username__exact=input_username)  # Username filter (case-insensitive)

    if select_all_cities:  # If "All Cities" is checked
        qs = User.objects.all()  # Get all user data without any filtering or arrangement
    elif input_city:  # If specific cities are selected
        qs = qs.filter(city__in=input_city)  # Filter by selected cities
        # Do not apply ordering to maintain original order

    if input_phone:
        qs = qs.filter(contact_number__exact=input_phone)  # Phone number filter

    # Paginate the queryset (4000 records per page)
    paginator = Paginator(qs, 4000)
    page_number = request.GET.get('page')  # Get page number from request
    page_obj = paginator.get_page(page_number)  # Paginate queryset

    # Prepare the context for rendering
    context = {
        'page_obj': page_obj,  # Paginated records
        'cities': list(cities),  # Cities dropdown list
        'input_userName': input_username,  # Preserve search input
        'input_city': input_city,  # Preserve city selections
        'input_phoneNumber': input_phone,  # Preserve phone number input
        'select_all_cities': select_all_cities is not None,  # Preserve "All Cities" checkbox state (True/False)
    }

    return render(request, 'index.html', context)  # Render index page


# Helper function to categorize age
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


# Graph Page view for displaying age category distribution
def Graph_Page(request):
    # Query to fetch data from the User model
    qs = User.objects.all().values('username', 'contact_number', 'city', 'age')
    df = pd.DataFrame(list(qs))  # Convert to DataFrame

    # Categorize the age using the helper function
    df['age_category'] = df['age'].apply(categorize_age)
    
    # Define the order for age categories
    age_order = ['<20', '20-30', '31-40', '41-50', '>50']
    df['age_category'] = pd.Categorical(df['age_category'], categories=age_order, ordered=True)

    # Count the frequencies of age categories
    age_category_freq = df['age_category'].value_counts().reindex(age_order).reset_index()
    age_category_freq.columns = ['age_category', 'frequency']

    # Calculate the total frequency and append it to the DataFrame
    total_frequency = age_category_freq['frequency'].sum()
    total_row = pd.DataFrame([{'age_category': 'Total', 'frequency': total_frequency}])
    age_category_freq = pd.concat([age_category_freq, total_row], ignore_index=True)

    # Convert the updated DataFrame to a dictionary
    df_dict = age_category_freq.to_dict(orient='records')

    # Create a bar plot of age category frequencies
    fig, ax = plt.subplots()
    ax.bar(age_category_freq['age_category'][:-1], age_category_freq['frequency'][:-1], color='skyblue')  # Exclude 'Total' for bar plot

    # Set labels and title for the plot
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

    # Pass the data and the image URI to the template
    return render(request, 'graph.html', {
        'age_category_data': df_dict,  # Age category data as a dictionary
        'data_uri': uri  # Base64-encoded image
    })
