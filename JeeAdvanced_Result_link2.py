import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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
    "SELECT SNO, REGNO, TRIM(DOB), MOBILE1, ADMNO, BRANCH, COURSE_NAME, BATCH_NAME, NEW_SUBBATCH, SUBBATCH FROM I_JEEADV_ADMITCARD_25  \
        WHERE DOB IS NOT NULL AND TRIM(PROCESS_STATUS) = 'P' AND SNO >= '"+str(start_sno)+"' AND  SNO <='"+str(end_sno)+"' ORDER BY SNO"
cur.execute(str_Jeeappno)
res = cur.fetchall()

driver = webdriver.Chrome()
driver.maximize_window()

for row in res:
    v_SNO = row[0]
    v_REGNO = row[1]
    v_dob = row[2].replace("-","/")
    v_MOBILE = row[3]
    v_admno = row[4]
    v_branch = row[5]
    v_course_name = row[6]
    v_batch_name = row[7]
    v_new_subbatch = row[8]
    v_subbatch = row[9]

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

    try:
        driver.get("https://jeeadv.iitm.ac.in/result24/login.php")
        #time.sleep(1)

        Registration_number = driver.find_element(By.NAME, "regno")
        Registration_number.send_keys(v_REGNO)

        dob = driver.find_element(By.NAME, "dob")
        dob.send_keys(v_dob)
        time.sleep(0.5)
        
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div/form/button'))
        ).click()

        body = WebDriverWait(driver, 1).until(EC.presence_of_all_elements_located((By.TAG_NAME, "body")))
        for b in body:
            body_arr = b.text.split('\n')

        if (body_arr[0].strip() != "Invalid AdvRollNo or Date of Birth."):
            tables = WebDriverWait(driver, 1).until(EC.presence_of_all_elements_located((By.TAG_NAME, "table")))
            for table in tables:
                data_arr = table.text.split('\n')

            o_rollno = data_arr[0].replace('JEE(Adv) 2024 RollNo ','')
            o_student = data_arr[1].replace('Candidate Name ','')
            o_phy_TOT = round(int(float(data_arr[2].replace('Physics ',''))))
            o_chem_TOT = round(int(float(data_arr[3].replace('Chemistry ',''))))
            o_mat_TOT = round(int(float(data_arr[4].replace('Mathematics ',''))))
            o_POSITIVE_MARK = round(int(float(data_arr[5].replace('Positive Total Marks ',''))))
            o_TOT = round(int(float(data_arr[6].replace('Total Marks ',''))))

            if ('CRL' in data_arr[7] ):
                o_CRL_RANK = data_arr[7].replace('CRL ','') 
            elif ('SC ' in data_arr[7]):
                o_SC_RANK = data_arr[7].replace('SC : ','') 
            elif ('ST ' in data_arr[7]):
                o_ST_RANK = data_arr[7].replace('ST : ','') 
            elif ('Result : ' in data_arr[7]):
                o_Result = data_arr[7].replace('Result : ','') 

            if (o_Result == ''):
                if ('CRL' in data_arr[8] ):
                    o_CRL_RANK = data_arr[8].replace('CRL ','') 
                elif ('SC ' in data_arr[8]):
                    o_SC_RANK = data_arr[8].replace('SC : ','') 
                elif ('ST ' in data_arr[8]):
                    o_ST_RANK = data_arr[8].replace('ST : ','') 
                elif ('Result : ' in data_arr[8]):
                    o_Result = data_arr[8].replace('Result : ','') 

            if (o_Result == ''):
                if ('OBC_NCL ' in data_arr[9] ):
                    o_OBC_NCL_RANK = data_arr[9].replace('OBC_NCL ','') 
                elif ('SC ' in data_arr[9]):
                    o_SC_RANK = data_arr[9].replace('SC ','') 
                elif ('ST ' in data_arr[9]):
                    o_ST_RANK = data_arr[9].replace('ST ','') 
                elif ('GEN EWS ' in data_arr[9]):
                    o_GEN_EWS_RANK = data_arr[9].replace('GEN EWS ','') 
                elif ('CRL_PWD ' in data_arr[9]):
                    o_CRL_PWD_RANK = data_arr[9].replace('CRL_PWD ','') 
                elif ('Result : ' in data_arr[9]):
                    o_Result = data_arr[9].replace('Result : ','') 

            if (o_Result == ''):
                if ('OBC_NCL_PWD ' in data_arr[10]):
                    o_OBC_NCL_PWD_RANK = data_arr[10].replace('OBC_NCL_PWD  ','') 
                elif ('CRL_PWD ' in data_arr[10]):
                    o_CRL_PWD_RANK = data_arr[10].replace('CRL_PWD ','') 
                elif ('Result : ' in data_arr[10] ):
                    o_Result = data_arr[10].replace('Result : ','') 

            if (o_Result == ''):
                if ('OBC_NCL_PWD ' in data_arr[11]):
                    o_OBC_NCL_PWD_RANK = data_arr[11].replace('OBC_NCL_PWD ','') 
                elif ('Result : ' in data_arr[11] ):
                    o_Result = data_arr[11].replace('Result : ','')             

            if (o_Result == ''):
                if ('OBC_NCL_PWD ' in data_arr[12]):
                    o_OBC_NCL_PWD_RANK = data_arr[12].replace('OBC_NCL_PWD ','') 
                elif ('GEN EWS_PWD ' in data_arr[12]):
                    o_GEN_EWS_PWD_RANK = data_arr[12].replace('GEN EWS_PWD ','')     
                elif ('Result : ' in data_arr[12] ):
                    o_Result = data_arr[12].replace('Result : ','')             

            o_phy1 = 0
            o_phy2 = 0

            o_chem1 = 0
            o_chem2 = 0

            o_mat1 = 0
            o_mat2 = 0

            insert_Jeemain_result = \
                    "INSERT INTO O_JEEADV_RESULT_25 (HTNO, NAME, DOB,PHONENO,PHY1,PHY2,PHY_TOT,CHE1,CHE2,CHE_TOT,MAT1,MAT2,MAT_TOT,TOT, \
                    POSITIVEMARK, CRL_RANK,CRL_PWD_RANK, GEN_EWS_PWD_RANK, GEN_EWS_RANK,OBC_NCL_PWD_RANK, OBC_NCL_RANK, PREP_CRL_PWD_RANK, PREP_GEN_EWS_PWD_RANK, \
                    PREP_OBC_NCL_PWD_RANK, PREP_SC_PWD_RANK, PREP_SC_RANK,PREP_ST_PWD_RANK, PREP_ST_RANK, SC_PWD_RANK, SC_RANK, ST_PWD_RANK, ST_RANK,REMARK, ADMNO, \
                    REGNO, BRANCH, COURSE_NAME, BATCH_NAME, NEW_SUBBATCH, SUBBATCH) \
                    VALUES ('"+ str(o_rollno) +"', '"+ o_student +"', '"+ str(v_MOBILE) +"', '"+ str(o_phy1) +"', '"+ str(o_phy2) +"', '"+ str(o_phy_TOT) +"', \
                    '"+ str(o_chem1) +"', '"+ str(o_chem2) +"','"+ str(o_chem_TOT) +"', '"+ str(o_mat1) +"','"+ str(o_mat2) +"', '"+ str(o_mat_TOT) +"', \
                    '"+ str(o_TOT) +"', '"+ str(o_POSITIVE_MARK) +"', '"+ str(o_CRL_RANK) +"', '"+ str(o_CRL_PWD_RANK) +"', '"+ str(o_GEN_EWS_PWD_RANK) +"', '"+ str(o_GEN_EWS_RANK) +"', \
                    '"+ str(o_OBC_NCL_PWD_RANK) +"', '"+ str(o_OBC_NCL_RANK) +"', '"+ str(o_PREP_CRL_PWD_RANK) +"', '"+ str(o_PREP_GEN_EWS_PWD_RANK) +"', '"+ str(o_PREP_OBC_NCL_PWD_RANK) +"', \
                    '"+ str(o_PREP_SC_PWD_RANK) +"', '"+ str(o_PREP_SC_RANK) +"', '"+ str(o_PREP_ST_PWD_RANK) +"', '"+ str(o_PREP_ST_RANK) +"', \
                    '"+ str(o_SC_PWD_RANK) +"', '"+ str(o_SC_RANK) +"', '"+ str(o_ST_PWD_RANK) +"', '"+ str(o_ST_RANK) +"', '"+ o_REMARK +"','"+ str(v_admno) +"','"+ str(v_REGNO) +"'  \
                    , '"+ str(v_branch) +"','"+ str(v_course_name) +"','"+ str(v_batch_name) +"','"+ str(v_new_subbatch) +"','"+ str(v_subbatch) +"')"
            cur.execute(insert_Jeemain_result) # Execute an INSERT statement
            
            update_Status = "UPDATE IN_ADV_RESULT_2024 SET PROCESS_STATUS = 'D', PROCESS_USER = '"+v_process_user+"', CREATEDDATE = SYSDATE WHERE HTNO = '"+ str(v_REGNO) +"'"
            cur.execute(update_Status) # Execute an UPDATE statement
            conn.commit() # Commit the changes to the database 
        else:
            update_Status = "UPDATE IN_ADV_RESULT_2024 SET PROCESS_STATUS = 'NE', PROCESS_USER = '"+v_process_user+"', CREATEDDATE = SYSDATE WHERE HTNO = '"+ str(v_REGNO) +"'"
            cur.execute(update_Status) # Execute an UPDATE statement
            conn.commit() # Commit the changes to the database 
    except Exception as e:
        print(e)
        update_Status = "UPDATE IN_ADV_RESULT_2024 SET PROCESS_STATUS = 'RR', PROCESS_USER = '"+v_process_user+"', CREATEDDATE = SYSDATE WHERE HTNO = '"+ str(v_REGNO) +"'"
        cur.execute(update_Status) # Execute an UPDATE statement
        conn.commit() # Commit the changes to the database    
        pass

    #finally:
driver.quit()
