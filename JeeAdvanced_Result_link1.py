from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import requests
from bs4 import BeautifulSoup
import oracledb



v_process_user = 'U1'


oracledb.init_oracle_client(lib_dir=r"D:\app\udaykumard\product\instantclient_23_6")
conn = oracledb.connect(user='RESULT', password='LOCALDEV', dsn='192.168.15.208:1521/orcldev')
cur = conn.cursor()

#--------------------Data slots --------------------------------------
str_dataslot = "SELECT PROCESS_USER, START_VAL, END_VAL FROM DATASLOTS_VAL_USER WHERE PROCESS_USER = '"+v_process_user+"'"
cur.execute(str_dataslot)
res_dataslot = cur.fetchall()

start_sno = res_dataslot[0][1]
end_sno = res_dataslot[0][2]

Sno = start_sno
#------------------------------ end --------------------------------------

str_Jeeappno = \
    "SELECT SNO, REGNO, TRIM(DOB), MOBILE1, ADMNO, BRANCH, COURSE_NAME, BATCH_NAME, NEW_SUBBATCH, SUBBATCH,HTNO FROM I_JEEADV_ADMITCARD_25  \
        WHERE DOB IS NOT NULL AND TRIM(PROCESS_STATUS) = 'P' AND SNO >= '"+str(start_sno)+"' AND  SNO <='"+str(end_sno)+"' AND MOBILE1 IS NOT NULL AND LENGTH(HTNO) = 9 ORDER BY SNO"
cur.execute(str_Jeeappno)
res = cur.fetchall()

driver = webdriver.Chrome()
driver.maximize_window()

