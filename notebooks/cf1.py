import pandas as pd
import numpy as np

pd.set_option('display.max_columns', 300)

def import_it(filepath):
    
    #select specific columns
    demo_features = ['X2SEX', 'X2RACE', 'X2DUALLANG', 'X2POVERTY185', 'X2SESQ5_U', 'X2CONTROL', 
                     'X2LOCALE', 'X2REGION']


    mvp_features = ['X2STU30OCC_STEM1', 'X2STUEDEXPCT', 'X2S2SSPR12', 'S2SPERSON1', 'S2SPERSON2', 
               'S2SLEARN', 'S2SBORN', 'S2SUSELIFE', 'S2SUSECLG', 'S2SUSEJOB', 
               'S2SSPR12', 'S2LIFES12', 'S2BIO1S12', 'S2BIO2S12', 'S2APBIOS12', 
               'S2IBIOS12', 'S2ANATOMYS12', 'S2OTHBIOS12', 'S2CHEM1S12', 'S2CHEM2S12', 'S2APCHEM12', 
               'S2IBCHEM12', 'S2EARTHS12', 'S2APENVS12', 'S2OTHENVS12', 'S2PHYSIC1S12', 
               'S2PHYSIC2S12', 'S2APPHYSIC12', 'S2IBPHYSIC12', 'S2PHYSS12', 'S2TECHS12', 'S2OTHPHYS12', 
               'S2INTGS1S12', 'S2INTGS2S12', 'S2GENS12', 'S2COMPAPP12', 'S2COMPPROG12', 
               'S2APCOMPSCI12', 'S2IBTECH12', 'S2OTHCOMP12', 'S2ENGINEER12', 'S2OTHS12', 'S2OTHS12SP', 
               'S2HISCIENCE12', 'S2APSCIENCE', 'S2IBSCIENCE', 'S2STOOKBEFORE', 'S2SENJOYS', 'S2SCHALLENGE', 
                'S2SHSREQ', 'S2SCLGADM', 'S2SCLGSUCC', 'S2SCAREER', 'S2SCNSLREC', 'S2STCHRREC', 
                'S2SPARREC', 'S2SFAMREC', 'S2SEMPREC', 'S2SFRIEND', 'S2SDOWELL', 'S2SASSIGNED', 
                'S2STCHTREAT', 'S2STCHINTRST', 'S2STCHEASY', 'S2STCHTHINK', 'S2STCHGIVEUP', 
                'S2SENJOYING', 'S2SWASTE', 'S2SBORING', 'S2SUSELIFE', 'S2SUSECLG', 'S2SUSEJOB', 
                'S2STESTS', 'S2STEXTBOOK', 'S2SSKILLS', 'S2SASSEXCL', 'S2APSCIENCE', 'S2HSPLAN', 
                'S2SUBMITPLAN', 'S2SCLUB', 'S2SCOMPETE', 'S2SSUMMERPRG', 'S2SGROUP', 'S2STUTORED', 
                'X4RFDGMJ123', 'X4RFDGMJSTEM']

    family_features = ['X2PAR1EDU', 'X2PAR1OCC_STEM1', 'X2PAR1RACE', 'X2PAR2EDU', 'X2PAR2OCC_STEM1', 
                       'X2PAR2RACE', 'X2PARPATTERN', 'X2MOMEDU', 'X2MOMOCC_STEM1', 'X2MOMRACE', 
                       'X2DADEDU', 'X2DADOCC_STEM1', 'X2DADRACE']

    cols_list = demo_features + mvp_features
    
    #read in specific columns
    df = pd.read_csv(filepath, usecols = cols_list)
    
    return df



