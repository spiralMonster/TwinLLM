from loguru import logger
import json

with open("configs/utils_configs/date_codes_to_num_days.json", "r") as file:
    code_config = json.load(file)



def _convert(day_date_code:str,date_code:str) -> int:
    len_code=len(date_code)

    days=day_date_code[:-len_code]
    days=int(days)

    num_days=days*code_config[date_code]
    num_days=int(num_days)

    return num_days


def ConvertCodeToDays(day_date_code:str) -> int:
    for date_code in code_config.keys():
        if date_code in day_date_code:
            num_days=_convert(day_date_code=day_date_code,date_code=date_code)
            return num_days


    logger.error("Invalid day_date_code!!!")
    return 0


if __name__=="__main__":
    code=input("Enter day-date code: ")
    num_days=ConvertCodeToDays(code)
    print(f"Code: {code}")
    print(f"Number of days: {num_days}")
