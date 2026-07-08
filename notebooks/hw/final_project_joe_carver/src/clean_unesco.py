import pandas as pd
from pathlib import Path
import os
import sys
import re
import numpy as np

# set-up output path
REPO_ROOT = Path(__file__).resolve().parents[1]
RAW_DATA_DIR = REPO_ROOT / 'data' / 'raw'
PROCESSED_DATA_DIR = REPO_ROOT / 'data' / 'processed'
DICT_DIR = REPO_ROOT / 'references' / 'dictionaries'

countries = {'AFG': 'Afghanistan',
 'ALB': 'Albania',
 'DZA': 'Algeria',
 'AND': 'Andorra',
 'AGO': 'Angola',
 'ATG': 'Antigua and Barbuda',
 'ARG': 'Argentina',
 'ARM': 'Armenia',
 'AUS': 'Australia',
 'AUT': 'Austria',
 'AZE': 'Azerbaijan',
 'BHS': 'Bahamas',
 'BHR': 'Bahrain',
 'BGD': 'Bangladesh',
 'BRB': 'Barbados',
 'BLR': 'Belarus',
 'BEL': 'Belgium',
 'BLZ': 'Belize',
 'BEN': 'Benin',
 'BTN': 'Bhutan',
 'BOL': 'Bolivia',
 'BIH': 'Bosnia and Herzegovina',
 'BWA': 'Botswana',
 'BRA': 'Brazil',
 'BRN': 'Brunei Darussalam',
 'BGR': 'Bulgaria',
 'BFA': 'Burkina Faso',
 'BDI': 'Burundi',
 'CPV': 'Cabo Verde',
 'KHM': 'Cambodia',
 'CMR': 'Cameroon',
 'CAN': 'Canada',
 'CAF': 'Central African Republic',
 'TCD': 'Chad',
 'CHL': 'Chile',
 'CHN': 'China',
 'COL': 'Colombia',
 'COM': 'Comoros',
 'COG': 'Congo',
 'COD': 'Congo, Democratic Republic of the',
 'CRI': 'Costa Rica',
 'CIV': "Côte d'Ivoire",
 'HRV': 'Croatia',
 'CUB': 'Cuba',
 'CYP': 'Cyprus',
 'CZE': 'Czechia',
 'DNK': 'Denmark',
 'DJI': 'Djibouti',
 'DMA': 'Dominica',
 'DOM': 'Dominican Republic',
 'ECU': 'Ecuador',
 'EGY': 'Egypt',
 'SLV': 'El Salvador',
 'GNQ': 'Equatorial Guinea',
 'ERI': 'Eritrea',
 'EST': 'Estonia',
 'SWZ': 'Eswatini',
 'ETH': 'Ethiopia',
 'FJI': 'Fiji',
 'FIN': 'Finland',
 'FRA': 'France',
 'GAB': 'Gabon',
 'GMB': 'Gambia',
 'GEO': 'Georgia',
 'DEU': 'Germany',
 'GHA': 'Ghana',
 'GRC': 'Greece',
 'GRD': 'Grenada',
 'GTM': 'Guatemala',
 'GIN': 'Guinea',
 'GNB': 'Guinea-Bissau',
 'GUY': 'Guyana',
 'HTI': 'Haiti',
 'HND': 'Honduras',
 'HUN': 'Hungary',
 'ISL': 'Iceland',
 'IND': 'India',
 'IDN': 'Indonesia',
 'IRN': 'Iran',
 'IRQ': 'Iraq',
 'IRL': 'Ireland',
 'ISR': 'Israel',
 'ITA': 'Italy',
 'JAM': 'Jamaica',
 'JPN': 'Japan',
 'JOR': 'Jordan',
 'KAZ': 'Kazakhstan',
 'KEN': 'Kenya',
 'KIR': 'Kiribati',
 'PRK': "Korea, Democratic People's Republic of",
 'KOR': 'Korea',
 'KWT': 'Kuwait',
 'KGZ': 'Kyrgyzstan',
 'LAO': "Laos",
 'LVA': 'Latvia',
 'LBN': 'Lebanon',
 'LSO': 'Lesotho',
 'LBR': 'Liberia',
 'LBY': 'Libya',
 'LIE': 'Liechtenstein',
 'LTU': 'Lithuania',
 'LUX': 'Luxembourg',
 'MDG': 'Madagascar',
 'MWI': 'Malawi',
 'MYS': 'Malaysia',
 'MDV': 'Maldives',
 'MLI': 'Mali',
 'MLT': 'Malta',
 'MHL': 'Marshall Islands',
 'MRT': 'Mauritania',
 'MUS': 'Mauritius',
 'MEX': 'Mexico',
 'FSM': 'Micronesia',
 'MDA': 'Moldova',
 'MCO': 'Monaco',
 'MNG': 'Mongolia',
 'MNE': 'Montenegro',
 'MAR': 'Morocco',
 'MOZ': 'Mozambique',
 'MMR': 'Myanmar',
 'NAM': 'Namibia',
 'NRU': 'Nauru',
 'NPL': 'Nepal',
 'NLD': 'Netherlands',
 'NZL': 'New Zealand',
 'NIC': 'Nicaragua',
 'NER': 'Niger',
 'NGA': 'Nigeria',
 'MKD': 'North Macedonia',
 'NOR': 'Norway',
 'OMN': 'Oman',
 'PAK': 'Pakistan',
 'PLW': 'Palau',
 'PAN': 'Panama',
 'PNG': 'Papua New Guinea',
 'PRY': 'Paraguay',
 'PER': 'Peru',
 'PHL': 'Philippines',
 'POL': 'Poland',
 'PRT': 'Portugal',
 'QAT': 'Qatar',
 'ROU': 'Romania',
 'RUS': 'Russia',
 'RWA': 'Rwanda',
 'KNA': 'Saint Kitts and Nevis',
 'LCA': 'Saint Lucia',
 'VCT': 'Saint Vincent and the Grenadines',
 'WSM': 'Samoa',
 'SMR': 'San Marino',
 'STP': 'Sao Tome and Principe',
 'SAU': 'Saudi Arabia',
 'SEN': 'Senegal',
 'SRB': 'Serbia',
 'SYC': 'Seychelles',
 'SLE': 'Sierra Leone',
 'SGP': 'Singapore',
 'SVK': 'Slovakia',
 'SVN': 'Slovenia',
 'SLB': 'Solomon Islands',
 'SOM': 'Somalia',
 'ZAF': 'South Africa',
 'SSD': 'South Sudan',
 'ESP': 'Spain',
 'LKA': 'Sri Lanka',
 'SDN': 'Sudan',
 'SUR': 'Suriname',
 'SWE': 'Sweden',
 'CHE': 'Switzerland',
 'SYR': 'Syria',
 'TJK': 'Tajikistan',
 'TZA': 'Tanzania',
 'THA': 'Thailand',
 'TLS': 'Timor-Leste',
 'TGO': 'Togo',
 'TON': 'Tonga',
 'TTO': 'Trinidad and Tobago',
 'TUN': 'Tunisia',
 'TUR': 'Turkey',
 'TKM': 'Turkmenistan',
 'TUV': 'Tuvalu',
 'UGA': 'Uganda',
 'UKR': 'Ukraine',
 'ARE': 'United Arab Emirates',
 'GBR': 'UK',
 'USA': 'USA',
 'URY': 'Uruguay',
 'UZB': 'Uzbekistan',
 'VUT': 'Vanuatu',
 'VEN': 'Venezuela',
 'VNM': 'Vietnam',
 'YEM': 'Yemen',
 'ZMB': 'Zambia',
 'ZWE': 'Zimbabwe'}


