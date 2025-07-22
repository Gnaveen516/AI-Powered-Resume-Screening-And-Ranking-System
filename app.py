
import streamlit as st
from PyPDF2 import PdfReader
import re
import spacy
from difflib import get_close_matches
import yake
import nltk
from nltk.corpus import wordnet as wn
from collections import defaultdict

def extract_text_from_pdf(file):
    pdf = PdfReader(file)
    text = ""
    for page in pdf.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\\n"
    return text.strip() if text else "No readable text found."


IT_INDUSTRY_KEYWORDS = [
    'pyspark',
    # Frameworks
    'spring boot', 'express.js', 'express', 'next.js', 'nuxt.js', 'nestjs', 'fastapi', 'rails', 'ruby on rails', 'laravel', 'symfony', 'cakephp', 'zend', 'yii', 'meteor', 'ember.js', 'backbone.js', 'sails.js', 'koa', 'adonisjs', 'flask', 'django', 'pyramid', 'bottle', 'web2py', 'play framework', 'micronaut', 'quarkus', 'vert.x', 'struts', 'jsf', 'gwt', 'vaadin', 'blade', 'beego', 'gin', 'echo', 'fiber', 'phoenix', 'asp.net', 'dotnet core', 'dotnet', 'wcf', 'wpf', 'silverlight', 'unity', 'unreal engine', 'godot', 'cryengine', 'libgdx', 'cocos2d', 'phaser', 'pixi.js', 'three.js', 'babylon.js', 'electron', 'cordova', 'ionic', 'capacitor', 'react native', 'xamarin', 'flutter', 'nativescript', 'qt', 'wxwidgets', 'gtk', 'tkinter', 'kivy', 'openframeworks', 'processing', 'p5.js', 'd3.js', 'chart.js', 'highcharts', 'plotly', 'leaflet', 'openlayers', 'arcgis', 'mapbox', 'kepler.gl', 'deck.gl', 'big data', 'hadoop', 'spark', 'storm', 'flink', 'kafka', 'cassandra', 'hbase', 'elasticsearch', 'solr', 'lucene', 'splunk', 'tableau', 'power bi', 'qlik', 'looker', 'superset', 'metabase', 'redash', 'databricks', 'snowflake', 'redshift', 'bigquery', 'airflow', 'dbt', 'talend', 'informatica', 'pentaho', 'ssis', 'ssrs', 'ssas', 'cognos', 'microstrategy', 'sap', 'oracle ebs', 'peoplesoft', 'workday', 'netsuite', 'salesforce', 'dynamics', 'zoho', 'hubspot', 'marketo', 'pardot', 'mailchimp', 'sendgrid', 'twilio', 'stripe', 'paypal', 'square', 'braintree', 'adyen', 'shopify', 'magento', 'woocommerce', 'prestashop', 'opencart', 'bigcommerce', 'erp', 'crm', 'scm', 'wms', 'lms', 'cms', 'ecommerce', 'saas', 'paas', 'iaas', 'fintech', 'edtech', 'healthtech', 'proptech', 'insurtech', 'govtech', 'martech', 'legaltech', 'iot', 'blockchain', 'crypto', 'defi', 'nft', 'ai', 'ml', 'dl', 'nlp', 'cv', 'ar', 'vr', 'xr', 'robotics', 'automation', 'rpa', 'devops', 'mlops', 'a11y', 'accessibility', 'security', 'cybersecurity', 'pentest', 'gdpr', 'hipaa', 'pci dss', 'sox', 'iso 27001', 'cmmc', 'soc 2', 'itil', 'cobit', 'togaf', 'six sigma', 'lean', 'agile', 'scrum', 'kanban', 'waterfall', 'prince2', 'pmp', 'csm', 'cspo', 'safe', 'it service management', 'service desk', 'helpdesk', 'support', 'sla', 'slo', 'sli', 'incident management', 'problem management', 'change management', 'release management', 'asset management', 'configuration management', 'cmdb', 'monitoring', 'observability', 'logging', 'alerting', 'tracing', 'metrics', 'dashboard', 'reporting', 'analytics', 'data warehouse', 'data lake', 'data mart', 'data pipeline', 'etl', 'elt', 'data governance', 'data quality', 'data catalog', 'data lineage', 'master data management', 'mdm', 'reference data', 'data stewardship', 'data privacy', 'data protection', 'data security', 'data compliance', 'data retention', 'data archiving', 'data migration', 'data integration', 'data synchronization', 'data replication', 'data backup', 'data restore', 'disaster recovery', 'business continuity', 'high availability', 'scalability', 'performance', 'optimization', 'tuning', 'capacity planning', 'load balancing', 'failover', 'redundancy', 'clustering', 'sharding', 'partitioning', 'caching', 'queue', 'messaging', 'pubsub', 'event streaming', 'event sourcing', 'cqrs', 'microservices', 'soa', 'monolith', 'serverless', 'container', 'containerization', 'orchestration', 'virtualization', 'hypervisor', 'bare metal', 'cloud', 'on-premise', 'hybrid', 'multi-cloud', 'edge', 'fog', 'cdn', 'dns', 'dhcp', 'vpn', 'firewall', 'ids', 'ips', 'waf', 'siem', 'soar', 'casb', 'sase', 'zero trust', 'identity', 'access management', 'iam', 'pam', 'mfa', 'sso', 'saml', 'oauth', 'openid', 'jwt', 'ldap', 'active directory', 'kerberos', 'radius', 'tacacs', 'certificate', 'pk', 'pki', 'ssl', 'tls', 'ssh', 'gpg', 'pgp', 'encryption', 'hashing', 'signing', 'token', 'api gateway', 'service mesh', 'sidecar', 'proxy', 'reverse proxy', 'load balancer', 'web server', 'app server', 'db server', 'file server', 'mail server', 'ftp server', 'dns server', 'dhcp server', 'ntp server', 'syslog', 'snmp', 'netflow', 'sflow', 'ipfix', 'wireshark', 'tcpdump', 'nmap', 'nessus', 'openvas', 'metasploit', 'burp suite', 'zap', 'owasp', 'cve', 'cwe', 'cisa', 'nist', 'iso', 'pci', 'hipaa', 'gdpr', 'sox', 'cmmc', 'soc', 'itil', 'cobit', 'togaf', 'six sigma', 'lean', 'agile', 'scrum', 'kanban', 'waterfall', 'prince2', 'pmp', 'csm', 'cspo', 'safe', 'it service management', 'service desk', 'helpdesk', 'support', 'sla', 'slo', 'sli', 'incident management', 'problem management', 'change management', 'release management', 'asset management', 'configuration management', 'cmdb', 'monitoring', 'observability', 'logging', 'alerting', 'tracing', 'metrics', 'dashboard', 'reporting', 'analytics', 'data warehouse', 'data lake', 'data mart', 'data pipeline', 'etl', 'elt', 'data governance', 'data quality', 'data catalog', 'data lineage', 'master data management', 'mdm', 'reference data', 'data stewardship', 'data privacy', 'data protection', 'data security', 'data compliance', 'data retention', 'data archiving', 'data migration', 'data integration', 'data synchronization', 'data replication', 'data backup', 'data restore', 'disaster recovery', 'business continuity', 'high availability', 'scalability', 'performance', 'optimization', 'tuning', 'capacity planning', 'load balancing', 'failover', 'redundancy', 'clustering', 'sharding', 'partitioning', 'caching', 'queue', 'messaging', 'pubsub', 'event streaming', 'event sourcing', 'cqrs', 'microservices', 'soa', 'monolith', 'serverless', 'container', 'containerization', 'orchestration', 'virtualization', 'hypervisor', 'bare metal', 'cloud', 'on-premise', 'hybrid', 'multi-cloud', 'edge', 'fog', 'cdn', 'dns', 'dhcp', 'vpn', 'firewall', 'ids', 'ips', 'waf', 'siem', 'soar', 'casb', 'sase', 'zero trust', 'identity', 'access management', 'iam', 'pam', 'mfa', 'sso', 'saml', 'oauth', 'openid', 'jwt', 'ldap', 'active directory', 'kerberos', 'radius', 'tacacs', 'certificate', 'pk', 'pki', 'ssl', 'tls', 'ssh', 'gpg', 'pgp', 'encryption', 'hashing', 'signing', 'token', 'api gateway', 'service mesh', 'sidecar', 'proxy', 'reverse proxy', 'load balancer', 'web server', 'app server', 'db server', 'file server', 'mail server', 'ftp server', 'dns server', 'dhcp server', 'ntp server', 'syslog', 'snmp', 'netflow', 'sflow', 'ipfix', 'wireshark', 'tcpdump', 'nmap', 'nessus', 'openvas', 'metasploit', 'burp suite', 'zap', 'owasp', 'cve', 'cwe', 'cisa', 'nist', 'iso', 'pci', 'hipaa', 'gdpr', 'sox', 'cmmc', 'soc', 'itil', 'cobit', 'togaf', 'six sigma', 'lean', 'agile', 'scrum', 'kanban', 'waterfall', 'prince2', 'pmp', 'csm', 'cspo', 'safe', 'it service management', 'service desk', 'helpdesk', 'support', 'sla', 'slo', 'sli', 'incident management', 'problem management', 'change management', 'release management', 'asset management', 'configuration management', 'cmdb', 'monitoring', 'observability', 'logging', 'alerting', 'tracing', 'metrics', 'dashboard', 'reporting', 'analytics', 'data warehouse', 'data lake', 'data mart', 'data pipeline', 'etl', 'elt', 'data governance', 'data quality', 'data catalog', 'data lineage', 'master data management', 'mdm', 'reference data', 'data stewardship', 'data privacy', 'data protection', 'data security', 'data compliance', 'data retention', 'data archiving', 'data migration', 'data integration', 'data synchronization', 'data replication', 'data backup', 'data restore', 'disaster recovery', 'business continuity', 'high availability', 'scalability', 'performance', 'optimization', 'tuning', 'capacity planning', 'load balancing', 'failover', 'redundancy', 'clustering', 'sharding', 'partitioning', 'caching', 'queue', 'messaging', 'pubsub', 'event streaming', 'event sourcing', 'cqrs', 'microservices', 'soa', 'monolith', 'serverless', 'container', 'containerization', 'orchestration', 'virtualization', 'hypervisor', 'bare metal', 'cloud', 'on-premise', 'hybrid', 'multi-cloud', 'edge', 'fog', 'cdn'
]

