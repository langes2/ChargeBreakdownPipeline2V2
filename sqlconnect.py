import psycopg2
from psycopg2 import extras
import pandas as pd
import os
import glob

# 1. Find the most recently modified file in the specified directory
directory = r"C:\Users\Public\Documents\CBwhole"
list_of_files = glob.glob(os.path.join(directory, "*.csv"))
latest_file = max(list_of_files, key=os.path.getmtime)

# 2. Read the CSV file
data_frame = pd.read_csv(latest_file, header=None)

#2.5 Convert df to list of tuples
data_to_upsert = [tuple(row) for row in data_frame.itertuples(index=False, name=None)]

# 3. Database connection details
db_params = {
    "user": "postgres",
    "password": "Crystalview2020_",
    "host": "localhost",
    "port": "5432",
    "database": "RM_Reports"
}

# 4. Upsert script
try:
    # Connect to PostgreSQL
    connection = psycopg2.connect(**db_params)
    cursor = connection.cursor()

    # Define the upsert query
    upsert_query = """
    INSERT INTO fullchargebreakdown (startdate, enddate, property, tenant, acc, unit, unittype, rc, bb, dp, nsffee, nsfadj, lc, note, prin, sales, lint, agradj, mgtfee, appfee, aj, cam, clubrc, cn, comm, dockrt, dw, ea, elect, fpf, gas, h2o, home, mhtax, petdep, petfee, ptax, rulefee, rvlot, sewer, schooltx, trash, bd, clean, invty, legal, mhtf, movein, mt, rfd, rntcr, rntlho, sndc, st, wcrd, violat, wb, sfrcr, tech, guest, epay, salestx, callfee, bbc, total)
    VALUES %s
    ON CONFLICT (startdate, enddate, property, tenant, acc) DO UPDATE SET
    unit = EXCLUDED.unit,
    unittype = EXCLUDED.unittype,
    rc = EXCLUDED.rc,
    bb = EXCLUDED.bb,
    dp = EXCLUDED.dp,
    nsffee = EXCLUDED.nsffee,
    nsfadj = EXCLUDED.nsfadj,
    lc = EXCLUDED.lc,
    note = EXCLUDED.note,
    prin = EXCLUDED.prin,
    sales = EXCLUDED.sales,
    lint = EXCLUDED.lint,
    agradj = EXCLUDED.agradj,
    mgtfee = EXCLUDED.mgtfee,
    appfee = EXCLUDED.appfee,
    aj = EXCLUDED.aj,
    cam = EXCLUDED.cam,
    clubrc = EXCLUDED.clubrc,
    cn = EXCLUDED.cn,
    comm = EXCLUDED.comm,
    dockrt = EXCLUDED.dockrt,
    dw = EXCLUDED.dw,
    ea = EXCLUDED.ea,
    elect = EXCLUDED.elect,
    fpf = EXCLUDED.fpf,
    gas = EXCLUDED.gas,
    h2o = EXCLUDED.h2o,
    home = EXCLUDED.home,
    mhtax = EXCLUDED.mhtax,
    petdep = EXCLUDED.petdep,
    petfee = EXCLUDED.petfee,
    ptax = EXCLUDED.ptax,
    rulefee = EXCLUDED.rulefee,
    rvlot = EXCLUDED.rvlot,
    sewer = EXCLUDED.sewer,
    schooltx = EXCLUDED.schooltx,
    trash = EXCLUDED.trash,
    bd = EXCLUDED.bd,
    clean = EXCLUDED.clean,
    invty = EXCLUDED.invty,
    legal = EXCLUDED.legal,
    mhtf = EXCLUDED.mhtf,
    movein = EXCLUDED.movein,
    mt = EXCLUDED.mt,
    rfd = EXCLUDED.rfd,
    rntcr = EXCLUDED.rntcr,
    rntlho = EXCLUDED.rntlho,
    sndc = EXCLUDED.sndc,
    st = EXCLUDED.st,
    wcrd = EXCLUDED.wcrd,
    violat = EXCLUDED.violat,
    wb = EXCLUDED.wb,
    sfrcr = EXCLUDED.sfrcr,
    tech = EXCLUDED.tech,
    guest = EXCLUDED.guest,
    epay = EXCLUDED.epay,
    salestx = EXCLUDED.salestx,
    callfee = EXCLUDED.callfee,
    bbc = EXCLUDED.bbc,
    total = EXCLUDED.total;
    """

    # Perform the upsert
    extras.execute_values(cursor, upsert_query, data_to_upsert)

    # Commit the transaction
    connection.commit()
    print(f"{cursor.rowcount} Records upserted successfully into table")

except (Exception, psycopg2.Error) as error:
    print("Error in transaction:", error)

finally:
    # Close the connection
    if connection:
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")