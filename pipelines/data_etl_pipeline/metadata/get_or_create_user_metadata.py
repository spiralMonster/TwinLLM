from document_categories.nosql_db_document_categories.user_document import UserDocument


def _get_metadata(user_full_name:str,user:UserDocument) -> dict:
    metadata={
        "query":{
            "user_full_name":user_full_name
        },
        "retrieved":{
            "user_id":str(user.id),
            "first_name":user.first_name,
            "last_name":user.last_name
        }
    }

    return metadata