# Predefined lists of technical and soft skills (expand as needed)
TECHNICAL_SKILLS = [
    'pyspark',
    'python', 'java', 'c++', 'c#', 'javascript', 'typescript', 'sql', 'mysql', 'postgresql', 'mongodb',
    'oracle', 'git', 'docker', 'kubernetes', 'aws', 'azure', 'gcp', 'linux', 'windows', 'tensorflow',
    'pytorch', 'scikit-learn', 'pandas', 'numpy', 'matplotlib', 'react', 'angular', 'node.js', 'flask',
    'django', 'html', 'css', 'spark', 'hadoop', 'tableau', 'power bi', 'jira', 'jenkins', 'rest', 'graphql',
    'agile', 'scrum', 'kanban', 'ci/cd', 'devops', 'selenium', 'c', 'r', 'matlab', 'sas', 'excel', 'cloud',
    'machine learning', 'deep learning', 'nlp', 'data science', 'data analysis', 'etl', 'api', 'microservices',
    'firebase', 'redis', 'elasticsearch', 'rabbitmq', 'kafka', 'bash', 'shell', 'unix', 'visual studio',
    'android', 'ios', 'swift', 'objective-c', 'php', 'laravel', 'symfony', 'spring', 'hibernate', 'dotnet',
    'assembly', 'fortran', 'cobol', 'go', 'rust', 'scala', 'perl', 'vb.net', 'powershell', 'typescript',
    'blockchain', 'solidity', 'unity', 'unreal', 'blender', 'opencv', 'jira', 'confluence', 'bitbucket',
    'trello', 'asana', 'maven', 'gradle', 'ant', 'webpack', 'babel', 'eslint', 'prettier', 'jest', 'mocha',
    'chai', 'pytest', 'unittest', 'junit', 'testng', 'cucumber', 'postman', 'soapui', 'swagger', 'openapi',
    'restful', 'graphql', 'json', 'xml', 'yaml', 'tomcat', 'nginx', 'apache', 'iis', 'ftp', 'smtp', 'imap',
    'pop3', 'ssl', 'tls', 'oauth', 'saml', 'jwt', 'sso', 'ldap', 'active directory', 'vpn', 'firewall',
    'ids', 'ips', 'wireshark', 'nmap', 'burp suite', 'metasploit', 'splunk', 'elk', 'graylog', 'prometheus',
    'grafana', 'zabbix', 'nagios', 'new relic', 'datadog', 'pagerduty', 'servicenow', 'snowflake', 'redshift',
    'bigquery', 'databricks', 'airflow', 'looker', 'd3.js', 'plotly', 'seaborn', 'beautifulsoup', 'scrapy',
    'requests', 'http', 'tcp', 'udp', 'ip', 'dns', 'dhcp', 'icmp', 'snmp', 'vlan', 'ospf', 'bgp', 'eigrp',
    'mpls', 'sdn', 'vxlan', 'evpn', 'vxworks', 'rtos', 'embedded', 'verilog', 'vhdl', 'fpga', 'asic', 'eda',
    'cadence', 'synopsys', 'mentor', 'altium', 'orcad', 'eagle', 'solidworks', 'autocad', 'catia', 'ansys',
    'comsol', 'abaqus', 'hypermesh', 'fluent', 'star-ccm+', 'openfoam', 'mathematica', 'maple', 'stata',
    'minitab', 'r studio', 'rstudio', 'jupyter', 'colab', 'spyder', 'pycharm', 'vscode', 'eclipse', 'intellij',
    'netbeans', 'xcode', 'android studio', 'emacs', 'vim', 'nano', 'notepad++', 'sublime', 'brackets',
    'atom', 'bluej', 'greenfoot', 'alice', 'scratch', 'arduino', 'raspberry pi', 'beaglebone', 'esp32',
    'esp8266', 'iot', 'zigbee', 'zwave', 'lora', 'sigfox', 'nb-iot', 'lte', '5g', 'wifi', 'bluetooth', 'rfid',
    'nfc', 'zigbee', 'zwave', 'lora', 'sigfox', 'nb-iot', 'lte', '5g', 'wifi', 'bluetooth', 'rfid', 'nfc'
]
SOFT_SKILLS = [
    'communication', 'leadership', 'teamwork', 'problem solving', 'critical thinking', 'adaptability',
    'creativity', 'work ethic', 'time management', 'conflict resolution', 'negotiation', 'decision making',
    'empathy', 'collaboration', 'organization', 'attention to detail', 'flexibility', 'initiative', 'motivation',
    'interpersonal', 'presentation', 'public speaking', 'customer service', 'project management', 'multitasking',
    'self-motivation', 'responsibility', 'accountability', 'stress management', 'patience', 'active listening'
]


