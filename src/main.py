from util.logger import log
import subprocess
import sys

def run_pipeline():
    log("STEP 1: Running scraper...")
    subprocess.run([sys.executable, "-m", "src.scrapper.banggood_scraper"], check=True)

    log("STEP 2: Cleaning scraped data...")
    subprocess.run([sys.executable, "-m", "src.cleaning_transformation.clean_banggood_data"], check=True)

    log("STEP 3: Running analysis...")
    subprocess.run([sys.executable, "-m", "src.analysis.banggood_analysis"], check=True)

    log("STEP 4: Uploading to SQL Server...")
    subprocess.run([sys.executable, "-m", "src.database_sql.banggood_to_sql"], check=True)

    log("Pipeline completed successfully.")

if __name__ == "__main__":
    run_pipeline()
