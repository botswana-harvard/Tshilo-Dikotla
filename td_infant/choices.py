from edc_constants.constants import NOT_APPLICABLE, OTHER

from tshilo_dikotla.constants import MIN_AGE_OF_CONSENT

from .constants import BROUGHT, REALTIME, CLOTH_NAPPY


NAPPY_TYPE = (
    (CLOTH_NAPPY, 'Cloth nappy'),
    ('commercial nappy', 'Commercial Nappy'),
    (OTHER, 'Other, specify'),
    (NOT_APPLICABLE, 'Not applicable'),
)


STOOL_COLLECTION_TIME = (
    (REALTIME, 'Real Time'),
    (BROUGHT, 'Brought by mother'),
    (NOT_APPLICABLE, 'Not applicable')
)

STOOL_STORED = (
    ('room temp', 'At room temperature (unrefrigerated)'),
    ('refrigerated', 'Refrigerated'),
    (NOT_APPLICABLE, 'Not applicable'),
)

OFF_STUDY_REASON = [
    ('not_18'.format(MIN_AGE_OF_CONSENT),
     ' Mother of infant found to be less than {} years of age'.format(MIN_AGE_OF_CONSENT)),
    ('not_citizen', ' Mother found not be a citizen of Botswana'),
    ('moved',
     ' Subject will be moving out of study area or unable to stay in study area'),
    ('lost_no_contact', ' Lost to follow-up, unable to locate'),
    ('lost_contacted',
     ' Lost to follow-up, contacted but did not come to study clinic'),
    ('withdrew_by_mother',
     ' Mother changed mind and withdrew consent'),
    ('withdrew_by_father',
     ' Father of baby did not want infant to participate and participant withdrew consent'),
    ('withdrew_by_family',
     ' Other family member did not want mother/infant to participate and participant withdrew consent'),
    ('hiv_pos', ' Infant found to be HIV-infected'),
    ('ill',
     ' Infant diagnosed with medical condition making survival to 12 months unlikely'),
    ('complete',
     (' Completion of protocol required period of time for observation (see Study '
      'Protocol for definition of Completion.) [skip to end of form]')),
    ('death',
     (' Participant death (complete the DEATH REPORT FORM AF005) (For '
      'EAE Reporting requirements see EAE Reporting Manual)')),
    (OTHER, ' Other'),
]

IMMUNIZATIONS = (
    ('Vitamin_A', 'Vitamin A'),
    ('BCG', 'BCG'),
    ('Hepatitis_B', 'Hepatitis B'),
    ('DPT', 'DPT (Diphtheria, Pertussis and Tetanus)'),
    ('Haemophilus_influenza', 'Haemophilus Influenza B Vaccine'),
    ('PCV_Vaccine', 'PCV Vaccine (Pneumonia Conjugated Vaccine)'),
    ('Polio', 'Polio'),
    ('Rotavirus', 'Rotavirus'),
    ('inactivated_polio_vaccine', 'Inactivated-Polio Vaccine'),
    ('Measles', 'Measles'),
    ('Pentavalent',
     'Pentavalent Vaccine (Contains DPT, Hepatitis B and Haemophilus Influenza B Vaccine)'),
    ('diptheria_tetanus', 'Diptheria and Tetanus'))

INFANT_VACCINATIONS = (
    ('Vitamin_A', 'Vitamin A'),
    ('BCG', 'BCG'),
    ('Hepatitis_B', 'Hepatitis B'),
    ('DPT', 'DPT (Diphtheria, Pertussis and Tetanus)'),
    ('Haemophilus_influenza', 'Haemophilus Influenza B Vaccine'),
    ('PCV_Vaccine', 'PCV Vaccine (Pneumonia Conjugated Vaccine)'),
    ('Polio', 'Polio'),
    ('inactivated_polio_vaccine', 'Inactivated-Polio Vaccine'),
    ('Rotavirus', 'Rotavirus'),
    ('Measles', 'Measles'),
    ('Pentavalent',
     'Pentavalent Vaccine (Contains DPT, Hepatitis B and Haemophilus Influenza B Vaccine)'),
    ('diphtheria_tetanus', 'Diphtheria and Tetanus'))

INFANT_AGE_VACCINE_GIVEN = (
    ('At Birth', 'At Birth'),
    ('After Birth', 'After Birth'),
    ('2', '2 months'),
    ('3', '3 months'),
    ('4', '4 months'),
    ('4-6', '4-6 months'),
    ('6-11', '6-11 months'),
    ('9', '9 months'),
    ('9-12', '9-12 months'),
    ('12-17', '12-17 months'),
    ('18', '18 months'),
    ('18-29', '18-29 months'),
    ('24-29', '24-29 months'),
    ('30-35', '30-35 months'),
    ('36-41', '36-41 months'),
    ('42-47', '42-47 months'),
    ('48-53', '48-53 months'),
    ('54-59', '54-59 months'))