# Load spaCy English model once
nlp = spacy.load("en_core_web_sm")

# Extract technical and soft skills from text with fuzzy matching
def extract_skills(text, threshold=0.85):
    text_lower = text.lower()
    found_skills = set()
    all_skills = TECHNICAL_SKILLS + IT_INDUSTRY_KEYWORDS + SOFT_SKILLS
    # Exact match
    for skill in all_skills:
        if re.search(r'\b' + re.escape(skill) + r'\b', text_lower):
            found_skills.add(skill)
    # Fuzzy match for skill-like phrases
    doc = nlp(text)
    noun_phrases = set(chunk.text.lower() for chunk in doc.noun_chunks)
    for phrase in noun_phrases:
        matches = get_close_matches(phrase, all_skills, n=1, cutoff=threshold)
        if matches:
            found_skills.add(matches[0])
        # If phrase looks like a skill (e.g., ends with 'skills', 'technologies', 'tools', etc.), add it
        if any(phrase.endswith(suffix) for suffix in ['skills', 'technologies', 'tools', 'languages', 'frameworks', 'platforms', 'approaches']):
            found_skills.add(phrase)
    return list(sorted(found_skills))

# Extract relevant sections from resume text
def extract_relevant_sections(resume_text):
    # Look for Skills, Experience, Certifications sections
    sections = re.split(r'\n(?=[A-Z][A-Za-z ]{2,30}:)', resume_text)
    relevant = []
    for section in sections:
        header = section.strip().split('\n', 1)[0].lower()
        if any(h in header for h in ['skill', 'experience', 'certification']):
            relevant.append(section)
    return '\n'.join(relevant) if relevant else resume_text