def clean_it(df):
    #select and rename target variable
    df.rename(columns = {'X4RFDGMJSTEM': 'target'}, inplace = True)

    #drop rows with non-response to S2SLEARN (and many other features) because they likely dropped the study
    df = df[df['S2SLEARN'] != -8]
    
    #create dummy variables for races
    df['ai_an'] = np.where(df['X2RACE'] == 1, 1, 0)
    df['asian'] = np.where(df['X2RACE'] == 2, 1, 0)
    df['black'] = np.where(df['X2RACE'] == 3, 1, 0)
    df['hispanic'] = np.where((df['X2RACE'] == 4) | (df['X2RACE'] == 5), 1, 0)
    df['multiple_race'] = np.where(df['X2RACE'] == 6, 1, 0)
    df['nh_pi'] = np.where(df['X2RACE'] == 7, 1, 0)
    df['white'] = np.where(df['X2RACE'] == 8, 1, 0)

    #change sex to a dummy variable for female
    df['female'] = np.where(df['X2SEX'] == 2, 1, 0)
    
    #combine hispanic into one column
    df['X2RACE'].replace({4:5}, inplace = True)
    
    #create dummy for public/private school
    df['private'] = [1 if x == 2 else 0 for x in df['X2CONTROL']]
    df['public'] = [1 if x == 1 else 0 for x in df['X2CONTROL']]
    
    #compile all subchoices of STEM domains into yes/no
    df.X2STU30OCC_STEM1.replace({-9:0, 9:0, 4:1, 5:1, 6:1}, inplace = True)

    classes = ['S2SSPR12', 'S2LIFES12', 'S2BIO1S12', 'S2BIO2S12', 'S2APBIOS12', 
               'S2IBIOS12', 'S2ANATOMYS12', 'S2OTHBIOS12', 'S2CHEM1S12', 'S2CHEM2S12', 'S2APCHEM12', 
               'S2IBCHEM12', 'S2EARTHS12', 'S2APENVS12', 'S2OTHENVS12', 'S2PHYSIC1S12', 
               'S2PHYSIC2S12', 'S2APPHYSIC12', 'S2IBPHYSIC12', 'S2PHYSS12', 'S2TECHS12', 'S2OTHPHYS12', 
               'S2INTGS1S12', 'S2INTGS2S12', 'S2GENS12', 'S2COMPAPP12', 'S2COMPPROG12', 
               'S2APCOMPSCI12', 'S2IBTECH12', 'S2OTHCOMP12', 'S2ENGINEER12', 'S2OTHS12', 'S2APSCIENCE', 
               'S2IBSCIENCE']

    #impute 'no' for items that are missing or were skipped due to not taking a science class
    for col in classes:
        df[col].replace({-9:0, -7:0}, inplace= True)
    
    
    #impute unknown with 'no' for if participating in science activity
    clubs_cols = ['S2SCLUB', 'S2SCOMPETE', 'S2SSUMMERPRG', 'S2SGROUP', 'S2STUTORED']

    for col in clubs_cols:
        df[col].replace({-9:0}, inplace = True)
        

    #create class for underrepresented group in STEM
    df['underrep'] = np.where((df['X2SEX'] == 2) |
                              (df['ai_an'] == 1) |
                              (df['black'] == 1) |
                              (df['hispanic'] == 1) |
                              (df['multiple_race'] == 1) |
                              (df['nh_pi'] == 1), 1, 0)
   
    #group HS science classes into broader subjects
    df['bio'] = np.where((df['S2LIFES12'] == 1) |
                          (df['S2BIO1S12'] == 1) |
                          (df['S2BIO2S12'] == 1) |
                          (df['S2APBIOS12'] == 1) |
                          (df['S2IBIOS12'] == 1) |
                         (df['S2ANATOMYS12'] == 1) |
                          (df['S2OTHBIOS12'] == 1), 1, 0)


    df['chem'] = np.where((df['S2CHEM1S12'] == 1) |
                          (df['S2CHEM2S12'] == 1) |
                          (df['S2APCHEM12'] == 1) |
                          (df['S2IBCHEM12'] == 1), 1, 0)


    df['enviro'] = np.where((df['S2EARTHS12'] == 1) |
                            (df['S2EARTHS12'] == 1) |
                            (df['S2APENVS12'] == 1) |
                            (df['S2OTHENVS12'] == 1), 1, 0)

    df['physics'] = np.where((df['S2PHYSIC1S12'] == 1) |
                             (df['S2PHYSIC2S12'] == 1) |
                             (df['S2APPHYSIC12'] == 1) |
                             (df['S2IBPHYSIC12'] == 1) |
                             (df['S2PHYSS12'] == 1), 1, 0)

    df['engineering'] = np.where((df['S2ENGINEER12'] == 1), 1, 0)


    df['compsci'] = np.where((df['S2COMPAPP12'] == 1) |
                             (df['S2COMPPROG12'] == 1) |
                             (df['S2APCOMPSCI12'] == 1) |
                             (df['S2IBTECH12'] == 1) |
                             (df['S2OTHCOMP12'] == 1), 1, 0)

    df['misc_class'] = np.where((df['S2OTHPHYS12'] == 1) |
                                (df['S2INTGS1S12'] == 1) |
                                (df['S2GENS12'] == 1), 1, 0)
    
    
    #impute 'no' for items that are missing or were skipped due to not taking a science class

    why_science = ['S2SENJOYS', 'S2SCHALLENGE', 'S2SHSREQ', 'S2SCLGADM', 
                   'S2SCLGSUCC', 'S2SCAREER', 'S2SCNSLREC', 'S2STCHRREC', 'S2SPARREC', 'S2SFAMREC', 
                   'S2SEMPREC', 'S2SFRIEND', 'S2SDOWELL', 'S2SASSIGNED']

    for col in why_science:
        df[col].replace({-9:0, -7:0}, inplace= True)

    
    #create column for students who took science earlier in the year (but don't now)
    df['took_science_2012'] = np.where((df['S2STOOKBEFORE'] == 1) |
                                       (df['bio'] == 1) |
                                       (df['chem'] == 1) |
                                       (df['enviro'] == 1) |
                                       (df['physics'] == 1) |
                                       (df['engineering'] == 1) |
                                       (df['compsci'] == 1) |
                                       (df['misc_class'] == 1), 1, 0)
    
    #change likert questions to agree/disagree
    likert_cols = ['S2SPERSON1', 'S2SPERSON2', 
               'S2SLEARN', 'S2SBORN', 'S2SUSELIFE', 'S2SUSECLG', 'S2SUSEJOB', 
                'S2STCHTREAT', 'S2STCHINTRST', 
               'S2STCHEASY', 'S2STCHTHINK', 'S2STCHGIVEUP', 'S2SENJOYING', 'S2SWASTE', 'S2SBORING', 
               'S2STESTS', 'S2STEXTBOOK', 'S2SSKILLS', 
               'S2SASSEXCL']

    for col in likert_cols:
        df[col].replace({2:1, 3:0, 4:0, -9:0, -7:0}, inplace = True)
        
    
    #change to yes/no
    df.S2HSPLAN = np.where(df['S2HSPLAN'] == 1, 1, 0)
    df.S2SUBMITPLAN = np.where(df['S2SUBMITPLAN'] == 1, 1, 0)
    
    #group expected highest education achieved to be highest degree completed
    df['EXPECT'] = df['X2STUEDEXPCT'].replace({1:1, 2:2, 3:2, 4:3, 5:2, 6:4, 7:4, 8:5, 9:5, 10:6, 11:6, 12:7, 13:8})
    
    return df