for row in res:
    v_SNO = row[0]
    v_REGNO = row[1]
    v_dob = row[2].replace("-","/")
    #v_dob = raw_dob[3:5] + '/' + raw_dob[0:2] + '/' + raw_dob[6:]
    v_MOBILE = row[3]
    v_admno = row[4]
    v_branch = row[5]
    v_course_name = row[6]
    v_batch_name = row[7]
    v_new_subbatch = row[8]
    v_subbatch = row[9]
    V_Htno = row[10]

    try:
        driver.get("https://results25.jeeadv.ac.in/")

        roll_number = driver.find_element(By.XPATH, '/html/body/div/div[2]/input')
        roll_number.clear()
        roll_number.send_keys(V_Htno)

        dob = driver.find_element(By.NAME, "dob")
        dob.clear()
        dob.send_keys(v_dob)

        Mobile_number = driver.find_element(By.XPATH, '/html/body/div/div[4]/input')
        Mobile_number.clear()
        Mobile_number.send_keys(v_MOBILE)
        
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/div[5]/button'))).click()
        try:
            time.sleep(0.1)
            ERR_MSG =''
            ERR_MSG = driver.find_element(By.XPATH, '/html/body/div/div[6]/strong').text
        except:
            pass
        if (ERR_MSG != 'Incorrect data!'):
            o_CRL_RANK = 0
            o_GEN_EWS_RANK = 0 #DONE
            o_OBC_NCL_PWD_RANK = 0 #DONE
            o_OBC_NCL_RANK = 0 #DONE
            o_CRL_PWD_RANK = 0
            o_GEN_EWS_PWD_RANK = 0
            o_PREP_CRL_PWD_RANK = 0
            o_PREP_GEN_EWS_PWD_RANK = 0
            o_PREP_OBC_NCL_PWD_RANK = 0
            o_PREP_SC_PWD_RANK = 0
            o_PREP_SC_RANK = 0
            o_PREP_ST_PWD_RANK = 0
            o_PREP_ST_RANK = 0
            o_SC_PWD_RANK = 0
            o_SC_RANK = 0 #DONE
            o_ST_PWD_RANK = 0
            o_ST_RANK = 0
            o_NCL_RANK = 0
            o_REMARK = ''
            
            time.sleep(0.1)
            o_rollno = driver.find_element(By.XPATH, '/html/body/div/div[6]/div[1]/table/tbody/tr[1]/td[2]').text
            o_student = driver.find_element(By.XPATH, '/html/body/div/div[6]/div[1]/table/tbody/tr[2]/td[2]').text
            o_chem1 = driver.find_element(By.XPATH, '/html/body/div/div[6]/div[1]/table/tbody/tr[3]/td[2]').text
            o_chem2 = driver.find_element(By.XPATH, '/html/body/div/div[6]/div[1]/table/tbody/tr[4]/td[2]').text
            o_chem_TOT = driver.find_element(By.XPATH, '/html/body/div/div[6]/div[1]/table/tbody/tr[5]/td[2]').text
            o_phy1 = driver.find_element(By.XPATH, '/html/body/div/div[6]/div[1]/table/tbody/tr[6]/td[2]').text
            o_phy2 = driver.find_element(By.XPATH, '/html/body/div/div[6]/div[1]/table/tbody/tr[7]/td[2]').text
            o_phy_TOT = driver.find_element(By.XPATH, '/html/body/div/div[6]/div[1]/table/tbody/tr[8]/td[2]').text
            o_mat1 =  driver.find_element(By.XPATH, '/html/body/div/div[6]/div[1]/table/tbody/tr[9]/td[2]').text
            o_mat2 =  driver.find_element(By.XPATH, '/html/body/div/div[6]/div[1]/table/tbody/tr[10]/td[2]').text
            o_mat_TOT =  driver.find_element(By.XPATH, '/html/body/div/div[6]/div[1]/table/tbody/tr[11]/td[2]').text
            o_TOT =  driver.find_element(By.XPATH, '/html/body/div/div[6]/div[1]/table/tbody/tr[12]/td[2]').text
            o_POSITIVE_MARK =  driver.find_element(By.XPATH, '/html/body/div/div[6]/div[1]/table/tbody/tr[13]/td[2]').text
            try:
                ROW_TXT =  driver.find_element(By.XPATH, '/html/body/div/div[6]/div[2]/strong').text 
                if ROW1_TXT == 'Not qualified.':
                    o_REMARK =  driver.find_element(By.XPATH, '/html/body/div/div[6]/div[2]/strong').text
            except:
                pass
            try:
                ROW1_TXT =  driver.find_element(By.XPATH, '/html/body/div/div[6]/div[2]/table/tbody/tr[1]/td[1]/strong').text 
                if ROW1_TXT == 'CRL Rank':
                    o_CRL_RANK =  driver.find_element(By.XPATH, '/html/body/div/div[6]/div[2]/table/tbody/tr/td[2]').text
                elif ROW1_TXT == 'CRL-PWD Rank':
                    o_CRL_PWD_RANK =  driver.find_element(By.XPATH, '/html/body/div/div[6]/div[2]/table/tbody/tr/td[2]').text
                elif ROW1_TXT == 'PREP-CRL-PWD Rank':
                    o_PREP_CRL_PWD_RANK =  driver.find_element(By.XPATH, '/html/body/div/div[6]/div[2]/table/tbody/tr/td[2]').text
                elif ROW1_TXT == 'PREP-SC Rank':
                    o_PREP_SC_RANK =  driver.find_element(By.XPATH, '/html/body/div/div[6]/div[2]/table/tbody/tr/td[2]').text
                elif ROW1_TXT == 'PREP-ST Rank':
                    o_PREP_ST_RANK =  driver.find_element(By.XPATH, '/html/body/div/div[6]/div[2]/table/tbody/tr/td[2]').text
                elif ROW1_TXT == 'SC Rank':
                    o_SC_RANK =  driver.find_element(By.XPATH, '/html/body/div/div[6]/div[2]/table/tbody/tr/td[2]').text
                elif ROW1_TXT == 'ST Rank':
                    o_ST_RANK =  driver.find_element(By.XPATH, '/html/body/div/div[6]/div[2]/table/tbody/tr/td[2]').text
            except:
                pass
            try:
                ROW2_TXT =  driver.find_element(By.XPATH, '/html/body/div/div[6]/div[2]/table/tbody/tr[2]/td[1]/strong').text 
        
                if ROW2_TXT == 'CRL-PWD Rank':
                    o_CRL_PWD_RANK =  driver.find_element(By.XPATH, '/html/body/div/div[6]/div[2]/table/tbody/tr[2]/td[2]').text
                elif ROW2_TXT == 'OBC-NCL Rank':
                    o_OBC_NCL_RANK =  driver.find_element(By.XPATH, '/html/body/div/div[6]/div[2]/table/tbody/tr[2]/td[2]').text
                elif ROW2_TXT == 'GEN-EWS Rank':
                    o_GEN_EWS_RANK =  driver.find_element(By.XPATH, '/html/body/div/div[6]/div[2]/table/tbody/tr[2]/td[2]').text
                elif ROW2_TXT == 'GEN-EWS-PWD Rank':
                    o_GEN_EWS_PWD_RANK =  driver.find_element(By.XPATH, '/html/body/div/div[6]/div[2]/table/tbody/tr[2]/td[2]').text
                elif ROW2_TXT == 'PREP-OBC-NCL-PWD Rank':
                    o_PREP_OBC_NCL_PWD_RANK =  driver.find_element(By.XPATH, '/html/body/div/div[6]/div[2]/table/tbody/tr[2]/td[2]').text
                elif ROW2_TXT == 'PREP-GEN-EWS-PWD Rank':
                    o_PREP_GEN_EWS_PWD_RANK =  driver.find_element(By.XPATH, '/html/body/div/div[6]/div[2]/table/tbody/tr[2]/td[2]').text
            except:
                pass
            try:
                ROW3_TXT =  driver.find_element(By.XPATH, '/html/body/div/div[6]/div[2]/table/tbody/tr[3]/td[1]/strong').text 
                if ROW3_TXT == 'CRL-PWD Rank':
                    o_CRL_PWD_RANK =  driver.find_element(By.XPATH, '/html/body/div/div[6]/div[2]/table/tbody/tr[3]/td[2]').text
            except:
                pass
            try:
                ROW4_TXT =  driver.find_element(By.XPATH, '/html/body/div/div[6]/div[2]/table/tbody/tr[4]/td[1]/strong').text 
                if ROW4_TXT == 'OBC-NCL-PWD Rank':
                    o_OBC_NCL_PWD_RANK =  driver.find_element(By.XPATH, '/html/body/div/div[6]/div[2]/table/tbody/tr[4]/td[2]').text
            except:
                pass
        
            insert_Jeemain_result = \
                    "INSERT INTO O_JEEADV_RESULT_25 (HTNO, NAME, DOB,PHONENO,PHY1,PHY2,PHY_TOT,CHE1,CHE2,CHE_TOT,MAT1,MAT2,MAT_TOT,TOT, \
                    POSITIVEMARK, CRL_RANK,CRL_PWD_RANK, GEN_EWS_PWD_RANK, GEN_EWS_RANK,OBC_NCL_PWD_RANK, OBC_NCL_RANK, PREP_CRL_PWD_RANK, PREP_GEN_EWS_PWD_RANK, \
                    PREP_OBC_NCL_PWD_RANK, PREP_SC_PWD_RANK, PREP_SC_RANK,PREP_ST_PWD_RANK, PREP_ST_RANK, SC_PWD_RANK, SC_RANK, ST_PWD_RANK, ST_RANK,REMARK, ADMNO, \
                    REGNO, BRANCH, COURSE_NAME, BATCH_NAME, NEW_SUBBATCH, SUBBATCH) \
                    VALUES ('"+ str(o_rollno) +"', '"+ o_student +"', '"+ str(v_dob) +"', '"+ str(v_MOBILE) +"', '"+ str(o_phy1) +"', '"+ str(o_phy2) +"', '"+ str(o_phy_TOT) +"', \
                    '"+ str(o_chem1) +"', '"+ str(o_chem2) +"','"+ str(o_chem_TOT) +"', '"+ str(o_mat1) +"','"+ str(o_mat2) +"', '"+ str(o_mat_TOT) +"', \
                    '"+ str(o_TOT) +"', '"+ str(o_POSITIVE_MARK) +"', '"+ str(o_CRL_RANK) +"', '"+ str(o_CRL_PWD_RANK) +"', '"+ str(o_GEN_EWS_PWD_RANK) +"', '"+ str(o_GEN_EWS_RANK) +"', \
                    '"+ str(o_OBC_NCL_PWD_RANK) +"', '"+ str(o_OBC_NCL_RANK) +"', '"+ str(o_PREP_CRL_PWD_RANK) +"', '"+ str(o_PREP_GEN_EWS_PWD_RANK) +"', '"+ str(o_PREP_OBC_NCL_PWD_RANK) +"', \
                    '"+ str(o_PREP_SC_PWD_RANK) +"', '"+ str(o_PREP_SC_RANK) +"', '"+ str(o_PREP_ST_PWD_RANK) +"', '"+ str(o_PREP_ST_RANK) +"', \
                    '"+ str(o_SC_PWD_RANK) +"', '"+ str(o_SC_RANK) +"', '"+ str(o_ST_PWD_RANK) +"', '"+ str(o_ST_RANK) +"', '"+ o_REMARK +"','"+ str(v_admno) +"','"+ str(v_REGNO) +"'  \
                    , '"+ str(v_branch) +"','"+ str(v_course_name) +"','"+ str(v_batch_name) +"','"+ str(v_new_subbatch) +"','"+ str(v_subbatch) +"')"
            cur.execute(insert_Jeemain_result) # Execute an INSERT statement
                
            update_Status = "UPDATE I_JEEADV_ADMITCARD_25 SET PROCESS_STATUS = 'D', PROCESS_USER = '"+v_process_user+"', CREATEDDATE = SYSDATE WHERE REGNO = '"+ str(v_REGNO) +"'"
            cur.execute(update_Status) # Execute an UPDATE statement
            conn.commit() # Commit the changes to the database 
        else:
            update_Status = "UPDATE I_JEEADV_ADMITCARD_25 SET PROCESS_STATUS = 'RR', PROCESS_USER = '"+v_process_user+"', CREATEDDATE = SYSDATE WHERE REGNO = '"+ str(v_REGNO) +"'"
            cur.execute(update_Status) # Execute an UPDATE statement
            conn.commit() # Commit the changes to the database 
    except Exception as e:
        update_Status = "UPDATE I_JEEADV_ADMITCARD_25 SET PROCESS_STATUS = 'NA', PROCESS_USER = '"+v_process_user+"', CREATEDDATE = SYSDATE WHERE REGNO = '"+ str(v_REGNO) +"'"
        cur.execute(update_Status) # Execute an UPDATE statement
        conn.commit() # Commit the changes to the database 