# Extract keywords from job description (technical/soft skills + skill-like noun phrases)
def extract_keywords(text):
    return extract_skills(text)

# Get similar words for a keyword using WordNet
def get_similar_words(keyword):
    similar = set()
    for syn in wn.synsets(keyword):
        for lemma in syn.lemmas():
            similar.add(lemma.name().replace('_', ' '))
    similar.discard(keyword)
    return list(similar)

def rank_resumes(job_description, resumes):
    # Extract keywords and similar words from job description
    keywords = list(sorted(set(extract_keywords(job_description))))
    keyword_set = set(keywords)
    similar_words = set()
    for kw in keywords:
        similar_words.update(get_similar_words(kw))
    similar_words = set(similar_words)  # ensure uniqueness
    all_keywords = keyword_set | similar_words

    resume_scores = []
    resume_matches = []
    resume_missing = []
    for resume in resumes:
        resume_text = resume.lower()
        resume_words = set(re.findall(r'\b\w[\w\-\.\+\#]*\b', resume_text))
        matched = set()
        for kw in all_keywords:
            # Compare keyword with all words in resume (case-insensitive)
            if any(kw.lower() == word for word in resume_words):
                matched.add(kw)
        score = len(matched & keyword_set) + 0.5 * len(matched & similar_words)
        missing = list(sorted(keyword_set - matched))
        resume_scores.append(score)
        resume_matches.append(list(sorted(matched)))
        resume_missing.append(missing)
    return resume_scores, keywords, list(sorted(similar_words)), resume_matches, resume_missing

