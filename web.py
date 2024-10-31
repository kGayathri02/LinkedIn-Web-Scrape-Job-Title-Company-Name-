import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

def web_scrape(URL):
    # URL = 'https://www.linkedin.com/jobs/search/?currentJobId=4059815192&distance=25&f_E=1%2C2&geoId=102713980&keywords=data%20analyst&origin=JOBS_HOME_KEYWORD_HISTORY&refresh=true'

    response = requests.get(URL)
    soup = BeautifulSoup(response.content, 'html.parser')


    job_titles = []
    companies = []
    locations = []
    posting_times = []
    job_links = []

    for job in soup.find_all('div', class_='base-card'):
        # job title
        title = job.find('h3', class_='base-search-card__title').get_text(strip=True)
        job_titles.append(title)
        
        # company name
        company = job.find('h4', class_='base-search-card__subtitle').get_text(strip=True)
        companies.append(company)
        
        # location
        location = job.find('span', class_='job-search-card__location').get_text(strip=True)
        locations.append(location)
        
        # Posting time
        time_tag = job.find('time', class_='job-search-card__listdate')
        posting_time = time_tag.get_text(strip=True) if time_tag else "Not specified"
        posting_times.append(posting_time)
        
        # job URL
        job_link = job.find('a', class_='base-card__full-link')['href']
        job_links.append(job_link)


    df = pd.DataFrame({
        'Job_Title': job_titles,
        'Company': companies,
        'Location': locations,
        'Posting_Time': posting_times,
        'Job_Link': job_links
    })
    
    return df




#Streamlit Part
st.markdown('# Web Scraping & Trend Analysis')
tab1, tab2, tab3, tab4= st.tabs(['Home','URL & Extract', 'Trend Analysis', 'Conclusion'])

with tab1:
    st.markdown('## Welcome!')
    st.markdown(''' Using Python's BeautifulSoup for data extraction, it gathers information such as job titles, companies, locations, and posting dates. 
    The data is processed, cleaned, and visualized using tools like Seaborn and Matplotlib in Streamlit for insights on hiring trends and demand across various regions.
    This analysis can help job seekers and recruiters better understand the job market landscape.''')

with tab2:
    url= st.text_input('Paste LinkedIn URL what Role You Searched')
    if st.button('Submit'):
        df= web_scrape(URL= url)
        st.dataframe(df)

    st.info("If you don't have a URl. You can use this https://www.linkedin.com/jobs/search/?currentJobId=4059815192&distance=25&f_E=1%2C2&geoId=102713980&keywords=data%20analyst&origin=JOBS_HOME_KEYWORD_HISTORY&refresh=true ")


with tab3:
    st.markdown("## Locations of Job Postings")
    df= web_scrape(URL=url)
    location_counts = df['Location'].value_counts().head(10)  
    fig= plt.figure(figsize=(10, 6))
    sns.barplot(x=location_counts.values, y=location_counts.index, hue= location_counts, palette='magma')
    plt.title("Top Job Posting Locations")
    plt.xlabel("Number of Postings")
    plt.ylabel("Location")
    st.pyplot(fig)

    st.markdown("## Job Title Distribution")
    title_counts = df['Job_Title'].value_counts().head(10)
    fig= plt.figure(figsize=(10, 6))
    sns.barplot(x=title_counts.values, y=title_counts.index,  hue=title_counts, palette='coolwarm')
    plt.title("Top Job Titles")
    plt.xlabel("Number of Postings")
    plt.ylabel("Job Title")
    st.pyplot(fig)

with tab4:
    st.markdown('''## Conclusion''')
    st.markdown('''### Here We can See by this Analysis:
- Major Job Locations are based on Bangalore, India. And Least Job Vancancies or Job Location is Urban Bangalore.
- Further Job Vacancies based on Hyderbad, Chennai...
                
### By Job Distribution Job, 
- We Searched Data Analyst, so We expect Data Analyst Role.
- We can Majority Job Vancancies is based on our requirement.
- And also we can see other suggestion which is related to our requirments like Data Analyyst PowerBi Specialist, Data Platform Analyst.''')
