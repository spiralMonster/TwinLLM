from enum import StrEnum

class DataCategory(StrEnum):
    POSTS="posts"
    ARTICLES="articles"
    REPOSITORIES="repositories"
    TWEETS="tweets"

    USERS="users"

    QUERIES="queries"
    CONVERSATION_HISTORY="conversation_history"
    CONVERSATION_SUMMARY="conversation_summary"