st.title("AI Resume Screening & Ranking System")
job_description = st.text_area("Enter the job description")
uploaded_files = st.file_uploader("Upload PDF resumes", type=["pdf"], accept_multiple_files=True)

if uploaded_files and job_description:
    resumes = [extract_text_from_pdf(file) for file in uploaded_files]
    scores, keywords, similar_words, matches, missing = rank_resumes(job_description, resumes)
    ranked = sorted(zip(uploaded_files, scores, matches, missing), key=lambda x: x[1], reverse=True)

    st.subheader("Extracted Job Description Keywords")
    st.write(", ".join(keywords))
    st.subheader("Similar Words Considered")
    st.write(", ".join(similar_words) if similar_words else "None found")

    st.subheader("Ranked Resumes & Tailoring Suggestions")
    total_keywords = len(keywords) if keywords else 1
    for i, (file, score, matched, miss) in enumerate(ranked, start=1):
        percent = int((len(matched) / total_keywords) * 100) if total_keywords > 0 else 0
        # Color system: red (0-49), orange (50-74), green (75-100)
        if percent < 50:
            color = '#e74c3c'  # red
        elif percent < 75:
            color = '#f39c12'  # orange
        else:
            color = '#27ae60'  # green
        st.markdown(f"<div style='display:flex;align-items:center;'><span style='font-weight:bold;font-size:1.1em;margin-right:10px;'>{i}. {file.name}</span> <span style='font-size:1.1em;color:{color};font-weight:bold;'>{percent}%</span></div>", unsafe_allow_html=True)
        st.progress(percent)
        st.write(f"Matched Keywords: {', '.join(matched) if matched else 'None'}")
        st.write(f"Missing Keywords: {', '.join(miss) if miss else 'None'}")
        if miss:
            st.info(f"Consider adding these keywords in your Skills, Experience, or Summary sections: {', '.join(miss)}")