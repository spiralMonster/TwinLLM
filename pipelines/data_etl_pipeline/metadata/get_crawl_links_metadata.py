from utils.exceptions.general_exceptions.invalid_metadata_exception import InvalidMetaDataException


def combine_metadata(metadata1:dict,metadata2:dict) -> dict:
    final_metadata={}

    for key in metadata1.keys():
        if key not in metadata2.keys():
            raise InvalidMetaDataException("Invalid Metadata received!!!")

        else:
            if key=="num_successful_crawls":
                final_metadata[key]=metadata1[key]+metadata2[key]

            elif key=="min_content_length":
                final_metadata[key]=min(metadata1[key],metadata2[key])

            elif key=="max_content_length":
                final_metadata[key]=max(metadata1[key],metadata2[key])

            else:
                final_metadata[key]=int(
                    (metadata1[key]+metadata2[key])/2
                )


    return final_metadata



def _get_metadata_(metadata:dict,crawler_metadata:dict,domain:str) -> dict:
    if domain not in metadata:
        metadata[domain]=crawler_metadata

    else:
        metadata1=metadata[domain]
        metadata2=crawler_metadata

        final_metadata=combine_metadata(
            metadata1=metadata1,
            metadata2=metadata2
        )

        metadata[domain]=final_metadata


    return metadata