def clean_unesco(df):
    """
    Note: this function linearly interpolates missing values to fill in gaps in the data 
    (since there are many). It does not backpropagate interpolation, so values are only 
    filled if a past value exists.
    
    """
    wide_df = df.set_index(['geoUnit', 'year']).unstack(level='year')['value']
    long_df = wide_df.reset_index().melt(
        id_vars = 'geoUnit',
        var_name = 'year',
        value_name = 'value'
    )
    long_df['year'] = long_df['year'].astype(int)
    long_df = long_df.sort_values(by=['geoUnit', 'year']).reset_index(drop=True)
    long_df['value'] = long_df.groupby('geoUnit')['value'].transform(lambda group: group.interpolate(method= 'linear'))
    long_df['country'] = [countries.get(country_code, np.nan) for country_code in long_df['geoUnit']]

    return long_df

def main():
    inbound = pd.read_csv(RAW_DATA_DIR / 'total_inbound_tertiary_students_2000-2026.csv')
    outbound = pd.read_csv(RAW_DATA_DIR / 'total_outbound_tertiary_students_2000-2026.csv')
    clean_in = clean_unesco(inbound)
    clean_out = clean_unesco(outbound)
    clean_in.to_csv(PROCESSED_DATA_DIR / 'inbound_students_processed.csv')
    clean_out.to_csv(PROCESSED_DATA_DIR / 'outbound_students_processed.csv')
    print(f'finished cleaning Unesco data, saved to: {PROCESSED_DATA_DIR}')

if __name__ == "__main__":    
    main()

def run():
    main()