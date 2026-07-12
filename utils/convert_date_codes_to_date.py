from datetime import date, timedelta
from loguru import logger

from utils.convert_date_codes_to_num_days import ConvertCodeToDays


def ConvertCodeToDate(day_date_code:str) -> str:
    num_days=ConvertCodeToDays(day_date_code=day_date_code)

    if num_days==0:
        logger.error("Invalid day_date_code format!!!!")
        return ""

    today_date=date.today()
    final_date=today_date+timedelta(days=-num_days)
    final_date=str(final_date)

    return final_date



if __name__=="__main__":
    code=input("Enter the code: ")
    date=ConvertCodeToDate(day_date_code=code)

    print(f"Date:{date}")