ARV_MODIFICATION_REASON = (
    ('Initial dose', 'Initial dose'),
    ('Never started', 'Never started'),
    ('Toxicity decreased_resolved', 'Toxicity decreased/resolved'),
    ('Completed PMTCT intervention', 'Completed PMTCT intervention'),
    ('Completed postpartum tail', 'Completed postpartum "tail"'),
    ('Scheduled dose increase', 'Scheduled dose increase'),
    ('Confirmed infant HIV infection, ending study drug',
     'Confirmed infant HIV infection, ending study drug'),
    ('completed protocol',
     'Completion of protocol-required period of study treatment'),
    ('HAART not available', 'HAART not available'),
    ('Anemia', 'Anemia'),
    ('Bleeding', 'Bleeding'),
    ('CNS symptoms', 'CNS symptoms (sleep, psych, etc)'),
    ('Diarrhea', 'Diarrhea'),
    ('Fatigue', 'Fatigue'),
    ('Headache', 'Headache'),
    ('Hepatotoxicity', 'Hepatotoxicity'),
    ('Nausea', 'Nausea'),
    ('Neutropenia', 'Neutropenia'),
    ('Thrombocytopenia', 'Thrombocytopenia'),
    ('Vomiting', 'Vomiting'),
    ('Rash', 'Rash'),
    ('Rash resolved', 'Rash resolved'),
    ('Neuropathy', 'Neuropathy'),
    ('Hypersensitivity_allergic reaction',
     'Hypersensitivity / allergic reaction'),
    ('Pancreatitis', 'Pancreatitis'),
    ('Lactic Acidiosis', 'Lactic Acidiosis'),
    ('Pancytopenia', 'Pancytopenia'),
    ('Virologic failure', 'Virologic failure'),
    ('Immunologic failure', 'Immunologic failure(CD4)'),
    ('Clinical failure', 'Clinical failure'),
    ('Clinician request',
     'Clinician request, other reason (including convenience)'),
    ('Subject request',
     'Subject request, other reason (including convenience)'),
    ('Non-adherence with clinic visits', 'Non-adherence with clinic visits'),
    ('Non-adherence with ARVs', 'Non-adherence with ARVs'),
    ('Death', 'Death'),
    ('OTHER', 'Other'),
)

DOSE_STATUS = (
    ('New', 'New'),
    ('Permanently discontinued', 'Permanently discontinued'),
    ('Temporarily held', 'Temporarily held'),
    ('Dose modified', 'Dose modified'),
    ('Resumed', 'Resumed'),
    ('Not initiated', 'Not initiated'),
)

ARV_DRUG_LIST = (
    ('Nevirapine', 'NVP'),
    ('Kaletra', 'KAL'),
    ('Aluvia', 'ALU'),
    ('Truvada', 'TRV'),
    ('Tenoforvir', 'TDF',),
    ('Zidovudine', 'AZT'),
    ('Lamivudine', '3TC'),
    ('Efavirenz', 'EFV'),
    ('Didanosine', 'DDI'),
    ('Stavudine', 'D4T'),
    ('Nelfinavir', 'NFV'),
    ('Abacavir', 'ABC'),
    ('Combivir', 'CBV'),
    ('Ritonavir', 'RTV'),
    ('Trizivir', 'TZV'),
    ('Raltegravir', 'RAL'),
    ('Saquinavir,soft gel capsule', 'FOR'),
    ('Saquinavir,hard capsule', 'INV'),
    ('Kaletra or Aluvia', 'KAL or ALU'),
    ('Atripla', 'ATR'),
    ('HAART,unknown', 'HAART,unknown'),
)

SOLID_FOODS = (
    ('Grains, roots and tubers', 'Grains, roots and tubers'),
    ('Legumes and nuts', 'Legumes and nuts'),
    (' Dairy products (milk, yogurt, cheese)',
     ' Dairy products (milk, yogurt, cheese)'),
    ('Flesh foods', 'Flesh foods (meat, fish, poultry and liver/organ meat)'),
    ('Eggs', 'Eggs'),
    ('Vitamin A rich fruts and vegetables (carrots)',
     'Vitamin A rich fruts and vegetables (carrots)'),
    ('Other fruits and vegetables', 'Other fruits and vegetables'),
    ('Other', 'Other')

)
